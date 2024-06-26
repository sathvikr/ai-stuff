import sys
import time
from collections import deque
from heapq import heappush, heappop


def get_size(puzzle):
    return int(len(puzzle) ** 0.5)


def find_goal(puzzle):
    if puzzle is None:
        return False

    pseudo_sorted = "".join(sorted(puzzle))

    return pseudo_sorted[1:] + pseudo_sorted[0]


def goal_test(puzzle):
    return puzzle == find_goal(puzzle)


def swap(string, i, j):
    l = list(string)
    l[i], l[j] = l[j], l[i]

    return "".join(l)


def get_children(board):
    size = get_size(board)
    children = set()
    index = board.index(".")

    if (index + 1) % size != 0:
        children.add(swap(board, index, index + 1))
    if index % size != 0:
        children.add(swap(board, index, index - 1))
    if index < len(board) - size:
        children.add(swap(board, index, index + size))
    if index >= 0 + size:
        children.add(swap(board, index, index - size))

    return children


def get_outoforderpairs_count(puzzle):
    count = 0

    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] != "." and puzzle[j] != "." and puzzle[i] > puzzle[j]:
                count += 1

    return count


def is_solvable(puzzle):
    size = get_size(puzzle)
    blank_index = puzzle.index(".")
    blank_row = blank_index // size
    outoforderpairs_count = get_outoforderpairs_count(puzzle)

    if size % 2 == 0:
        return (blank_row % 2 == 0) != (outoforderpairs_count % 2 == 0)
    else:
        return outoforderpairs_count % 2 == 0


def bfs(puzzle):
    fringe, visited = deque([[puzzle]]), {puzzle}

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

    return None


def k_dfs(puzzle, k):
    fringe = deque([(puzzle, 0, {puzzle})])

    while len(fringe) > 0:
        current_node = fringe.pop()
        current_state, depth, ancestors = current_node

        if goal_test(current_state):
            return current_node

        if depth < k:
            children = get_children(current_state)

            for child in children:
                if child not in ancestors:
                    temp = (child, depth + 1, {*ancestors, child})

                    fringe.append(temp)

    return None


def id_dfs(puzzle):
    max_depth = 0
    result = None

    while result is None:
        result = k_dfs(puzzle, max_depth)
        max_depth += 1

    return result


def get_coordinates(index, size):
    return index // size, index % size


def heuristic(puzzle):
    taxicab_distance = 0
    goal_state = find_goal(puzzle)
    size = get_size(puzzle)

    for i in range(len(puzzle)):
        if puzzle[i] != ".":
            coordinates = get_coordinates(i, size)
            goal_coordinates = get_coordinates(goal_state.index(puzzle[i]), size)

            deltax = abs(coordinates[0] - goal_coordinates[0])
            deltay = abs(coordinates[1] - goal_coordinates[1])

            taxicab_distance += deltax + deltay

    return taxicab_distance


def a_star(root):
    start_node = (heuristic(root), root, 0)
    closed = set()
    fringe = [[]] * 81
    fringe[start_node[0]].append(start_node)
    # fringe.add(start_node)

    while any(fringe):
        current_node = list(filter(None, fringe))[0]
        fringe[current_node[0][0]].pop(0)
        print(current_node)
        f, current_state, current_depth = current_node[0]

        if goal_test(current_state):
            return current_node

        if current_state not in closed:
            closed.add(current_state)

            for child in get_children(current_state):
                if child not in closed:
                    temp = [current_depth + 1 + heuristic(child), child, current_depth + 1]
                    fringe[temp[0]].append(temp)

    return None


# def a_star(puzzle):
#     start_node = (heuristic(puzzle), puzzle, 0)
#     closed = set()
#     fringe = []
#     heappush(fringe, start_node)
#
#     while len(fringe) > 0:
#         current_node = heappop(fringe)
#         f, current_state, current_depth = current_node
#
#         if goal_test(current_state):
#             return current_node
#
#         if current_state not in closed:
#             closed.add(current_state)
#             children = get_children(current_state)
#
#             for child in children:
#                 if child not in closed:
#                     temp = (current_depth + 1 + heuristic(child), child, current_depth + 1)
#
#                     heappush(fringe, temp)
#
#     return None


file_name = "Sliding Puzzles Files/slide_puzzle_tests_2.txt"

with open(file_name) as file:
    line_list = [line.strip() for line in file]

for i in range(len(line_list)):
    size, puzzle, search_alg = line_list[i].split()
    solution_length, alg_name = None, ""
    start = time.perf_counter()

    if is_solvable(puzzle):

        if search_alg == "!":
            solution_length = len(bfs(puzzle)) - 1
            end = time.perf_counter()

            print("Line %s:" % i, puzzle, solution_length, "moves found in", (end - start),
                  "seconds with BFS")

            start = time.perf_counter()
            solution_length = id_dfs(puzzle)[1]
            end = time.perf_counter()

            print("Line %s:" % i, puzzle, solution_length, "moves found in", (end - start),
                  "seconds with ID-DFS")

            start = time.perf_counter()
            solution_length = a_star(puzzle)[2]
            end = time.perf_counter()

            print("Line %s:" % i, puzzle, solution_length, "moves found in", (end - start),
                  "seconds with A*")
        else:
            if search_alg == "B":
                solution_length = len(bfs(puzzle)) - 1
                alg_name = "BFS"
            elif search_alg == "I":
                solution_length = id_dfs(puzzle)[1]
                alg_name = "ID-DFS"
            elif search_alg == "A":
                solution_length = a_star(puzzle)[2]
                alg_name = "A*"

            end = time.perf_counter()

            if solution_length is not None:
                print("Line %s:" % i, puzzle, solution_length, "moves found in", (end - start), "seconds with %s" % alg_name)
    else:
        end = time.perf_counter()

        print("Line %s:" % i, puzzle, "no solution determined in", (end - start), "seconds")

    print()



