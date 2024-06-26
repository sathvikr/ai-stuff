
def nicely_print(board):
    size = int(len(board) ** 0.5)
    board_rows = [board[i:i + size] for i in range(0, len(board), size)]

    for row in board_rows:
        print(" ".join(list(row)))


def add_border(board):
    new_board = "??????????"

    for i in range(0, 64, 8):
        new_board += "?" + board[i:i + 8] + "?"

    return new_board + "??????????"


def get_bordered_index(original_index):
    return original_index // 8 * 2 + original_index + 11


def get_original_index(bordered_index):
    return bordered_index - 11 - (bordered_index - 10) // 10 * 2


def get_outflanking_index(board, token, index, direction):
    opposite_token = "o" if token == "x" else "x"
    steps = 1
    location = index + steps * direction

    while board[location] == opposite_token:
        steps += 1
        location = index + steps * direction

    if steps > 1 and board[location] == token:
        return get_original_index(location)

    return -1


def get_outflanking_info(board, token, index):
    outflanking_info = []
    original_directions = (-1, 1, -7, 7, -8, 8, -9, 9)
    directions = (-1, 1, -9, 9, -10, 10, -11, 11)

    for i in range(len(directions)):
        original_direction, direction = original_directions[i], directions[i]
        outflanking_index = get_outflanking_index(board, token, index, direction)

        if outflanking_index != -1:
            outflanking_info.append((outflanking_index, original_direction))

    return outflanking_info


def is_outflanking(board, token, index):
    directions = (-1, 1, -9, 9, -10, 10, -11, 11)

    for direction in directions:
        outflanking_index = get_outflanking_index(board, token, index, direction)

        if outflanking_index != -1:
            return True

    return False


def possible_moves(board, token):
    new_board = add_border(board)
    possible_moves = []

    for i, cell in enumerate(board):
        if cell == "." and is_outflanking(new_board, token, get_bordered_index(i)):
            possible_moves.append(i)

    return possible_moves


def is_game_over(board):
    return board.count(".") == 0 or len(possible_moves(board, "x")) == 0 and len(possible_moves(board, "o")) == 0


def get_winner(board, player):
    player_count = board.count(player)
    opposite_count = board.count("o" if player == "x" else "x")

    if player_count > opposite_count:
        return 1
    if opposite_count > player_count:
        return -1

    return 0


def make_move(board, token, index):
    outflanking_info = get_outflanking_info(add_border(board), token, get_bordered_index(index))

    for outflanking_index, outflanking_direction in outflanking_info:
        step = 1
        location = index

        while location != outflanking_index:
            board = board[:location] + token + board[location + 1:]
            location = index + step * outflanking_direction
            step += 1

    return board
