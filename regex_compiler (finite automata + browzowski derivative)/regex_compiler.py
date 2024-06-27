import collections
from pprint import pprint

alphabet = ["a", "b"]
tokens = []


def tokenize(regex):
    capturing_group = 0
    i = 0

    while regex[i] == "(" and regex[-i - 1] == ")":
        capturing_group -= 1
        i += 1

    for j, char in enumerate(regex):
        if char in {"(", ")"}:
            capturing_group += 1
        elif char in {"?", "+", "*"}:
            if regex[j - 1] == ")":
                tokens.append([char, capturing_group - 1, None])
            else:
                tokens[-1][-1] = char
        else:
            tokens.append([char, capturing_group, None])


def combine(arg0, arg1, op):
    if op == "" and (arg0 is None or arg1 is None):
        return None
    elif op == "|":
        if arg0 is None and arg1 is None:
            return None
        elif arg0 is None and arg1 is not None:
            return arg1
        elif arg0 is not None and arg1 is None:
            return arg0

    combined = []

    if arg0 is not None:
        for token in arg0:
            combined.append(token)

        if arg1 is not None and op == "|":
            combined.append(["|", get_initial_capturing_group(arg0), None])

    if arg1 is not None:
        for token in arg1:
            combined.append(token)

    return combined


def get_initial_capturing_group(tokenized_regex):
    for token in tokenized_regex:
        if len(token) == 3:
            return token[1]

    return -1


def has_epsilon(tokenized_regex):
    for token in tokenized_regex:
        if len(token) != 0 and token[2] not in {"?", "+", "*"}:
            return False

    return True


# def brzozowski_derivative(tokenized_regex, wrt_char):
#     if tokenized_regex is None or len(tokenized_regex) == 0:
#         return None
#     elif len(tokenized_regex) == 1:
#         if tokenized_regex[0] == []:
#             tokenized_regex = tokenized_regex[1:]
#         else:
#             char, capturing_group, quantifier = tokenized_regex[0]
#
#             if quantifier is None or quantifier == "?":
#                 return [] if char == wrt_char else None
#             elif quantifier in {"+", "*"}:
#                 return combine(
#                     brzozowski_derivative([[char, capturing_group, None]], wrt_char), [[char, capturing_group, "*"]],
#                     "")
#
#     if tokenized_regex == []:
#         return []
#
#     r1 = []
#     r2 = []
#     initial_capturing_group = get_initial_capturing_group(tokenized_regex)
#     passed_union = False
#
#     for i, token in enumerate(tokenized_regex):
#         if len(token) == 3:
#             char, capturing_group, quantifier = token
#
#             if char == "|":
#                 passed_union = True
#
#             if capturing_group > initial_capturing_group:
#                 r2.append(token)
#             elif passed_union and (
#                     initial_capturing_group < capturing_group != tokenized_regex[i - 1][1] or 0 == capturing_group):
#                 r2.append(token)
#             else:
#                 r1.append(token)
#
#     if len(r2) == 0:
#         r1 = [tokenized_regex[0]]
#         r2 = tokenized_regex[1:]
#
#     # print(r1, r2)
#
#     if r2[0][0] == "|":
#         t1 = brzozowski_derivative(r1, wrt_char)
#         t2 = brzozowski_derivative(r2[1:], wrt_char)
#
#         # print(t1, t2)
#
#         return combine(t1, t2, "|")
#     else:
#         # return r2
#         # print(r1)
#         t1 = combine(brzozowski_derivative(r1, wrt_char), r2, "")
#
#         # if empty string is accepted by regex r1, return t1 | deriv(r2) else return t1
#         if has_epsilon(r1):
#             return combine(t1, brzozowski_derivative(r2, wrt_char), "|")
#
#         return t1


def brzozowski_derivative(tokenized_regex, wrt_char):
    if tokenized_regex is None or len(tokenized_regex) == 0:
        return None
    elif len(tokenized_regex) == 1:
        if tokenized_regex[0] == []:
            tokenized_regex = []


def dfa_helper(tokenized_regex, pseudo_dfa):
    for wrt_char in alphabet:
        deriv = brzozowski_derivative(tokenized_regex, wrt_char)
        str_deriv = str(deriv)

        if deriv is not None:
            # print(tokenized_regex, "-->", str_deriv, "(", wrt_char, ")")
            # if deriv in DFA, connect current state to that state by wrt_char
            if str_deriv in pseudo_dfa:
                pseudo_dfa[str(tokenized_regex)][wrt_char] = str_deriv
            # else, make new state with deriv and connect current state to new state by wrt_char and call to_dfa(deriv)
            else:
                pseudo_dfa[str_deriv] = {}
                pseudo_dfa[str(tokenized_regex)][wrt_char] = str_deriv
                dfa_helper(deriv, pseudo_dfa)

    # final states are the nullable ones

    return pseudo_dfa


def to_dfa(tokenized_regex):
    pseudo_dfa = collections.defaultdict(dict)
    pseudo_dfa[str(tokenized_regex)] = {}

    return dfa_helper(tokenized_regex, pseudo_dfa)


def clean_dfa(to_clean):
    dfa = collections.defaultdict(dict)
    final_states = []
    keys = list(to_clean.keys())

    for i, state in enumerate(to_clean):
        if len(to_clean[state]) == 0:
            dfa[i] = {}
            final_states.append(i)
        else:
            for connection in to_clean[state]:
                dfa[i][connection] = keys.index(to_clean[state][connection])

    return dfa, final_states

#         if curr_regex.epsilon_aux() == RegEx.EPSILON:
#             self.final_states.append(curr_regex)
#
#         for letter in self.alphabet:
#             deriv = curr_regex.brzozowski_derivative(letter)
#             str_deriv = str(deriv)
#             # print(curr_regex, letter, deriv)
#             # print(curr_regex, type(curr_regex), curr_regex.a, curr_regex.b, letter, deriv)
#
#             if deriv != RegEx.NULL:
#                 if str_deriv in pseudo_dfa:
#                     pseudo_dfa[str(curr_regex)][letter] = str_deriv
#                 else:
#                     pseudo_dfa[str_deriv] = {}
#                     pseudo_dfa[str(curr_regex)][letter] = str_deriv
#
#                     if deriv != RegEx.EPSILON:
#                         self.compilation_helper(deriv, pseudo_dfa)

def print_transition_table(dfa, language):
    print("*\t\t" + "\t\t".join([letter for letter in language]))

    for state in dfa:
        row = str(state) + "\t"

        for letter in language:
            row += "\t" + str(dfa[state][letter]) + "\t" if letter in dfa[state] else "\t_\t"

        print(row)


# regex = "a|(ab|b*a)*"
regex = "ab?a*"
tokenize(regex)

pseudo_dfa = to_dfa(tokens)
dfa, final_states = clean_dfa(pseudo_dfa)
print_transition_table(dfa, alphabet)
print("Final:", final_states)

# print(tokens)
# print(brzozowski_derivative(tokens, "a"))

# pprint(pseudo_dfa)