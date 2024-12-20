import numpy as np
from queue import PriorityQueue

np.set_printoptions(threshold=np.inf, linewidth=600)

file_path = "data/reindeer.txt"
ex1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

ex2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


def move(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1])


def process_text(file):
    mat = np.array([list(line) for line in file.split("\n")])
    return mat


#################### TASK 1 ####################

with open(file_path, "r") as file:
    # mat = process_text(ex2)
    mat = process_text(file.read())

start = tuple(np.argwhere(mat == "S")[0])
end = tuple(np.argwhere(mat == "E")[0])
dirs = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

queue = PriorityQueue()
# POSITION - COST - DIRECTION - VISITED
queue.put((start, 0, ">", frozenset([start])))

min_cost = float("inf")
tile_cost = {}

while not queue.empty():
    pos, cost, this_dir, visited = queue.get()

    # Advance only routes that are less costy
    if cost > min_cost:
        continue

    # Save minimum cost for each tile
    if tile_cost.get((pos, this_dir), float("inf")) < cost:
        continue
    tile_cost[(pos, this_dir)] = cost

    proposals = [(move(pos, dirs[c]), c) for c in dirs]
    for p, new_dir in proposals:

        if mat[tuple(p)] == "#":
            continue

        new_cost = cost + 1 if new_dir == this_dir else cost + 1001

        if p == end:
            if new_cost < min_cost:
                min_cost = new_cost
                min_paths = set(visited)
            elif new_cost == min_cost:
                min_paths |= visited

        if p not in visited:
            if new_cost < min_cost:
                queue.put((p, new_cost, new_dir, visited | {p}))

print(min_cost)

#################### TASK 2 ####################
# plus one to also count the E cell
print(len(min_paths) + 1)
