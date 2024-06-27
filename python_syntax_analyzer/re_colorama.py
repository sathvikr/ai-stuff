import re
import sys

from colorama import init, Back

def get_flag(flag):
    if flag == "i":
        return re.I
    if flag == "m":
        return re.M
    if flag == "s":
        return re.S
    if flag == "u":
        return re.U


def compile_regex(pseudo_regex):
    pattern = re.match(r"^[/].*[/]", pseudo_regex)
    flag_str = pseudo_regex[len(pattern.group()):]
    flags = 0

    for flag in flag_str:
        flags |= get_flag(flag)

    return re.compile(pattern.group()[1:len(pattern.group()) - 1], flags=flags)


init()
text = "While inside they wined and dined, safe from the howling wind.\n" \
       "And she whined, it seemed, for the 100th time, into the ear of her friend,\n" \
       "Why indeed should I wind the clocks up, if they all run down in the end?"

regex = compile_regex(sys.argv[1])
matches = [match for match in re.finditer(regex, text)]
colors = (Back.CYAN, Back.YELLOW)
color = colors[0]
shift = 0

for i, match in enumerate(matches):
    span = match.span()

    if i > 0 and matches[i - 1].span()[1] == span[0]:
        color = colors[1] if color == colors[0] else colors[0]

    text = text[:span[0] + shift] + color + match.group() + Back.RESET + text[span[1] + shift:]
    shift += 10

print(text)
