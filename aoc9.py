from itertools import groupby

file_path = "data/disk_fragmenter.txt"
ex = "2333133121414131402"


def parse_file(file):

    id_num = 0
    free = False
    seq = []

    for e in file.rstrip():
        # for e in ex:
        if free:
            seq.extend(["."] * int(e))
        else:
            seq.extend([str(id_num)] * int(e))
            id_num += 1

        free = not free

    return seq


def refragment(seq):

    last_idx = -1
    finish = False

    for idx, _ in enumerate(seq):
        while seq[idx] == ".":

            if idx == (len(seq) + last_idx):
                finish = True
                break

            if seq[last_idx] != ".":
                seq[idx], seq[last_idx] = seq[last_idx], "."
            else:
                last_idx -= 1

        if finish:
            break

    return seq


def refragment_by_block(seq):

    # Get all groups of same numbers
    cleaned_seq = [i for i in seq if i != "."]
    groups = [list(g[1]) for g in groupby(cleaned_seq)]
    groups.reverse()

    count = False

    # For each of these groups
    for g in groups:
        for i, _ in enumerate(seq):
            if seq[i] == "." and not count:
                start = i
                count = True

            elif seq[i] != "." and count:
                count = False

                # If I've found a group that fits in the empty space
                if len(g) <= (i - start):

                    start_g = seq.index(g[0])
                    end_g = start_g + len(g)

                    if start_g < start:
                        continue

                    # Swap the group with the empty space
                    seq[start : start + len(g)] = g
                    seq[start_g:end_g] = ["."] * len(g)

                    break

    return seq


#################### TASK 1 ####################

with open(file_path, "r") as file:
    seq = parse_file(file.read())

seq = refragment(seq)
result = sum([i * int(e) for i, e in enumerate(seq) if e != "."])
print(result)


#################### TASK 2 ####################

with open(file_path, "r") as file:
    seq = parse_file(file.read())

seq = [int(e) if e != "." else "." for e in seq]
seq = refragment_by_block(seq)
result = sum([i * int(e) for i, e in enumerate(seq) if e != "."])
print(result)
