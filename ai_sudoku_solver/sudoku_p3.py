import math
import string
import sys
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

    return row_constraint_sets + col_constraint_sets + block_constraint_sets


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
            if index in constraint_set:
                neighbors[index] |= constraint_set

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


def constraint_propagation(state, neighbors, constraint_sets, symbol_set):
    changes_made = False

    for constraint_set in constraint_sets:
        for val in symbol_set:
            val_indices = [index for index in constraint_set if val in state[index]]

            if len(val_indices) == 1:
                state[val_indices[0]] = val
                changes_made = True

    if changes_made:
        state = forward_looking(state, [index for index, cell in enumerate(state) if len(cell) == 1], neighbors)

    return state


def csp_backtracking(state, neighbors, symbol_set, constraint_sets, size):
    var = get_most_constrained_var(state, size)

    if var == -1:
        return state

    for val in state[var]:
        new_state = state.copy()
        new_state[var] = val
        checked_state = forward_looking(new_state, [var], neighbors)

        if checked_state is not None:
            propagated_state = constraint_propagation(checked_state, neighbors, constraint_sets, symbol_set)

            if propagated_state is not None:
                result = csp_backtracking(checked_state, neighbors, symbol_set, constraint_sets, size)

                if result is not None:
                    return result

    return None


def get_solution(state):
    size, subblock_width, subblock_height, symbol_set = get_puzzle_information(state)
    constraint_sets = get_constraint_sets(state, get_size(state), subblock_width, subblock_height)
    neighbors = get_neighbors_dictionary(state, constraint_sets)

    puzzle = get_possibilities(state, symbol_set)
    solved_indices = [index for index, cell in enumerate(puzzle) if len(cell) == 1]
    checked_state = forward_looking(puzzle, solved_indices, neighbors)

    solution = csp_backtracking(checked_state, neighbors, symbol_set, constraint_sets, size)

    return "".join(solution)


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


with open(sys.argv[1]) as f:
    puzzles = [line.strip() for line in f]

for i, puzzle in enumerate(puzzles):
    print(get_solution(puzzle))


# puzzle = ".....13....4...2..9...5........8..51.2.7..............5..4...6..1.2..7..........."
#
# print_possibilities(puzzle, get_size(puzzle))
# solution = get_solution(puzzle)
# print()
# print_possibilities(solution, get_size(puzzle))
