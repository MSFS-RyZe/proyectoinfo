from segment import *

n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)
n3 = Node("C", 6, 8)

s1 = Segment("AB", n1, n2)
s2 = Segment("BC", n2, n3)

print(s1.__dict__)
print(s2.__dict__)
