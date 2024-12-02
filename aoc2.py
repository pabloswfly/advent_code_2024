file_path = "data/levels.txt"


def is_ascending(l):
    for i in range(1, len(l)):
        if l[i - 1] >= l[i] or abs(l[i - 1] - l[i]) > 3:
            return False
    return True


def is_descending(l):
    for i in range(1, len(l)):
        if l[i - 1] <= l[i] or abs(l[i - 1] - l[i]) > 3:
            return False
    return True


#################### TASK 1 ####################

count = 0

with open(file_path, "r") as file:

    levels = [l.rstrip() for l in file]

    for lev in levels:
        int_lev = [int(n) for n in lev.split(" ")]

        if is_ascending(int_lev) or is_descending(int_lev):
            count += 1

print(count)


#################### TASK 12 ####################

count = 0

with open(file_path, "r") as file:

    levels = [l.rstrip() for l in file]

    for lev in levels:
        int_lev = [int(n) for n in lev.split(" ")]

        for i, _ in enumerate(int_lev):

            comb = int_lev[:i] + int_lev[i + 1 :]

            if is_ascending(comb) or is_descending(comb):
                count += 1
                break

print(count)
