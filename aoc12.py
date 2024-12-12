from scipy.ndimage import label
import numpy as np


file_path = "data/fences.txt"
ex1 = """AAAA
BBCD
BBCC
EEEC"""

ex2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

ex3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

ex4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

ex5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""


def up(i, j):
    return int(this_mat[i - 1, j] == 0)


def down(i, j):
    return int(this_mat[i + 1, j] == 0)


def left(i, j):
    return int(this_mat[i, j - 1] == 0)


def right(i, j):
    return int(this_mat[i, j + 1] == 0)


def count_edges(mat, g):

    prev_set = set()
    result = 0
    prev_r = []

    for r in mat:

        changes = [abs(r[i] - r[i - 1]) for i in range(1, len(r))]
        this_set = set(np.nonzero(changes)[0])
        common = this_set & prev_set

        for c in common:
            # Check if there's a cross in the fences and count it as one
            if r[c] - r[c + 1] != prev_r[c] - prev_r[c + 1]:
                result += 1

        result += len(this_set - prev_set)
        prev_set = this_set
        prev_r = r

    return result


#################### TASK 1 ####################

mat = []
with open(file_path, "r") as file:
    for line in file.read().splitlines():
        # for line in ex3.splitlines():
        mat.append([e for e in line])

mat = np.array(mat)
result = 0

for plot in np.unique(mat):

    this_mat = mat.copy()

    this_mat[np.where(mat == plot)] = 1
    this_mat[np.where(mat != plot)] = 0
    this_mat = np.pad(this_mat, 1)
    this_mat = this_mat.astype(int)

    labels, n = label(this_mat)

    for g in range(1, n + 1):

        idxs = list(zip(*np.where(labels == g)))
        area = len(idxs)
        perim = 0

        for i in idxs:
            # Check the four neighbors
            perim += np.sum([up(*i), down(*i), left(*i), right(*i)])

        result += perim * area

print(result)

#################### TASK 2 ####################

result = 0

for plot in np.unique(mat):

    this_mat = mat.copy()

    this_mat = (mat == plot).astype(int)
    this_mat = np.pad(this_mat, 1)
    this_mat = this_mat.astype(int)

    labels, n = label(this_mat)

    for g in range(1, n + 1):

        g_mat = (labels == g).astype(int)

        area = np.sum(g_mat)

        perim = 0
        # Horizontally
        perim += count_edges(g_mat, g)
        # Vertically
        perim += count_edges(g_mat.T, g)

        result += perim * area

print(result)
