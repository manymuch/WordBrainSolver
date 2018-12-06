#!/usr/bin/env python
# Copyright 2018 JiaxinZhang jiaxin@bu.edu
# Copyright 2018 XunLin xunlin@bu.edu
"""wordbrainsolver"""
import numpy as np
from collections import Counter
from sys import argv

class wordbox():
    """create a NxN box for box"""
    def __init__(self,letters_list):
        self.length = len(letters_list[0])+2
        self.letters_array = [[0]*self.length]*self.length
        for i in range(1, self.length-1):
            self.letters_array[i] = [0]+list(letters_list[i-1])+[0]
        self.letters_array = np.asarray(self.letters_array)

    def __drop_column(self, column):
        """drop in a column"""
        for i in range(1, self.length-2):
            if column[-i] == '0':
                # look up and find a non zero element
                j = i + 1
                while (column[-j] == '0'):
                    if j >= self.length-2:
                        return column
                    j = j + 1
                # switch that non zero elment with the zero element with index=i
                column[-i] = column[-j]
                column[-j] = '0'
        return column

    def drop(self):
        """do something that drop the letter if there are 0 in the box"""
        for column_idx in range(1,self.length):
            column = self.letters_array[1:-1,column_idx]
            self.letters_array[1:-1,column_idx] = self.__drop_column(column)

    def show(self):
        for letters in self.letters_array:
            print(letters)

    # def find_letter(self,x,y,letter):
    #     threebythree = self.letters_array[x-1:x+2,y-1:y+2]
    #     threebythree[1,1] = '0'
    #     possible_answer = np.transpose(np.where(threebythree == letter))
    #     for coordinate in possible_answer:
    #         yield threebythree[coordinate[0]][coordinate[1]], coordinate
    #
    # def find_next(self,x,y):
    #
    #
    #
    #
    # def find_path(self,word):
    #     for letter in list(word):
    #         next = self.find_letter(x,y,letter)
    #         if next is not None:







def classify_length(word_list):
    """preprocess the word list to dictionary of list, copy from Asignment8"""
    whole_dict = {}
    for word in word_list:
        if len(word) in whole_dict:
            whole_dict[len(word)].append(word)
        else:
            whole_dict[len(word)] = [word]
    return whole_dict

def read_wordlist(filename):
    """read the word list"""
    with open(filename) as file:
        return file.read().split()

def input_puzzle(letters_list):
    letter = input()
    if '*' in letter:
        answer_length = []
        answer_pattern = letter.split()
        for pattern in answer_pattern:
            answer_length.append(pattern.count('*'))
        letters_list.append(answer_length)
    else:
        letters_list.append(letter)
        input_puzzle(letters_list)
        return letters_list

def dictionarize(puzzle):
    #join the list member to a string and dictionarize the puzzle letters
    letter = ''.join(puzzle)
    dict = {}
    for idx, char in enumerate(letter):
        if char in dict:
            dict[char] = dict[char]+1
        else:
            dict[char] = 1
    return dict



#------word list tree------------------------
class Node:
    # to be complete
    def __init__(self, data):
        self.data = data
        self.children = {}

    def add_child(self, data):
        self.children[data] = {}

class Trie:
    # to be complete
    def __init__(self):
        self.is_word = False
        self.child = {}

    def add(self, word):
        if word[0] in self.head:
            self.add
        else:
            self.head[word[0]] = {}
            self.add(word[1:])






# this is for sovle_a_word.surround
# where negatvie index of a the grid is nothing
class NoNegativeList(list):
    def __getitem__(self,n):
        if n < 0:
            raise IndexError("...")
        return list.__getitem__(self, n)

class solve_all():
    def __init__(self,letters_list):
        # the grid here and index is like this
        # if you input:
        # abc
        # def
        # ghi
        # ***
        # the grid is
        # ['g','d','a'],['h','e','b'],['i','f','c']
        #
        self.route = []
        self.index = 0 # answer_line index
        self.length = len(letters_list)
        self.grid = NoNegativeList([])
        for i in range(self.length):
            column = NoNegativeList([])
            for j in range(self.length):
                column.append(letters_list[self.length-1-j][i])
            self.grid.append(column)
        print(self.grid)

    # get all surround letter for a specific coordinate
    def surround(self,coordinate):
        x = coordinate[0]
        y = coordinate[1]
        print(self.grid[x][y])
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i!=x or j!=y:
                    try:
                        yield self.grid[i][j], [i,j]
                    except:
                        pass

    # answer_line shoud be a list
    # for example answer_line = list("a**** *** ***")
    def solve(self,answer_line,coordinate):
        if answer_line[self.index] == ' ':
            drop()
            # delete (all the letter before index) in self.grid according to route
            self.index += 1
        else:
            for letter, coordinate in self.surround(coordinate):
                route_copy = self.route.copy()
                if answer_line.has_a_child(letter):# has_a_child() to be implemented
                    route_copy.append(coordinate)
                    answer_line[self.index] = letter
                    self.index += 1
                    solve(answer_line, coordinate)



#finding possible word combnition from wordlist
def W2L(word_dict,letter,number):
    letter_dict = dictionarize(letter)
    result = []
    if number in word_dict:
        #iterate through all the words that have length=number
        for idx,word in enumerate(word_dict[number]):
            #iterate through all the character in a word
            letter_dict_copy = letter_dict.copy()
            flag = True
            for idx,char in enumerate(list(word)):
                if char in letter_dict_copy:
                    if letter_dict_copy[char] == 1:
                        letter_dict_copy.pop(char)
                    else:
                        letter_dict_copy[char] = letter_dict_copy[char] - 1
                else:
                    flag = False
                    break
            if flag:
                result.append(word)
    return result



if __name__== "__main__":
    small_dict = read_wordlist(argv[1])

    # Dead loop, only exit with EOFError
    while True:
        # Loop for each puzzle
        whole_list = input_puzzle([])
        letters_list = whole_list[:-1]
        answer_length = whole_list[-1]






        # test for drop
        # a_wordbox = wordbox(letters_list)
        # a_wordbox.show()
        # a_wordbox.drop()
        # print("   ")
        # a_wordbox.show()



        print(dictionarize(letters_list))
        print(answer_length)
        # Solve for each solution
        for WordNumber in answer_length:
            raw_result = W2L(small_dict, letters_list, WordNumber)
            print(raw_result)
            a_wordbox.find_path(raw_result[0])
