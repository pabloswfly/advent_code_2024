import numpy as np

np.set_printoptions(threshold=np.inf, linewidth=210)


file_path = "data/robots.txt"
ex = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


def process_text(file):

    robots = []

    for line in file.split("\n"):

        p, v = [l.split("=")[1] for l in line.split(" ")]
        p = np.array([int(p.split(",")[0]), int(p.split(",")[1])])
        v = np.array([int(v.split(",")[0]), int(v.split(",")[1])])

        robots.append([p, v])

    return robots


def correct_pos(p, limits):
    if p[0] >= limits[1]:
        p[0] -= limits[1]
    elif p[0] < 0:
        p[0] += limits[1]
    if p[1] < 0:
        p[1] += limits[0]
    elif p[1] >= limits[0]:
        p[1] -= limits[0]
    return p


def simulate_robot(r, n, limits):

    for _ in range(n):
        r[0] = correct_pos(r[0] + r[1], limits)

    return r[0]


def simulate_second(robots, limits):

    for r in robots:
        r[0] = correct_pos(r[0] + r[1], limits)

    return robots


def count_non_zero_neighbor(mat, coor):

    row, col = coor

    row_min = max(0, row - 1)
    row_max = min(mat.shape[0], row + 2)
    col_min = max(0, col - 1)
    col_max = min(mat.shape[1], col + 2)

    # Extract the neighborhood
    neighs = mat[row_min:row_max, col_min:col_max]

    return np.count_nonzero(neighs) - (mat[row, col] != 0)


#################### TASK 1 ####################

with open(file_path, "r") as file:
    robots = process_text(file.read())
    limits = (103, 101)
    # robots = process_text(ex)
    # limits = (7, 11)

mat = np.zeros(limits, dtype=int)

# Iterate over the robots
for i, r in enumerate(robots):
    p = simulate_robot(r, 100, limits)
    mat[p[1], p[0]] += 1

mids = np.array(mat.shape) // 2
mat = np.delete(mat, mids[0], axis=0)
mat = np.delete(mat, mids[1], axis=1)

result = 1
result *= mat[: mids[0], : mids[1]].sum()
result *= mat[: mids[0], mids[1] :].sum()
result *= mat[mids[0] :, : mids[1]].sum()
result *= mat[mids[0] :, mids[1] :].sum()

print(result)


#################### TASK 2 ####################


with open(file_path, "r") as file:
    robots = process_text(file.read())
    limits = (103, 101)
    # robots = process_text(ex)
    # limits = (7, 11)

# Iterate over the seconds
for i in range(1, 10000):
    robots = simulate_second(robots, limits)
    mat = np.zeros(limits, dtype=int)
    for r in robots:
        mat[r[0][1], r[0][0]] += 1

    result = 0
    for y, x in list(zip(*np.nonzero(mat))):
        result += count_non_zero_neighbor(mat, (y, x))

    # Found this threshold empirically
    if result > 1000:
        print(mat)
        print(result)
        print("Iteration: ", i)
