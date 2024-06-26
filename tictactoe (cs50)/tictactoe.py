import sys


def print_state(state):
    print("Current board:")

    for i in range(0, 9, 3):
        print(state[i:i + 3])

    print()


def score_string(string):
    if string == "XXX":
        return 1
    elif string == "OOO":
        return -1

    return 0


def get_winner(state):
    for i in range(0, 9, 3):
        row = state[i:i + 3]
        row_score = score_string(row)

        if row_score != 0:
            return row_score

    for i in range(3):
        col = state[i] + state[i + 3] + state[i + 6]
        col_score = score_string(col)

        if col_score != 0:
            return col_score

    lr_diag = state[0] + state[4] + state[8]
    lr_diag_score = score_string(lr_diag)

    if lr_diag_score != 0:
        return lr_diag_score

    rl_diag = state[2] + state[4] + state[6]
    rl_diag_score = score_string(rl_diag)

    if rl_diag_score != 0:
        return rl_diag_score

    if "." not in state:
        return 0

    return None


def get_available_squares(state):
    return [i for i, cell in enumerate(state) if cell == "."]


def get_children(state, maximizing):
    children = []
    player = "X" if maximizing else "O"

    for i, cell in enumerate(state):
        if cell == ".":
            children.append((i, state[:i] + player + state[i + 1:]))

    return children


def player_move(state, square, symbol):
    return state[:square] + symbol + state[square + 1:]


def max_move(state):
    winner = get_winner(state)

    if winner is not None:
        return -1, state

    max_score = -1
    max_state = state

    for child in get_children(state, True):
        score = min_step(child[1])

        if max_state == state or score > max_score:
            max_score = score
            max_state = child

        print("Moving at", child[0], "results in a", encoded_scores[score])

    return max_state


def min_move(state):
    winner = get_winner(state)

    if winner is not None:
        return -1, state

    min_score = 1
    min_state = state

    for child in get_children(state, False):
        score = max_step(child[1])

        if min_state == state or score < min_score:
            min_score = score
            min_state = child

        print("Moving at", child[0], "results in a", encoded_scores[-score])

    return min_state


def max_step(state):
    winner = get_winner(state)

    if winner is not None:
        return winner

    max_score = -1

    for child in get_children(state, True):
        score = min_step(child[1])

        if score > max_score:
            max_score = score

    return max_score


def min_step(state):
    winner = get_winner(state)

    if winner is not None:
        return winner

    min_score = 1

    for child in get_children(state, False):
        score = max_step(child[1])

        if score < min_score:
            min_score = score

    return min_score


def print_winner(winner):
    if winner == 0:
        print("We tied!")
    elif winner == 1 and ai_token == "X" or winner == -1 and ai_token == "O":
        print("I win!")
    else:
        print("You win!")


def ai_turn(board):
    square, board = max_move(board) if ai_token == "X" else min_move(board)
    print("\nI choose space", square, "\n")
    print_state(board)

    return board


def player_turn(board):
    print("\nYou can move to any of these spaces:", get_available_squares(board))
    board = player_move(board, int(input("Your choice? ")), "X" if ai_token == "O" else "O")
    print_state(board)

    return board


board = sys.argv[1]

encoded_scores = {
    -1: "loss.",
    0: "tie.",
    1: "win."
}

encoded_players = {
    1: "X",
    -1: "O"
}

x_to_move = board.count("X") == board.count("O")

if board == ".........":
    ai_token = input("Should I play as X or O? ")
    ai_moves_first = ai_token == "X"
else:
    ai_token = "X" if board.count("X") == board.count("O") else "O"
    ai_moves_first = True

print_state(board)

while True:
    if ai_moves_first:
        winner = get_winner(board)

        if winner is not None:
            print_winner(winner)

            break

        board = ai_turn(board)
        x_to_move = not x_to_move
        winner = get_winner(board)

        if winner is not None:
            print_winner(winner)

            break

        board = player_turn(board)
        x_to_move = not x_to_move
    else:
        winner = get_winner(board)

        if winner is not None:
            print_winner(winner)

            break

        board = player_turn(board)
        x_to_move = not x_to_move

        winner = get_winner(board)

        if winner is not None:
            print_winner(winner)

            break

        board = ai_turn(board)
        x_to_move = not x_to_move

