#!/usr/bin/env python
# Copyright 2018 JiaxinZhang jiaxin@bu.edu
# Copyright 2018 XunLin xunlin@bu.edu
"""wordbrainsolver"""
import numpy as np
from collections import Counter
from sys import argv

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
    letters_list.append(letter)
    if '*' not in letter:
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
class Trie():

    def __init__(self,word_list):
        self._end = '*'
        self.trie = dict()
        for word in word_list:
            self.add_word(word)

    def __repr__(self):
        return repr(self.trie)

    def add_word(self, word):

        temp_trie = self.trie
        for letter in word:
            if letter in temp_trie:
                temp_trie = temp_trie[letter]
            else:
                temp_trie = temp_trie.setdefault(letter, {})
        temp_trie[self._end] = self._end
        return temp_trie

    def find_next(self, word,next_letter):
        sub_trie = self.trie
        for letter in word:
            sub_trie = sub_trie[letter]
        return (next_letter in sub_trie)

    def find_word(self, word):
        sub_trie = self.trie

        for letter in word:
            if letter in sub_trie:
                sub_trie = sub_trie[letter]
            else:
                return False
        else:
            if self._end in sub_trie:
                return True
            else:
                return False



# this is for sovle_a_word.surround
# where negatvie index of a the grid is nothing
class NoNegativeList(list):
    def __getitem__(self,n):
        if n < 0:
            raise IndexError("...")
        return list.__getitem__(self, n)

class wordbrainsolver():
    def __init__(self,letters_list,trie):
        # the grid here and index is like this
        # if you input:
        # abc
        # def
        # ghi
        # ***
        # the grid is
        # ['g','d','a'],['h','e','b'],['i','f','c']
        #
        self.trie = trie
        #self.index = 0 # answer_line index
        self.length = len(letters_list)
        self.grid = NoNegativeList([])
        for i in range(self.length):
            column = NoNegativeList([])
            for j in range(self.length):
                column.append(letters_list[self.length-1-j][i])
            self.grid.append(column)
        print(self.grid)

    def all_grid(self):
        for x,column in enumerate(self.grid):
            for y,letter in enumerate(column):
                yield letter, [x,y]

    # get all surround letter for a specific coordinate
    def surround(self,coordinate,route):
        x = coordinate[0]
        y = coordinate[1]
        # print(self.grid[x][y])
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if [i,j] not in route:
                    try:
                        yield self.grid[i][j], [i,j]
                    except:
                        pass

    # answer_line shoud be a list
    # for example answer_line = list("a**** *** ***")
    def solve(self, answer_line, coordinate, index,route):
        # print(answer_line)
        if answer_line[index] == ' ':# to be implemented
            print("new word")
            # delete (all the letter before index) in self.grid according to route
            self.solve(answer_line, None, index+1)
        elif len(answer_line) == index+1:
            for letter, coordinate in self.surround(coordinate,route):
                #print(str(answer_line[:index])+letter)
                if self.trie.find_word(''.join(answer_line[:index])+letter):
                    #print("find a word")
                    local_route  = route.copy()
                    local_route.append(coordinate)
                    answer_line[index] = letter
                    print(answer_line)
            #print(' ')

        else:
            if coordinate is None:
                for letter, coordinate in self.all_grid():
                    if self.trie.find_next(answer_line[:index],letter):
                        local_route  = route.copy()
                        local_route.append(coordinate)
                        answer_line[index] = letter
                        self.solve(answer_line, coordinate, index+1,local_route)
            else:
                for letter, coordinate in self.surround(coordinate,route):
                    if self.trie.find_next(answer_line[:index],letter):
                        local_route  = route.copy()
                        local_route.append(coordinate)
                        answer_line[index] = letter
                        self.solve(answer_line, coordinate, index+1,local_route)

if __name__== "__main__":
    small_list = read_wordlist(argv[1])
    small_trie = Trie(small_list)
    # Dead loop, only exit with EOFError
    while True:
        # Loop for each puzzle
        puzzle = input_puzzle([])
        wordbrain = wordbrainsolver(puzzle[:-1],small_trie)
        wordbrain.solve(list(puzzle[-1]),None,0,[])
        exit()





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
