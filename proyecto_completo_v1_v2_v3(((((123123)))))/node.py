from math import *
class Node: #Define un nodo
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = [] #Lista de los nodos vecinos

def AddNeighbor(n1, n2): #Esta función añade un nodo vecino 
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True

def Distance(n1, n2): #Genera la función distancia
    x1 = getattr(n1, 'x', getattr(n1, 'longitude', 0))
    y1 = getattr(n1, 'y', getattr(n1, 'latitude', 0))
    x2 = getattr(n2, 'x', getattr(n2, 'longitude', 0))
    y2 = getattr(n2, 'y', getattr(n2, 'latitude', 0))
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c