file_path = "data/page_order.txt"

#################### TASK 1 ####################


def process_text(file):

    mode_learn = True
    seqs = []
    orders = []

    for line in file.split("\n"):

        if line in ["", " "]:
            mode_learn = False
            continue

        if mode_learn:
            a, b = line.split("|")
            orders.append([int(a), int(b)])

        else:
            seqs.append([int(x) for x in line.split(",")])

    return seqs, orders


def is_seq_ok(seq, orders):

    for ord in orders:
        if ord[0] in seq and ord[1] in seq:
            if seq.index(ord[0]) > seq.index(ord[1]):
                return False
    return True


result = 0
not_ok_seqs = []

with open(file_path, "r") as file:
    seqs, orders = process_text(file.read())

for seq in seqs:

    if is_seq_ok(seq, orders):
        result += seq[int((len(seq) - 1) / 2)]
    else:
        not_ok_seqs.append(seq)

print(result)


#################### TASK 2 ####################

for seq in not_ok_seqs:

    while not is_seq_ok(seq, orders):
        for ord in orders:
            if ord[0] in seq and ord[1] in seq:

                idx0 = seq.index(ord[0])
                idx1 = seq.index(ord[1])

                if idx0 > idx1:
                    seq[idx0], seq[idx1] = seq[idx1], seq[idx0]

result = sum([seq[int((len(seq) - 1) / 2)] for seq in not_ok_seqs])
print(result)
