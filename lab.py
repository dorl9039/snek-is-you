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


def get_cell(game, location):
    """
    Given location coordinates of row i and column j as a tuple, returns the specified 
    cell (a list) in the game representation.
    """
    i, j = location
    cell = game["width"] * i + j
    return game["cells"][cell]


def get_coordinates(game, c):
    """
    Given an index of game["cells"], c, returns the cell's coordinates as a 
    tuple.
    """
    i = c // game["width"]
    j = c % game["width"]
    return i, j


def remove_word(game, location, word):
    """
    Given parameters:
        game: a dictionary that internally represents the game board.
        location = a tuple of integers representing coordinates
        word: a string representing a Word object.

    Mutates the given game representation to remove word from cell (i, j).
    """
    i, j = location
    c = game["width"] * i + j
    copy_cell = list(game["cells"][c])
    copy_cell.remove(word)
    game["cells"][c] = copy_cell


def move_word_append(game, new_location, location, word):
    """
    Given parameters:
        game: a dictionary that internally represents the game board.
        new_location: a tuple of integers representing the coordinates of where 
            the word should be added.
        location: a tuple of integers representing the coordinates of where the word
            should be removed.
        word: a string representing a Word object.

    Mutates the given game representation by appending word to cell in new 
        location.
    """
    new_i, new_j = new_location
    c = game['width'] * new_i + new_j
    copy_cell = list(game["cells"][c])
    copy_cell.append(word)
    game["cells"][c] = copy_cell

    remove_word(game, location, word)


def move_word_insert(game, new_location, location, word):
    """
    Given parameters:
        game: a dictionary that internally represents the game board.
        new_location: a tuple of integers representing the coordinates of where 
            the word should be added.
        location: a tuple of integers representing the coordinates of where the 
            word should be removed.
        word: a string representing a Word object.

    Mutates the given game representation by inserting word to cell in new 
        location.
    """
    new_i, new_j = new_location
    c = game['width'] * new_i + new_j
    copy_cell = list(game["cells"][c])
    copy_cell.insert(0, word)
    game["cells"][c] = copy_cell

    remove_word(game, location, word)


def get_next_location(game, location, direction):
    """
    Given parameters:
        game: a representation (of the form returned from new_game)
        location: coordinates (tuple) for the starting cell
        direction: a string that maps to an element in direction_vector
    
    Returns the new location (a tuple) of the objects in the cell if the move
        is valid. Otherwise returns the original location (as a tuple)
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

    return next_i, next_j


def get_opposite_location(game, location, direction):
    """
    Given parameters:
        game: a representation of the game board, of the form returned from new_game
        location: coordinates (tuple) for the starting cell
        direction: a string that maps to an element in direction_vector

    Returns the opposite location of the direction vector if the move is valid. 
    Otherwise returns the original location (as a tuple)
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

    return next_i, next_j


def push(game, copy_game, location, direction, word, roles):
    """
    Given parameters:
        game: a list representation of the game board.
        copy_game: a copy of game...not sure why I need it??
        location: a tuple, coordinates of the object with PUSH behavior.
        direction: a string that maps to direction_vectors.
        word: a string representing the PUSH object.
        roles: a dictionary mapping properties to objects.

    Mutates game with by PUSHing objects along until it isn't possible, 
    in which case returns False. 
    """
    next_location = get_next_location(game, location, direction)
    next_cell = get_cell(game, next_location)
    opp_location = get_opposite_location(game, location, direction)
    opp_cell = get_cell(game, opp_location)

    while word in get_cell(copy_game, location): 
        if location == next_location:
            return False
        if len(next_cell) != 0:
            # Checks all the cells for possible obstructions to PUSH
            for next_text in next_cell:
                # An object with STOP and PUSH priorities should PUSH.
                if roles.get(next_text) and "STOP" in roles.get(next_text) \
                    and "PUSH" in roles.get(next_text):
                    roles[next_text].remove("STOP")
                # Object can't be pushed into another object with STOP property.
                if roles.get(next_text) and "STOP" in roles.get(next_text): 
                    return False

            for next_text in next_cell:   
                # Looks to next cell to determine PUSH behavior 
                if roles.get(next_text) and "PUSH" in roles.get(next_text): 
                    if not push(game, copy_game, next_location, direction, next_text, roles):
                        return False
        # Checks for objects behind to PULL
        if len(opp_cell) != 0:
            for opp_text in opp_cell:
                # Object being PULLed should not have PUSH behavior
                if roles.get(opp_text) and "PULL" in roles.get(opp_text) \
                    and "PUSH" not in roles.get(opp_text):
                    remove_word(copy_game, opp_location, opp_text)
                    move_word_append(game, location, opp_location,  opp_text)

        remove_word(copy_game, location, word)
        move_word_insert(game, next_location, location, word)

    return True


