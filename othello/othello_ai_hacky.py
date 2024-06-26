import sys
from math import inf

START_STATE = "........" \
              "........" \
              "........" \
              "...ox..." \
              "...xo..." \
              "........" \
              "........" \
              "........"

CORNER_CELLS = {
    0: {1, 8, 9},
    7: {6, 15, 14},
    56: {57, 48, 49},
    63: {62, 55, 54}
}

CORNER_EDGES = {
    0: {1, 2, 3, 8, 16, 24},
    7: {4, 5, 6, 15, 23, 31},
    56: {48, 40, 32, 57, 58, 59},
    63: {55, 47, 39, 62, 61, 60}
}

CENTER_CELLS = {27, 28, 35, 36}

CENTER_16 = (18, 19, 20, 21,
             26, 27, 28, 29,
             34, 35, 36, 37,
             42, 43, 44, 45)

EDGES = (2, 3, 4, 5,
         16, 24, 32, 40, 56,
         23, 31, 39, 47, 63,
         58, 59, 60, 61)


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


def is_game_over(board):
    x_moves = possible_moves(board, "x")
    o_moves = possible_moves(board, "o")

    return len(x_moves) == len(o_moves) == 0


def evaluate(board):
    # Mobility
    x_moves = possible_moves(board, "x")
    o_moves = possible_moves(board, "o")
    x_count, o_count = board.count("x"), board.count("o")
    total_count = x_count + o_count

    if len(x_moves) + len(o_moves) == 0:
        return 1000000 * (x_count - o_count)

    mobility_weight = (64 - total_count) / 10
    mobility_score = len(x_moves) - len(o_moves)

    # Corners and Adjacents
    x_corners = o_corners = 0
    x_bad_x_square = o_bad_x_square = 0
    x_good_x_square = o_good_x_square = 0

    for corner, adjacents in CORNER_CELLS.items():
        if board[corner] == "x":
            x_corners += 1
        elif board[corner] == "o":
            o_corners += 1

        for adj in adjacents:
            if board[adj] == "x":
                if board[corner] != "x":
                    x_bad_x_square += 1
                else:
                    x_good_x_square += 1
            elif board[adj] == "o":
                if board[corner] != "o":
                    o_bad_x_square += 1
                else:
                    o_good_x_square += 1

    corner_weight = 100
    corner_score = x_corners - o_corners

    bad_adj_weight = -100
    bad_adj_score = x_bad_x_square - o_bad_x_square

    good_adj_weight = 100
    good_adj_score = x_good_x_square - o_good_x_square

    # Edges
    x_edges, o_edges = 0, 0

    for corner, edges in CORNER_EDGES.items():
        for edge in edges:
            if board[edge] == "x":
                if board[corner] == "x":
                    x_edges += 5
                else:
                    x_edges += 1
            elif board[edge] == "o":
                if board[corner] == "o":
                    o_edges += 5
                else:
                    o_edges += 1

    edge_weight = total_count / 10
    edge_score = x_edges - o_edges

    # Center
    x_center, o_center = 0, 0

    for cell in CENTER_16:
        if board[cell] == "x":
            x_center += 1
        elif board[cell] == "o":
            o_center += 1

    center_weight = 0
    center_score = x_center - o_center

    score = mobility_weight * mobility_score + \
            corner_weight * corner_score + \
            good_adj_weight * good_adj_score + \
            bad_adj_weight * bad_adj_score + \
            edge_weight * edge_score + \
            center_weight * center_score

    return score


def negamax(board, player, depth, alpha, beta):
    if depth <= 0 or is_game_over(board):
        return player * evaluate(board)

    max_score = -inf
    legal_moves = possible_moves(board, "x" if player == 1 else "o")

    if len(legal_moves) == 0:
        return -negamax(board, -player, depth - 1, -beta, -alpha)

    for move in legal_moves:
        child = make_move(board, "x" if player == 1 else "o", move)
        max_score = max(max_score, -negamax(child, -player, depth - 1, -beta, -alpha))
        alpha = max(alpha, max_score)

        if alpha >= beta:
            break

    return max_score


def find_next_move(board, player, depth):
    token = 1 if player == "x" else -1
    max_score = -inf
    max_move = -1

    for move in possible_moves(board, player):
        child = make_move(board, player, move)
        score = -negamax(child, -token, depth, -inf, inf)

        if score > max_score:
            max_score = score
            max_move = move

    return max_move


# class Strategy():
#    logging = True  # Optional
#
#    def best_strategy(self, board, player, best_move, still_running):
#        depth = 1
#
#        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
#
#            best_move.value = find_next_move(board, player, depth)
#
#            depth += 1


board = sys.argv[1]
player = sys.argv[2]
depth = 2

# for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all

print(find_next_move(board, player, depth))
    # depth += 1