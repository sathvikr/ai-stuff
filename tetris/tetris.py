import sys

PIECES = {
    "I": ("####",
          "#\n#\n#\n#"),
    "O": ("##\n"
          "##",),
    "T": (" # \n"
          "###",
          "#\n"
          "##\n"
          "#",
          "###\n"
          " # ",
          " #\n"
          "##\n"
          " #"),
    "S": (" ##\n"
          "## ",
          "# \n"
          "##\n"
          " #"),
    "Z": ("##\n"
          " ##",
          " #\n"
          "##\n"
          "# "),
    "J": ("#\n"
          "###",
          "##\n"
          "#\n"
          "#",
          "###\n"
          "  #",
          " #\n"
          " #\n"
          "##"),
    "L": ("  #\n"
          "###",
          "#\n"
          "#\n"
          "##",
          "###\n"
          "#",
          "##\n"
          " #\n"
          " #")
}

PIECE_OFFSETS = {
    "I": ((0, 0, 0, 0), (0,)),
    "O": ((0, 0),),
    "T": ((0, 0, 0), (0, -1), (-1, 0, -1), (-1, 0)),
    "S": ((0, 0, -1), (-1, 0)),
    "Z": ((-1, 0, 0), (0, -1)),
    "J": ((0, 0, 0), (0, -2), (-1, -1, 0), (0, 0)),
    "L": ((0, 0, 0), (0, 0), (0, -1, -1), (-2, 0))
}

PIECE_BOTTOM_COLS = {
    "I": (0, 0),
    "O": (0,),
    "T": (0, 0, 1, 1),
    "S": (0, 1),
    "Z": (1, 0),
    "J": (0, 0, 2, 0),
    "L": (0, 0, 0, 1)
}

PIECE_HEIGHTS = {
    "I": (1, 4),
    "O": (2,),
    "T": (2, 3, 2, 3),
    "S": (2, 3),
    "Z": (2, 3),
    "J": (2, 3, 2, 3),
    "L": (2, 3, 2, 3)
}

PIECE_SIZE = 4
col_heights = [0] * 10


def initialize_col_heights(board):
    for count in range(20):
        row = board[count * 10: (count + 1) * 10]

        for i, cell in enumerate(row):
            if cell == "#" and col_heights[i] == 0:
                col_heights[i] = 20 - count


def print_board(board):
    print("=======================")

    for count in range(20):
        row = board[count * 10: (count + 1) * 10]
        print(' '.join(list(("|" + row + "|"))), " ", 20 - count)
        print("=======================")
        print()

    print("  0 1 2 3 4 5 6 7 8 9  ")
    print()


def get_collision_cell(piece, orientation, columns):
    l = []

    for i, column in enumerate(columns):
        l.append(col_heights[column] + 1 + PIECE_OFFSETS[piece][orientation][i])

    return max(l)


