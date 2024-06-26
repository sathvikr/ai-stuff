import sys


def print_state(state):
    print("Current board:")

    for i in range(0, 9, 3):
        print(state[i:i + 3])

    print()


def score_string(string, x_to_move):
    if x_to_move:
        if string == "XXX":
            return 1
        elif string == "OOO":
            return -1
    else:
        if string == "XXX":
            return -1
        elif string == "OOO":
            return 1

    return 0


def get_winner(state, x_to_move):
    for i in range(0, 9, 3):
        row = state[i:i + 3]
        row_score = score_string(row, x_to_move)

        if row_score != 0:
            return row_score

    for i in range(3):
        col = state[i] + state[i + 3] + state[i + 6]
        col_score = score_string(col, x_to_move)

        if col_score != 0:
            return col_score

    lr_diag = state[0] + state[4] + state[8]
    lr_diag_score = score_string(lr_diag, x_to_move)

    if lr_diag_score != 0:
        return lr_diag_score

    rl_diag = state[2] + state[4] + state[6]
    rl_diag_score = score_string(rl_diag, x_to_move)

    if rl_diag_score != 0:
        return rl_diag_score

    if "." not in state:
        return 0

    return None


def get_children(state, x_to_move):
    children = []
    player = "X" if x_to_move else "O"

    for i, cell in enumerate(state):
        if cell == ".":
            children.append(state[:i] + player + state[i + 1:])

    return children


def negamax(state, x_to_move):
    winner = get_winner(state, x_to_move)

    if winner is not None:
        return winner, state

    max_score = -1
    max_state = state

    for child in get_children(state, x_to_move):
        score = -negamax(child, not x_to_move)[0]

        if max_state == state or score > max_score:
            max_score = score
            max_state = child

    return max_score, max_state


def ai_move(state, x_to_move):
    max_score, max_square = -1, -1
    max_state = state

    for i, cell in enumerate(state):
        if cell == ".":
            child = make_move(state, i, "X" if x_to_move else "O")
            score = -negamax(child, not x_to_move)[0]

            if max_state == state or score > max_score:
                max_score = score
                max_square = i
                max_state = child

            print("Moving at", i, "results in a", encoded_scores[score])

    return max_square, max_state


def get_available_squares(state):
    return [i for i, cell in enumerate(state) if cell == "."]


def make_move(state, square, token):
    return state[:square] + token + state[square + 1:]


def player_move(state, square, available_squares, x_to_move):
    if square in available_squares:
        symbol = "X" if x_to_move else "O"

        return state[:square] + symbol + state[square + 1:]
    else:
        return None


def print_winner(winner):
    if winner == 1:
        print("I win!")
    elif winner == 0:
        print("We tied!")
    else:
        print("You win!")


def ai_turn(board):
    square, board = ai_move(board, x_to_move)
    print("\nI choose space " + str(square) + ".\n")
    print_state(board)

    return board


def player_turn(board):
    available_squares = get_available_squares(board)
    print("\nYou can move to any of these squares:", available_squares)
    board = player_move(board, int(input("Your choice? ")), available_squares, x_to_move)
    print_state(board)

    return board


board = sys.argv[1]

encoded_scores = {
    1: "win",
    0: "tie",
    -1: "loss"
}

x_to_move = board.count("X") == board.count("O")

if board == ".........":
    ai_moves_first = input("Should I play as X or O? ") == "X"
else:
    ai_moves_first = True

print_state(board)

while True:
    if ai_moves_first:
        winner = get_winner(board, x_to_move)

        if winner is not None:
            print_winner(winner)

            break

        board = ai_turn(board)
        x_to_move = not x_to_move
        winner = get_winner(board, not x_to_move)

        if winner is not None:
            print_winner(winner)

            break

        board = player_turn(board)
        x_to_move = not x_to_move
    else:
        winner = get_winner(board, not x_to_move)

        if winner is not None:
            print_winner(winner)

            break

        board = player_turn(board)
        x_to_move = not x_to_move

        winner = get_winner(board, x_to_move)

        if winner is not None:
            print_winner(winner)

            break

        board = ai_turn(board)
        x_to_move = not x_to_move
