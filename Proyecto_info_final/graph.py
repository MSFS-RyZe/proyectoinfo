import matplotlib.pyplot as plt
from node import *
from segment import *
from path import Path  # Make sure path.py exists and defines Path
import math
import webbrowser
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import time


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

# A* para grafo clásico
# Esto iría en path.py o donde esté FindShortestPath

# Dummy AddNodeToPath implementation (replace with actual logic if needed)
def AddNodeToPath(path_obj, node):
    if not hasattr(path_obj, 'nodes'):
        path_obj.nodes = []
    path_obj.nodes.append(node)

def FindShortestPath(graph, origin_name, dest_name):
    import heapq
    origin = next((n for n in graph.nodes if n.name == origin_name), None)
    dest = next((n for n in graph.nodes if n.name == dest_name), None)
    if not origin or not dest:
        return None

    queue = [(0, [origin])]
    visited = set()

    while queue:
        cost, path = heapq.heappop(queue)
        node = path[-1]
        if node == dest:
            # Construir objeto Path con los nodos
            p = Path()
            for n in path:
                AddNodeToPath(p, n)
            return p
        if node in visited:
            continue
        visited.add(node)
        for neighbor in node.neighbors:
            if neighbor not in path:
                new_cost = cost + math.sqrt((node.x - neighbor.x)**2 + (node.y - neighbor.y)**2)
                heapq.heappush(queue, (new_cost, path + [neighbor]))
    return None

def abrir_youtube():
    # Solo abre el enlace de YouTube
    webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0")

def mostrar_foto_sorpresa():
    # Solo crea y muestra la ventana con la foto
    ventana_foto = tk.Toplevel()
    ventana_foto.title("¡Sorpresa!")
    ventana_foto.geometry("600x600")
    ventana_foto.configure(bg='white')
    
    try:
        # Cargar y mostrar la imagen
        imagen_sorpresa = Image.open("foto.jpg")
        imagen_sorpresa = imagen_sorpresa.resize((550, 550))
        imagen_tk = ImageTk.PhotoImage(imagen_sorpresa)
        
        # Mostrar la imagen en un label
        label_imagen = tk.Label(ventana_foto, image=imagen_tk, bg='white')
        label_imagen.image = imagen_tk
        label_imagen.pack(expand=True, pady=20)
        
        # Botón para cerrar la ventana
        boton_cerrar = tk.Button(
            ventana_foto,
            text="Cerrar",
            command=ventana_foto.destroy,
            font=("Arial", 12, "bold"),
            bg="#ff6b6b",
            fg="white",
            padx=20,
            pady=10
        )
        boton_cerrar.pack(pady=20)
        
    except FileNotFoundError:
        mensaje_error = tk.Label(
            ventana_foto,
            text="No se pudo cargar la imagen 'foto.jpg'\n\nAsegúrate de que el archivo esté\nen la misma carpeta que el programa",
            font=("Arial", 14),
            bg='white',
            fg='red',
            justify='center'
        )
        mensaje_error.pack(expand=True)
        
        boton_cerrar = tk.Button(
            ventana_foto,
            text="Cerrar",
            command=ventana_foto.destroy,
            font=("Arial", 12, "bold"),
            bg="#ff6b6b",
            fg="white"
        )
        boton_cerrar.pack(pady=20)

def abrir_sorpresa():
    # Ejecuta ambos comandos inmediatamente, sin delay
    abrir_youtube()
    time.sleep(2)  # Pequeño delay para que se abra YouTube antes de mostrar la foto
    mostrar_foto_sorpresa()

import tkinter as tk

def funcionalidad():
    # Crear nueva ventana
    ventana_foto = tk.Toplevel()
    ventana_foto.title("Funcionalidades del Programa")
    ventana_foto.geometry("600x600")
    ventana_foto.configure(bg='white')

    # Crear un widget Text para mostrar texto largo
    texto_funcionalidades = tk.Text(
        ventana_foto,
        wrap="word",              # Para que el texto se ajuste al ancho
        font=("Arial", 12),
        bg="white",
        fg="black"
    )
    texto_funcionalidades.insert("1.0", """
Este programa ofrece las siguientes funcionalidades:

1. Una cálida bienvenida con un sonido gracioso
2. Un enlace a un video de YouTube que te hará reír
3. Una foto sorpresa que se mostrará después de ver el video
4. Una canción de fondo para acompañar la experiencia
5. Destacar los aeropuertos con simbolos de avión
6. Personalización del google earth para solamente ver aeropuertos y rutas deseadas
8. Una interfaz gráfica amigable y fácil de usar
9. Posibilidad de guardar y cargar grafos para continuar trabajando en ellos

¡Explora todas las opciones del menú para descubrir lo que puedes hacer!
""")
    texto_funcionalidades.config(state="disabled")  # Desactivar edición
    texto_funcionalidades.pack(padx=20, pady=20, fill="both", expand=True)
