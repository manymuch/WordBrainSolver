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
        print(self.letters_array)
        for i in range(1, self.length-1):
            self.letters_array[i] = [0]+list(letters_list[i-1])+[0]


    def drop(self):
        """do something that drop the letter if there are 0 in the box"""
        pass

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

if __name__== "__main__":
    small_dict = classify_length(read_wordlist(argv[1]))


    letters_list = []
    while True:
        letter = input()
        if '*' in letter:
            answer_format = letter
            break
        else:
            letters_list.append(letter)
    a_wordbox = wordbox(letters_list)
    a_wordbox.show()
