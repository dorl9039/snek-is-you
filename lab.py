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
    copy_cell.remove(word)
    game["cells"][c] = copy_cell


def move_word_append(game, new_location, location, word):
    """
    Parameters
    game: a dictionary that internally represents the game board.
    location: a tuple with coordinates (i, j) of where the word should be added.
    word: a string representing a Word object.

    Mutates the given game representation to add word to new location and remove it from old.
    """
    c = game['width'] * new_location[0] + new_location[1]
    copy_cell = list(game["cells"][c])
    copy_cell.append(word)
    game["cells"][c] = copy_cell

    remove_word(game, location, word)

def move_word_insert(game, new_location, location, word):
    c = game['width'] * new_location[0] + new_location[1]
    copy_cell = list(game["cells"][c])
    copy_cell.insert(0, word)
    game["cells"][c] = copy_cell

    remove_word(game, location, word)

def get_next_location(game, location, direction):
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

def get_opposite_location(game, location, direction):
    """
    Given a game representation (of the form returned from new_game), coordinates for a location 
    (tuple), and a direction, returns the opposite location of the direction vector if the move is valid. Otherwise returns the original location (as a tuple)
    """
    i, j = location
    delta_i = -(direction_vector[direction][0])
    delta_j = -(direction_vector[direction][1])

    if i + delta_i < 0:
        next_i = i
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

def push(game, copy_game, location, direction, word, roles):
    """
    Pushes an object...??
    """
    i, j = location
    next_i, next_j = get_next_location(game, (i,j), direction)
    next_cell = get_cell(game, next_i, next_j)
    opp_i, opp_j = get_opposite_location(game, (i,j), direction)
    opp_cell = get_cell(game, opp_i, opp_j)

    while word in get_cell(copy_game, i, j): 
        result = True
        if i == next_i and j == next_j:
            return False

        if len(next_cell) != 0:
            for text in next_cell:
                if roles.get(text) and "STOP" in roles.get(text) and "PUSH" in roles.get(text):
                    roles[text].remove("STOP")

            for text in next_cell:
                # checks all the cells in the path of PUSH for a STOP. Keeps objects from moving
                if roles.get(text) and "STOP" in roles.get(text): 
                    return False

            for text in next_cell:    
                if roles.get(text): 
                    if "PUSH" in roles.get(text): 
                        result = result and push(game, copy_game, (next_i, next_j), direction, text, roles)

                    elif "YOU" in roles.get(text):
                        remove_word(copy_game, (i, j), word)
                        move_word_insert(game, (next_i, next_j), (i, j), word)
                        return True

                    if not result:
                        return False

        if len(opp_cell) != 0:
            for text in opp_cell:
                if roles.get(text) and "PULL" in roles.get(text):
                    remove_word(copy_game, (opp_i, opp_j), text)
                    move_word_append(game, (i, j), (opp_i, opp_j),  text) 
        
        remove_word(copy_game, (i, j), word)
        move_word_insert(game, (next_i, next_j), (i, j), word)

    return True


def pull(game, copy_game, location, direction, word, roles):
    i, j = location
    next_i, next_j = get_next_location(game, (i,j), direction)
    next_cell = get_cell(game, next_i, next_j)
    opp_i, opp_j = get_opposite_location(game, (i,j), direction)
    opp_cell = get_cell(game, opp_i, opp_j)

    while word in get_cell(copy_game, i, j):
        #base case: if opp_cell has "STOP" property
        if len(next_cell) != 0:
        # iterates through the cell in case a "STOP" object is within
            for next_text in next_cell:
                if (roles.get(next_text) and "STOP" in roles.get(next_text)) or (i == next_i and j == next_j):
                    return False
                elif roles.get(next_text) and "PUSH" in roles.get(next_text):
                    remove_word(copy_game, (next_i, next_j), next_text)
                    next2_i, next2_j = get_next_location(game, (next_i, next_j), direction)
                    move_word_insert(game, (next2_i, next2_j), (next_i, next_j), next_text)

        #base case: if opp_cell behind "YOU" obj is an edge:
        if i == opp_i and j == opp_j:
            remove_word (copy_game, (i, j), word)
            move_word_append(game, (next_i, next_j), (i, j), word)
            return False

        if len(opp_cell) != 0:
            for opp_text in opp_cell:
                if roles.get(opp_text) and "PULL" in roles.get(opp_text):
                    pull(game, copy_game, (opp_i, opp_j), direction, opp_text, roles)

        remove_word(copy_game, (i, j), word)
        move_word_append(game, (next_i, next_j), (i, j),  word) 
        
    return True

