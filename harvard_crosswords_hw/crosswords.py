import sys

import math, re


def print_grid(grid, width) -> None:
    to_print = ""

    for i, cell in enumerate(grid):
        delim = "\n" if (i + 1) % width == 0 else " "
        to_print += cell + delim

    print(to_print)


def process_seed_string(seed_string) -> tuple:
    match = re.finditer("\d+x\d+", seed_string).__next__()
    coordinates = match.group().split("x")
    word_begin_index = match.end()

    orientation = seed_string[0]
    r, c = coordinates
    word = seed_string[word_begin_index:]

    return orientation, int(r), int(c), word


def build_pseudo_grid(height, width, seed_strings) -> str:
    grid = "-" * height * width

    for seed_string in seed_strings:
        orientation, r, c, word = process_seed_string(seed_string)
        word_start_index = r * width + c
        step = 1 if orientation == "H" else width

        for i, letter in enumerate(word):
            grid = grid[:word_start_index + i * step] + letter + grid[word_start_index + i * step + 1:]

    return grid


def get_block_index(string) -> int:
    try:
        index = string.index("#")
    except ValueError:
        index = -1

    return index


def get_row(state, width, row_index) -> str:
    return state[row_index * width:(row_index + 1) * width]


def get_col(state, width, col_index) -> str:
    col = ""

    for index, cell in enumerate(state):
        if index % width == col_index:
            col += cell

    return col


def is_odd(width, height) -> bool:
    return width % 2 == height % 2 == 1


# identify if wall exists row wise and column wise

def are_spaces_connected(state, width) -> bool:
    for i in range(width, len(state), width):
        prev_row = get_row(state, width, i - width)
        curr_row = get_row(state, width, i)

        prev_block_index = get_block_index(prev_row)
        curr_block_index = get_block_index(curr_row)

        if abs(prev_block_index - curr_block_index) > 1:
            return True

    for i in range(1, width, 1):
        prev_col = get_col(state, width, i - 1)
        curr_col = get_col(state, width, i)

        prev_block_index = get_block_index(prev_col)
        curr_block_index = get_block_index(curr_col)

        if abs(prev_block_index - curr_block_index) > 1:
            return True

    return False


def is_legal_state(state, height, width, block_limit) -> bool:
    if state.count("#") > block_limit:
        return False
    if is_odd(width, height) and block_limit % 2 == 0 and state[len(state) // 2] == "#":
        return False
    # if not are_spaces_connected(state, width):
    #     return False

    return True


# place a block
# place implied blocks
# if fails, backtrack
# fail: disconnected, too many blocks, if odd check center square


def get_next_row(state, height, width) -> int:
    next_row = -1
    next_row_block_count = math.inf

    for i in range(height):
        row = get_row(state, width, i)
        row_block_count = row.count("#")

        if row_block_count < next_row_block_count:
            next_row_block_count = row_block_count
            next_row = i

    return next_row


def get_possible_cells(state, width, row_index) -> list:
    row = get_row(state, width, row_index)

    return [index for index, cell in enumerate(row) if cell == "-"]


def get_implied_squares(state, index) -> list:
    implied_squares = []

    implied_squares.append(index)

    return implied_squares


# make move and also implied moves, if state[implied move index] != "-" return None
def place_blocking_squares(state, index) -> [None, str]:
    implied_squares = get_implied_squares(state, index)

    if len(implied_squares) == 0:
        return state

    for implied_index in implied_squares:
        opposite_index = -implied_index - 1

        if state[implied_index] != "-" or state[opposite_index] != "-":
            return None

        state = state[:implied_index] + "#" + state[implied_index + 1:]
        state = state[:opposite_index] + "#" + state[opposite_index + 1:]

    return state


def add_blocking_squares(state, height, width, block_limit) -> [None, str]:
    block_count = state.count("#")

    if block_count == block_limit:
        return state

    row_index = get_next_row(state, height, width)

    if row_index == math.inf:
        return state

    for cell_index in get_possible_cells(state, width, row_index):
        new_state = place_blocking_squares(state, row_index * width + cell_index)

        if new_state is not None and is_legal_state(new_state, height, width, block_limit):
            result = add_blocking_squares(new_state, height, width, block_limit)

            if result is not None:
                return result


def build_grid(height, width, block_count, seed_strings) -> str:
    pseudo_grid = build_pseudo_grid(height, width, seed_strings)

    if is_odd(width, height) and block_count % 2 == 1:
        pseudo_grid = pseudo_grid[:len(pseudo_grid) // 2] + "#" + pseudo_grid[len(pseudo_grid) // 2 + 1:]

    return add_blocking_squares(pseudo_grid, height, width, block_count)


args = ["7x13", 11]
dimensions = args[0].split("x")
width, height = int(dimensions[0]), int(dimensions[1])
block_count = int(args[1])
seed_strings = args[2].split(" ") if len(args) > 2 else []

grid = build_grid(height, width, block_count, seed_strings)

# grid = "#O#----------#r#----------#e#----------##-----------##-----------##-----------##-----------"
print_grid(grid, int(width))

# Sathvik Redrouthu, 1, 2024
