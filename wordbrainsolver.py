#!/usr/bin/env python
# Copyright 2018 JiaxinZhang jiaxin@bu.edu
# Copyright 2018 XunLin xunlin@bu.edu
"""wordbrainsolver"""
import copy
from sys import argv


def read_wordlist(filename):
    """read the word list"""
    with open(filename) as file:
        return file.read().split()


def input_puzzle(letters_list):
    """input puzzle"""
    try:
        letter = input()
    except EOFError:
        return letters_list
    letters_list.append(letter)
    if '*' not in letter:
        input_puzzle(letters_list)
    return letters_list


def input_puzzle_wrapper():
    """input puzzle wrapper"""
    puzzle = input_puzzle([])
    letters_list = puzzle[:-1]
    grids = NoNegativeList([])
    length = len(letters_list)
    for i in range(length):
        column = NoNegativeList([])
        for j in range(length):
            column.append(letters_list[length - 1 - j][i])
        grids.append(column)
    return grids, puzzle[-1].split(" ")


def drop(grids, route):
    """drop a Grid"""
    for a_route in sorted(route, key=lambda l: l[1], reverse=True):
        del grids[a_route[0]][a_route[1]]
    for idx, column in enumerate(grids):
        if column == []:
            # del Grid[idx]
            grids[idx] = ['0']
    return grids
# ------word list tree------------------------


class Trie():
    """Words are saved in the Trie dictionary"""

    def __init__(self, word_list):
        self._end = '*'
        self.trie = dict()
        for word in word_list:
            self.add_word(word)

    def add_word(self, word):
        """add a word to the Trie"""
        temp_trie = self.trie
        for letter in word:
            if letter in temp_trie:
                temp_trie = temp_trie[letter]
            else:
                temp_trie = temp_trie.setdefault(letter, {})
        temp_trie[self._end] = self._end
        return temp_trie

    def find_next(self, word, next_letter):
        """find next letter in the Trie"""
        sub_trie = self.trie
        for letter in word:
            sub_trie = sub_trie[letter]
        return (next_letter in sub_trie)

    def find_word(self, word):
        """determine if the path is a word"""
        sub_trie = self.trie
        for letter in word:
            if letter in sub_trie:
                sub_trie = sub_trie[letter]
            else:
                return False
        else:
            return bool(self._end in sub_trie)


# this is for sovle_a_word.surround
class NoNegativeList(list):
    """Negatvie index of a the grid is nothing"""

    def __getitem__(self, n):
        if n < 0:
            raise IndexError("666")
        return list.__getitem__(self, n)

    def __copy__(self):
        return NoNegativeList(self)


