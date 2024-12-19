from functools import cache
import numpy as np
import time

file_path = "data/towels.txt"
ex = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def process_text(file):

    towels = []
    for i, line in enumerate(file.split("\n")):
        if i == 0:
            patterns = line.split(", ")

        elif i != 1:
            towels.append(line)

    return patterns, towels


@cache
def count_options(towel):

    if not towel:
        return 1

    options = 0

    for p in patterns:
        if towel.startswith(p):
            options += count_options(towel[len(p) :])

    return options


#################### TASK 1 ####################

start = time.time()

with open(file_path, "r") as file:
    patterns, towels = process_text(file.read())
    # patterns, towels = process_text(ex)

result = [count_options(t) for t in towels]

print(np.count_nonzero(result))
print(time.time() - start)

#################### TASK 2 ####################

print(np.sum(result))
