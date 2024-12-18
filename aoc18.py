import numpy as np
import time

np.set_printoptions(threshold=np.inf, linewidth=600)

file_path = "data/bytes.txt"
ex = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


def up(i, j):
    return i - 1, j


def down(i, j):
    return i + 1, j


def left(i, j):
    return i, j - 1


def right(i, j):
    return i, j + 1


def get_mat(file, shape, bytes):

    mat = np.zeros(shape)

    for line in file.split("\n")[:bytes]:
        a, b = line.split(",")
        mat[int(b), int(a)] = 1

    mat = np.pad(mat, 1, constant_values=1)

    return np.array(mat)


def get_bytes(file):

    bytes = []
    for line in file.split("\n"):
        a, b = line.split(",")
        bytes.append((int(a), int(b)))

    return bytes


def find_path(mat, shape):

    pos_list = [(1, 1)]
    visited = [[(1, 1)]]
    steps = 0

    while True:
        new_pos = []
        for pos in pos_list:

            if tuple(pos) == shape:
                return steps - 1

            for direction in dirs:
                # Get a new position proposal
                prop = tuple(direction(*pos))

                if mat[prop] == 0 and prop not in visited:
                    visited.append(prop)
                    new_pos.append(prop)

        if not new_pos:
            return None

        pos_list = new_pos
        steps += 1


#################### TASK 1 ####################

start = time.time()

with open(file_path, "r") as file:
    shape = (71, 71)
    mat = get_mat(file.read(), shape=shape, bytes=1024)
    # shape = (7, 7)
    # mat = get_bytes(ex, shape=shape, bytes=12)

dirs = [up, down, left, right]

print(find_path(mat, shape))

print(time.time() - start)

#################### TASK 2 ####################

with open(file_path, "r") as file:
    shape = (71, 71)
    bytes = get_bytes(file.read())

mat = np.zeros(shape)
for byte in bytes[:1024]:
    mat[byte] = 1

mat = np.pad(mat, 1, constant_values=1)
mat = np.array(mat)

for i, byte in enumerate(bytes[1024:], 1024):

    mat[byte[0] + 1, byte[1] + 1] = 1
    if not find_path(mat, shape):
        print(",".join(map(str, byte)))
        break
