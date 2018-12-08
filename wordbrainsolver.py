#!/usr/bin/env python
# Copyright 2018 JiaxinZhang jiaxin@bu.edu
# Copyright 2018 XunLin xunlin@bu.edu
"""wordbrainsolver"""
import numpy as np
from collections import Counter
from sys import argv
import copy

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

def input_puzzle_wrapper():
    puzzle = input_puzzle([])
    letters_list = puzzle[:-1]
    grid = NoNegativeList([])
    length = len(letters_list)
    for i in range(length):
        column = NoNegativeList([])
        for j in range(length):
            column.append(letters_list[length-1-j][i])
        grid.append(column)
    return grid, puzzle[-1].split(" ")

def drop(grid,route):
    for a_route in sorted(route,key=lambda l:l[1], reverse=True):
        del grid[a_route[0]][a_route[1]]
    for idx, column in enumerate(grid):
        if column == []:
            del grid[idx]
    return grid
#------word list tree------------------------
class Trie():

    def __init__(self,word_list):
        self._end = '*'
        self.trie = dict()
        for word in word_list:
            self.add_word(word)

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
            raise IndexError("666")
        return list.__getitem__(self, n)
    def __copy__(self):
        return NoNegativeList(self)

class one_word_solver():

    def __init__(self,letters_list,trie):
        self.trie = trie
        self.grid = letters_list
        self.all_route = []

        # print(self.grid)
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

    def surround_wrapper(self,coordinate,route):
        if coordinate == None:
            return self.all_grid()
        else:
            return self.surround(coordinate,route)

    def solve(self, answer_line, coordinate, index,route):
        if len(answer_line) == index+1:
            for letter, coordinate in self.surround(coordinate,route):
                if self.trie.find_word(''.join(answer_line[:index])+letter):
                    local_route  = route.copy()
                    local_route.append(coordinate)
                    answer_line[index] = letter
                    self.all_route.append(local_route)
        else:
            for letter, coordinate in self.surround_wrapper(coordinate,route):
                if self.trie.find_next(answer_line[:index],letter):
                    local_route  = route.copy()
                    local_route.append(coordinate)
                    answer_line[index] = letter
                    self.solve(answer_line, coordinate, index+1,local_route)

class wordbrainsolver():
    def __init__(self,trie, answer_list):
        self.trie = trie
        self.answer_list = answer_list

    def solve(self,index,grid):
        if len(self.answer_list) == index+1:
            one_wordbrain = one_word_solver(grid,self.trie)
            one_wordbrain.solve(list(self.answer_list[-1]),None,0,[])
            if one_wordbrain.all_route != []:
                word = ""
                for coordinate in one_wordbrain.all_route[0]:
                    word += grid[coordinate[0]][coordinate[1]]
                for i in range(len(self.answer_list)-1):
                    print(self.answer_list[i])
                print(word)
        else:
            one_wordbrain = one_word_solver(grid, self.trie)
            one_wordbrain.solve(list(self.answer_list[index]),None,0,[])
            for route in one_wordbrain.all_route:
                local_grid = copy.deepcopy(grid)

                word = ""
                for coordinate in route:
                    word += local_grid[coordinate[0]][coordinate[1]]
                self.answer_list[index] = word
                new_grid = drop(local_grid,route)
                self.solve(index+1,new_grid)

if __name__== "__main__":
    small_list = read_wordlist(argv[1])
    small_trie = Trie(small_list)
    # Dead loop, only exit with EOFError
    while True:
        # Loop for each puzzle
        grid, answer_list = input_puzzle_wrapper()

        wordbrain = wordbrainsolver(small_trie, answer_list)
        wordbrain.solve(0,grid)


        print('.')
