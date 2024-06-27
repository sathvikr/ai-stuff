import math
import random
import sys
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np


def generate_bin_arr_helper(n, arr, tuples, i=0):
    if i == n:
        tuples.append(tuple(arr))
        return

    arr[i] = 0
    generate_bin_arr_helper(n, arr, tuples, i + 1)

    arr[i] = 1
    generate_bin_arr_helper(n, arr, tuples, i + 1)


def generate_bin_arr(n):
    tuples = []
    generate_bin_arr_helper(n, [0] * n, tuples)

    return tuples


def truth_table(bits, n):
    table_size = 2 ** bits
    inputs = generate_bin_arr(bits)
    table = [0] * table_size
    rem = n

    for i in range(table_size - 1, -1, -1):
        table[table_size - i - 1] = inputs[i], rem // 2 ** i
        rem %= 2 ** i

    return table


def generate_possible_tts(bits):
    possible_tts = []

    for i in range(0, 2 ** (2 ** bits)):
        possible_tts.append(truth_table(bits, i))

    return possible_tts


def pretty_print_tt(table):
    for row in table:
        inputs, output = row

        for input in inputs:
            print(input, "", end="")

        print("| ", output)


def dot(a, b):
    product = 0

    for i in range(len(a)):
        product += a[i] * b[i]

    return product


def add(a, b):
    sum = [0] * len(a)

    for i in range(len(a)):
        sum[i] = a[i] + b[i]

    return tuple(sum)


def multiply(a, b):
    prod = [0] * len(a)

    for i in range(len(a)):
        prod[i] = a[i] * b

    return prod


def step(num):
    return 1 if num > 0 else 0


def sigmoid(num):
    return 1 / (1 + np.power(math.e, -num))


def sigmoid_deriv(num):
    y = sigmoid(num)

    return y * (1 - y)


def perceptron(A, w, b, x):
    return A(dot(w, x) + b)


def f(w1, x1, w2, x2, b):
    return w1 * x1 + w2 * x2 + b


def check(n, w, b):
    error = 0
    tt = truth_table(len(w), n)

    for input, output in tt:
        error += abs(output - perceptron(step, w, b, input))

    return 1 - error / len(tt)


# try "-3" (right before i have to do le)

def train_epoch(tt, A, w, b, learning_rate):
    for input, output in tt:
        f_star = perceptron(A, w, b, input)
        w = add(w, multiply(input, (output - f_star) * learning_rate))
        b += (output - f_star) * learning_rate

    return w, b


def train(n, A, w, b, learning_rate=1, epoch_limit=100):
    tt = truth_table(len(w), n)
    w, b = train_epoch(tt, A, w, b, learning_rate)
    num_epochs = 1

    while num_epochs < epoch_limit:
        w2, b2 = train_epoch(tt, A, w, b, learning_rate)

        if (w2, b2) == (w, b):
            break

        w = w2
        b = b2
        num_epochs += 1

    return w, b


def num_modelable(bits):
    count = 0
    num_truth_tables = 2 ** (2 ** bits)

    for n in range(0, num_truth_tables):
        w, b = train(n, step, (0,) * bits, 0)
        accuracy = check(n, w, b)

        if accuracy == 1:
            count += 1

    print(f"{num_truth_tables} possible functions, {count} can be modeled")


def run_xor(in1, in2):
    p3 = perceptron(step, (-1, -2), 3, (in1, in2))  # NAND
    p4 = perceptron(step, (1, 1), 0, (in1, in2))  # OR
    p5 = perceptron(step, (1, 2), -2, (p3, p4))

    return p5


def graph_perceptrons():
    truth_tables = generate_possible_tts(2)
    x1 = np.arange(-2, 2, 0.1)
    y1 = np.arange(-2, 2, 0.1)
    orig_x1 = x1

    x1 = np.concatenate((x1[x1 < 0], [0], x1[x1 > 0]))
    x1 = np.concatenate((x1[x1 < 1], [1], x1[x1 > 1]))
    x1_list = list(x1)

    for n, tt in enumerate(truth_tables):
        above = False
        print(n, tt)
        w, b = train(n, step, (0, 0), 0)
        print(w, b)

        for x in orig_x1:
            for y in y1:
                output = perceptron(step, w, b, (x, y))
                plt.plot(x, y, ".", color="green" if output == 1 else "red")

        if w[1] != 0:
            x2 = (-b - w[0] * x1) / w[1]

            for input, output in tt:
                if output == 1:
                    color = "green"

                    if input[1] > x2[x1_list.index(input[0])]:
                        above = True
                else:
                    color = "red"

                plt.plot(input[0], input[1], "bo", color=color)

            plt.plot(x1, x2, linestyle="--", color="black")
            plt.fill_between(x1, x2, 2, color="cyan") if above else plt.fill_between(x1, -2, x2, color="cyan")
        else:
            for input, output in tt:
                plt.plot(input[0], input[1], "bo", color="green" if output == 1 else "red")

        plt.xlim([-2, 2])
        plt.ylim(-2, 2)
        plt.show()


