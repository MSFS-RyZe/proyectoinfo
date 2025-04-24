import matplotlib.pyplot as plt
from node import *
from segment import *
import math
import tkinter as tk
from tkinter import filedialog

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

def AddNode(g, n):
    if n.name in [node.name for node in g.nodes]:
        return False
    g.nodes.append(n)
    return True

def AddSegment(g, name, origin_name, dest_name):
    origin = next((n for n in g.nodes if n.name == origin_name), None)
    dest = next((n for n in g.nodes if n.name == dest_name), None)
    if not origin or not dest:
        return False
    seg = Segment(name, origin, dest)
    g.segments.append(seg)
    AddNeighbor(origin, dest)
    return True

def DeleteNode(g, name):
    node = next((n for n in g.nodes if n.name == name), None)
    if not node:
        return False
    g.nodes.remove(node)
    g.segments = [s for s in g.segments if s.origin != node and s.destination != node]
    for n in g.nodes:
        if node in n.neighbors:
            n.neighbors.remove(node)
    return True

def GetClosest(g, x, y):
    return min(g.nodes, key=lambda n: math.hypot(n.x - x, n.y - y))

def Plot(g):
    for node in g.nodes:
        plt.plot(node.x, node.y, 'o', color='gray')
        plt.text(node.x + 0.2, node.y + 0.2, node.name)
    for seg in g.segments:
        x_vals = [seg.origin.x, seg.destination.x]
        y_vals = [seg.origin.y, seg.destination.y]
        plt.plot(x_vals, y_vals, 'black')
        mid_x = (seg.origin.x + seg.destination.x) / 2
        mid_y = (seg.origin.y + seg.destination.y) / 2
        plt.text(mid_x, mid_y, f"{seg.cost:.2f}", color='red')
    plt.axis('equal')
    plt.show()

def PlotNode(g, name):
    node = next((n for n in g.nodes if n.name == name), None)
    if not node:
        return False
    for n in g.nodes:
        color = 'blue' if n == node else ('green' if n in node.neighbors else 'gray')
        plt.plot(n.x, n.y, 'o', color=color)
        plt.text(n.x + 0.2, n.y + 0.2, n.name)
    for seg in g.segments:
        if seg.origin == node and seg.destination in node.neighbors:
            x_vals = [seg.origin.x, seg.destination.x]
            y_vals = [seg.origin.y, seg.destination.y]
            plt.plot(x_vals, y_vals, 'red')
            mid_x = (seg.origin.x + seg.destination.x) / 2
            mid_y = (seg.origin.y + seg.destination.y) / 2
            plt.text(mid_x, mid_y, f"{seg.cost:.2f}", color='red')
    plt.axis('equal')
    plt.show()
    return True

def SaveGraph(g, filename):
    with open(filename, 'w') as f:
        for node in g.nodes:
            f.write(f"NODE {node.name} {node.x} {node.y}\n")
        for seg in g.segments:
            f.write(f"SEGMENT {seg.name} {seg.origin.name} {seg.destination.name}\n")

def LoadGraph(filename):
    g = Graph()
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if parts[0] == 'NODE':
                AddNode(g, Node(parts[1], float(parts[2]), float(parts[3])))
            elif parts[0] == 'SEGMENT':
                AddSegment(g, parts[1], parts[2], parts[3])
    return g

def GetReachableNodes(graph, start_name):
    visited = set()
    to_visit = [start_name]
    while to_visit:
        current = to_visit.pop()
        if current not in visited:
            visited.add(current)
            node = next((n for n in graph.nodes if n.name == current), None)
            if node:
                to_visit.extend([n.name for n in node.neighbors])
    return visited

