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


def get_winner(state):
    return 1 if len(state) % 2 == 0 else -1


def negamax(state, player, alpha, beta):
    if state in words:
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

    if state in words:
        return winning_moves

    player = 1 if len(state) % 2 == 0 else -1

    for move in get_possible_moves(state):
        score = -negamax(state + move, -player, -inf, inf)

        if score == 1:
            winning_moves.append(move)

    return sorted(winning_moves)


filename = sys.argv[1]
min_size = int(sys.argv[2])
current_state = sys.argv[3].upper() if len(sys.argv) > 3 else ""

words = get_words(filename, min_size)
words_dict = get_words_dictionary(words)
winning_moves = find_winning_moves(current_state)

if len(winning_moves) > 0:
    print(winning_moves)
else:
    print("Next player will lose!")
