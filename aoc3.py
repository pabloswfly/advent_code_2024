import re

file_path = "data/mul_corrupt.txt"

#################### TASK 1 ####################

result = 0

with open(file_path, "r") as file:

    for line in [l.rstrip() for l in file]:
        mul = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line)
        mul = [(int(x), int(y)) for x, y in mul]
        result += sum([x * y for x, y in mul])

print(result)


#################### TASK 12 ####################

result = 0
record = True

with open(file_path, "r") as file:

    for line in [l.rstrip() for l in file]:
        re_match = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"

        mul = re.findall(re_match, line)
        mul = [x[0] for x in mul]

        for p in mul:
            if p == "do()":
                record = True
            elif p == "don't()":
                record = False
            elif record:
                nums = [int(x) for x in re.findall(r"\d{1,3}", p)]
                result += nums[0] * nums[1]

print(result)
