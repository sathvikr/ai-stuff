import sys
import time
from heapq import heappush, heappop
from collections import defaultdict
from math import pi, acos, sin, cos
from string import ascii_letters


def get_distance(node1, node2):
    if node1 == node2:
        return 0

    y1, x1 = node1
    y2, x2 = node2

    R = 3958.76
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0

    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R


def get_first_letter_index(str, letters):
    for i in range(len(str)):
        if str[i] in letters:
            return i

    return -1


def generate_node_graph(nodes):
    node_graph = {}

    for node in nodes:
        id, latitude, longitude = node.split()

        node_graph[id] = (float(latitude), float(longitude))

    return node_graph


def generate_city_names(cities):
    city_names = {}
    letters = set(ascii_letters)

    for city in cities:
        first_letter_index = get_first_letter_index(city, letters)

        id = city[:first_letter_index - 1]
        name = city[first_letter_index:]

        city_names[name] = id

    return city_names


def generate_train_network(node_graph, edges):
    train_network = defaultdict(set)

    for edge in edges:
        start, end = edge.split()
        distance = get_distance(node_graph[start], node_graph[end])

        train_network[start].add((end, distance))
        train_network[end].add((start, distance))

    return train_network


def get_children(state, train_network):
    return train_network[state]


def dijkstra(start, end, train_network):
    visited = set()
    fringe = []

    heappush(fringe, (0, start))

    while len(fringe) > 0:
        current_node = heappop(fringe)
        current_distance, current_state = current_node

        if current_state == end:
            return current_node

        if current_state not in visited:
            visited.add(current_state)

            children = get_children(current_state, train_network)

            for child in children:
                child_state, child_distance = child

                if child_state not in visited:
                    heappush(fringe, (current_distance + child_distance, child_state))

    return None


def a_star(start, end, node_graph, train_network):
    visited = set()
    fringe = []

    heappush(fringe, (0, start, 0))

    while len(fringe) > 0:
        current_node = heappop(fringe)
        f, current_state, current_distance = current_node

        if current_state == end:
            return current_node

        if current_state not in visited:
            visited.add(current_state)

            children = get_children(current_state, train_network)

            for child in children:
                child_state, child_distance = child

                if child_state not in visited:
                    actual_distance = current_distance + child_distance
                    estimated_distance = get_distance(node_graph[child_state], node_graph[end])

                    heappush(fringe,
                             (actual_distance + estimated_distance, child_state, current_distance + child_distance))

    return None


with open("rrNodes.txt") as f:
    node_list = [line.strip() for line in f]

with open("rrNodeCity.txt") as f:
    city_list = [line.strip() for line in f]

with open("rrEdges.txt") as f:
    edge_list = [line.strip() for line in f]


start_city = sys.argv[1]
end_city = sys.argv[2]

start_time = time.perf_counter()
node_graph = generate_node_graph(node_list)
city_names = generate_city_names(city_list)
train_network = generate_train_network(node_graph, edge_list)
end_time = time.perf_counter()

print("Time to create data structures: %s" % (end_time - start_time))

start_id = city_names[start_city]
end_id = city_names[end_city]

start_time = time.perf_counter()
shortest_path = dijkstra(start_id, end_id, train_network)
end_time = time.perf_counter()

print(start_city, "to", end_city, "with Dijkstra: %s" % shortest_path[0], "in", (end_time - start_time), "seconds")

start_time = time.perf_counter()
shortest_path = a_star(start_id, end_id, node_graph, train_network)
end_time = time.perf_counter()

print(start_city, "to", end_city, "with A*: %s" % shortest_path[2], "in", (end_time - start_time), "seconds")