def p_net(A, x, w_list, b_list):
    A = np.vectorize(A)
    a = [np.array([])] * len(w_list)
    a[0] = x

    for layer in range(1, len(w_list)):
        a[layer] = A(np.add(np.matmul(a[layer - 1], w_list[layer]), b_list[layer]))

    return a[len(w_list) - 1]


def test_diamond(w_list, b_list):
    for i in np.arange(0, 1, 0.1):
        for j in np.arange(0, 1, 0.1):
            net = p_net(step, (i, j), w_list, b_list)[0][0]
            actual = abs(i) + abs(j) < 1
            print(net == actual)


def test_circle(w_list, b_list):
    num_correct = 0
    c = 0

    while c < 500:
        i, j = random.uniform(0, 1), random.uniform(0, 1)
        net = p_net(step, (i, j), w_list, b_list)[0][0].round()
        actual = (i + j) ** .5 < 1

        if net == actual:
            num_correct += 1
        else:
            print(i, ",", j)

        c += 1

    print(f"Accuracy: {num_correct / 5}%")


def a(x, y):
    return 4 * x ** 2 - 3 * x * y + 2 * y ** 2 + 24 * x - 20 * y


def b(x, y):
    return (1 - y) ** 2 + (x - y ** 2) ** 2


def grad_a(x, y):
    return [8 * x - 3 * y + 24, 4 * (y - 5) - 3 * x]


def grad_b(x, y):
    return [2 * (x - y ** 2), 2 * (-2 * x * y + 2 * y ** 3 + y - 1)]


def gradient_descent(f, error=10 ** -8):
    if f == a:
        grad = grad_a
    elif f == b:
        grad = grad_b
    else:
        return

    x, y = 0, 0
    gradient = grad(x, y)

    while abs(gradient[0]) > error or abs(gradient[1]) > error:
        new_f = make_funct(f, gradient, (x, y))
        learning_rate = one_d_minimize(new_f, 0, 1) # LINE OPTIMIZATION HERE

        x -= gradient[0] * learning_rate
        y -= gradient[1] * learning_rate

        gradient = grad(x, y)

        print(f"Location:{x}, {y}")
        print("Gradient:", gradient)


def one_d_minimize(f, left, right, tolerance=10 ** -8):
    length = right - left
    # print(length)

    if length < tolerance:
        return (left + right) / 2

    slice_size = length / 3
    x1, x2 = left + slice_size, right - slice_size

    if f(x1) > f(x2):
        return one_d_minimize(f, x1, right, tolerance)
    else:
        return one_d_minimize(f, left, x1, tolerance)


def make_funct(f, gradient, location):
    def new_f(learning_rate):
        t = np.subtract(location, np.multiply(learning_rate, gradient))

        return f(t[0], t[1])

    return new_f


def get_circle_training_set(n):
    training_set = []

    for _ in range(n):
        i, j = random.uniform(-1, 1), random.uniform(-1, 1)
        x = np.array([[i, j]])
        y = np.array([[int((i ** 2 + j ** 2) ** .5 < 1)]])

        training_set.append((x, y))

    return training_set


def create_network(architecture):
    w_list = [None]
    b_list = [None]

    for i in range(len(architecture) - 1):
        rows, cols = architecture[i], architecture[i + 1]
        w_list.append(np.random.uniform(-1, 1, (rows, cols)))
        b_list.append(np.random.uniform(-1, 1, (1, cols)))

    return w_list, b_list


def forward_propagation_error(w_list, b_list, x, y):
    a = p_net(sigmoid, x, w_list, b_list)
    print(a)

    calculated = (y - np.matrix.round(a))[0]

    return np.dot(calculated, calculated) / 2


