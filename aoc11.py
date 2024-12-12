from collections import defaultdict
import numpy as np
import time


file_path = "data/stones.txt"
ex = "125 17"


def simulate(n_times, seq):
    for _ in range(n_times):
        new_seq = []

        for val in seq:

            n_digits = len(str(val))

            if val == 0:
                new_seq.append(1)

            elif val >= 10 and n_digits % 2 == 0:

                factor = 10 ** (n_digits // 2)
                new_seq.append(val // factor)
                new_seq.append(val % factor)

            else:
                new_seq.append(val * 2024)

        seq = np.array(new_seq)

    return len(seq)


def simulate_fast(n_times, stones):

    for _ in range(n_times):
        new_stones = defaultdict(int)

        for s, count in stones.items():
            if s == 0:
                new_stones[1] += count
            elif len(str(s)) % 2 == 0:
                s = str(s)
                lh, rh = s[: len(s) // 2], s[len(s) // 2 :]
                new_stones[int(lh)] += count
                new_stones[int(rh)] += count
            else:
                new_stones[s * 2024] += count

        stones = new_stones

    return new_stones


#################### TASK 1 ####################

with open(file_path, "r") as file:
    seq = [int(n) for n in file.read().split(" ")]
    # seq = np.array([int(n) for n in ex.split(" ")])

start = time.time()
print(simulate(35, seq.copy()))
print(time.time() - start)

#################### TASK 2 ####################

stones = {n: 1 for n in seq}

start = time.time()
new_stones = simulate_fast(75, stones)
print(sum(new_stones.values()))
print(time.time() - start)
