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
