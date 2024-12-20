import numpy as np

np.set_printoptions(threshold=np.inf, linewidth=600)

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


def check_if_box(bigmat, pos):

    if bigmat[*pos] == "[":
        other_half = (pos[0], pos[1] + 1)
        return BigBox(pos, other_half, bigmat)

    elif bigmat[*pos] == "]":
        other_half = (pos[0], pos[1] - 1)
        return BigBox(other_half, pos, bigmat)

    return None


class BigBox:
    def __init__(self, pos_left, pos_right, mat):
        self.pos = (pos_left, pos_right)
        self.mat = mat
        self.moved = True

    def _adjacent_pos(self, c):
        """Return adjacent positions based on the direction."""
        return [move(p, dirs[c]) for p in self.pos]

    def _find_boxes(self, positions):
        """Return BigBox instances for given positions if they exist."""
        boxes = [check_if_box(self.mat, p) for p in positions]
        boxes = [b for b in boxes if isinstance(b, BigBox)]
        if len(boxes) > 1 and boxes[0].is_equal(boxes[1]):
            boxes = [boxes[0]]
        return boxes

    def _can_move(self, positions, c):
        """Check if the box can move in the given direction."""
        if any(self.mat[*p] == "#" for p in positions):
            return False
        elif all(self.mat[*p] == "." for p in positions):
            return True

        for other_box in self._find_boxes(positions):
            if not other_box.check_up_down(c):
                return False
        return True

    def check_up_down(self, c):
        """Check if the box can move up or down."""
        positions = self._adjacent_pos(c)
        return self._can_move(positions, c)

    def move_up_down(self, c):
        """Move the box up or down if possible."""
        positions = self._adjacent_pos(c)

        if self._can_move(positions, c):
            for other_box in self._find_boxes(positions):
                other_box.move_up_down(c)
            self.update_mat(positions)
            self.moved = True
        else:
            self.moved = False

    def move_left_right(self, c):
        positions = self._adjacent_pos(c)

        new_pos = [p for p in positions if self.mat[*p] not in ["[", "]"]]
        if new_pos:
            self.moved = self.mat[*new_pos[0]] == "."
            if self.moved:
                self.update_mat(positions)

        else:
            other_pos = (
                move(positions[0], dirs[c])
                if c == "<"
                else move(positions[1], dirs[c])
            )
            other_box = check_if_box(self.mat, other_pos)

            if isinstance(other_box, BigBox):
                other_box.move_left_right(c)
                self.moved = other_box.moved
                if self.moved:
                    self.update_mat(positions)

    def update_mat(self, pos):
        self.mat[*self.pos[0]], self.mat[*self.pos[1]] = [".", "."]
        self.pos = pos
        self.mat[*self.pos[0]], self.mat[*self.pos[1]] = ["[", "]"]

    def is_equal(self, other):
        return self.pos == other.pos


#################### TASK 1 ####################

with open(file_path, "r") as file:
    mat, seq = process_text(file.read())
    # mat, seq = process_text(ex2)

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

boxes = np.argwhere(mat == "O")
result = sum([b[0] * 100 + b[1] for b in boxes])
print(result)

#################### TASK 2 ####################

with open(file_path, "r") as file:
    mat, seq = process_text(file.read())
    # mat, seq = process_text(ex2)

changes = {"#": "##", ".": "..", "O": "[]", "@": "@."}
box_repr = ["[", "]"]

bigmat = []
for i in range(mat.shape[0]):
    line = "".join([changes[mat[i, j]] for j in range(mat.shape[1])])
    bigmat.append(list(line))
bigmat = np.array(bigmat)

prev_pos = np.argwhere(bigmat == "@")[0]
for i, c in enumerate(seq):
    pos = move(prev_pos, dirs[c])

    if bigmat[*pos] != "#":
        box = check_if_box(bigmat, pos)
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

boxes = np.argwhere(bigmat == "[")
result = sum([b[0] * 100 + b[1] for b in boxes])
print(result)
