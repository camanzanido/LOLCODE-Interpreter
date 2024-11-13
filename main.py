import re

file = open("input.txt", "r")
lines = file.readlines()

for line in lines:
    print(line, end="")