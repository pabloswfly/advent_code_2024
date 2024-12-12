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


def is_touching(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def is_touching_group(group, v):
    for g in group:
        if is_touching(g, v):
            return True
    return False


def merge_groups(groups):
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            if any(is_touching_group(groups[i], v) for v in groups[j]):
                groups[i].extend(groups[j])
                groups[j] = []
    # Remove empty groups
    groups = [g for g in groups if g]
    return groups


def instantiate_groups(idxs):

    groups = [[idxs[0]]]

    for idx in idxs[1:]:
        for i, group in enumerate(groups):
            if is_touching_group(group, idx):
                group.append(idx)
                break
        else:
            groups.append([idx])

    return groups


#################### TASK 1 ####################

mat = []
with open(file_path, "r") as file:
    # for line in file.read().splitlines():
    for line in ex4.splitlines():
        mat.append([e for e in line])

mat = np.array(mat)
result = 0

for plot in np.unique(mat):

    plot_indeces = list(zip(*np.where(mat == plot)))
    groups = instantiate_groups(plot_indeces)

    # Merge groups that are touching together
    prev_groups = []
    while groups != prev_groups:
        prev_groups = groups
        groups = merge_groups(groups)

    # Compute the total cost for a certain plot
    for g in groups:
        area = len(g)
        perim = 4 * area - sum([int(is_touching(j, i)) for i in g for j in g])
        result += perim * area

print(result)

#################### TASK 2 ####################

result = 0


def count_edges_by_row(plot, mat):

    n_edges = 0

    prev_idxs = np.where(mat[0] == plot)[0]

    for i in range(1, mat.shape[0] + 1):

        if i == mat.shape[0]:
            idxs = []
        else:
            idxs = np.where(mat[i] == plot)[0]

        # If this row is empty, and the previous row is not, we have two edges
        if len(idxs) == 0:
            if len(prev_idxs) > 0:
                n_edges += 2
                prev_idxs = idxs

            continue
        # Else, if the previous row is empty, we continue
        elif len(prev_idxs) == 0:
            prev_idxs = idxs
            continue

        print(idxs)
        spaces = [y - x - 1 for x, y in zip(idxs[:-1], idxs[1:])]
        print("spaces: ", spaces)

        # If there are differences among rows
        if len(prev_idxs) != len(idxs):
            if min(idxs) != min(prev_idxs):
                n_edges += 1
            if max(idxs) != max(prev_idxs):
                n_edges += 1

        prev_idxs = idxs

    return n_edges


for plot in np.unique(mat):

    print(plot)

    plot_indeces = list(zip(*np.where(mat == plot)))
    groups = instantiate_groups(plot_indeces)

    # Merge groups that are touching together
    prev_groups = []
    while groups != prev_groups:
        prev_groups = groups
        groups = merge_groups(groups)

    # Compute the total cost for a certain plot
    for g in groups:
        area = len(g)

        rows = np.array([n[0] for n in g])
        cols = np.array([n[1] for n in g])

        n_edges_row = count_edges_by_row(plot, mat)
        n_edges_col = count_edges_by_row(plot, mat.T)
        print(n_edges_row, n_edges_col)

        perim = n_edges_row + n_edges_col
        result += perim * area

print(result)
