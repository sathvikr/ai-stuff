import collections
import sys


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


def did_player_win(state, player):
    if len(state) % 3 != player:
        return 1

    return -1


def get_loser(state):
    loser = len(state) % 3

    return loser if loser != 0 else 3


def get_player(state):
    return len(state) % 3 + 1


def get_player_value(player, ai_player):
    return 1 if player == ai_player else -1


def get_prev_player(player):
    return player - 1 if player != 1 else 3


def negamax(state, ai_player, current_player):
    if state in words:
        loser = get_loser(state)
        prev_player = get_prev_player(current_player)

        if ai_player in {current_player, prev_player}:
            return -1 if current_player == loser else 1
        elif loser in {current_player, prev_player}:
            return -1
        else:
            return 1

    possible_moves = get_possible_moves(state)

    max_score = -1

    for move in possible_moves:
        child = state + move
        next_player = get_player(child)

        if ai_player in {current_player, next_player}:
            score = -negamax(child, ai_player, next_player)
        else:
            score = negamax(child, ai_player, next_player)

        max_score = max(max_score, score)

    return max_score


def find_winning_moves(state):
    winning_moves = []

    if state in words:
        return winning_moves

    ai_player = get_player(state)

    for move in get_possible_moves(state):
        child = state + move
        next_player = get_player(child)
        score = -negamax(child, ai_player, next_player)

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
