from path import *
from node import Node
from graph import *

# Crear nodos para pruebas
n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)
n3 = Node("C", 6, 8)
n4 = Node("D", 10, 10)

# Crear un path y añadir nodos
p = Path()
AddNodeToPath(p, n1)
AddNodeToPath(p, n2)
AddNodeToPath(p, n3)

print("Path nodes:", [n.name for n in p.nodes])
print("Total path cost:", p.cost)
print("Contains B:", ContainsNode(p, n2))
print("Contains D:", ContainsNode(p, n4))
print("Cost to B:", CostToNode(p, n2))
print("Cost to D (not in path):", CostToNode(p, n4))

# Visualizar usando una clase Graph mínima
class DummyGraph:
    def __init__(self):
        self.nodes = [n1, n2, n3, n4]
        self.segments = []

g = DummyGraph()
PlotPath(g, p)
