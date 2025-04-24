from graph import *

def CreateGraph_1():
    G = Graph()
    for name, x, y in [("A",1,20),("B",8,17),("C",15,20),("D",18,15),("E",2,4),
                       ("F",6,5),("G",12,12),("H",10,3),("I",19,1),("J",13,5),
                       ("K",3,15),("L",4,10)]:
        AddNode(G, Node(name, x, y))
    for name, o, d in [("AB","A","B"),("AE","A","E"),("AK","A","K"),("BA","B","A"),
                       ("BC","B","C"),("BF","B","F"),("BK","B","K"),("BG","B","G"),
                       ("CD","C","D"),("CG","C","G"),("DG","D","G"),("DH","D","H"),
                       ("DI","D","I"),("EF","E","F"),("FL","F","L"),("GB","G","B"),
                       ("GF","G","F"),("GH","G","H"),("ID","I","D"),("IJ","I","J"),
                       ("JI","J","I"),("KA","K","A"),("KL","K","L"),("LK","L","K"),
                       ("LF","L","F")]:
        AddSegment(G, name, o, d)
    return G

print("Probando el grafo...")
G = CreateGraph_1()
Plot(G)
PlotNode(G, "C")
n = GetClosest(G, 15, 5)
print(n.name) # Debe ser J
n = GetClosest(G, 8, 19)
print(n.name) # Debe ser B