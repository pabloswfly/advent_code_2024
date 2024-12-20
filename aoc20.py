import numpy as np
import time

file_path = "data/race.txt"
ex1 = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def move(pos, delta, times=1):
    for _ in range(times):
        pos = (pos[0] + delta[0], pos[1] + delta[1])
    return pos


def is_inside(p):
    return (
        p[0] >= 0 and p[0] < mat.shape[0] and p[1] >= 0 and p[1] < mat.shape[1]
    )


def process_text(file):
    mat = np.array([list(line) for line in file.split("\n")])
    return mat


def find_path(mat):

    start = tuple(np.argwhere(mat == "S")[0])
    end = tuple(np.argwhere(mat == "E")[0])
    path = [start]

    while True:
        proposals = [move(path[-1], dirs[c]) for c in dirs]
        for p in proposals:
            if mat[tuple(p)] != "#" and p not in path:
                new_pos = p
                break

        path.append(new_pos)
        if new_pos == end:
            break

    return path


def find_cheats(start, path, max_len=20):

    cheats = []
    for start in path:
        pos_list = [start]
        visited = [start]

        for i in range(1, max_len + 1):

            new_pos = []
            for pos in pos_list:
                for c in dirs:
                    prop = tuple(move(pos, dirs[c]))
                    if is_inside(prop):
                        if prop not in visited:
                            visited.append(prop)
                            new_pos.append(prop)
                        if mat[prop] in [".", "E"]:
                            cheats.append((start, prop, i))

            if not new_pos:
                break
            pos_list = new_pos

    return list(set(cheats))


def find_shortcuts(path, cheats, min_len=100):

    times_dic = {}
    for start, end, t in cheats:
        ch = (start, end)
        if ch in times_dic:
            times_dic[ch] = t if t < times_dic[ch] else times_dic[ch]
        else:
            times_dic[ch] = t

    result = 0
    for start, end in times_dic.keys():
        short = path[path.index(start) : path.index(end)]
        if len(short) - times_dic[(start, end)] >= min_len:
            result += 1
    return result


#################### TASK 1 ####################

with open(file_path, "r") as file:
    # mat = process_text(ex1)
    mat = process_text(file.read())

dirs = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

path = find_path(mat)
cheats = find_cheats(mat, path, max_len=2)
result = find_shortcuts(path, cheats, min_len=100)
print(result)


#################### TASK 2 ####################

starting_time = time.time()

cheats = find_cheats(mat, path, max_len=20)
result = find_shortcuts(path, cheats, min_len=100)
print(result)
print("Elapsed time: ", time.time() - starting_time)

"""result = [s for s in shortcuts if s >= 50]
for s in sorted(set(result)):
    print(s, ":    ", result.count(s))"""
