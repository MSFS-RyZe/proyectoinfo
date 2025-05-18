from node import Distance

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
    cost = 0.0
    for i in range(len(path.nodes)):
        if path.nodes[i] == node:
            return cost
        if i > 0:
            cost += Distance(path.nodes[i-1], path.nodes[i])
    return -1

def PlotPath(graph, path):
    import matplotlib.pyplot as plt
    for node in graph.navPoints.values() if hasattr(graph, 'navPoints') else graph.nodes:
        if node in path.nodes:
            color = 'blue' if node == path.nodes[0] else ('green' if node == path.nodes[-1] else 'red')
        else:
            color = 'gray'
        x = getattr(node, 'x', getattr(node, 'longitude', 0))
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
        plt.plot([x1, x2], [y1, y2], 'red', linewidth=2)
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        plt.text(mx, my, f"{Distance(n1,n2):.2f}", fontsize=8, color='black')

    plt.axis('equal')
    plt.title("Camino o nodos alcanzables")
    plt.show()
