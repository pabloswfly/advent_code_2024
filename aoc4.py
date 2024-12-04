import numpy as np

file_path = "data/xmas.txt"

#################### TASK 1 ####################


def check_xmas(l, result):

    for i in range(0, len(l) - 3):
        x = "".join(l[i : i + 4])
        if x == "XMAS" or x == "SAMX":
            result += 1

    return result


def get_diagonals(mat):

    diags = []
    rows, cols = mat.shape

    # Top-left to bottom-right diagonals
    for d in range(-rows + 1, cols):
        diags.append(mat.diagonal(d))

    # Top-right to bottom-left diagonals
    flipped_mat = np.fliplr(mat)
    for d in range(-rows + 1, cols):
        diags.append(flipped_mat.diagonal(d))

    return diags


mat = []
result = 0

with open(file_path, "r") as file:
    for line in [l.rstrip() for l in file]:
        mat.append([x for x in line])

mat = np.array(mat)

for row in mat:
    result = check_xmas(row, result)
for col in mat.T:
    result = check_xmas(col, result)

# Check diagonals
for diag in get_diagonals(mat):
    result = check_xmas(diag, result)

print(result)


#################### TASK 12 ####################


def check_mas(l):

    for i in range(0, len(l) - 2):
        x = "".join(l[i : i + 3])
        if x == "MAS" or x == "SAM":
            return 1

    return 0


result = 0

# Check only diagonals this time
for i in range(0, mat.shape[0] - 2):
    for j in range(0, mat.shape[1] - 2):
        submat = mat[i : i + 3, j : j + 3]

        n_sam_diags = sum([check_mas(diag) for diag in get_diagonals(submat)])
        if n_sam_diags == 2:
            result += 1

print(result)
