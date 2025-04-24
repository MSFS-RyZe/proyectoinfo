import matplotlib.pyplot as plt
from node import *
from segment import *

class Graph:
    def __init__(self):
        self.segments = []  # Lista de segmentos en el grafo
        self.nodes = []     # Lista de nodos en el grafo

    def AddNode(self, n):
        # Añade un nodo al grafo si no existe ya
        for node in self.nodes:
            if node == n:
                return
        self.nodes.append(n)

class Graph:
    def __init__(self):
        self.segments = []  # Lista de segmentos en el grafo

    def AddNode(self, n):
        # Añade un nodo al grafo si no existe ya
        for node in self.nodes:
            if node.name == n.name:
                return False  # El nodo ya existe
            else:
                self.nodes.append(n)
                return True

    def AddSegment(self, nameOriginNode, nameDestinationNode):
        origin = None
        destination = None

    # Busca los nodos en la lista de nodos
        for node in self.nodes:
            if node.name == nameOriginNode:
                origin = node
            if node.name == nameDestinationNode:
                destination = node

    # Si ambos nodos existen, se añade el segmento
        if origin and destination:
            # Crea el segmento y añade el nodo destino como vecino
            segment = Segment(nameOriginNode + '-' + nameDestinationNode, origin, destination)
            self.segments.append(segment)
            origin.neighbors.append(destination)
            return True
        return False


    def GetClosest(self, g, x, y):
        closest_node = None
        closest_distance = float('inf')
        
        # Comprobar cada nodo y calcular la distancia euclidiana
        for node in g.nodes:
            distance = Distance(node, Node("", x, y))
            if distance < closest_distance:
                closest_distance = distance
                closest_node = node
        
        return closest_node

    def Plot(self):
        plt.figure(figsize=(8, 8))
    
    # Plot de todos los nodos
        for node in self.nodes:
            plt.scatter(node.x, node.y, color='gray')  # Solo grafica el punto
            plt.text(node.x + 1, node.y + 1, node.name, fontsize=12)  # Muestra el nombre del nodo cerca del punto
    
    # Plot de todos los segmentos
        for segment in self.segments:
            plt.plot([segment.origin.x, segment.destination.x],
                    [segment.origin.y, segment.destination.y], 'r')  # Dibuja el segmento
            mid_x = (segment.origin.x + segment.destination.x) / 2
            mid_y = (segment.origin.y + segment.destination.y) / 2
            plt.text(mid_x, mid_y, f"{segment.cost:.2f}", fontsize=12, color='black')  # Muestra el costo del segmento
    
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Gráfico del Grafo')
        plt.grid(True)
        plt.show()


    def PlotNode(self, g, nameOrigin):
        origin = None
        
        # Encontrar el nodo origen por su nombre
        for node in g.nodes:
            if node.name == nameOrigin:
                origin = node
        
        if origin is None:
            return False  # Nodo origen no encontrado
        
        # Crear el plot
        plt.figure(figsize=(-1, 8))
        
        # Plot de todos los nodos
        for node in g.nodes:
            if node == origin:
                plt.scatter(node.x, node.y, color='blue', label=node.name)
            elif node in origin.neighbors:
                plt.scatter(node.x, node.y, color='green', label=node.name)
            else:
                plt.scatter(node.x, node.y, color='gray', label=node.name)
            plt.text(node.x + 1, node.y + 1, node.name, fontsize=12)
        
        # Plot de los segmentos desde el nodo origen
        for neighbor in origin.neighbors:
            plt.plot([origin.x, neighbor.x], [origin.y, neighbor.y], 'r')
            mid_x = (origin.x + neighbor.x) / 2
            mid_y = (origin.y + neighbor.y) / 2
            plt.text(mid_x, mid_y, f"{Distance(origin, neighbor):.2f}", fontsize=12, color='black')
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Gráfico del Nodo {origin.name} y sus Vecinos')
        plt.grid(True)
        plt.show()
        
        return True
