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
    small_dict = classify_length(read_wordlist(argv[1]))


    # Dead loop, only exit with EOFError
    while True:
        letters_list = []
        answer_length = []
        flag = False
        # Loop for each puzzle
        while True:
            letter = input()
            if '*' in letter:
                answer_pattern = letter.split()
                for pattern in answer_pattern:
                    answer_length.append(pattern.count('*'))
                flag = True
                break
            else:
                if flag:
                    break
                else:
                    letters_list.append(letter)
        a_wordbox = wordbox(letters_list)
        a_wordbox.show()
        print(dictionarize(letters_list))
        print(answer_length)
        # Solve for each solution
        for WordNumber in answer_length:
            raw_result = W2L(small_dict, letters_list, WordNumber)
            print(raw_result)
    # ---------------------quit---------------------