def pull(game, copy_game, location, direction, word, roles):
    """
    Given parameters:
        game: a list representation of the game board.
        copy_game: a copy of game...not sure why I need it??
        location: a tuple, coordinates of the PULL object.
        direction: a string that maps to direction_vectors.
        word: a string representing the PULL object.
        roles: a dictionary mapping properties to objects.

    Mutates game with by PULLing objects along until it isn't possible, 
    in which case returns False. 
    """
    i, j = location
    next_location = get_next_location(game, location, direction)
    next_cell = get_cell(game, next_location)
    opp_location = get_opposite_location(game, location, direction)
    opp_cell = get_cell(game, opp_location)

    while word in get_cell(copy_game, location):
        if len(next_cell) != 0:
            for next_text in next_cell:
                # Prevents object from being PULLed through an obstruction. 
                # E.g., if YOU is overlaid with a STOP object.
                if (roles.get(next_text) and "STOP" in roles.get(next_text)) \
                    or (location == next_location):
                    return False
                # a PUSH object can PULL objects behind it
                elif roles.get(next_text) and "PUSH" in roles.get(next_text) \
                    and "PULL" not in roles.get(next_text):
                    remove_word(copy_game, next_location, next_text)
                    next2_location = get_next_location(game, next_location, direction)
                    move_word_insert(game, next2_location, next_location, next_text)

        # Ensures the last object in the PULL chain still gets moved
        if location == opp_location:
            remove_word (copy_game, location, word)
            move_word_append(game, next_location, location, word)
            return False
        # Recursively checks and calls pull on subsequent PULL objects
        if len(opp_cell) != 0:
            for opp_text in opp_cell:
                if roles.get(opp_text) and "PULL" in roles.get(opp_text):
                    pull(game, copy_game, opp_location, direction, opp_text, roles)

        remove_word(copy_game, location, word)
        move_word_append(game, next_location, location,  word) 

    return True


def find_subjects(game, location, direction, subj_lst):
    """
    Given parameters:
        game: a list of lists representing the game board
        location: a tuple for the coordinates of the "IS" cell
        direction: a string that maps to direction_vector. Subjects are only 
            ever either "up" or "left" of the IS cell.
        subj_list: a list of NOUNS.

    Finds NOUNS and mutates subj_list by appending NOUNS found.
    """

    cell = get_cell(game, location)
    next_location= get_next_location(game, location, direction)
    next_cell = get_cell(game, next_location)

    for x in cell:
        if x in NOUNS:
            subj_lst.append(x.lower())
            for y in next_cell:
                if y == "AND":
                    next2_location = get_next_location(game, next_location, direction)
                    find_subjects(game, next2_location, direction, subj_lst)


def find_predicates(game, location, direction, pred_lst):
    """
    Given parameters:
        game: a list of lists representing the game board
        location: a tuple for the coordinates of the "IS" cell
        direction: a string that maps to direction_vector. Predicates are only 
            ever either "down" or "right" of the IS cell.
        pred_list: a list of NOUNS or PROPERTIES.

    Finds NOUNS or PROPERTIES and mutates pred_list by appending found words.
    """
    cell = get_cell(game, location)
    next_location= get_next_location(game, location, direction)
    next_cell = get_cell(game, next_location)

    for x in cell:
        if x in NOUNS or x in PROPERTIES:
            pred_lst.append(x)
            for y in next_cell:
                if y == "AND":
                    next2_location = get_next_location(game, next_location, direction)
                    find_predicates(game, next2_location, direction, pred_lst)


