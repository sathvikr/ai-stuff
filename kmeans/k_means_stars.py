
import random
from math import log, inf


def read_dataset(filename):
    dataset = {}

    with open(filename) as f:
        line_list = [line.strip().split(",") for line in f]

    for i in range(1, len(line_list)):
        line = line_list[i]
        dataset[(log(float(line[0])), log(float(line[1])), log(float(line[2])), float(line[3]))] = int(line[4])

    return dataset


def get_squared_error(star_a, star_b):
    error = 0

    for i in range(len(star_a)):
        error += (star_a[i] - star_b[i]) ** 2

    return error


def get_closest_mean_index(star, means):
    min_index = -1
    min_error = inf

    for i, mean in enumerate(means):
        error = get_squared_error(star, mean)

        if error < min_error:
            min_index = i
            min_error = error

    return min_index


def get_new_mean(star_list):
    mean = [0, 0, 0, 0]

    for star in star_list:
        for i, attr in enumerate(star):
            mean[i] += attr

    for i, attr in enumerate(mean):
        mean[i] /= len(star_list)

    return tuple(mean)


def k_means(k, stars, err=0.0005):
    means = random.sample(stars, k)
    star_lists = tuple([] for _ in range(k))
    changed = True

    while changed:
        changed = False

        for star in stars:
            index = get_closest_mean_index(star, means)
            star_lists[index].append(star)

        for i, star_list in enumerate(star_lists):
            new_mean = get_new_mean(star_list)

            if get_squared_error(means[i], new_mean) > err:
                changed = True

            means[i] = new_mean

        if changed:
            star_lists = tuple([] for _ in range(k))

    return means, star_lists


dataset = read_dataset("star_data.csv")
means, star_groups = k_means(6, list(dataset.keys()), err=0.0000005)

for i, mean in enumerate(means):
    print("Mean:", mean)
    print("Star group:")

    for star in star_groups[i]:
        print(star, "- Star type:", dataset[star])

    print()

