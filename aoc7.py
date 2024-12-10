from itertools import product
import operator as op

file_path = "data/calibration_equations.txt"
ex = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def apply_operations(vals, ops):
    result = vals[0]
    for val, this_op in zip(vals[1:], ops):
        result = this_op(result, val)
    return result


def concatenation(a, b):
    return int(str(a) + str(b))


def generate_all_operations(n):
    return product([op.add, op.mul], repeat=n - 1)


def generate_all_operations_extended(n):
    return product([op.add, op.mul, concatenation], repeat=n - 1)


#################### TASK 1 ####################

eqs = {}
result = 0

with open(file_path, "r") as file:
    for line in file.read().splitlines():
        # for line in ex.splitlines():
        parts = line.split(": ")
        eqs[int(parts[0])] = list(map(int, parts[1].split()))

for k, v in eqs.items():
    for ops in generate_all_operations(len(v)):
        if apply_operations(v, ops) == k:
            result += k
            break

print(result)

#################### TASK 2 ####################

result = 0

for k, v in eqs.items():
    for ops in generate_all_operations_extended(len(v)):
        if apply_operations(v, ops) == k:
            result += k
            break

print(result)
