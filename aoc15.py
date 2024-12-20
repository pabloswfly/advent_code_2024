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
            other_box.move(move(new_pos, dirs[c]), mark="O")
            self.moved = other_box.moved
            if self.moved:
                self.pos = new_pos

        elif self.mat[*new_pos] == "#":
            self.moved = False

    def update_mat(self, char):
        self.mat[*self.pos] = char


def move(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1])


#################### TASK 1 ####################

with open(file_path, "r") as file:
    # mat, seq = process_text(file.read())
    mat, seq = process_text(ex2)

dirs = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
prev_pos = np.argwhere(mat == "@")[0]

for c in seq:

    pos = move(prev_pos, dirs[c])

    if mat[pos] != "#":
        if mat[pos] == "O":

            box = Box(pos, mat)
            box.move(move(pos, dirs[c]), mark=".")
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
    mat, seq = process_text(file.read())
    # mat, seq = process_text(ex2)

bigmat = np.zeros((mat.shape[0], mat.shape[1] * 2), dtype=str)

changes = {"#": "##", ".": "..", "O": "[]", "@": "@."}

bigmat = []
for i in range(mat.shape[0]):
    line = "".join([changes[mat[i, j]] for j in range(mat.shape[1])])
    bigmat.append(list(line))

bigmat = np.array(bigmat)
print(bigmat)

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
        self.left = pos_left
        self.right = pos_right
        self.mat = mat
        self.moved = True

    def check_up_down(self, c):
        left, right = [move(p, dirs[c]) for p in [self.left, self.right]]
        if any(self.mat[*p] == "#" for p in [left, right]):
            return False
        return True

    def move_up_down(self, c):
        left, right = [move(p, dirs[c]) for p in [self.left, self.right]]

        if any(self.mat[*p] == "#" for p in [left, right]):
            self.moved = False
        else:
            others = [check_if_box(bigmat, p) for p in [left, right]]
            others = [b for b in others if isinstance(b, BigBox)]
            if len(others) > 1 and others[0].is_equal(others[1]):
                others = [others[0]]

            print([(b.left, b.right) for b in others])
            can_be_moved = all(b.check_up_down(c) for b in others)

            if can_be_moved:
                for other_box in others:
                    other_box.move_up_down(c)
                self.moved = True
                self.update_mat(left, right)
            else:
                self.moved = False

    def move_left_right(self, c):
        left, right = [move(p, dirs[c]) for p in [self.left, self.right]]

        new_pos = [p for p in [left, right] if bigmat[*p] not in ["[", "]"]]
        if not new_pos:
            if c == "<":
                other_box = check_if_box(bigmat, move(left, dirs[c]))
            else:
                other_box = check_if_box(bigmat, move(right, dirs[c]))

            other_box.move_left_right(c)
            self.moved = other_box.moved
            if self.moved:
                self.update_mat(left, right)

        elif self.mat[*new_pos[0]] == ".":
            self.update_mat(left, right)
            self.moved = True

        elif self.mat[*new_pos[0]] == "#":
            self.moved = False

    def update_mat(self, left, right):
        self.mat[*self.left], self.mat[*self.right] = [".", "."]
        self.left, self.right = left, right
        self.mat[*self.left], self.mat[*self.right] = ["[", "]"]

    def is_equal(self, other):
        return self.left == other.left and self.right == other.right


prev_pos = np.argwhere(bigmat == "@")[0]

for c in seq:

    pos = move(prev_pos, dirs[c])

    if bigmat[*pos] != "#":
        box = check_if_box(bigmat, pos)
        mark = [".", "."]

        if isinstance(box, BigBox):
            if c in ["<", ">"]:
                box.move_left_right(c)
            else:
                box.move_up_down(c)

            if not box.moved:
                continue

        bigmat[*prev_pos] = "."
        bigmat[*pos] = "@"
        prev_pos = pos
print(bigmat)

boxes = np.argwhere(bigmat == "[")
result = sum([b[0] * 100 + b[1] for b in boxes])
print(result)
