import collections
import math
import random
from pprint import pprint

import matplotlib.pyplot as plt


def get_map(dataset):
    datamap = collections.defaultdict(list)
    headers = dataset[0]

    for i in range(1, len(dataset)):
        for j in range(0, len(dataset[i])):
            datamap[headers[j]].append(dataset[i][j])

    return datamap


def get_datamap_outcomes(datamap):
    return list(datamap.items())[-1]


def split_datamap(datamap, column_name):
    new_datamaps = {}

    for value in set(datamap[column_name]):
        curr_datamap = collections.defaultdict(list)

        for index, elem in enumerate(datamap[column_name]):
            if elem == value:
                for feature_name in datamap:
                    curr_datamap[feature_name].append(datamap[feature_name][index])

        new_datamaps[value] = curr_datamap

    return new_datamaps


def get_entropy(column):
    entropy = 0
    total = 0
    counts = {}

    for elem in column:
        counts[elem] = 1 if elem not in counts else counts[elem] + 1
        total += 1

    for count in counts.values():
        entropy += count / total * math.log2(count / total)

    return -entropy


def get_datamap_entropy(datamap):
    return get_entropy(list(datamap.items())[-1][1])


def get_expected_entropy(datamap, column_name, outcomes):
    # print(outcomes)
    entropy = 0

    for value in set(datamap[column_name]):
        new_dataset = [outcomes[index] for index, elem in enumerate(datamap[column_name]) if elem == value]
        entropy += len(new_dataset) / len(datamap[column_name]) * get_entropy(new_dataset)

    return entropy


def get_ideal_decision_tree(datamap, tree=None):
    if tree is None:
        tree = {}

    items = list(datamap.items())
    outcomes = items[-1][1]
    datamap_entropy = get_entropy(outcomes)
    max_info_gain = -math.inf
    optimal_feature_name = ""

    for i in range(len(datamap) - 1):
        feature_name = items[i][0]
        information_gain = datamap_entropy - get_expected_entropy(datamap, feature_name, outcomes)

        if information_gain > max_info_gain:
            optimal_feature_name = feature_name
            max_info_gain = information_gain

    if datamap_entropy != 0 and max_info_gain == 0:
        optimal_feature_name = random.choice(items[:-1])[0]

    smaller_datamaps = split_datamap(datamap, optimal_feature_name)
    tree[optimal_feature_name + "?"] = {}

    if datamap_entropy != 0 and max_info_gain == 0:
        # print(get_datamap_outcomes(datamap))
        tree[optimal_feature_name + "?"][random.choice(list(smaller_datamaps.keys()))] = random.choice(get_datamap_outcomes(datamap)[1])
    else:
        # print(datamap_entropy, max_info_gain)
        for optimal_feature_value in smaller_datamaps:
            datamap_entropy = get_datamap_entropy(smaller_datamaps[optimal_feature_value])
            smaller_datamap = smaller_datamaps[optimal_feature_value]

            if datamap_entropy == 0:
                tree[optimal_feature_name + "?"][optimal_feature_value] = get_datamap_outcomes(smaller_datamap)[1][0]
            else:
                tree[optimal_feature_name + "?"][optimal_feature_value] = get_ideal_decision_tree(smaller_datamap, {})

    return tree


def print_decision_tree_helper(f, tree, indent=0):
    for key in tree:
        if indent > 0:
            f.write("\n")

        f.write("  " * indent + " * " + str(key))

        if isinstance(tree[key], dict):
            print_decision_tree_helper(f, tree[key], indent + 1)
        else:
            f.write(" --> " + str(tree[key]))


def print_decision_tree(filename, tree):
    with open(filename, "w") as f:
        print_decision_tree_helper(f, tree)


def classify(tree, headers, feature_vector):
    ans = tree
    i = 0

    while i < len(feature_vector):
        if type(ans) == str:
            break
        elif headers[i] + "?" in ans.keys():
            if feature_vector[i] not in ans[headers[i] + "?"].keys():
                ans = ans[headers[i] + "?"][random.choice(list(ans[headers[i] + "?"].keys()))]
            else:
                ans = ans[headers[i] + "?"][feature_vector[i]]
            i = -1

        i += 1

    return ans


def get_mode(dataset, index):
    mode = None
    highest_count = 0
    counts = {}

    for i in range(1, len(dataset)):
        row = dataset[i]
        counts[row[index]] = 0 if row[index] not in counts else counts[row[index]] + 1

    for choice in counts:
        if highest_count < counts[choice] and choice != "?":
            highest_count = counts[choice]
            mode = choice

    return mode


def get_preprocessed_dataset(dataset):
    preprocessed_dataset = []
    modes = [get_mode(dataset, i) for i in range(0, len(dataset[0]))]

    for row in dataset:
        new_row = []

        for i in range(1, len(row)):
            if row[i] != "?":
                new_row.append(row[i])
            else:
                new_row.append(modes[i])

        preprocessed_dataset.append(new_row)

    return preprocessed_dataset


def train_test_split(dataset, split=50):
    non_headers = dataset[1:]
    random.shuffle(non_headers)
    dataset = [dataset[0]] + non_headers

    return [dataset[i] for i in range(len(dataset) - split)], \
           [dataset[i] for i in range(len(dataset) - split, len(dataset))]


def is_valid(dataset):
    initial_classification = dataset[0][-1]

    for i in range(1, len(dataset)):
        if dataset[i][-1] != initial_classification:
            return True

    return False


def build_learning_curve(training_set, testing_set, start, stop, step):
    learning_curve = []

    headers, training_set = training_set[0], training_set[1:]
    # print(training_set)

    for size in range(start, stop, step):
        train = random.sample(training_set, size - 1)

        while not is_valid(train):
            train = random.sample(training_set, size - 1)

        print(len(train))

        train = [headers] + train
        tree = get_ideal_decision_tree(get_map(train))
        num_correct = 0

        # pprint(tree)

        for row in testing_set:
            feature_vector, actual_classification = row[:-1], row[-1]
            # print(feature_vector)
            classification = classify(tree, headers, feature_vector)
            # print(classification, actual_classification)

            if classification == actual_classification:
                num_correct += 1

        learning_curve.append((size, num_correct / len(testing_set)))

    pprint(learning_curve)
    plt.scatter(*zip(*learning_curve))
    plt.show()


with open("nursery.csv") as f:
    dataset = [line.strip().split(",") for line in f]

training_set, testing_set = train_test_split(get_preprocessed_dataset(dataset), split=500)

build_learning_curve(training_set, testing_set, 500, 12000, 500)
# pprint(training_set)
# tree = get_ideal_decision_tree(get_map(training_set))
# pprint(tree)
# print(testing_set[0])
# print(classify(tree, training_set[0], testing_set[0]))