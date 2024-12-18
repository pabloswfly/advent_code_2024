import numpy as np

np.set_printoptions(threshold=np.inf, linewidth=600)

file_path = "data/program.txt"
ex = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

ex2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


def process_text(file):

    reg = []
    program = False

    for line in file.split("\n"):
        if not line:
            program = True
            continue

        if program:
            prog = [int(n) for n in line.split(": ")[1].split(",")]
        else:
            reg.append(int(line.split(": ")[1]))

    return prog, *reg


def run_program(prog, a):

    p, b, c, out = 0, 0, 0, []

    while p >= 0 and p < len(prog):

        num = prog[p + 1]
        combos = [0, 1, 2, 3, a, b, c, 99999]
        comb = combos[num]

        match prog[p]:
            case 0:
                a = int(a / 2**comb)  # adv
            case 1:
                b = b ^ num  # bxl
            case 2:
                b = comb % 8  # bst
            case 3:
                p = p if a == 0 else num - 2  # jnz
            case 4:
                b = b ^ c  # bxc
            case 5:
                out.append(comb % 8)  # out
            case 6:
                b = int(a / 2**comb)  # bdv
            case 7:
                c = int(a / 2**comb)  # cdv
        p += 2

    return out


# Find a as a recursive function by reverse-engineer the value of a
# such that the program output matches a reversed version of the program


# The function essentially builds the value digit-by-digit in base-8.
def find_a(a=0, depth=0):

    # If the recursion depth matches the length of the program
    if depth == len(prog):
        return a

    for i in range(8):

        # We build a in base-8 (octal-system)
        output = run_program(prog, a * 8 + i)

        if output and output[0] == rev_prog[depth]:
            print(a)
            print(depth)
            if result := find_a((a * 8 + i), depth + 1):
                return result
    return 0


#################### TASK 1 ####################

with open(file_path, "r") as file:
    prog, a, b, c = process_text(file.read())
    # prog, a, b, c = process_text(ex)

result = ",".join(str(n) for n in run_program(prog, a))
print(result)

#################### TASK 2 ####################

# Reverse the program
rev_prog = prog[::-1]

result = find_a()
print(result)
