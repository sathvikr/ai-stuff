from heapq import heappush, heappop


def get_area(rectangle):
    return rectangle[0] * rectangle[1]


def get_total_piece_area(rectangles):
    total_piece_area = 0

    for rectangle in rectangles:
        total_piece_area += get_area(rectangle)

    return total_piece_area


def invert_rectangle(rectangle):
    return rectangle[1], rectangle[0]


def get_edge_width(edge):
    return edge[2] - edge[1]


def peek(heap):
    return heap[0] if len(heap) > 0 else None


def add_rectangle(state, rectangle):
    height, width = rectangle
    top = heappop(state)

    # (y, x1, x2)

    if top[0] + height > containing_rectangle[0]:
        return None

    next_edge = peek(state)

    while next_edge is not None and (next_edge[0], next_edge[1]) == (top[0], top[2]):
        heappop(state)
        top = (top[0], top[1], next_edge[2])

        next_edge = peek(state)

    if top[1] + width > top[2]:
        return None

    bottom = top[0] + height, top[1], top[1] + width
    heappush(state, bottom)

    if top[2] - bottom[2] > 0:
        heappush(state, (top[0], bottom[2], top[2]))

    return state


def csp_backtracking(index, state):
    count = rectangle_count
    if len(rectangles) == index:
        return state

    for i, rectangle in enumerate(rectangles):
        if rectangle_count[i] == 0:
            continue

        for is_inverted in (True, False):
            new_state = state.copy()
            val = inverted[i] if is_inverted else rectangle
            new_state = add_rectangle(new_state, val)

            if new_state is not None:
                rectangle_count[i] -= 1

                solution.append(val)
                result = csp_backtracking(index + 1, new_state)

                if result is not None:
                    return result

                solution.pop()

                rectangle_count[i] += 1

    return None


pseudo_puzzles = ["4 7 7x4",
                  "2 3 1x2 2x2",
                  "18 9 3x11 5x7 4x8 6x10 1x2",
                  "4 8 4x1 1x6 1x3 3x1 1x3 1x3 6x1 1x4",
                  "11 12 3x6 2x5 4x10 7x9 1x1",
                  "9 18 3x8 5x10 4x11 6x7 1x2",
                  "13 14 4x5 3x8 6x11 7x10 2x1",
                  "19 19 1x19 1x12 6x9 9x15 15x3 10x6 3x12"]

pseudo_puzzle = pseudo_puzzles[0]

puzzle = pseudo_puzzle.split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
inverted = [invert_rectangle(rectangle) for rectangle in rectangles]
containing_rectangle = (puzzle_height, puzzle_width)
initial_state = [(0, 0, puzzle_width)]

puzzle_area = get_area(containing_rectangle)
total_piece_area = get_total_piece_area(rectangles)

rectangle_count = [1 for _ in rectangles]

if puzzle_area != total_piece_area:
    print("Containing rectangle incorrectly sized")
else:
    # print(initial_state)
    # print(rectangles)

    #
    # for rectangle in rectangles:
    # print(add_rectangle(initial_state, rectangle))
    solution = []
    csp_backtracking(0, initial_state)
    print(solution)
