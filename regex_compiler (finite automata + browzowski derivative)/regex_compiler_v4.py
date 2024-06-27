import collections


class RegEx:
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())


class Token:
    def __init__(self, value):
        self.value = value
        self.none = False if value is not None else True
        self.unary = True

    def __repr__(self):
        return str(self.value) if not self.none else "{}"

    def epsilon_aux(self):
        return RegEx.NULL

    def brzozowski_derivative(self, wrt_char):
        if self.value != wrt_char:
            return RegEx.NULL

        return RegEx.EPSILON


class Epsilon(RegEx):
    def __init__(self):
        self.none = False
        self.unary = True

    def epsilon_aux(self):
        return RegEx.EPSILON

    def __repr__(self):
        return "{e}"

    def brzozowski_derivative(self, wrt_char):
        return RegEx.NULL


class QuestionMark(RegEx):
    def __init__(self, token):
        self.token = token
        self.none = False
        self.unary = True

    def __repr__(self):
        return str(self.token) + "?" if isinstance(self.token, Token) else "(" + str(self.token) + ")?"

    def epsilon_aux(self):
        return RegEx.EPSILON

    def brzozowski_derivative(self, wrt_char):
        return self.token.brzozowski_derivative(wrt_char)


class Star(RegEx):
    def __init__(self, token):
        self.token = token
        self.none = False
        self.unary = True

    def __repr__(self):
        return str(self.token) + "*" if isinstance(self.token, Token) else "(" + str(self.token) + ")*"

    def epsilon_aux(self):
        return RegEx.EPSILON

    def brzozowski_derivative(self, wrt_char):
        d1 = self.token.brzozowski_derivative(wrt_char)

        if d1 == RegEx.NULL:
            return RegEx.NULL
        elif d1 == RegEx.EPSILON:
            return Star(self.token)

        return Concat(d1, Star(self.token))


class Plus(RegEx):
    def __init__(self, token):
        self.token = token
        self.none = False
        self.unary = True

    def __repr__(self):
        return str(self.token) + "+" if isinstance(self.token, Token) else "(" + str(self.token) + ")+"

    def epsilon_aux(self):
        return RegEx.NULL

    def brzozowski_derivative(self, wrt_char):
        d1 = self.token.brzozowski_derivative(wrt_char)

        if d1 == RegEx.NULL:
            return RegEx.NULL
        elif d1 == RegEx.EPSILON:
            return Star(self.token)

        return Concat(d1, Star(self.token))


class Union(RegEx):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.none = False
        self.unary = False

        # print("union: ", self.a, self.b)

        if (self.a, self.b) == (RegEx.NULL, RegEx.NULL):
            self.none = True

    def __repr__(self):
        if RegEx.NULL != self.a and RegEx.NULL != self.b and RegEx.EPSILON != self.a and RegEx.EPSILON != self.b:
            return "(" + str(self.a) + "|" + str(self.b) + ")"
        elif self.a not in {RegEx.NULL, RegEx.EPSILON}:
            return str(self.a)
        elif self.b not in {RegEx.NULL, RegEx.EPSILON}:
            return str(self.b)

        return ""

    def epsilon_aux(self):
        if (self.a.epsilon_aux(), self.b.epsilon_aux()) == (RegEx.NULL, RegEx.NULL):
            return RegEx.NULL

        return RegEx.EPSILON

    def brzozowski_derivative(self, wrt_char):
        d1 = self.a.brzozowski_derivative(wrt_char)
        d2 = self.b.brzozowski_derivative(wrt_char)
        # print(d1, type(d1))

        # print("blob", d1, d2)

        # print(self.a, d1)

        if d1.none and d2.none:
            return RegEx.NULL
        elif d1.none or d1 == RegEx.EPSILON and not d2.none:
            return d2
        elif d2.none or (d2 == RegEx.EPSILON or d1 == d2) and not d1.none:
            return d1

        return Union(d1, d2)


