
b = Board(0, 0)

b.state[0, 0] = 3
b.state[0, 2] = 1
# b.state[0, 0] = 0
# b.state[2, 2] = 2
# b.state[0, 1] = 1

print(b)

#print(MT(b))
print(CB(b))
