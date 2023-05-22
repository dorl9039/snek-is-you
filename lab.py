"""6.009 Lab 10: Snek Is You Video Game"""

import doctest

# NO ADDITIONAL IMPORTS!

# All words mentioned in lab. You can add words to these sets,
# but only these are guaranteed to have graphics.
NOUNS = {"SNEK", "FLAG", "ROCK", "WALL", "COMPUTER", "BUG"}
PROPERTIES = {"YOU", "WIN", "STOP", "PUSH", "DEFEAT", "PULL"}
WORDS = NOUNS | PROPERTIES | {"AND", "IS"}

# Maps a keyboard direction to a (delta_row, delta_column) vector.
direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


class Text:
    """
    A subclass of class Word that represents a family of graphical objects on the board. E.g., "ROCK" refers to all graphical objects
    represented by "rock". All Nouns can be assigned properties, which are specific behaviors like 
    'push' and 'win'.
    """
    def __init__(self, word):
        self.word = word

SNEK = Text("SNEK")


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, where UPPERCASE
    strings represent word objects and lowercase strings represent regular
    objects (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['snek'], []],
        [['SNEK'], ['IS'], ['YOU']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.

    Returns game representation as a dictionary with keys: height (int), width (int),
    and cells (list of lists).
    """
    game = {
        "height": len(level_description),
        "width": len(level_description[0]),
        "cells": []
    }

    for row in level_description:
        for cell in row:
            game["cells"].append(cell)
    
    return game

def get_cell(game, i, j):
    """
    Given coordinates of row i and column j, returns the specified cell in the game representation.
    """
    cell = game["width"] * i + j
    return game["cells"][cell]

def get_coordinates(game, c):
    """
    Given an index of game["cells"], c, returns the cell's coordinates as a tuple.
    """
    i = c // game["width"]
    j = c % game["width"]
    return (i, j)

def add_word(game, location, word):
    """
    Parameters
    game: a dictionary that internally represents the game board.
    location: a tuple with coordinates (i, j) of where the word should be added.
    word: a string representing a Word object.

    Mutates the given game representation to add word to new location.
    """
    c = game['width'] * location[0] + location[1]
    copy_cell = list(game["cells"][c])
    copy_cell.append(word)
    game["cells"][c] = copy_cell

def remove_word(game, location, word):
    """
    Parameters
    game: a dictionary that internally represents the game board.
    location: a tuple with coordinates (i, j) of where the word should be added.
    word: a string representing a Word object.

    Mutates the given game representation to remove word from cell (i, j).
    """
    c = game["width"] * location[0] + location[1]
    copy_cell = list(game["cells"][c])
    # print("copy_cell:", copy_cell)
    # print("word:", word)
    copy_cell.remove(word)
    game["cells"][c] = copy_cell

def move_word(game, new_location, location, word):
    add_word(game, new_location, word)
    remove_word(game, location, word)

def next_location(game, location, direction):
    """
    Given a game representation (of the form returned from new_game), coordinates for a location 
    (tuple), and a direction, returns the new location (as a tuple) of the objects in the cell 
    if the move is valid. Otherwise returns the original location (as a tuple)
    """
    i, j = location
    delta_i = direction_vector[direction][0]
    delta_j = direction_vector[direction][1]

    if i + delta_i < 0:
        next_i = i
        print(f"i + delta_i < 0. next_i {next_i} = i {i}")
    elif i + delta_i >= game["height"]:
        next_i = i
    else:
        next_i = i + delta_i

    if j + delta_j < 0:
        next_j = j
    elif j + delta_j >= game["width"]:
        next_j = j
    else:
        next_j = j + delta_j

    return (next_i, next_j)


def push(game, copy_game, location, direction, word=None):
    # word should be passed in once I figure out how to do this non-hard-coded. 
    # Perhaps use isinstance on word for Push, Stop, etc?
    # print()
    # print("game:", game)
    # print("copy_game:", copy_game)
    # print("first line word:", word)
    i, j = location
    next_i, next_j = next_location(game, (i,j), direction)
    # print(f"i = {i}, j = {j}, next_i = {next_i}, next_j = {next_j}")

    if i == next_i and j == next_j:
        # print("i == next_i, j == next_j")
        return False
    
    wall = "wall"
    rock = "rock"

    if wall in get_cell(game, next_i, next_j):
        return False
    elif len(get_cell(game, next_i, next_j)) != 0:
        # print("elif: next cell is not empty")
        text = get_cell(game, next_i, next_j)[0]
        # print("word in next cell is:", word)
        result = push(game, copy_game, (next_i, next_j), direction, text)
        if not result:
            return False
    # elif word in get_cell(game, next_i, next_j):
    #     print("enter elif")
    #     # print("rock is in", f'next_i: {next_i}, next_j: {next_j}, {get_cell(game, next_i, next_j)}')
    #     result = push(game, copy_game, (next_i, next_j), direction, word)
    #     if not result:
    #         return False
    # print("last line word:", word)
    remove_word(copy_game, (i, j), word)
    move_word(game, (next_i, next_j), (i, j), word)


    return True

    # for obj in get_cell(game, next_i, next_j):
    #     if isinstance(obj, Stop):
    #         return False
    #     elif isinstance(obj, Push):
    #         return push(game, (next_i, next_j), direction, obj)
    #     else:
    #         remove_word(copy_game, (i, j), obj)
    #         move_word(game, (next_i, next_j), (i, j), obj)
    #         return game


def step_game(game, direction):
    """
    Given a game representation (as returned from new_game), modify that game
    representation in-place according to one step of the game.  The user's
    input is given by direction, which is one of the following:
    {'up', 'down', 'left', 'right'}.

    step_game should return a Boolean: True if the game has been won after
    updating the state, and False otherwise.
    """
    copy_game = {
        "height": game["height"],
        "width": game["width"],
        "cells": list(game["cells"])
    }
    snek = "snek"
    wall = "wall"
    rock = "rock"


    can_move = True
    # Iterates through all the cells
    for c in range(len(copy_game["cells"])):
        # focuses on cells that have snek in them
        while snek in copy_game["cells"][c]:
            i, j = get_coordinates(game, c)
            next_i, next_j = next_location(game, (i, j), direction)
            print(f"i = {i}, next_i = {next_i}, j = {j}, next_j = {next_j}")
            # snek can't move if wall is in its way
            if wall in get_cell(game, next_i, next_j):
                return False

            # snek can push the rock, but only if there isn't a wall or edge in its way
            elif rock in get_cell(game, next_i, next_j):
                print("entered elif rock in get cell")
                if not push(game, copy_game, (next_i, next_j), direction, rock):
                    return False
            # snek can push text objects, but only if there isn't a wall or edge in its way
            # and if other objects in front of it have push property
            elif len(get_cell(game, next_i, next_j)) > 0 and get_cell(game, next_i, next_j)[0] in WORDS:
                print("entered elif text in get cell")
                word = get_cell(game, next_i, next_j)[0]
                if not push(game, copy_game, (next_i, next_j), direction, word):
                    return False

                    
                # secondary_i, secondary_j = new_location(game, (next_i, next_j), direction)
                # if wall in get_cell(game, secondary_i, secondary_j):
                #     can_move = False
                #     break
                # elif rock in get_cell(game, secondary_i, secondary_j):

                    #recursion?? Need to keep pushing rocks as long as its possible 

            # if can_move:
            remove_word(copy_game, (i, j), snek)
            move_word(game, (next_i, next_j), (i, j), snek)

    
    return False


def dump_game(game):
    """
    Given a game representation (as returned from new_game), convert it back
    into a level description that would be a suitable input to new_game.

    This function is used by the GUI and tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    level_description = []
    for row in range(game["height"]):
        row_description = []

        for column in range(game["width"]):
            cell = get_cell(game, row, column)
            row_description.append(cell)

        level_description.append(row_description)

    return level_description