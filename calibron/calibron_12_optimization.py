import collections
import sys
import time
from heapq import heappush, heappop


def get_area(rectangle):
    return rectangle[0] * rectangle[1]


def get_total_area(rectangle_list):
    total_piece_area = 0

    for rectangle in rectangle_list:
        total_piece_area += get_area(rectangle)

    return total_piece_area


def invert_rectangle(rectangle):
    return rectangle[1], rectangle[0]


def get_rectangle(pseudo_rectangle):
    y2, x1, x2, y1 = pseudo_rectangle

    return y2 - y1, x2 - x1


def state_to_rectangles(state):
    return [get_rectangle(pseudo_rectangle) for pseudo_rectangle in state]


def add_rectangle(state, rectangle):
    highest_rectangle = heappop(state)

    if highest_rectangle[0] + rectangle[0] > containing_rectangle[0]:
        return None

    next_rectangle = state[0] if len(state) > 0 else None

    while next_rectangle is not None and (next_rectangle[0], next_rectangle[1]) == (
    highest_rectangle[0], highest_rectangle[2]):
        heappop(state)
        # (y2, x1, x2, y1)
        highest_rectangle = (highest_rectangle[0], highest_rectangle[1], next_rectangle[2], highest_rectangle[0] - rectangle[0])

        next_rectangle = state[0] if len(state) > 0 else None

    if highest_rectangle[1] + rectangle[1] > highest_rectangle[2]:
        return None

    lowest_rectangle = highest_rectangle[0] + rectangle[0], highest_rectangle[1], highest_rectangle[1] + rectangle[1], highest_rectangle[0]
    heappush(state, lowest_rectangle)

    if highest_rectangle[2] - lowest_rectangle[2] > 0:
        leftover_rectangle = highest_rectangle[0], lowest_rectangle[2], highest_rectangle[2], highest_rectangle[0]

        heappush(state, leftover_rectangle)

    return state


def goal_test():
    for var, rectangle in enumerate(rectangles):
        if rectangle_count[var] > 0:
            return False

    return True


def get_next_unassigned_var():
    for var, rectangle in enumerate(rectangles):
        if rectangle_count[var] > 0 and sorted_value_length[var] > 0:
            return var

    return -1


def get_sorted_values(state, var):
    sorted_values = []
    rectangle = rectangles[var]

    if add_rectangle(state.copy(), invert_rectangle(rectangle)) is not None:
        sorted_values.append(True)

    if add_rectangle(state.copy(), rectangle) is not None:
        sorted_values.append(False)

    sorted_value_length[var] = len(sorted_values)

    return sorted_values


def csp_backtracking(state, sol):
    # print(state)
    if goal_test():
        return sol

    for var, rectangle in enumerate(rectangles):
        if rectangle_count[var] == 0:
            continue

        sorted_values = get_sorted_values(state, var)

        for val in sorted_values:
            new_rectangle = invert_rectangle(rectangle) if val else rectangle
            new_state = state.copy()
            add_rectangle(new_state, new_rectangle)
            x1, y2 = state[0][1], state[0][0]

            sol.append((y2, x1, new_rectangle[0], new_rectangle[1]))

            rectangle_count[var] -= 1
            result = csp_backtracking(new_state, sol)
            rectangle_count[var] += 1

            if result is not None:
                return result

            sol.pop()

    return None


def print_solution(sol):
    for rectangle in sol:
        curr_rect = ""

        for val in rectangle:
            curr_rect += str(val) + " "

        curr_rect = curr_rect[:-1]

        print(curr_rect)


bad_pseudo_puzzles = ["10 13 3x6 2x5 4x10 7x9 1x1",
                      "8 5 4x2 4x2 4x2 4x2 2x4"]

pseudo_puzzles = ["4 7 7x4",
                  "2 3 1x2 2x2",
                  "18 9 3x11 5x7 4x8 6x10 1x2",
                  "4 8 4x1 1x6 1x3 3x1 1x3 1x3 6x1 1x4",
                  "11 12 3x6 2x5 4x10 7x9 1x1",
                  "9 18 3x8 5x10 4x11 6x7 1x2",
                  "13 14 4x5 3x8 6x11 7x10 2x1",
                  "19 19 1x19 1x12 6x9 9x15 15x3 10x6 3x12"]

# pseudo_puzzle = "24 24 4x7 7x4 7x5 11x4 9x3 2x8 22x3 8x4 14x11 8x10 2x12 5x3 9x3"
# pseudo_puzzle = "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
pseudo_puzzle = sys.argv[1]

# print(pseudo_puzzles[i])
# pseudo_puzzle = pseudo_puzzles[2]
# pseudo_puzzle = sys.argv[1]
puzzle = pseudo_puzzle.split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])

rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
inverted_rectangles = [invert_rectangle(rectangle) for rectangle in rectangles]
containing_rectangle = (puzzle_height, puzzle_width)

rectangle_count = [1 for _ in rectangles]
sorted_value_length = [2 for _ in rectangles]

puzzle_area = get_area(containing_rectangle)
total_piece_area = get_total_area(rectangles)

if puzzle_area != total_piece_area:
    print("Containing rectangle incorrectly sized.")
else:
    start_time = time.perf_counter()
    initial_state = [(0, 0, puzzle_width, 0)]
    solution = csp_backtracking(initial_state, [])
    end_time = time.perf_counter()

    if solution is None:
        print("No solution.")
    else:
        print_solution(solution)
