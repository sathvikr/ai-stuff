import string
from math import inf
from pprint import pprint


def read_word_dictionary(filename, min_length):
    words = set()

    with open(filename) as f:
        for line in f:
            word = line.strip().lower()

            if len(word) >= min_length and word.isalpha():
                words.add(word)

    return words


def get_possible_moves(state):
    possible_moves = []

    if state in word_dictionary:
        return possible_moves

    for char in string.ascii_lowercase:
        if " " + state + char in all_words:
            possible_moves.append(char)

    return possible_moves


def get_winner(state):
    return 1 if len(state) % 2 == 0 else -1


def negamax(state, player, alpha, beta):
    if state in word_dictionary:
        return player * get_winner(state)

    max_score = -1

    for move in get_possible_moves(state):
        max_score = max(max_score, -negamax(state + move, -player, -beta, -alpha))
        alpha = max(alpha, max_score)

        if alpha >= beta:
            break

    return max_score


def find_winning_moves(state):
    winning_moves = []
    player = 1 if len(state) % 2 == 0 else -1

    print(get_possible_moves(state))

    for move in get_possible_moves(state):
        score = negamax(state + move, -player, -inf, inf)
        print(move, score)

        if score == -1:
            winning_moves.append(move)

    return winning_moves


word_dictionary = read_word_dictionary("words_all.txt", 4)
all_words = " " + " ".join(word_dictionary)

print(find_winning_moves(""))
