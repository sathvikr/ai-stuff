from collections import deque

GOAL_INDEX = 17


def get_size(puzzle):
    return int(len(puzzle) ** 0.5)


def print_puzzle(puzzle):
    size = get_size(puzzle)

    for i in range(0, len(puzzle), size):
        print(puzzle[i:i + size])


def get_cars(puzzle):
    return set(puzzle) - {"."}


def get_car_size(car, puzzle, vertical):
    car_size = 0
    car_index = puzzle.index(car)
    puzzle_size = get_size(puzzle)

    row, col = car_index // puzzle_size, car_index % puzzle_size

    if vertical:
        for i in range(col, len(puzzle) - (puzzle_size - col) + 1):
            if puzzle[i] == car:
                car_size += 1
    else:
        for i in range(row, (row + 1) * puzzle_size):
            if puzzle[i] == car:
                car_size += 1

    return car_size


def is_vertical(car, puzzle):
    car_index = puzzle.index(car)
    size = get_size(puzzle)

    return car_index > size - 1 and puzzle[car_index] == puzzle[car_index - size] or \
           car_index <= len(puzzle) - size - 1 and puzzle[car_index] == puzzle[car_index + size]


def goal_test(puzzle):
    return puzzle[GOAL_INDEX] == "R" and not is_vertical("R", puzzle)


def get_sliding_moves(car, car_size, puzzle, car_index, end, step):
    sliding_moves = set()

    initial_move_state = puzzle.replace(car, ".")

    for i in range(car_index, end, step):
        if puzzle[i] == ".":
            move_state = initial_move_state[0:i] + car + initial_move_state[i + 1:]

            for j in range(1, car_size):
                move_state = move_state[0:i - j * step] + car + move_state[i - j * step + 1:]
                move_state = move_state[0:i - j * step] + car + move_state[i - j * step + 1:]

            if move_state != puzzle:
                sliding_moves.add(move_state)
        elif puzzle[i] == car:
            continue
        else:
            break

    return sliding_moves


def get_legal_moves(car, puzzle):
    legal_moves = set()
    car_index = puzzle.index(car)
    vertical = is_vertical(car, puzzle)
    car_size = get_car_size(car, puzzle, vertical)
    size = get_size(puzzle)

    if vertical:
        col = car_index % size

        up_moves = get_sliding_moves(car, car_size, puzzle, car_index, col - 1, -size)
        legal_moves |= up_moves

        down_moves = get_sliding_moves(car, car_size, puzzle, car_index, (size - 1) * size + col + 1, size)
        legal_moves |= down_moves
    else:
        row = car_index // size

        left_moves = get_sliding_moves(car, car_size, puzzle, car_index, row * size - 1, -1)
        legal_moves |= left_moves

        right_moves = get_sliding_moves(car, car_size, puzzle, car_index, (row + 1) * size, 1)
        legal_moves |= right_moves

    return legal_moves


def get_children(puzzle):
    children = set()
    cars = get_cars(puzzle)

    for car in cars:
        children |= get_legal_moves(car, puzzle)

    return children


def bfs(puzzle):
    fringe = deque([[puzzle]])
    visited = {puzzle}

    while len(fringe) > 0:
        current_path = fringe.popleft()
        current_node = current_path[-1]

        if goal_test(current_node):
            return current_path

        children = get_children(current_node)

        for child in children:
            if child not in visited:
                fringe.append([*current_path, child])
                visited.add(child)


initial_state = "ABCCCD" \
                "AB..JD" \
                "ERR.JK" \
                "EFF.JK" \
                "..G..." \
                "HHGII."

solution_path = bfs(initial_state)

for state in solution_path:
    print_puzzle(state)
    print()

print("Found a solution that is", len(solution_path) - 1, "moves long.")