class Onewordsolver():
    """solve one word"""

    def __init__(self, letters_list, trie):
        self.trie = trie
        self.grid = letters_list
        self.all_route = []
        # print(self.grid)

    def all_grid(self):
        """iterate the grid"""
        for x_x, column in enumerate(self.grid):
            for y_y, letter in enumerate(column):
                yield letter, [x_x, y_y]

    def surround(self, coordinate, route):
        """get all surround letter for a specific coordinate"""
        x_x = coordinate[0]
        y_y = coordinate[1]
        # print(self.grid[x][y])
        for i in range(x_x - 1, x_x + 2):
            for j in range(y_y - 1, y_y + 2):
                if [i, j] not in route:
                    try:
                        yield self.grid[i][j], [i, j]
                    except BaseException:
                        pass

    def surround_wrapper(self, coordinate, route):
        """wrapp and return the coordinate and route"""
        if coordinate is None:
            return self.all_grid()
        else:
            return self.surround(coordinate, route)

    def solve(self, old_answer_line, coordinate, index, route, global_index):
        """recursion solver for one word"""
        answer_line = old_answer_line.copy()
        global ORIGINAL_HINT
        if len(answer_line) == index + \
                1 and ORIGINAL_HINT[global_index][index] == '*':
            for letter, coordinates in self.surround(coordinate, route):
                if self.trie.find_word(''.join(answer_line[:index]) + letter):
                    local_route = route.copy()
                    local_route.append(coordinates)
                    answer_line[index] = letter
                    self.all_route.append(local_route)

        elif len(answer_line) == index + 1 and ORIGINAL_HINT[global_index][index] != '*':
            for letter, coordinates in self.surround(coordinate, route):
                if self.trie.find_word(''.join(
                        answer_line[:index]) + letter) and letter == ORIGINAL_HINT[global_index][index]:
                    local_route = route.copy()
                    local_route.append(coordinates)
                    answer_line[index] = letter
                    self.all_route.append(local_route)

        elif ORIGINAL_HINT[global_index][index] != '*':
            # print(original_hint[global_index])
            # print(answer_line)
            # print("global_index = "+str(global_index))
            # print("letter index = "+str(index))
            # print("gird = "+str(np.asarray(self.grid)))
            # print("letter = "+str(original_hint[global_index][index]))
            coordinates = []
            for idx1, column in enumerate(self.grid):
                for idx2, letter in enumerate(column):
                    if letter == ORIGINAL_HINT[global_index][index]:
                        coordinates.append([idx1, idx2])
            for coord in coordinates:
                local_route = route.copy()
                local_route.append(coord)
                self.solve(
                    answer_line,
                    coord,
                    index + 1,
                    local_route,
                    global_index)
        else:
            for letter, coordinates in self.surround_wrapper(
                    coordinate, route):
                if self.trie.find_next(answer_line[:index], letter):
                    local_route = route.copy()
                    local_route.append(coordinates)
                    answer_line[index] = letter
                    self.solve(
                        answer_line,
                        coordinates,
                        index + 1,
                        local_route,
                        global_index)


class Wordbrainsolver():
    """solve multiple words"""

    def __init__(self, trie, answer_list):
        self.trie = trie
        self.answer_list = answer_list
        self.print_history = []

    def solve(self, index, grid):
        """recursion solver for multiple words"""
        if len(self.answer_list) == index + 1:
            one_wordbrain = Onewordsolver(grid, self.trie)
            one_wordbrain.solve(list(self.answer_list[-1]), None, 0, [], index)

            words = ""
            for i in range(len(self.answer_list) - 1):
                words += (str(self.answer_list[i]) + ' ')

            for route in one_wordbrain.all_route:
                last_word = ""
                for coordinate in route:
                    last_word += grid[coordinate[0]][coordinate[1]]
                self.print_history.append(words + last_word)
        else:
            one_wordbrain = Onewordsolver(grid, self.trie)
            one_wordbrain.solve(
                list(
                    self.answer_list[index]),
                None,
                0,
                [],
                index)
            for route in one_wordbrain.all_route:
                local_grid = copy.deepcopy(grid)
                word = ""
                for coordinate in route:
                    word += local_grid[coordinate[0]][coordinate[1]]
                self.answer_list[index] = word
                new_grid = drop(local_grid, route)
                self.solve(index + 1, new_grid)


if __name__ == "__main__":
    SMALL_LIST = read_wordlist(argv[1])
    LARGE_LIST = read_wordlist(argv[2])
    SMALL_TRIE = Trie(SMALL_LIST)
    LARGE_TRIE = Trie(LARGE_LIST)
    # Dead loop, only exit with EOFError
    while True:
        # Loop for each puzzle
        GRID, ANSWER_LIST = input_puzzle_wrapper()
        ORIGINAL_HINT = ANSWER_LIST.copy()
        ANSWER_COPY = ANSWER_LIST.copy()
        WORD_BRAIN = Wordbrainsolver(SMALL_TRIE, ANSWER_LIST)
        WORD_BRAIN.solve(0, GRID)
        PRINT_HISTORY = list(set(WORD_BRAIN.print_history))
        if PRINT_HISTORY == []:
            WORD_BRAIN = Wordbrainsolver(LARGE_TRIE, ANSWER_LIST)
            WORD_BRAIN.solve(0, GRID)
            PRINT_HISTORY = list(set(WORD_BRAIN.print_history))
        PRINT_HISTORY.sort()
        for answer in PRINT_HISTORY:
            print(answer)
        print('.')