class Concat(RegEx):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.none = False
        self.unary = False

        if RegEx.NULL == self.a or RegEx.NULL == self.b:
            self.none = True

    def __repr__(self):
        c_repr = ""

        if self.none:
            return c_repr
        if self.a != RegEx.EPSILON:
            c_repr += str(self.a)
        if self.b != RegEx.EPSILON:
            c_repr += str(self.b)

        return "(" + c_repr + ")"

    def epsilon_aux(self):
        if self.a.epsilon_aux() == RegEx.NULL or self.b.epsilon_aux() == RegEx.NULL:
            return RegEx.NULL

        return RegEx.EPSILON

    def brzozowski_derivative(self, wrt_char):
        d1 = self.a.brzozowski_derivative(wrt_char)
        d2 = self.b.brzozowski_derivative(wrt_char)
        # print(d1, type(d1))

        # (d1)(self.b)|d2

        # print(d1, d2, self.a, self.b)
        # print(self.a.epsilon_aux())

        if not d2.none and self.a.epsilon_aux() == RegEx.EPSILON:
            # print(";jldsj;fls", self.a)
            if d1.none or self.b.none:
                return d2

            t1 = Concat(d1, self.b)

            if t1 == d2:
                return t1

            return Union(t1, d2)

        if d1 == RegEx.EPSILON:
            return self.b
        if d1 == RegEx.NULL:
            return RegEx.NULL
        if self.b == RegEx.EPSILON:
            return d1

        return Concat(d1, self.b)


class Tokenizer:
    def __init__(self, alphabet, regex):
        self.alphabet = alphabet
        self.regex = regex
        self.tokens = []
        self.pos = -1
        self.current_char = ""
        self.current_token = None
        self.next_char()
        self.advance()

    def next_char(self):
        self.pos += 1
        self.current_char = self.regex[self.pos] if self.pos < len(self.regex) else None

    def get_next_char(self):
        return self.regex[self.pos + 1] if self.pos + 1 < len(self.regex) else None

    def advance(self):
        if self.pos >= len(self.regex):
            self.current_token = None
        else:
            if self.current_char == "(":
                self.current_token = "("
                self.next_char()
            elif self.current_char == ")":
                if self.get_next_char() is not None and (self.get_next_char().isalpha() or self.get_next_char() == "("):
                    self.regex = self.regex[:self.pos + 1] + "-" + self.regex[self.pos + 1:]

                self.current_token = ")"
                self.next_char()
            elif self.get_next_char() in {"?", "+", "*"}:
                if self.get_next_char() == "?":
                    self.current_token = QuestionMark(Token(self.current_char))
                elif self.get_next_char() == "+":
                    self.current_token = Plus(Token(self.current_char))
                elif self.get_next_char() == "*":
                    self.current_token = Star(Token(self.current_char))

                self.next_char()

                if self.get_next_char() is not None and self.get_next_char() not in {"|", "-", ")", "+", "*", "?"}:
                    self.regex = self.regex[:self.pos + 1] + "-" + self.regex[self.pos + 1:]

                self.next_char()
            elif self.current_char in {"|", "-"}:
                self.current_token = self.current_char
                self.next_char()
            elif self.get_next_char() is not None and self.get_next_char() not in {"|", "-", ")", "+", "*", "?"}:
                self.regex = self.regex[:self.pos + 1] + "-" + self.regex[self.pos + 1:]
                self.current_token = Token(self.current_char) if self.current_char.isalpha() else self.current_char
                self.next_char()
            else:
                self.current_token = Token(self.current_char) if self.current_char.isalpha() else self.current_char
                self.next_char()


