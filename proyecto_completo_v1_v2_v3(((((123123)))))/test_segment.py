from node import *
from segment import *

n1 = Node('A', 0, 0)
n2 = Node('B', 3, 4)
s = Segment('S1', n1, n2)
print(s.name, s.origin.name, s.destination.name, s.cost)  # should print S1 A B 5.0
