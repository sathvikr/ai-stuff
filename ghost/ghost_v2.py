import collections
import sys
from math import inf


def get_words(filename, min_length):
    words = set()

    with open(filename) as f:
        for line in f:
            word = line.strip().upper()

            if len(word) >= min_length and word.isalpha():
                words.add(word)

    return words


def get_words_dictionary(words):
    words_dict = collections.defaultdict(set)

    for word in words:
        for i in range(1, len(word)):
            words_dict[word[:i]].add(word)

    return words_dict


def get_possible_moves(state):
    if state == "":
        return {word[0] for word in words}

    return {word[len(state)] for word in words_dict[state]}


def get_winner(state, ai_player):
    return 1 if len(state) % 2 == ai_player else -1


def get_player(state, num_players):
    return len(state) % num_players


def get_player_value(player, ai_player):
    return 1 if player == ai_player else -1


def negamax(state, ai_player, player, num_players):
    if state in words:
        if num_players > 2:
            num_players -= 1
        else:
            return player * get_winner(state, ai_player)

    possible_moves = get_possible_moves(state)

    if len(possible_moves) == 0:
        return 0

    max_score = -1

    for move in possible_moves:
        child = state + move
        score = -negamax(child, ai_player, get_player_value(get_player(child, num_players), ai_player), num_players)
        max_score = max(max_score, score)

    return max_score


def find_winning_moves(state, num_players):
    winning_moves = []

    if state in words:
        return winning_moves

    player = get_player(state, num_players)

    for move in get_possible_moves(state):
        score = negamax(state + move, player, 1, num_players)

        print(move, score)

        if score == -1:
            winning_moves.append(move)

    return sorted(winning_moves)


filename = "words_test.txt"
min_size = 4
current_state = "app"

words = get_words(filename, min_size)
words_dict = get_words_dictionary(words)
winning_moves = find_winning_moves(current_state, 3)

print(winning_moves)