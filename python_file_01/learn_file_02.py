# t = open("test.txt", "w")
# for i in range(0, 10):
#     t.write("hello world\n")
# t.close()

import os as o
import time as d

with open("test.txt", "r") as t, \
        open("test_copy.txt", "w") as t2:
    for line in t:
        if line.startswith("hello"):
            replace = line.replace("hello", "hi")
            t2.write(replace)
o.remove("test.txt")
o.rename("test_copy.txt", "test.txt")
