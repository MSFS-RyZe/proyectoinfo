from node import Distance

class Segment: #Definimos la clase segment
    def __init__(self, name, origin, destination):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Distance(origin, destination) #Te da el coste entre dos nodos, para calcular la distancia. 
