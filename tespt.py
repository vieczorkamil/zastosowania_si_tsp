path = [1, 2, 3, 4, 5, 6, 7, 8, 9]


x1 = 2
x2 = 5
path[x1:x2] = reversed(path[x1:x2])

print(path)