def get_next_cell(game, c, direction):
    i, j = get_coordinates(game, c)
    next_i, next_j = get_next_location(game, (i, j), direction)

    return get_cell(game, next_i, next_j)


def find_subjects(game, i, j, direction, subj_lst):
    """
    Parameters:
    game: representation of gameplay, dictionary with height, width, and cells
    i, j = coordinates
    direction = string
    Returns a list of NOUNS found
    """

    cell = get_cell(game, i, j)
    next_i, next_j = get_next_location(game, (i, j), direction)
    next_cell = get_cell(game, next_i, next_j)

    for x in cell:
        if x in NOUNS:
            subj_lst.append(x.lower())
            for y in next_cell:
                if y == "AND":
                    next2_i, next2_j = get_next_location(game, (next_i, next_j), direction)
                    find_subjects(game, next2_i, next2_j, direction, subj_lst)


def find_predicates(game, i, j, direction, pred_lst):
    """
    Returns a list of PROPERTIES
    """
    cell = get_cell(game, i, j)
    next_i, next_j = get_next_location(game, (i, j), direction)
    next_cell = get_cell(game, next_i, next_j)
    
    for x in cell:
        if x in NOUNS or x in PROPERTIES:
            pred_lst.append(x)
            for y in next_cell:
                if y == "AND":
                    next2_i, next2_j = get_next_location(game, (next_i, next_j), direction)
                    find_predicates(game, next2_i, next2_j, direction, pred_lst)


def parse_rules(game):
    """
    Takes a game representation as argument. Parses through the cells of the game to 
    attribute properties to nouns. Returns roles (a dictionary).
    """
    roles = {}
    noun_swaps = {}

    for word in WORDS:
        roles[word] = "PUSH"

    for c in range(len(game["cells"])):
        if "IS" in game["cells"][c]:
            vert_subj = []
            vert_pred = []
            horz_subj = []
            horz_pred = []

            i, j = get_coordinates(game, c)
            up_i, up_j = get_next_location(game, (i, j), "up")
            down_i, down_j = get_next_location(game, (i, j), "down")
            left_i, left_j = get_next_location(game, (i, j), "left")
            right_i, right_j = get_next_location(game, (i, j), "right")
            
            find_subjects(game, up_i, up_j, "up", vert_subj)
            find_predicates(game, down_i, down_j, "down", vert_pred)

            find_subjects(game, left_i, left_j, "left", horz_subj)
            find_predicates(game, right_i, right_j, "right", horz_pred)

            if vert_pred:
                vert_pred_nouns = []
                vert_pred_props = []
                for pred in vert_pred:
                    if pred in NOUNS:
                        vert_pred_nouns.append(pred)
                    elif pred in PROPERTIES:
                        vert_pred_props.append(pred)

            if horz_pred:
                horz_pred_nouns = []
                horz_pred_props = []
                for pred in horz_pred:
                    if pred in NOUNS:
                        horz_pred_nouns.append(pred)
                    elif pred in PROPERTIES:
                        horz_pred_props.append(pred)

            if vert_subj and vert_pred:
                if vert_pred_props:
                    for subj in vert_subj:
                        if subj.lower() in roles:
                            roles[subj.lower()] += vert_pred_props
                        else:
                            roles[subj.lower()] = vert_pred_props                
                if vert_pred_nouns:
                    for subj in vert_subj:
                        # subj can only mutate into another NOUN once. So any other NOUN in the
                        # predicate list should be disregarded
                        noun_swaps[subj.lower()] = vert_pred_nouns[0].lower()

            if horz_subj and horz_pred:
                if horz_pred_props:
                    for subj in horz_subj:
                        if subj in roles:
                            roles[subj.lower()] += horz_pred_props
                        else:
                            roles[subj.lower()] = horz_pred_props
                if horz_pred_nouns:
                    for subj in horz_subj:
                        # subj can only mutate into another NOUN once. So any other NOUN in the
                        # predicate list should be disregarded
                        noun_swaps[subj.lower()] = horz_pred_nouns[0].lower()

    return roles, noun_swaps


