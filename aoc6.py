import numpy as np

file_path = "data/guard_patrol.txt"
ex = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def is_inside(a, b, mat):
    return 0 <= a < mat.shape[0] and 0 <= b < mat.shape[1]


def is_wall(a, b, mat):
    return mat[a, b] == "#"


def update_pos(proposal, g, g_pos, guard_out, mat):

    turns_dic = {"^": ">", "v": "<", "<": "^", ">": "v"}

    if is_inside(*proposal, mat):
        if not is_wall(*proposal, mat):
            g_pos = proposal
        else:
            g = turns_dic[g]

    else:
        guard_out = False

    return g_pos, g, guard_out


def simulate_patrol(mat, g, g_pos, guard_out):

    if g == "^":
        proposal = (g_pos[0] - 1, g_pos[1])
        g_pos, g, guard_out = update_pos(proposal, g, g_pos, guard_out, mat)
    elif g == ">":
        proposal = (g_pos[0], g_pos[1] + 1)
        g_pos, g, guard_out = update_pos(proposal, g, g_pos, guard_out, mat)
    elif g == "v":
        proposal = (g_pos[0] + 1, g_pos[1])
        g_pos, g, guard_out = update_pos(proposal, g, g_pos, guard_out, mat)
    elif g == "<":
        proposal = (g_pos[0], g_pos[1] - 1)
        g_pos, g, guard_out = update_pos(proposal, g, g_pos, guard_out, mat)

    mat[g_pos[0], g_pos[1]] = "X"

    return mat, g, g_pos, guard_out


#################### TASK 1 ####################

mat = []

with open(file_path, "r") as file:
    for line in file.read().splitlines():
        # for line in ex.splitlines():
        mat.append([e for e in line])

mat = np.array(mat)

for g in ["^", "v", "<", ">"]:
    if np.where(mat == g):
        g_pos = np.where(mat == g)
        g_pos = (g_pos[0][0], g_pos[1][0])
        break

mat_sol = mat.copy()
mat_sol[g_pos[0], g_pos[1]] = "X"
guard_out = True

while guard_out:
    mat_sol, g, g_pos, guard_out = simulate_patrol(
        mat_sol, g, g_pos, guard_out
    )

print(np.count_nonzero(mat_sol == "X"))

#################### TASK 2 ####################
##### SUPER MEGA NOT OPTIMIZED FOR TIME LOL ####

result = 0

for init_g in ["^", "v", "<", ">"]:
    if np.where(mat == init_g):
        g_pos = np.where(mat == init_g)
        init_g_pos = (g_pos[0][0], g_pos[1][0])
        break

for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):

        new_mat = mat.copy()

        if mat[i, j] == ".":
            new_mat[i, j] = "#"

            n_iters = 0
            guard_out = True
            g = init_g
            g_pos = init_g_pos

            while guard_out:
                new_mat, g, g_pos, guard_out = simulate_patrol(
                    new_mat, g, g_pos, guard_out
                )

                n_iters += 1
                if n_iters > 10000:
                    result += 1
                    break

print(result)