class Parser:
    def __init__(self, alphabet, regex):
        self.tokenizer = Tokenizer(alphabet, regex)
        self.expression_tree = None
        self.num_concats = 0

    def get_precedence(self, operator):
        if operator == "-":
            return 2
        elif operator == "|":
            return 1

        return 0

    def apply_unary_operator(self, a, operator):
        if operator == "?":
            return QuestionMark(a)
        elif operator == "+":
            return Plus(a)
        elif operator == "*":
            return Star(a)

        return None

    def apply_binary_operator(self, a, b, operator):
        if operator == "|":
            return Union(a, b)
        elif operator == "-":
            return Concat(a, b)

        return None

    def parse(self):
        expression_stk = []
        operator_stk = []

        while self.tokenizer.current_token is not None:
            # print(self.tokenizer.current_token, expression_stk, operator_stk)
            if isinstance(self.tokenizer.current_token, Token) or \
                    isinstance(self.tokenizer.current_token, QuestionMark) or \
                    isinstance(self.tokenizer.current_token, Star) or \
                    isinstance(self.tokenizer.current_token, Plus):
                expression_stk.append(self.tokenizer.current_token)
            elif self.tokenizer.current_token == "(":
                operator_stk.append("(")
            elif self.tokenizer.current_token == ")":
                while len(operator_stk) > 0 and operator_stk[-1] != "(":
                    op = operator_stk.pop()

                    if op in {"?", "+", "*"}:
                        expression_stk.append(self.apply_unary_operator(expression_stk.pop(), op))
                    else:
                        b, a = expression_stk.pop(), expression_stk.pop()
                        expression_stk.append(self.apply_binary_operator(a, b, op))

                operator_stk.pop()
            elif self.tokenizer.current_token in {"|", "-"}:
                self.num_concats += 1
                while len(operator_stk) > 0 and self.get_precedence(operator_stk[-1]) >= self.get_precedence(
                        self.tokenizer.current_token):
                    op = operator_stk.pop()

                    if op in {"?", "+", "*"}:
                        expression_stk.append(self.apply_unary_operator(expression_stk.pop(), op))
                    else:
                        b, a = expression_stk.pop(), expression_stk.pop()
                        expression_stk.append(self.apply_binary_operator(a, b, op))

                operator_stk.append(self.tokenizer.current_token)
            elif self.tokenizer.current_token in {"?", "+", "*"}:
                expression_stk.append(self.apply_unary_operator(expression_stk.pop(), self.tokenizer.current_token))

            self.tokenizer.advance()

        while len(operator_stk) > 0:
            op = operator_stk.pop()

            if op in {"?", "+", "*"}:
                expression_stk.append(self.apply_unary_operator(expression_stk.pop(), op))
            else:
                b, a = expression_stk.pop(), expression_stk.pop()
                expression_stk.append(self.apply_binary_operator(a, b, op))

        self.expression_tree = expression_stk[-1] if len(expression_stk) > 0 else RegEx.EPSILON


class Compiler:
    def __init__(self, alphabet, regex):
        parser = Parser(alphabet, regex)
        parser.parse()

        self.alphabet = alphabet
        self.parsed_regex = parser.expression_tree
        self.dfa = collections.defaultdict(dict)
        self.final_states = []

    def compilation_helper(self, curr_regex):
        start = self.parsed_regex
        states = {start}
        pseudo_dfa = collections.defaultdict(dict)
        pseudo_dfa[start] = {}
        expression_stk = [self.parsed_regex]

        while len(expression_stk) > 0:
            state = expression_stk.pop()

            for letter in alphabet:
                next_state = state.brzozowski_derivative(letter)

                if state != RegEx.NULL:
                    if next_state not in states:
                        states.add(state)

                        if state == RegEx.EPSILON:
                            pseudo_dfa[state] = {}

                        expression_stk.append(next_state)

                    if next_state != RegEx.NULL:
                        pseudo_dfa[state][letter] = next_state

        return pseudo_dfa

    def compile(self):
        pseudo_dfa = self.compilation_helper(self.parsed_regex)
        keys = list(pseudo_dfa.keys())

        for i, state in enumerate(pseudo_dfa):
            if len(pseudo_dfa[state]) == 0:
                self.dfa[i] = {}
            else:
                for connection in pseudo_dfa[state]:
                    self.dfa[i][connection] = keys.index(pseudo_dfa[state][connection])

        for state in pseudo_dfa:
            if state.epsilon_aux() == RegEx.EPSILON:
                self.final_states.append(keys.index(state))
        # self.final_states = [3, 2]

    def matches(self, string):
        state = 0

        for letter in string:
            if letter not in self.dfa[state]:
                return False

            state = self.dfa[state][letter]

        return state in self.final_states

    def print_transition_table(self):
        print("*\t\t" + "\t\t".join([letter for letter in self.alphabet]))

        for state in self.dfa:
            row = str(state) + "\t"

            for letter in self.alphabet:
                row += "\t" + str(self.dfa[state][letter]) + "\t" if letter in self.dfa[state] else "\t_\t"

            print(row)

        print("Final:", self.final_states)


RegEx.EPSILON = Epsilon()
RegEx.NULL = Token(None)

alphabet = ["a", "b"]
regex = "a|(ab|b*a)*"

print(regex)

compiler = Compiler(alphabet, regex)
compiler.compile()
compiler.print_transition_table()

with open("../dfa_ex_tests.txt") as file:
    tests = [line.strip() for line in file]

for test in tests:
    print(compiler.matches(test), test)