def step_game(game, direction):
    """
    Given a game representation (as returned from new_game), modify that game
    representation in-place according to one step of the game.  The user's
    input is given by direction, which is one of the following:
    {'up', 'down', 'left', 'right'}.

    step_game should return a Boolean: True if the game has been won after
    updating the state, and False otherwise.
    """
    roles = parse_rules(game)[0]
    noun_swaps = parse_rules(game)[1]

    copy_game = {
        "height": game["height"],
        "width": game["width"],
        "cells": list(game["cells"])
    }

    for c in range(len(copy_game["cells"])):
        i, j = get_coordinates(game, c)
        next_i, next_j = get_next_location(game, (i, j), direction)
        #can this just be stored as a tuple variable?
        next_cell = get_cell(game, next_i, next_j)
        opp_i, opp_j = get_opposite_location(game, (i, j), direction)
        opp_cell = get_cell(game, opp_i, opp_j)
        
        for text in copy_game["cells"][c]:
            move_YOU = True
            if i == next_i and j == next_j:
                break

            # moves the YOU object
            if text in roles and "YOU" in roles.get(text):
                if len(next_cell) != 0:
                    for next_text in next_cell:
                        if roles.get(next_text) and "PUSH" in roles.get(next_text):
                            if not push(game, copy_game, (next_i, next_j), direction, next_text, roles):
                                move_YOU = False
                                break
                        elif roles.get(next_text) and "STOP" in roles.get(next_text):
                            move_YOU = False
                            break
                        elif roles.get(next_text) and "DEFEAT" in roles.get(next_text):
                            while text in game["cells"][c]:
                                remove_word(game, (i, j), text)
                            move_YOU = False
                            break

                if not move_YOU:
                    break

                if len(opp_cell) != 0:
                    for opp_text in opp_cell:
                        if roles.get(opp_text) and "PULL" in roles.get(opp_text):
                            if i == opp_i and j == opp_j:
                                break
                            pull(game, copy_game, (opp_i, opp_j), direction, opp_text, roles)     

                if move_YOU:
                    remove_word(copy_game, (i, j), text)
                    move_word_append(game, (next_i, next_j), (i, j), text)
    if noun_swaps:
        for cell in game["cells"]:
            for idx, obj in enumerate(cell):
                if obj in noun_swaps:
                    print("obj:", obj)
                    print("value for obj:", noun_swaps[obj])
                    cell[idx] = noun_swaps[obj]
                    print(game)
                    print()

    # Victory check. Commented out b/c test 20 doesn't have WIN
    print("game at end of move:", game["cells"])
    roles = parse_rules(game)[0]
    you = None
    win = None
    defeat = None
    for x in roles:
        if "YOU" in roles.get(x):
        	you = x

        if "WIN" in roles.get(x):
        	win = x

        if "DEFEAT" in roles.get(x):
            defeat = x

    for c in range(len(game["cells"])):
        if you in game["cells"][c] and defeat in game["cells"][c]:
            i, j = get_coordinates(game, c)
            remove_word(game, (i, j), defeat)
        if you in game["cells"][c] and win in game["cells"][c]:
            return True
    
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