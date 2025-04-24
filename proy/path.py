from graph import *
from segment import *
from node import *

class Path:
    def __init__(self):
        self.nodes = []
        self.cost = 0.0

def AddNodeToPath(path, node):
    if path.nodes:
        path.cost += Distance(path.nodes[-1], node)
    path.nodes.append(node)

def ContainsNode(path, node):
    return node in path.nodes

def CostToNode(path, node):
    if node not in path.nodes:
        return -1
    cost = 0.0
    for i in range(1, path.nodes.index(node) + 1):
        cost += Distance(path.nodes[i - 1], path.nodes[i])
    return cost

def PlotPath(graph, path):
    import matplotlib.pyplot as plt
    for node in graph.nodes:
        color = 'blue' if node == path.nodes[0] else ('green' if node == path.nodes[-1] else ('red' if node in path.nodes else 'gray'))
        plt.plot(node.x, node.y, 'o', color=color)
        plt.text(node.x + 0.2, node.y + 0.2, node.name)

    for segment in graph.segments:
        x_vals = [segment.origin.x, segment.destination.x]
        y_vals = [segment.origin.y, segment.destination.y]
        plt.plot(x_vals, y_vals, 'lightgray')

    for i in range(len(path.nodes) - 1):
        x_vals = [path.nodes[i].x, path.nodes[i+1].x]
        y_vals = [path.nodes[i].y, path.nodes[i+1].y]
        plt.plot(x_vals, y_vals, 'red', linewidth=2)
        mid_x = (path.nodes[i].x + path.nodes[i+1].x) / 2
        mid_y = (path.nodes[i].y + path.nodes[i+1].y) / 2
        plt.text(mid_x, mid_y, f"{Distance(path.nodes[i], path.nodes[i+1]):.2f}", fontsize=8, color='black')

    plt.axis('equal')
    plt.title("Camino más corto o nodos alcanzables")
    plt.show()
