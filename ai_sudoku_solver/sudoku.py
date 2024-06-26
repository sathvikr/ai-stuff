import math
import string
import sys
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


def get_neighbors_dictionary(puzzle, constraint_sets):
    neighbors = defaultdict(set)

    for index, cell in enumerate(puzzle):
        for constraint_set in constraint_sets:
            for constrained_indices in constraint_set:
                if index in constrained_indices:
                    neighbors[index] |= constrained_indices

    return neighbors


def get_next_unassigned_var(state):
    try:
        return state.index(".")
    except ValueError:
        return -1


def get_sorted_values(state, var, neighbors, symbol_set):
    sorted_values = symbol_set.copy()

    for square_index in neighbors[var]:
        if state[square_index] in sorted_values:
            sorted_values.remove(state[square_index])

    return sorted_values


def csp_backtracking(state, neighbors, symbol_set):
    var = get_next_unassigned_var(state)

    if var == -1:
        return state

    sorted_values = get_sorted_values(state, var, neighbors, symbol_set)

    for val in sorted_values:
        new_state = state[:var] + val + state[var + 1:]
        result = csp_backtracking(new_state, neighbors, symbol_set)

        if result is not None:
            return result

    return None


def get_solution(puzzle):
    size, subblock_width, subblock_height, symbol_set = get_puzzle_information(puzzle)
    constraint_sets = get_constraint_sets(puzzle, get_size(puzzle), subblock_width, subblock_height)
    neighbors = get_neighbors_dictionary(puzzle, constraint_sets)
    solution = csp_backtracking(puzzle, neighbors, symbol_set)
    print_puzzle(solution, get_size(solution))

    print(is_solved(solution, constraint_sets))

    return solution


def get_duplicate_count(puzzle, constraint_set, i):
    count = 0

    for index in constraint_set:
        if puzzle[index] == puzzle[i]:
            count += 1

    return count


def is_solved(puzzle, constraint_sets):
    duplicate_vals = []

    for constraint_set in constraint_sets:
        for index in constraint_set:
            duplicate_count = get_duplicate_count(puzzle, constraint_set, index)

            if duplicate_count > 1:
                duplicate_vals.append(index)

    if len(duplicate_vals) > 0:
        print(duplicate_vals)

        return False

    return True


# start_time = time.perf_counter()
#
# with open("Sudoku Files/puzzles_2_variety_easy.txt") as f:
#     puzzles = [line.strip() for line in f]
#
#
# for i, puzzle in enumerate(puzzles):
#     print("Puzzle #%s:" % i, puzzle)
#     print("Solution:", get_solution(puzzle))
#
#
# end_time = time.perf_counter()
#
# print("\nElapsed time:", (end_time - start_time), "sec")

puzzle = ".....1.5.1.3......4.........5.62........8...37.....1...8.....2....3..5.....9....."
solution = get_solution(puzzle)


# with open(sys.argv[1]) as f:
#     puzzles = [line.strip() for line in f]

# for puzzle in puzzles:
# puzzle = ".....3" \
#         ".6.45." \
#         "....15" \
#         "12...." \
#         ".12.3." \
#         "6....."

# print_puzzle(get_solution(puzzle), get_size(puzzle))

# with open("Sudoku Files/") as f:
#     puzzles = [line.strip() for line in f]
#
#
# start_time = time.perf_counter()
#
# for i, puzzle in enumerate(puzzles):
#     print(i, puzzle)
#     print(i, get_solution(puzzle))
#
# end_time = time.perf_counter()
#
# print(end_time - start_time)