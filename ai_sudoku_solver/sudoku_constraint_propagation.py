import math
import string
import sys
import time
from collections import defaultdict


def get_size(pseudo_puzzle):
    return int(len(pseudo_puzzle) ** 0.5)


def get_subblock_width(pseudo_puzzle_size):
    for i in range(math.ceil(pseudo_puzzle_size ** 0.5), pseudo_puzzle_size):
        if pseudo_puzzle_size % i == 0:
            return i

    return -1


def get_subblock_height(pseudo_puzzle_size):
    for i in range(int(pseudo_puzzle_size ** 0.5), 0, -1):
        if pseudo_puzzle_size % i == 0:
            return i

    return -1


def get_symbol_set(pseudo_puzzle_size):
    symbols = "123456789" + string.ascii_uppercase

    return set(symbols[:pseudo_puzzle_size])


def get_puzzle_information(pseudo_puzzle):
    size = get_size(pseudo_puzzle)

    return size, get_subblock_width(size), get_subblock_height(size), get_symbol_set(size)


def print_pseudo_puzzle(pseudo_puzzle, puzzle_size):
    for i in range(0, len(pseudo_puzzle), puzzle_size):
        print(pseudo_puzzle[i:i + puzzle_size])


def print_puzzle(puzzle, puzzle_size):
    for i in range(0, len(puzzle), puzzle_size):
        current_row = "|"
        for square in puzzle[i:i + puzzle_size]:
            current_square = square

            for i in range(len(current_square), puzzle_size):
                current_square += " "

            current_row += current_square + "|"

        print(current_row)


def get_puzzle(pseudo_puzzle, symbol_set):
    puzzle = []
    symbols = "".join(sorted(symbol_set))

    for cell in pseudo_puzzle:
        if cell == ".":
            puzzle.append(symbols)
        else:
            puzzle.append(cell)

    return puzzle


def get_constraint_sets(pseudo_puzzle, puzzle_size, subblock_width, subblock_height):
    row_constraint_sets = [set() for _ in range(puzzle_size)]
    col_constraint_sets = [set() for _ in range(puzzle_size)]
    block_constraint_sets = [set() for _ in range(puzzle_size)]

    block_set_index = 0
    block_counter = 0
    total_counted = 0

    for index, cell in enumerate(pseudo_puzzle):
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


def get_neighbors_dictionary(pseudo_puzzle, constraint_sets):
    neighbors = defaultdict(set)

    for index, cell in enumerate(pseudo_puzzle):
        for constraint_set in constraint_sets:
            for constrained_indices in constraint_set:
                if index in constrained_indices:
                    neighbors[index] |= constrained_indices

    return neighbors


def forward_looking(state, solved):
    # solved = [index for index, cell in enumerate(state) if len(cell) == 1]
    visited = set(solved)

    while len(solved) > 0:
        solved_index = solved[-1]

        # print("Solved:", solved)
        # print("Visited:", visited)
        # print("Now processing index", solved_index, "value =", state[solved_index])

        for index in neighbors_dictionary[solved_index]:
            if index in solved or index not in visited:
                state[index] = state[index].replace(state[solved_index], "")

                if index not in visited:
                    if len(state[index]) == 1:
                        solved.append(index)
                        visited.add(index)

            if len(state[index]) == 0:
                return None

        # print_puzzle(state, size)
        # print()

        solved.remove(solved_index)

    return state


def count_occurrences(state, constraint_set, value):
    count = 0

    if value not in constraint_set:
        return count

    for index in constraint_set:
        if state[index] == value:
            count += 1

    return count


def constraint_propagation(state, constraint_sets):
    for constraint_set in constraint_sets:
        for index in constraint_set:
            value = state[index]
            num_occurrences = count_occurrences(state, constraint_set, value)

            if num_occurrences == 0:
                return None
            elif num_occurrences == 1:
                state[index] = value

    return state


def get_most_constrained_var(state, puzzle_size):
    most_constrained_var = -1
    most_constrained_cell_size = puzzle_size

    for index, cell in enumerate(state):
        if len(cell) == 2:
            return index
        elif most_constrained_cell_size > len(cell) > 1:
            most_constrained_var = index
            most_constrained_cell_size = len(cell)

    return most_constrained_var


def get_sorted_values(state, index):
    return state[index]


def csp_backtracking_with_forward_looking(state, solved, pseudo_puzzle_size):
    var = get_most_constrained_var(state, pseudo_puzzle_size)

    if var == -1:
        return state

    for val in get_sorted_values(state, var):
        new_state = state.copy()
        new_state[var] = val
        checked_state = forward_looking(new_state, [var])

        if checked_state is not None:
            result = csp_backtracking_with_forward_looking(checked_state, solved, pseudo_puzzle_size)

            if result is not None:
                return result

    return None


with open(sys.argv[1]) as f:
    pseudo_puzzles = [line.strip() for line in f]

start_time = time.perf_counter()
#
for i, pseudo_puzzle in enumerate(pseudo_puzzles):
    # i = 47
    # pseudo_puzzle = pseudo_puzzles[i]

    # print("Puzzle #%s:" % i, pseudo_puzzle)

    size, subblock_width, subblock_height, symbol_set = get_puzzle_information(pseudo_puzzle)

    # print_pseudo_puzzle(pseudo_puzzle, size)

    constraint_sets = get_constraint_sets(pseudo_puzzle, size, subblock_width, subblock_height)
    neighbors_dictionary = get_neighbors_dictionary(pseudo_puzzle, constraint_sets)

    for key in neighbors_dictionary:
        if key in neighbors_dictionary[key]:
            neighbors_dictionary[key].remove(key)

    puzzle = get_puzzle(pseudo_puzzle, symbol_set)
    solved = [index for index, cell in enumerate(puzzle) if len(cell) == 1]
    checked_puzzle = forward_looking(puzzle, solved)
    solution = csp_backtracking_with_forward_looking(checked_puzzle, solved, size)

    print("".join(solution))

# print("Puzzle:")
# print_pseudo_puzzle(pseudo_puzzle, size)
# print("Solution:")
# print_puzzle(solution, size)

end_time = time.perf_counter()
# print("Elapsed time:", end_time - start_time, "sec")
#