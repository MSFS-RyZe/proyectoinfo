from node import *  # Importamos la clase Node y la función Distance

class Segment:
    def __init__(self, name: str, origin: Node, destination: Node):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Distance(origin, destination)  # Calculamos la distancia entre los dos nodos

    def __repr__(self):
        return f"Segment({self.name}, origin={self.origin.name}, destination={self.destination.name}, cost={self.cost})"