def train_network(w_list, b_list, training_set, learning_rate=0.1, max_epochs=500, save_progress=False, print_progress=False):
    N = len(w_list) - 1
    A = np.vectorize(sigmoid)
    A_deriv = np.vectorize(sigmoid_deriv)
    a = [np.array([])] * (N + 1)
    dot_list = [np.array([])] * (N + 1)
    delta_list = [np.array([])] * (N + 1)

    for epoch in range(max_epochs):
        for x, y in training_set:
            a[0] = x

            for layer in range(1, N + 1):
                dot_list[layer] = np.dot(a[layer - 1], w_list[layer]) + b_list[layer]
                a[layer] = A(dot_list[layer])

            delta_list[N] = np.multiply(A_deriv(dot_list[N]), y - a[N])

            for layer in range(N - 1, 0, -1):
                delta_list[layer] = np.multiply(A_deriv(dot_list[layer]),
                                                np.matmul(delta_list[layer + 1], np.transpose(w_list[layer + 1])))

            for layer in range(1, N + 1):
                b_list[layer] = b_list[layer] + learning_rate * delta_list[layer]
                # print((learning_rate * np.transpose(a[layer - 1])).shape, delta_list[layer].shape)
                w_list[layer] = w_list[layer] + np.matmul(learning_rate * np.transpose(a[layer - 1]), delta_list[layer])

        num_misclassified = 0

        if save_progress:
            save_matrix_list("saved_weights.txt", w_list)
            save_matrix_list("saved_biases.txt", b_list)

        if print_progress:
            for x, y in training_set:
                net = np.matrix.round(p_net(sigmoid, x, w_list, b_list))

                if net != y:
                    num_misclassified += 1

            print(f"Epoch: {epoch}, misclassified: {num_misclassified}/{len(training_set)}")
        # else:
        #     print("Epoch:", epoch)

    return w_list, b_list


def save_matrix(file_name, matrix):
    with open(file_name, "w") as file:
        for line in matrix:
            np.savetxt(file, line, fmt='%.2f')

        file.write("\n")


def save_matrix_list(file_name, matrix_list):
    for matrix in matrix_list:
        if matrix is not None:
            save_matrix(file_name, np.asmatrix(matrix))


def get_inaccuracy_ratio(w_list, b_list, data):
    num_wrong = 0

    for x, y in data:
        a = p_net(sigmoid, x, w_list, b_list)

        if np.argmax(a) != np.argmax(y):
            num_wrong += 1

    return num_wrong / len(data)


# command_line = sys.argv[1]
# #
# if command_line == "S":
#     sum_training_set = [
#         (np.array([[0, 0]]), np.array([[0, 0]])),
#         (np.array([[0, 1]]), np.array([[0, 1]])),
#         (np.array([[1, 0]]), np.array([[0, 1]])),
#         (np.array([[1, 1]]), np.array([[1, 0]]))
#     ]
#     w_list, b_list = create_network((2, 2, 2))
#     w_list, b_list = train_network(w_list, b_list, sum_training_set, learning_rate=0.9, max_epochs=1000)
#
#     for entry in sum_training_set:
#         forward_propagation_error(w_list, b_list, entry[0], entry[1])
# elif command_line == "C":
#     w_list, b_list = create_network((2, 4, 1))
#     w_list, b_list = train_network(w_list, b_list, get_circle_training_set(10000), learning_rate=0.1, max_epochs=151, print_progress=True)
#

training_data = []

with open("../mnist_train.csv") as file:
    for line in file:
        cleaned_line = line.strip().split(",")
        training_data.append((np.array([[int(i) / 255 for i in cleaned_line[1:]]]),
                              np.array([[0] * int(cleaned_line[0]) + [1] + [0] * (10 - int(cleaned_line[0]) - 1)])))


testing_data = []
#
with open("../mnist_test.csv") as file:
    for line in file:
        cleaned_line = line.strip().split(",")
        testing_data.append((np.array([[int(i) / 255 for i in cleaned_line[1:]]]),
                              np.array([[0] * int(cleaned_line[0]) + [1] + [0] * (10 - int(cleaned_line[0]) - 1)])))


print("done preprocessing")

architecture = (784, 300, 10)
w_list, b_list = create_network(architecture)
w_list, b_list = train_network(w_list, b_list, training_data, 0.3, max_epochs=11, save_progress=True)

print("Summary:")
print("Network architecture:", architecture)
print("Training inaccuracy:", get_inaccuracy_ratio(w_list, b_list, training_data))
print("Testing inaccuracy:", get_inaccuracy_ratio(w_list, b_list, testing_data))
print("Epochs: 11")

# if sys.argv[1] == "A":
#     gradient_descent(a)
# elif sys.argv[1] == "B":
#     gradient_descent(b)