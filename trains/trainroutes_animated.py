import sys
import tkinter as tk
from heapq import heappush, heappop
from collections import defaultdict
from math import pi, acos, sin, cos
from string import ascii_letters

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
UPDATE_FREQUENCY = 100

lines = defaultdict(list)


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


def geographic_to_cartesian(geographic):
    latitude, longitude = geographic
    x = longitude
    y = SCREEN_HEIGHT - latitude

    return (x + SCREEN_WIDTH / 2) * 10 - 3.625 * SCREEN_WIDTH, (y - SCREEN_HEIGHT / 2) * 10 - 4.25 * SCREEN_HEIGHT


def draw_train_routes(canvas, node_graph, edges):
    for edge in edges:
        start, end = edge.split()

        line = canvas.create_line(
            [geographic_to_cartesian(node_graph[start]), geographic_to_cartesian(node_graph[end])])

        lines[(start, end)] = line
        lines[(end, start)] = line


def dijkstra(root, canvas, start, end, train_network):
    visited = set()
    fringe = []

    heappush(fringe, (0, [start]))

    i = 0

    while len(fringe) > 0:
        current_node = heappop(fringe)
        current_distance, current_path = current_node
        current_state = current_path[-1]

        if current_state == end:
            return current_path

        if current_state not in visited:
            visited.add(current_state)

            children = get_children(current_state, train_network)

            for child in children:
                child_state, child_distance = child

                if child_state not in visited:
                    temp_path = current_path.copy()
                    temp_path.append(child_state)

                    heappush(fringe, (current_distance + child_distance, temp_path))

                    canvas.itemconfig(lines[(current_state, child_state)], fill="red")

                    if i % UPDATE_FREQUENCY == 0:
                        root.update()

        i += 1

    return None


def a_star(root, canvas, start, end, node_graph, train_network):
    visited = set()
    fringe = []

    heappush(fringe, (0, [start], 0))

    i = 0

    while len(fringe) > 0:
        current_node = heappop(fringe)
        f, current_path, current_distance = current_node
        current_state = current_path[-1]

        if current_state == end:
            return current_path

        if current_state not in visited:
            visited.add(current_state)

            children = get_children(current_state, train_network)

            for child in children:
                child_state, child_distance = child

                if child_state not in visited:
                    actual_distance = current_distance + child_distance
                    estimated_distance = get_distance(node_graph[child_state], node_graph[end])

                    heappush(fringe,
                             (actual_distance + estimated_distance, [*current_path, child_state], current_distance + child_distance))
                    canvas.itemconfig(lines[(current_state, child_state)], fill="blue")

                    if i % UPDATE_FREQUENCY == 0:
                        root.update()
        i += 1

    return None


def color_path(canvas, path, color):
    for i in range(len(path) - 1):
        canvas.itemconfig(lines[(path[i], path[i + 1])], fill=color)


with open("Train Routes Files/rrNodes.txt") as f:
    node_list = [line.strip() for line in f]

with open("Train Routes Files/rrNodeCity.txt") as f:
    city_list = [line.strip() for line in f]

with open("Train Routes Files/rrEdges.txt") as f:
    edge_list = [line.strip() for line in f]

node_graph = generate_node_graph(node_list)
city_names = generate_city_names(city_list)
train_network = generate_train_network(node_graph, edge_list)

# start_city = sys.argv[1]
# end_city = sys.argv[2]
start_city = "Las Vegas"
end_city = "Washington DC"
start_id = city_names[start_city]
end_id = city_names[end_city]

# Dijkstra Search
root_dijkstra = tk.Tk()
canvas_dijkstra = tk.Canvas(root_dijkstra, height=800, width=800, bg="black")

draw_train_routes(canvas_dijkstra, node_graph, edge_list)

canvas_dijkstra.pack(expand=True)

shortest_path_dijkstra = dijkstra(root_dijkstra, canvas_dijkstra, start_id, end_id, train_network)
color_path(canvas_dijkstra, shortest_path_dijkstra, "#66ff00")

root_dijkstra.mainloop()

# A* Search
root_a_star = tk.Tk()
canvas_a_star = tk.Canvas(root_a_star, height=800, width=800, bg="black")

draw_train_routes(canvas_a_star, node_graph, edge_list)

canvas_a_star.pack(expand=True)

shortest_path_a_star = a_star(root_a_star, canvas_a_star, start_id, end_id, node_graph, train_network)
color_path(canvas_a_star, shortest_path_a_star, "blue")

root_a_star.mainloop()
