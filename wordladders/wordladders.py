import sys
import time
from collections import deque, defaultdict


def get_legal_words(filepath):
    start_time = time.perf_counter()

    legal_words = set()

    with open(filepath) as file:
        for line in file:
            legal_words.add(line.strip())

    end_time = time.perf_counter()

    print("Time to create the data structure was: %s" % (end_time - start_time), "seconds")
    print("There are %s" % len(legal_words), "words in this dict.")

    return legal_words


def create_pseudo_graph(legal_words):
    graph = defaultdict(set)

    for word in legal_words:
        for i in range(len(word)):
            graph[word[:i] + "_" + word[i + 1:]].add(word)

    return graph


def get_pseudo_children(word, graph):
    stored_children = set()

    for i in range(len(word)):
        stored_children |= graph[word[:i] + "_" + word[i + 1:]]

    return stored_children


def create_graph(legal_words):
    graph = {}
    pseudo_graph = create_pseudo_graph(legal_words)

    for word in legal_words:
        graph[word] = get_pseudo_children(word, pseudo_graph)

    return graph


def bfs(start, end, graph):
    if start == end:
        return [start, end]

    fringe, visited = deque([[start]]), {start}

    while len(fringe) > 0:
        current_path = fringe.popleft()
        current_node = current_path[-1]
        children = graph[current_node]

        for child in children:
            if child not in visited:
                if child == end:
                    current_path.append(child)

                    return current_path

                fringe.append([*current_path, child])
                visited.add(child)

    return None


def solve_puzzles(filepath, legal_words):
    start_time = time.perf_counter()
    graph = create_graph(legal_words)

    with open(filepath) as file:
        line_list = [line.strip() for line in file]

    for i in range(len(line_list)):
        start, end = line_list[i].split()
        word_ladder = bfs(start, end, graph)

        print("\nLine: %s" % i)

        if word_ladder is None:
            print("No solution!")
        else:
            print("Length is: %s" % len(word_ladder))

            for word in word_ladder:
                print(word)

    end_time = time.perf_counter()

    print("\nTotal time to create the graph and solve these puzzles was: %s" % (end_time - start_time), "seconds")


def solve(dictionary_filepath, puzzle_filepath):
    legal_words = get_legal_words(dictionary_filepath)
    solve_puzzles(puzzle_filepath, legal_words)


solve("Word Ladders Files/words_06_longer.txt", "Word Ladders Files/puzzles_longer.txt")