def FindShortestPath(graph, origin_name, destination_name):
    origin = next(n for n in graph.nodes if n.name == origin_name)
    destination = next(n for n in graph.nodes if n.name == destination_name)

    paths = [Path([origin])]
    visited = set()

    while paths:
        paths.sort(key=lambda p: p.EstimatedTotalCost(destination))
        current_path = paths.pop(0)
        current_node = current_path.LastNode()

        if current_node.name == destination_name:
            return current_path

        if current_node.name in visited:
            continue
        visited.add(current_node.name)

        for neighbor in current_node.neighbors:
            if current_path.ContainsNode(neighbor):
                continue
            segment = next((s for s in graph.segments if s.origin.name == current_node.name and s.destination.name == neighbor.name), None)
            if segment:
                new_path = Path(current_path.nodes[:])
                new_path.real_cost = current_path.real_cost
                new_path.AddNode(neighbor, segment.cost)
                paths.append(new_path)

    return None
import matplotlib.pyplot as plt

def PlotReachability(graph, start_node_name):
    start_node = next((n for n in graph.nodes if n.name == start_node_name), None)
    if not start_node:
        return

    reachable = GetReachableNodes(graph, start_node_name)

    # Plot nodes
    for node in graph.nodes:
        color = "gray"
        if node.name == start_node_name:
            color = "blue"
        elif node.name in reachable:
            color = "green"
        plt.plot(node.x, node.y, 'o', color=color)
        plt.text(node.x + 0.3, node.y + 0.3, node.name)

    # Plot segments
    for seg in graph.segments:
        x1, y1 = seg.origin.x, seg.origin.y
        x2, y2 = seg.destination.x, seg.destination.y
        if seg.origin.name == start_node_name and seg.destination.name in reachable:
            plt.plot([x1, x2], [y1, y2], 'r')
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            plt.text(mid_x, mid_y, f"{seg.cost:.2f}", fontsize=8)
        else:
            plt.plot([x1, x2], [y1, y2], 'k', alpha=0.3)

    plt.title(f"Reachability from {start_node_name}")

def PlotPath(graph, path):
    # Plot all nodes (light gray)
    for node in graph.nodes:
        plt.plot(node.x, node.y, 'o', color="lightgray")
        plt.text(node.x + 0.3, node.y + 0.3, node.name)

    # Plot all segments (light gray)
    for seg in graph.segments:
        plt.plot([seg.origin.x, seg.destination.x], [seg.origin.y, seg.destination.y], 'k', alpha=0.2)

    # Plot path segments (red)
    for i in range(len(path.nodes) - 1):
        n1 = path.nodes[i]
        n2 = path.nodes[i + 1]
        plt.plot([n1.x, n2.x], [n1.y, n2.y], 'r', linewidth=2)

    # Highlight start and end
    plt.plot(path.nodes[0].x, path.nodes[0].y, 'o', color="blue")
    plt.plot(path.nodes[-1].x, path.nodes[-1].y, 'o', color="green")

    plt.title(f"Shortest Path: {path.nodes[0].name} → {path.nodes[-1].name}")

def PlotPath(graph, path):
    # Plot all nodes (light gray)
    for node in graph.nodes:
        plt.plot(node.x, node.y, 'o', color="lightgray")
        plt.text(node.x + 0.3, node.y + 0.3, node.name)

    # Plot all segments (light gray)
    for seg in graph.segments:
        plt.plot([seg.origin.x, seg.destination.x], [seg.origin.y, seg.destination.y], 'k', alpha=0.2)

    # Plot path segments (red)
    for i in range(len(path.nodes) - 1):
        n1 = path.nodes[i]
        n2 = path.nodes[i + 1]
        plt.plot([n1.x, n2.x], [n1.y, n2.y], 'r', linewidth=2)

    # Highlight start and end
    plt.plot(path.nodes[0].x, path.nodes[0].y, 'o', color="blue")
    plt.plot(path.nodes[-1].x, path.nodes[-1].y, 'o', color="green")

    plt.title(f"Shortest Path: {path.nodes[0].name} → {path.nodes[-1].name}")

