from node import *
from segment import *

# Creamos tres nodos
node1 = Node("A", 0.0, 0.0)  # Nodo A en (0, 0)
node2 = Node("B", 3.0, 4.0)  # Nodo B en (3, 4)
node3 = Node("C", 6.0, 8.0)  # Nodo C en (6, 8)

# Creamos dos segmentos
segment1 = Segment("Segment1", node1, node2)  # Segmento entre A y B
segment2 = Segment("Segment2", node2, node3)  # Segmento entre B y C

# Imprimimos los detalles de los segmentos
print(segment1)
print(segment2)
