import time
from collections import deque, defaultdict


def get_legal_words(filepath):
    legal_words = set()

    with open(filepath) as file:
        for line in file:
            legal_words.add(line.strip())

    return legal_words


def create_graph(legal_words):
    graph = defaultdict(set)

    for word in legal_words:
        for i in range(len(word)):
            graph[word[:i] + "_" + word[i + 1:]].add(word)

    return graph


def get_stored_children(word, graph):
    stored_children = set()

    for i in range(len(word)):
        temp = graph[word[:i] + "_" + word[i + 1:]]

        stored_children |= temp

    return stored_children


def bfs(start, end, graph):
    if start == end:
        return [start, end]

    fringe, visited = deque([[start]]), {start}

    while len(fringe) > 0:
        current_path = fringe.popleft()
        current_node = current_path[-1]
        children = get_stored_children(current_node, graph)

        for child in children:
            if child not in visited:
                if child == end:
                    current_path.append(child)

                    return current_path

                fringe.append([*current_path, child])
                visited.add(child)

    return None


start_time = time.perf_counter()
legal_words = get_legal_words("Word Ladders Files/words_06_longer.txt")
end_time = time.perf_counter()

print("Time to create the data structure was: %s" % (end_time - start_time), "seconds")
print("There are %s" % len(legal_words), "words in this dict.")

start_time = time.perf_counter()
graph = create_graph(legal_words)

with open("Word Ladders Files/puzzles_longer.txt") as file:
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

print("\nTotal time to solve these puzzles was: %s" % (end_time - start_time), "seconds")
