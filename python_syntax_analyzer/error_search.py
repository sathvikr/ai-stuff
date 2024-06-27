import re

IDENTIFIER = r"[a-zA-Z_]\w*"
FUNCTION = IDENTIFIER + r" *\("

test_file = "error_example.py"
keywords = {"if", "else", "for", "while", "print"}
function_set = set()
variable_set = set()

errors = [
    [],
    [],
    [],
    [],
    []
]

error_messages = ["Variable starting with digit",
                  "Undeclared variable on lines",
                  "= instead of == on lines",
                  "== instead of = on lines",
                  "Undefined function on lines"]


def check_illegal_var_error(line_number, line):
    if re.search(r"\b[0-9]\w+", line) is not None:
        errors[0].append(line_number)


def check_undeclared_var_error(line_number, line):
    matches = re.findall(r"\b" + IDENTIFIER + r"\." + FUNCTION, line)

    for match in matches:
        result = match[:match.index(".")].strip()

        if result not in variable_set and result not in keywords:
            errors[1].append(line_number)


def declare_var(line):
    match = re.match(IDENTIFIER + r" *= *.", line)

    if match is not None:
        variable_set.add(match.group()[:match.group().index("=")].strip())


def check_equality_error_a(line_number, line):
    if re.search(r"(if|elif|while|return|([a-zA-Z]\w* *=)) *[ (] *\w+ = ", line) is not None:
        errors[2].append(line_number)


def check_equality_error_b(line_number, line):
    if re.match(r" *\b" + IDENTIFIER + r" *==", line) is not None:
        errors[3].append(line_number)


def check_undefined_function_error(line_number, line):
    matches = re.findall(r"\b" + FUNCTION, line)

    for match in matches:
        result = match[:-1].strip()

        if result not in function_set and result not in keywords:
            errors[4].append(line_number)


def declare_function(line):
    match = re.match(r"def " + IDENTIFIER, line)

    if match is not None:
        function_set.add(match.group().split()[1])


with open(test_file) as file:
    line_list = [line.rstrip() for line in file]

for line_number, line in enumerate(line_list):
    declare_var(line)
    declare_function(line)

    check_illegal_var_error(line_number + 1, line)
    check_equality_error_a(line_number + 1, line)
    check_equality_error_b(line_number + 1, line)
    check_undeclared_var_error(line_number + 1, line)
    check_undefined_function_error(line_number + 1, line)

for i in range(len(errors)):
    print(error_messages[i], "on lines", errors[i])
