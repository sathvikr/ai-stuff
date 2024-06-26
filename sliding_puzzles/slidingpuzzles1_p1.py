import sys
import time
from collections import deque


def print_puzzle(s, board):
    for i in range(0, len(board), s):
        print(board[i: i + s])


def find_goal(board):
    if board is None:
        return False

    pseudo_sorted = "".join(sorted(board))

    return pseudo_sorted[1:] + pseudo_sorted[0]


def swap(string, i, j):
    l = list(string)
    l[i], l[j] = l[j], l[i]

    return "".join(l)


def get_children(board):
    s = int(len(board) ** 0.5)
    children = set()
    index = board.index(".")

    if (index + 1) % s != 0:
        children.add(swap(board, index, index + 1))
    if index % s != 0:
        children.add(swap(board, index, index - 1))
    if index < len(board) - s:
        children.add(swap(board, index, index + s))
    if index >= 0 + s:
        children.add(swap(board, index, index - s))

    return children


def is_parent(child, parent):
    return child in get_children(parent)


def goal_test(board):
    return board == find_goal(board)


def solvable_game_states(goal_state):
    fringe = deque()
    visited = {goal_state}

    fringe.append(goal_state)

    while len(fringe) > 0:
        children = get_children(fringe.popleft())

        for child in children:
            if child not in visited:
                fringe.append(child)
                visited.add(child)

    return visited


def bfs_solution(board):
    fringe = deque()
    visited = {board}

    fringe.append([board])

    while len(fringe) > 0:
        current_path = fringe.popleft()
        current_node = current_path[-1]

        if goal_test(current_node):
            return current_path

        children = get_children(current_node)

        for child in children:
            if child not in visited:
                path_copy = current_path.copy()
                path_copy.append(child)
                fringe.append(path_copy)
                visited.add(child)

    return None


def get_hardest_puzzle(goal_state):
    fringe = deque()
    fringe.append((goal_state, 0))

    visited = {goal_state}
    max_visited = set()

    max_length = 0

    while len(fringe) > 0:
        current_node, length = fringe.popleft()
        children = get_children(current_node)
        length += 1

        for child in children:
            if child not in visited:
                fringe.append((child, length))
                visited.add(child)

                if length > max_length:
                    max_visited = {child}

                    max_length = length
                elif length == max_length:
                    max_visited.add(child)

    return max_visited, max_length


def bi_bfs(board):
    forward, goal = True, find_goal(board)
    fringe, goal_fringe = deque(), deque()
    visited, goal_visited = {board}, {goal}

    fringe.append([board])
    goal_fringe.append([goal])
    backwards_path, found = [], False

    while len(fringe) > 0 or len(goal_fringe) > 0:
        current_path = fringe.popleft() if forward else goal_fringe.popleft()
        current_node = current_path[-1]

        if forward and not found and current_node in goal_visited:
            found = True
            backwards_path = current_path.copy()

        if not forward and found and is_parent(current_node, backwards_path[-1]):
            return backwards_path + current_path[0:len(current_path) - 2][::-1]

        children = get_children(current_node)

        for child in children:
            if (forward and child not in visited) or (not forward and child not in goal_visited):
                path_copy = current_path.copy()
                path_copy.append(child)

                if forward:
                    fringe.append(path_copy)
                    visited.add(child)
                else:
                    goal_fringe.append(path_copy)
                    goal_visited.add(child)

        forward = not forward

    return None


file_name = sys.argv[1]

with open(file_name) as file:
    line_list = [line.strip() for line in file]

line_number = 0

for line in line_list:
    line_arr = line.split()
    size, puzzle = int(line_arr[0]), line_arr[1]

    start = time.perf_counter()
    solution_path = bfs_solution(puzzle)
    end = time.perf_counter()

    print("Line %s:" % line_number, puzzle, len(solution_path) - 1, "moves found in", (end - start), "seconds (BFS)")

    start = time.perf_counter()
    solution_path = bi_bfs(puzzle)
    end = time.perf_counter()

    print("Line %s:" % line_number, puzzle, len(solution_path) - 1, "moves found in", (end - start), "seconds (BiBFS)")

    line_number += 1
