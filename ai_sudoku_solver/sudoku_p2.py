import math
import string
import time
from collections import defaultdict


def get_size(puzzle):
    return int(len(puzzle) ** 0.5)


def get_subblock_width(puzzle_size):
    for i in range(math.ceil(puzzle_size ** 0.5), puzzle_size):
        if puzzle_size % i == 0:
            return i

    return -1


def get_subblock_height(puzzle_size):
    for i in range(int(puzzle_size ** 0.5), 0, -1):
        if puzzle_size % i == 0:
            return i

    return -1


def get_symbol_set(puzzle_size):
    symbols = "123456789" + string.ascii_uppercase

    return set(symbols[:puzzle_size])


def get_puzzle_information(puzzle):
    size = get_size(puzzle)

    return size, get_subblock_width(size), get_subblock_height(size), get_symbol_set(size)


def print_puzzle(puzzle, puzzle_size):
    for i in range(0, len(puzzle), puzzle_size):
        print(puzzle[i:i + puzzle_size])


def print_possibilities(puzzle, puzzle_size):
    for i in range(0, len(puzzle), puzzle_size):
        current_row = "|"
        for square in puzzle[i:i + puzzle_size]:
            current_square = square

            for i in range(len(current_square), puzzle_size):
                current_square += " "

            current_row += current_square + " | "

        print(current_row)


def get_constraint_sets(puzzle, puzzle_size, subblock_width, subblock_height):
    row_constraint_sets = [set() for _ in range(puzzle_size)]
    col_constraint_sets = [set() for _ in range(puzzle_size)]
    block_constraint_sets = [set() for _ in range(puzzle_size)]

    block_set_index = 0
    block_counter = 0
    total_counted = 0

    for index, cell in enumerate(puzzle):
        set_index = index // puzzle_size

        row_constraint_sets[set_index].add(index)
        col_constraint_sets[set_index].add(puzzle_size * (index % puzzle_size) + set_index)
        block_constraint_sets[block_set_index].add(index)

        if block_counter < subblock_width - 1:
            block_counter += 1
        else:
            block_set_index += 1
            block_counter = 0

        if (index + 1) % puzzle_size == 0 and total_counted != puzzle_size * subblock_height - 1:
            block_set_index -= subblock_height

        if total_counted == puzzle_size * subblock_height - 1:
            total_counted = 0
        else:
            total_counted += 1

    return row_constraint_sets, col_constraint_sets, block_constraint_sets


def get_possibilities(puzzle, symbol_set):
    puzzle_with_possibilities = []
    symbols = "".join(sorted(symbol_set))

    for cell in puzzle:
        if cell == ".":
            puzzle_with_possibilities.append(symbols)
        else:
            puzzle_with_possibilities.append(cell)

    return puzzle_with_possibilities


def get_neighbors_dictionary(puzzle, constraint_sets):
    neighbors = defaultdict(set)

    for index, cell in enumerate(puzzle):
        for constraint_set in constraint_sets:
            for constrained_indices in constraint_set:
                if index in constrained_indices:
                    neighbors[index] |= constrained_indices

    return neighbors


def get_most_constrained_var(state, puzzle_size):
    most_constrained_var = -1
    most_constrained_cell_size = puzzle_size

    for index, cell in enumerate(state):
        if len(cell) == 2:
            return index
        elif most_constrained_cell_size >= len(cell) > 1:
            most_constrained_var = index
            most_constrained_cell_size = len(cell)

    return most_constrained_var


def get_sorted_values(state, var, neighbors, symbol_set):
    sorted_values = symbol_set.copy()

    for square_index in neighbors[var]:
        if state[square_index] in sorted_values:
            sorted_values.remove(state[square_index])

    return sorted_values


def forward_looking(state, solved_indices, neighbors):
    # solved_indices = [index for index, cell in enumerate(state) if len(cell) == 1]

    for solved_index in solved_indices:
        for index in neighbors[solved_index]:
            prev_possibilities = state[index]

            if index != solved_index:
                state[index] = prev_possibilities.replace(str(state[solved_index]), "")

            if state[index] == "":
                return None
            elif len(state[index]) == 1 and state[index] != prev_possibilities:
                solved_indices.append(index)

    return state


def to_row_col(n, size):
    return n // size, n % size


def csp_backtracking_with_forward_looking(state, neighbors, symbol_set, size):
    var = get_most_constrained_var(state, size)

    if var == -1:
        return state

    for val in state[var]:
        new_state = state.copy()
        new_state[var] = val
        checked_state = forward_looking(new_state, [var], neighbors)

        if checked_state is not None:
            result = csp_backtracking_with_forward_looking(checked_state, neighbors, symbol_set, size)

            if result is not None:
                return result

    return None


def get_solution(puzzle):
    size, subblock_width, subblock_height, symbol_set = get_puzzle_information(puzzle)
    constraint_sets = get_constraint_sets(puzzle, get_size(puzzle), subblock_width, subblock_height)
    neighbors = get_neighbors_dictionary(puzzle, constraint_sets)

    puzzle = get_possibilities(puzzle, symbol_set)
    solved_indices = [index for index, cell in enumerate(puzzle) if len(cell) == 1]
    puzzle = forward_looking(puzzle, solved_indices, neighbors)

    return "".join(csp_backtracking_with_forward_looking(puzzle, neighbors, symbol_set, size))


# puzzle = "..3.2.6.." \
#          "9..3.5..1" \
#          "..18.64.." \
#          "..81.29.." \
#          "7.......8" \
#          "..67.82.." \
#          "..26.95.." \
#          "8..2.3..9" \
#          "..5.1.3.."

puzzle = "3.......7" \
         "....6..2." \
         ".5..3...." \
         "2..7....." \
         "...4..5.." \
         "......21." \
         "6.....3.8" \
         ".....1..." \
         "...5....."

answer = "386124957179865423452937681241756839938412576567398214615279348823641795794583162"


size, subblock_width, subblock_height, symbol_set = get_puzzle_information(puzzle)
puzzle = get_possibilities(puzzle, symbol_set)
constraint_sets = get_constraint_sets(puzzle, size, subblock_width, subblock_height)
neighbors = get_neighbors_dictionary(puzzle, constraint_sets)

start_time = time.perf_counter()

with open("Sudoku Files/puzzles_3_standard_medium.txt") as f:
    puzzles = [line.strip() for line in f]


for i, puzzle in enumerate(puzzles):
    print("Puzzle #%s:" % i, puzzle)
    print("Solution:", get_solution(puzzle))


end_time = time.perf_counter()

print("\nElapsed time:", (end_time - start_time), "sec")

# print_possibilities(puzzle, size)
# print()
# solved_indices = [index for index, cell in enumerate(puzzle) if len(cell) == 1]
# puzzle = forward_looking(puzzle, solved_indices, neighbors)
# print_possibilities(puzzle, size)
# print()
# solution = csp_backtracking_with_forward_looking(puzzle, neighbors, symbol_set, size)
# print_possibilities(solution, size)
# print()
# print_possibilities(answer, size)
