class NavSegment: #Representa conexiones o segmentos numerados
    def __init__(self, origin_number, destination_number, distance):
        self.origin_number = int(origin_number) #Número del nodo de origen
        self.destination_number = int(destination_number) #Número del nodo del destino
        self.distance = float(distance) #Distancia o coste entre los nodos

    def __repr__(self): #Define como se representa el segmento al ser mostrado
        return f"NavSegment({self.origin_number} -> {self.destination_number}, {self.distance})"
