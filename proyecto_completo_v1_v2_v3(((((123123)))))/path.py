from node import Distance
import matplotlib.pyplot as plt


class Path:
    def __init__(self):
        self.nodes = [] #Lista de los nodos en el camino, colocados en orden en la lista
        self.cost = 0.0 #Coste del camino en formato float 

def AddNodeToPath(path, node): #Añade un nodo al final del camino, si ya hay nodos, añade la distancia al coste 
    if path.nodes:
        path.cost += Distance(path.nodes[-1], node)
    path.nodes.append(node)

def ContainsNode(path, node): #True si está en el camino, False si el nodo no lo está
    return node in path.nodes

def CostToNode(path, node): #Calcula el coste hasta un nodo 
    cost = 0.0 
    for i in range(len(path.nodes)):
        if path.nodes[i] == node:
            return cost
        if i > 0:
            cost += Distance(path.nodes[i-1], path.nodes[i])
    return -1

def PlotPath(graph, path): #Visualiza el camino sobre el grafo. 
    for node in graph.navPoints.values() if hasattr(graph, 'navPoints') else graph.nodes: #
        if node in path.nodes:
            color = 'blue' if node == path.nodes[0] else ('green' if node == path.nodes[-1] else 'red') #Determina los colores dependiendo del estado del nodo. hasattr te devuelve true si el atributo dicho se encuentra dentro del objeto especificado. 
        else:
            color = 'gray'
        x = getattr(node, 'x', getattr(node, 'longitude', 0)) #getattr te da el valor del atributo especificado.
        y = getattr(node, 'y', getattr(node, 'latitude', 0))
        plt.plot(x, y, 'o', color=color)
        name = getattr(node, 'name', str(node))
        plt.text(x + 0.2, y + 0.2, name)

    for i in range(len(path.nodes) - 1):
        n1 = path.nodes[i]
        n2 = path.nodes[i+1]
        x1 = getattr(n1, 'x', getattr(n1, 'longitude', 0))
        y1 = getattr(n1, 'y', getattr(n1, 'latitude', 0))
        x2 = getattr(n2, 'x', getattr(n2, 'longitude', 0))
        y2 = getattr(n2, 'y', getattr(n2, 'latitude', 0))
        plt.plot([x1, x2], [y1, y2], 'green', linewidth=2)
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        plt.text(mx, my, f"{Distance(n1,n2):.2f}", fontsize=8, color='black')

    plt.axis('equal') #genera el display visual 
    plt.title("Camino o nodos alcanzables")
    plt.show()


