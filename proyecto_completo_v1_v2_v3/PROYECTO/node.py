import math
from tkinter import *
from graph import *
from airSpace import *
from test_graph import *
from segment import *
from path import *
from test_path import *

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

def AddNeighbor(n1, n2):
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True

def Distance(n1, n2):
    x1 = getattr(n1, 'x', getattr(n1, 'longitude', 0))
    y1 = getattr(n1, 'y', getattr(n1, 'latitude', 0))
    x2 = getattr(n2, 'x', getattr(n2, 'longitude', 0))
    y2 = getattr(n2, 'y', getattr(n2, 'latitude', 0))
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
