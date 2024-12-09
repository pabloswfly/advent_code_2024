import numpy as np
from itertools import combinations

file_path = "data/antennas.txt"
ex = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def count_antinodes(a, b, result, antinodes):

    diff = np.subtract(a, b)

    anti_a = np.add(a, diff).tolist()
    anti_b = np.subtract(b, diff).tolist()

    if is_inside(*anti_a, mat) and anti_a not in antinodes:
        antinodes.append(anti_a)
        result += 1

    if is_inside(*anti_b, mat) and anti_b not in antinodes:
        antinodes.append(anti_b)
        result += 1

    return result, antinodes


def count_antinodes_expanded(a, b, result, antinodes, mat):

    diff = np.subtract(a, b)
    anti_a_found = True
    anti_b_found = True

    while anti_a_found or anti_b_found:

        anti_a = np.add(a, diff).tolist()
        anti_b = np.subtract(b, diff).tolist()

        if is_inside(*anti_a, mat):
            if anti_a not in antinodes:
                antinodes.append(anti_a)
                result += 1
                mat_plot[anti_a[0], anti_a[1]] = "#"
        else:
            anti_a_found = False

        if is_inside(*anti_b, mat):
            if anti_b not in antinodes:
                antinodes.append(anti_b)
                result += 1
                mat_plot[anti_b[0], anti_b[1]] = "#"
        else:
            anti_b_found = False

        a = np.array(anti_a)
        b = np.array(anti_b)

    return result, antinodes


def is_inside(a, b, mat):
    return 0 <= a < mat.shape[0] and 0 <= b < mat.shape[1]


def is_empty(a, b, mat):
    return mat[a, b] == "."


#################### TASK 1 ####################

mat = []

with open(file_path, "r") as file:
    for line in file.read().splitlines():
        # for line in ex.splitlines():
        mat.append([e for e in line])

mat = np.array(mat)
antinodes = []
result = 0

for e in np.unique(mat):

    if e == ".":
        continue

    print(f"Element: {e}")

    occurrences = list(zip(*np.where(mat == e)))
    for a, b in combinations(occurrences, 2):
        result, antinodes = count_antinodes(a, b, result, antinodes)


print(result)


#################### TASK 2 ####################

antinodes = []
mat_plot = mat.copy()

for e in np.unique(mat):

    if e == ".":
        continue

    print(f"Element: {e}")

    occurrences = list(zip(*np.where(mat == e)))
    for a, b in combinations(occurrences, 2):
        result, antinodes = count_antinodes_expanded(
            a, b, result, antinodes, mat_plot
        )

    for occ in occurrences:
        if occ not in antinodes:
            result += 1
            mat_plot[occ[0], occ[1]] = "#"

print(mat_plot)
print(np.count_nonzero(mat_plot == "#"))
