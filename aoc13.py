import numpy as np


file_path = "data/claw_machines.txt"
ex = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


def process_text(file):

    machines = []
    mach = {}

    for line in file.split("\n"):

        if line in ["", " "]:
            machines.append(mach)
            mach = {}
            continue

        if line.startswith("Button"):
            button, coords = line.split(": ")
            x, y = coords.split(", ")
            mach[button.split(" ")[1]] = np.array(
                [
                    int(x.split("+")[1]),
                    int(y.split("+")[1]),
                ]
            )

        elif line.startswith("Prize"):
            x, y = line.split(": ")[1].split(", ")
            mach["Prize"] = np.array(
                [int(x.split("=")[1]), int(y.split("=")[1])]
            )

    machines.append(mach)

    return machines


# Solution inspired in the following post:
"""
// n_a * a1 + n_b * b1 = p1
// n_a * a2 + n_b * b2 = p2
// <=>
// n_a * a1 * b2 + n_b * b1 * b2 = p1 * b2
// n_a * a2 * b1 + n_b * b1 * b2 = p2 * b1
// n_b * b1 * b2 = p2 * b1 - n_a * a2 * b1
// <=>
// by substituting the last left term on the first equation:
// n_a * a1 * b2 - n_a * a2 * b1 = p1 * b2 - p2 * b1
// n_a * (a1 * b2 - a2 * b1) = p1 * b2 - p2 * b1
// n_a = (p1 * b2 - p2 * b1) / (a1 * b2 - a2 * b1)
// <=>
// and similary:
// n_b = (p1 * a2 - p2 * a1) / (a2 * b1 - a1 * b2)
"""


def solve(m):

    a1, a2 = m["A"]
    b1, b2 = m["B"]
    p1, p2 = m["Prize"]

    n_a = (p1 * b2 - p2 * b1) // (a1 * b2 - b1 * a2)
    n_b = (p1 * a2 - p2 * a1) // (a2 * b1 - a1 * b2)

    if a1 * n_a + b1 * n_b == p1 and a2 * n_a + b2 * n_b == p2:
        return 3 * n_a + n_b
    else:
        return 0


#################### TASK 1 ####################

with open(file_path, "r") as file:
    machines = process_text(file.read())
    # machines = process_text(ex)


cost = {"A": 3, "B": 1}
total_cost = 0

for m in machines:
    for i in range(101):
        for j in range(101):
            if np.array_equal(m["A"] * i + m["B"] * j, m["Prize"]):
                total_cost += i * cost["A"] + j * cost["B"]
                break

print(total_cost)

#################### TASK 2 ####################

a_lot = 10000000000000
total_cost = 0

for m in machines:
    m["Prize"] = m["Prize"] + a_lot
    total_cost += solve(m)

print(total_cost)
