from graph import *
from node import *
from segment import *

def test():
    # Crear el grafo
    g = Graph()

    # Crear nodos (agentes)
    nodeA = Node('A', 0, 0)
    nodeB = Node('B', 2, 3)
    nodeC = Node('C', 5, 1)
    nodeD = Node('D', 7, 5)

    # Añadir nodos al grafo
    g.AddNode(nodeA)
    g.AddNode(nodeB)
    g.AddNode(nodeC)
    g.AddNode(nodeD)

    # Añadir segmentos (conexiones) entre los nodos
    g.AddSegment('A', 'B')
    g.AddSegment('B', 'C')
    g.AddSegment('C', 'D')

    # Mostrar el grafo completo
    g.Plot()

    # Mostrar el grafo de un nodo específico (por ejemplo, el nodo 'C' y sus vecinos)
    g.PlotNode(g, 'C')  # Aquí debes pasar el grafo 'g' junto con el nombre del nodo.

    # Obtener el nodo más cercano a unas coordenadas (por ejemplo, (3, 2))
    closest_node = g.GetClosest(3, 2)  # Ya no es necesario pasar 'g' aquí.
    print(f'El nodo más cercano a (3, 2) es: {closest_node.name}')

def CreateGraph_2():
    # Crear un grafo personalizado
    g2 = Graph()

    # Crear nodos
    nodeX = Node('X', 1, 2)
    nodeY = Node('Y', 4, 5)
    nodeZ = Node('Z', 6, 7)

    # Añadir nodos al grafo
    g2.AddNode(nodeX)
    g2.AddNode(nodeY)
    g2.AddNode(nodeZ)

    # Añadir segmentos entre los nodos
    g2.AddSegment('X', 'Y')
    g2.AddSegment('Y', 'Z')

    # Mostrar el grafo completo
    g2.Plot()

    # Mostrar el grafo de un nodo específico (por ejemplo, el nodo 'Y' y sus vecinos)
    g2.PlotNode(g2, 'Y')  # Aquí también debes pasar el grafo 'g2'

# Llamar a las funciones de test y crear un nuevo grafo
test()
CreateGraph_2()
