class Path:
    def __init__(self, nodes=[]):
        self.nodes = nodes[:]  # list of Node objects
        self.real_cost = 0.0

    def AddNode(self, node, cost):
        self.nodes.append(node)
        self.real_cost += cost

    def LastNode(self):
        return self.nodes[-1]

    def ContainsNode(self, node):
        return node in self.nodes

    def EstimatedTotalCost(self, dest_node):
        return self.real_cost + Distance(self.LastNode(), dest_node)