def drop_piece(piece, orientation, board, column, bottom_most_row):
    if PIECE_HEIGHTS[piece][orientation] + bottom_most_row - 1 > 20:
        return "GAME OVER"

    flattened_index = (20 - bottom_most_row) * 10 + column
    num_blocks_before = board.count("#")
    # to detect if a piece has properly been placed, check number of "#" before and
    # after and see if the number increased exactly by the number of "#" in the piece (which is always 4)

    if piece == "I":
        if orientation == 0:
            board = board[:flattened_index] + "####" + board[flattened_index + 4:]
        elif orientation == 1:
            board = board[:flattened_index + -30] + "#" + board[flattened_index + -29:]
            board = board[:flattened_index + -20] + "#" + board[flattened_index + -19:]
            board = board[:flattened_index + -10] + "#" + board[flattened_index + -9:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]
    elif piece == "O":
        board = board[:flattened_index + -10] + "##" + board[flattened_index + -8:]
        board = board[:flattened_index] + "##" + board[flattened_index + 2:]
    elif piece == "T":
        if orientation == 0:
            board = board[:flattened_index + -10] + " # " + board[flattened_index + -7:]
            board = board[:flattened_index] + "###" + board[flattened_index + 3:]
        elif orientation == 1:
            board = board[:flattened_index + -20] + "#" + board[flattened_index + -19:]
            board = board[:flattened_index + -10] + "##" + board[flattened_index + -8:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]
        elif orientation == 2:
            board = board[:flattened_index + -11] + "###" + board[flattened_index + -8:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]
        elif orientation == 3:
            board = board[:flattened_index + -20] + "#" + board[flattened_index + -19:]
            board = board[:flattened_index + -11] + "##" + board[flattened_index + -9:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]
    elif piece == "S":
        if orientation == 0:
            board = board[:flattened_index + -9] + "##" + board[flattened_index + -7:]
            board = board[:flattened_index] + "##" + board[flattened_index + 2:]
        elif orientation == 1:
            board = board[:flattened_index + -21] + "#" + board[flattened_index + -20:]
            board = board[:flattened_index + -11] + "##" + board[flattened_index + -9:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]
    elif piece == "Z":
        if orientation == 0:
            board = board[:flattened_index + -11] + "##" + board[flattened_index + -9:]
            board = board[:flattened_index] + "##" + board[flattened_index + 2:]
        elif orientation == 1:
            board = board[:flattened_index + -19] + "#" + board[flattened_index + -18:]
            board = board[:flattened_index + -10] + "##" + board[flattened_index + -8:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]
    elif piece == "J":
        if orientation == 0:
            board = board[:flattened_index + -10] + "#" + board[flattened_index + -9:]
            board = board[:flattened_index] + "###" + board[flattened_index + 3:]
        elif orientation == 1:
            board = board[:flattened_index + -20] + "##" + board[flattened_index + -18:]
            board = board[:flattened_index + -10] + "#" + board[flattened_index + -9:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]
        elif orientation == 2:
            board = board[:flattened_index + -12] + "###" + board[flattened_index + -9:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]
        elif orientation == 3:
            board = board[:flattened_index + -19] + "#" + board[flattened_index + -18:]
            board = board[:flattened_index + -9] + "#" + board[flattened_index + -8:]
            board = board[:flattened_index] + "##" + board[flattened_index + 2:]
    elif piece == "L":
        if orientation == 0:
            board = board[:flattened_index + -8] + "#" + board[flattened_index + -7:]
            board = board[:flattened_index] + "###" + board[flattened_index + 3:]
        elif orientation == 1:
            board = board[:flattened_index + -20] + "#" + board[flattened_index + -19:]
            board = board[:flattened_index + -10] + "#" + board[flattened_index + -9:]
            board = board[:flattened_index] + "##" + board[flattened_index + 2:]
        elif orientation == 2:
            board = board[:flattened_index + -10] + "###" + board[flattened_index + -7:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]
        elif orientation == 3:
            board = board[:flattened_index + -21] + "##" + board[flattened_index + -19:]
            board = board[:flattened_index + -10] + "#" + board[flattened_index + -9:]
            board = board[:flattened_index] + "#" + board[flattened_index + 1:]

    num_blocks_after = board.count("#")

    return board if num_blocks_after - num_blocks_before == 4 else None


def delete_row(board, row_index):
    return " " * 10 + board[:(20 - row_index) * 10] + board[(20 - row_index + 1) * 10:]


def delete_completed_lines(piece_just_dropped, orientation, bottom_most_row, board):
    i = bottom_most_row

    while i < bottom_most_row + PIECE_HEIGHTS[piece_just_dropped][orientation]:
        row = board[(20 - i) * 10: (20 - i + 1) * 10]

        if " " not in row:
            board = delete_row(board, i)
            i -= 1

        i += 1

    return board


# test = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     " \
#        "## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
test = sys.argv[1]
cleaned_board = test
initialize_col_heights(test)

f = open("tetrisout.txt", "w")

for piece in PIECES:
    for orientation, oriented_piece in enumerate(PIECES[piece]):
        column_template = [i for i in range(len(PIECE_OFFSETS[piece][orientation]))]

        for i in range(0, 11 - len(column_template)):
            columns = [i + j for j in range(len(column_template))]
            column = columns[PIECE_BOTTOM_COLS[piece][orientation]]
            bottom_most_row = get_collision_cell(piece, orientation, columns)
            new_board = drop_piece(piece, orientation, test, column, bottom_most_row)

            if new_board == "GAME OVER":
                f.write("GAME OVER\n")
            elif new_board is not None:
                cleaned_board = delete_completed_lines(piece, orientation, bottom_most_row, new_board)
                f.write(cleaned_board + "\n")

f.close()