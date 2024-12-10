import numpy as np

file_path = "data/trails.txt"
ex = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


def right(a, b):
    return a, b + 1


def left(a, b):
    return a, b - 1


def up(a, b):
    return a - 1, b


def down(a, b):
    return a + 1, b


def is_inside(v, mat):
    return 0 <= v[0] < mat.shape[0] and 0 <= v[1] < mat.shape[1]


#################### TASK 1 ####################

mat = []
with open(file_path, "r") as file:
    for line in file.read().splitlines():
        # for line in ex.splitlines():
        mat.append([int(e) for e in line])

mat = np.array(mat)
result = 0
all_trails = []

# For each starting point, where we have a 0 in the matrix
all_starts = list(zip(*np.where(mat == 0)))
for start in all_starts:

    trails = [[start]]

    for trail in trails:

        # New position is the last element of the trail
        pos = trail[-1]

        # All different movement proposals
        proposals = [right(*pos), left(*pos), up(*pos), down(*pos)]

        # For each proposal, if fulfills requirements, add it as a new possible trail
        for new_pos in proposals:
            if is_inside(new_pos, mat) and mat[new_pos] - mat[pos] == 1:
                trails.append(trail + [new_pos])

    # Extract all trails ending in 9 (peak), and save coordinates of last element
    complete_trails = [t[-1] for t in trails if len(t) == 10]
    all_trails.append([t for t in trails if len(t) == 10])

    # Count number of unique coordinates (unique peaks)
    result += len(list(set((complete_trails))))

print(result)


#################### TASK 2 ####################

result = sum([len(trails) for trails in all_trails])
print(result)
