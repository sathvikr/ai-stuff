import copy
import sys
import time
from heapq import heappush, heappop
from pprint import pprint


def get_area(rectangle):
    return rectangle[0] * rectangle[1]


def get_total_area(rectangle_list):
    total_piece_area = 0

    for rectangle in rectangle_list:
        total_piece_area += get_area(rectangle)

    return total_piece_area


def peek(heap):
    return heap[0] if len(heap) > 0 else None


def invert_rectangle(rectangle):
    return rectangle[1], rectangle[0]


def get_rectangle(pseudo_rectangle):
    y2, x1, x2, y1 = pseudo_rectangle

    return y2 - y1, x2 - x1


def state_to_rectangles(state):
    return [get_rectangle(pseudo_rectangle) for pseudo_rectangle in state]


def add_rectangle(state, rectangle):
    # (y2, x1, x2, y1)
    height, width = rectangle
    top = heappop(state)

    # (y2, x1, x2, y1)

    if top[0] + height > containing_rectangle[0]:
        return None

    next_edge = peek(state)

    while next_edge is not None and (next_edge[0], next_edge[1]) == (top[0], top[2]):
        heappop(state)
        top = (top[0], top[1], next_edge[2], 0)

        next_edge = peek(state)

    if top[1] + width > top[2]:
        return None

    bottom = top[0] + height, top[1], top[1] + width, 0
    heappush(state, bottom)

    if top[2] - bottom[2] > 0:
        heappush(state, (top[0], bottom[2], top[2], 0))

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

    if add_rectangle(copy.deepcopy(state), invert_rectangle(rectangle)) is not None:
        sorted_values.append(True)

    if add_rectangle(copy.deepcopy(state), rectangle) is not None:
        sorted_values.append(False)

    sorted_value_length[var] = len(sorted_values)

    return sorted_values


def csp_backtracking(state, sol):
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

            sol.append(new_rectangle)

            rectangle_count[var] -= 1
            result = csp_backtracking(new_state, sol)
            rectangle_count[var] += 1

            if result is not None:
                return result

            sol.pop()

    return None


def print_solution(sol):
    solution_string = str(puzzle_height) + " " + str(puzzle_width)

    for rectangle in sol:
        solution_string += " " + str(rectangle[0]) + "x" + str(rectangle[1])

    print(solution_string)


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
pseudo_puzzle = pseudo_puzzles[7]
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
