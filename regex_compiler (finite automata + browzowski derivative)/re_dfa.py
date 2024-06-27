import sys


def read_dfa(lines):
    dfa = {}
    language, num_states, final_states = lines[0].split("\n")
    num_states = int(num_states)
    final_states = [int(i) for i in final_states.split(" ")]

    for i in range(1, num_states + 1):
        info = lines[i].split("\n")
        state = int(info[0])
        dfa[state] = {}

        for j in range(1, len(info)):
            letter, connection = info[j].split()
            dfa[state][letter] = int(connection)

    return dfa, language, final_states


def print_transition_table(dfa, language):
    print("*  " + "  ".join([letter for letter in language]))

    for state in dfa:
        row = str(state) + " "

        for letter in language:
            row += " " + str(dfa[state][letter]) + " " if letter in dfa[state] else " _ "

        print(row)


def matches(string, dfa, final_states):
    state = 0

    for letter in string:
        if letter not in dfa[state]:
            return False

        state = dfa[state][letter]

    return state in final_states


def print_dfa_test_info(dfa, language, final, test):
    print_transition_table(dfa, language)
    print(matches(test, dfa, final), test)
    print(final)
    print()


dfas = [
    {
        0: {
            "a": 1
        },
        1: {
            "a": 2
        },
        2: {
            "b": 3
        },
        3: {}
    },
    {
        0: {
            "0": 0,
            "1": 1,
            "2": 0
        },
        1: {
            "0": 0,
            "1": 1,
            "2": 0
        }
    },
    {
        0: {
            "a": 0,
            "b": 1,
            "c": 0
        },
        1: {
            "a": 1,
            "b": 1,
            "c": 1
        }
    },
    {
        0: {
            "0": 1,
            "1": 0,
        },
        1: {
            "0": 0,
            "1": 2,
        },
        2: {
            "0": 0,
            "1": 1
        }
    },
    {
        0: {
            "0": 1,
            "1": 3
        },
        1: {
            "0": 0,
            "1": 2
        },
        2: {
            "0": 3,
            "1": 1
        },
        3: {
            "0": 2,
            "1": 0
        }
    },
    {
        0: {
            "a": 1,
            "b": 0,
            "c": 0,
        },
        1: {
            "a": 1,
            "b": 2,
            "c": 0
        },
        2: {
            "a": 1,
            "b": 0
        }
    },
    {
        0: {
            "0": 0,
            "1": 1
        },
        1: {
            "0": 2,
            "1": 0
        },
        2: {
            "0": 2,
            "1": 3
        },
        3: {
            "0": 2,
            "1": 4
        },
        4: {
            "0": 4,
            "1": 4
        }
    }
]

languages = ["ab", "012", "abc", "01", "01", "abc", "01"]
final_states = [[3], [1], [1], [0], [0], [0, 1, 2], [4]]

try:
    i = int(sys.argv[1])

    with open(sys.argv[2]) as f:
        test_strings = [test_string.strip() for test_string in f]

    dfa, language = dfas[i - 1], languages[i - 1]

    print_transition_table(dfa, language)
    print("Final nodes:", final_states[i - 1])

    for test_string in test_strings:
        print(matches(test_string, dfa, final_states[i - 1]), test_string)
except ValueError:
    dfa_file, test_file = sys.argv[1], sys.argv[2]

    dfa_line_list = open(dfa_file).read().split("\n\n")
    dfa, language, final_states = read_dfa(dfa_line_list)

    print_transition_table(dfa, language)
    print("Final nodes:", final_states)

    with open(test_file) as f:
        test_strings = [test_string.strip() for test_string in f]

    for test_string in test_strings:
        print(matches(test_string, dfa, final_states), test_string)

