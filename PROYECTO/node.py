import math

class Node:
    def __init__(self, name: str, x: float, y: float): # string palabra, floats para numeros decimales
        self.name = name
        self.x = x
        self.y = y
        self.Neighbours = []  # List to store Neighbouring nodes

    def add_Neighbour(self, node): # Añade un nodo a la lista de vecinos 
        if node not in self.Neighbours:  # Si el nodo no es vecino, lo añade
            self.Neighbours.append(node) # lo añade en la lista de vecinos

    def __repr__(self):
        return f"Node({self.name}, x={self.x}, y={self.y}, Neighbours={[n.name for n in self.Neighbours]})"
    
def AddNeighbour (n1: Node, n2: Node) -> bool: # Añade n2 a la lista de vecinos de n1. bool para: si n2 ya es vecino, la función devuelve False. Si se añade correctamente, devuelve True.
    if n2 in n1.Neighbours:
        return False
    else:
        n1.add_Neighbour(n2)
        return True
def Distance(n1: Node, n2: Node) -> float: # float para los decimales
    return math.sqrt((n2.x - n1.x)**2 + (n2.y - n1.y)**2) # raiz de la suma de los cuadrados de las diferencias de las coordenadas x e y (distnacia euclidiana entre 2 puntos)
