import numpy as np

np.set_printoptions(linewidth=100)

file_path = "data/boxes.txt"
ex1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

ex2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


def process_text(file):
    mat = []
    seq = ""
    instructions = False

    for line in file.split("\n"):
        if not line:
            instructions = True
            continue

        if instructions:
            seq += line
        else:
            mat.append(list(line))

    return np.array(mat), seq


def up(i, j):
    return i - 1, j


def down(i, j):
    return i + 1, j


def left(i, j):
    return i, j - 1


def right(i, j):
    return i, j + 1


class Box:
    def __init__(self, pos, mat):
        self.pos = pos
        self.mat = mat
        self.moved = True

    def move(self, new_pos, mark):
        if self.mat[*new_pos] == ".":
            self.update_mat(mark)
            self.pos = new_pos
            self.update_mat("O")
            self.moved = True

        elif self.mat[*new_pos] == "O":
            other_box = Box(new_pos, self.mat)
            other_box.move(dirs[c](*new_pos), mark="O")
            self.moved = other_box.moved
            if self.moved:
                self.pos = new_pos

        elif self.mat[*new_pos] == "#":
            self.moved = False

    def update_mat(self, char):
        self.mat[*self.pos] = char


#################### TASK 1 ####################

with open(file_path, "r") as file:
    # mat, seq = process_text(file.read())
    mat, seq = process_text(ex2)

dirs = {"^": up, "v": down, "<": left, ">": right}
prev_pos = np.argwhere(mat == "@")[0]

for c in seq:

    pos = dirs[c](*prev_pos)

    if mat[*pos] != "#":
        if mat[*pos] == "O":

            box = Box(pos, mat)
            box.move(dirs[c](*pos), mark=".")
            if not box.moved:
                continue

        mat[*prev_pos] = "."
        mat[*pos] = "@"
        prev_pos = pos

print(mat)

boxes = np.argwhere(mat == "O")
result = sum([b[0] * 100 + b[1] for b in boxes])
print(result)

#################### TASK 2 ####################

with open(file_path, "r") as file:
    # mat, seq = process_text(file.read())
    mat, seq = process_text(ex2)

bigmat = np.zeros((mat.shape[0], mat.shape[1] * 2), dtype=str)

changes = {"#": "##", ".": "..", "O": "[]", "@": "@."}

bigmat = []
for i in range(mat.shape[0]):
    line = "".join([changes[mat[i, j]] for j in range(mat.shape[1])])
    bigmat.append(list(line))

bigmat = np.array(bigmat)
print(bigmat)

dirs = {"^": up, "v": down, "<": left, ">": right}
b_list = ["[", "]"]


def check_if_box(bigmat, pos):

    box = None

    if bigmat[*pos] == "[":
        other_half = (pos[0], pos[1] + 1)
        box = BigBox(pos, other_half, bigmat)

    elif bigmat[*pos] == "]":
        other_half = (pos[0], pos[1] - 1)
        box = BigBox(other_half, pos, bigmat)

    return box


class BigBox:
    def __init__(self, pos_left, pos_right, mat):
        self.pos_left = pos_left
        self.pos_right = pos_right
        self.mat = mat
        self.moved = True

    def move_up_down(self, c, mark):
        new_left = dirs[c](*self.pos_left)
        new_right = dirs[c](*self.pos_right)
        cont = True

        if any(self.mat[*p] == "#" for p in [new_left, new_right]):
            self.moved = False
        else:
            other_boxes = [
                check_if_box(bigmat, p) for p in [new_left, new_right]
            ]
            for other_box in other_boxes:
                if isinstance(other_box, BigBox):
                    other_box.move_up_down(c, mark=[".", "."])
                    self.moved = other_box.moved
                    if self.moved:
                        self.update_mat(mark)
                        self.pos_left, self.pos_right = new_left, new_right
                        self.update_mat(b_list)
                        cont = False
            if cont:
                self.update_mat(mark)
                self.pos_left, self.pos_right = new_left, new_right
                self.update_mat(b_list)
                self.moved = True

    def move_left_right(self, c, mark):
        new_left = dirs[c](*self.pos_left)
        new_right = dirs[c](*self.pos_right)
        other_box = check_if_box(bigmat, dirs[c](*new_left))

        if any(self.mat[*p] == "." for p in [new_left, new_right]):
            self.update_mat(mark)
            self.pos_left, self.pos_right = new_left, new_right
            self.update_mat(b_list)
            self.moved = True

        elif isinstance(other_box, BigBox):
            other_box.move_left_right(c, mark=b_list)
            self.moved = other_box.moved
            if self.moved:
                self.pos_left, self.pos_right = new_left, new_right

        elif any(self.mat[*p] == "#" for p in [new_left, new_right]):
            self.moved = False

    def update_mat(self, chars):
        self.mat[*self.pos_left] = chars[0]
        self.mat[*self.pos_right] = chars[1]


ex3 = """##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############"""

mat = []
for line in ex3.split("\n"):
    mat.append(list(line))
bigmat = np.array(mat)

prev_pos = np.argwhere(bigmat == "@")[0]
seq = ["<", "v", "v", "<", "<", "^", "^", "<", "<", "^", "^"]

for c in seq:

    pos = dirs[c](*prev_pos)
    print(c)

    if bigmat[*pos] != "#":
        box = check_if_box(bigmat, pos)

        if isinstance(box, BigBox):
            if c in ["<", ">"]:
                box.move_left_right(c, mark=[".", "."])
            elif c in ["^", "v"]:
                box.move_up_down(c, mark=[".", "."])

            if not box.moved:
                continue

        bigmat[*prev_pos] = "."
        bigmat[*pos] = "@"
        prev_pos = pos
        print(bigmat)
