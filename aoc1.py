file_path = "data/two_lists.txt"

#################### TASK 1 ####################

with open(file_path, "r") as file:

    lists = [l.rstrip() for l in file]
    l1 = [int(l.split("   ")[0]) for l in lists]
    l2 = [int(l.split("   ")[1]) for l in lists]

    l1.sort(reverse=False)
    l2.sort(reverse=False)

    result = sum([abs(x - y) for x, y in zip(l1, l2)])
    print(result)


#################### TASK 2 ####################

with open(file_path, "r") as file:

    lists = [l.rstrip() for l in file]
    l1 = [int(l.split("   ")[0]) for l in lists]
    l2 = [int(l.split("   ")[1]) for l in lists]

    sim = []
    for e in l1:
        n_times = l2.count(e)
        sim.append(n_times * e)

    print(sum(sim))