def parse_rules(game):
    """
    Takes a game representation as argument. Parses through the cells of the game to 
    attribute PROPERTIES to NOUNS or NOUNS to NOUNS. 
    Returns a dictionary of roles and a dictionary of NOUNS to be swapped.
    """
    roles = {}
    noun_swaps = {}

    # All WORDS have only PUSH property
    for word in WORDS:
        roles[word] = "PUSH"

    for c in range(len(game["cells"])):
        if "IS" in game["cells"][c]:
            vert_subj = []
            vert_pred = []
            horz_subj = []
            horz_pred = []

            location = get_coordinates(game, c)
            up_location = get_next_location(game, location, "up")
            down_location = get_next_location(game, location, "down")
            left_location = get_next_location(game, location, "left")
            right_location = get_next_location(game, location, "right")
            
            find_subjects(game, up_location, "up", vert_subj)
            find_predicates(game, down_location, "down", vert_pred)

            find_subjects(game, left_location, "left", horz_subj)
            find_predicates(game, right_location, "right", horz_pred)

            # Splits up vertical predicates into NOUNS and PROPERTIES to be
            # handled differently later
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
                # Assigns PROPERTIES to NOUNS in roles dictionary
                if vert_pred_props:
                    for subj in vert_subj:
                        if subj.lower() in roles:
                            roles[subj.lower()] += vert_pred_props
                        else:
                            roles[subj.lower()] = vert_pred_props                
                if vert_pred_nouns:
                    for subj in vert_subj:
                        # Subject(s) can only mutate into another NOUN once. 
                        # So any other NOUN in the predicate list can be disregarded
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

    copy_game = {
        "height": game["height"],
        "width": game["width"],
        "cells": list(game["cells"])
    }

    for c in range(len(copy_game["cells"])):
        location = get_coordinates(game, c)
        next_location = get_next_location(game, location, direction)
        next_cell = get_cell(game, next_location)
        opp_location = get_opposite_location(game, location, direction)
        opp_cell = get_cell(game, opp_location)
        
        for text in copy_game["cells"][c]:
            move_YOU = True
            if location == next_location:
                break

            if text in roles and "YOU" in roles.get(text):
                if len(next_cell) != 0:
                    for next_text in next_cell:
                        if roles.get(next_text) and "PUSH" in roles.get(next_text):
                            if not push(game, copy_game, next_location, direction, next_text, roles):
                                move_YOU = False
                                break
                        elif roles.get(next_text) and "STOP" in roles.get(next_text):
                            move_YOU = False
                            break
                        elif roles.get(next_text) and "DEFEAT" in roles.get(next_text):
                            while text in game["cells"][c]:
                                remove_word(game, location, text)
                            move_YOU = False
                            break

                if not move_YOU:
                    break

                if len(opp_cell) != 0:
                    for opp_text in opp_cell:
                        if roles.get(opp_text) and "PULL" in roles.get(opp_text):
                            if location == opp_location:
                                break
                            pull(game, copy_game, opp_location, direction, opp_text, roles)     

                if move_YOU:
                    remove_word(copy_game, location, text)
                    move_word_append(game, next_location, location, text)
    
    # Mutate game board to reflect rules regarding NOUN swaps.
    # Happens after objects move because an object can only change types at
    # most once a turn.
    noun_swaps = parse_rules(game)[1]
    if noun_swaps:
        for cell in game["cells"]:
            for idx, obj in enumerate(cell):
                if obj in noun_swaps:
                    cell[idx] = noun_swaps[obj]
   
    # Victory check
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
            location = get_coordinates(game, c)
            remove_word(game, location, defeat)
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
            cell = get_cell(game, (row, column))
            row_description.append(cell)

        level_description.append(row_description)

    return level_description