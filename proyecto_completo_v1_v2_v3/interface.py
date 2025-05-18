import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from graph import *
from test_graph import *
from path import *
from airSpace import AirSpace, PlotAirSpace

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Interface")
        self.graph = Graph()
        self.airspace = None

        tk.Button(root, text="Cargar grafo de ejemplo", command=self.load_example).pack(fill='x')
        tk.Button(root, text="Cargar grafo desde archivo", command=self.load_file).pack(fill='x')
        tk.Button(root, text="Guardar grafo", command=self.save_file).pack(fill='x')
        tk.Button(root, text="Mostrar grafo", command=self.plot_graph).pack(fill='x')
        tk.Button(root, text="Mostrar vecinos de un nodo", command=self.plot_node).pack(fill='x')
        tk.Button(root, text="Añadir nodo", command=self.add_node).pack(fill='x')
        tk.Button(root, text="Añadir segmento", command=self.add_segment).pack(fill='x')
        tk.Button(root, text="Eliminar nodo", command=self.delete_node).pack(fill='x')
        tk.Button(root, text="Diseñar grafo desde cero", command=self.reset_graph).pack(fill='x')
        tk.Button(root, text="Ver alcanzables desde nodo", command=self.show_reachability).pack(fill='x')
        tk.Button(root, text="Camino más corto entre nodos", command=self.show_shortest_path).pack(fill='x')

        tk.Button(root, text="Cargar espacio aéreo (3 archivos)", command=self.load_airspace).pack(fill='x')
        tk.Button(root, text="Mostrar vecinos NavPoint", command=self.show_neighbors_navpoint).pack(fill='x')
        tk.Button(root, text="Ver alcanzables desde NavPoint", command=self.show_reachables_navpoint).pack(fill='x')
        tk.Button(root, text="Mostrar mapa del espacio aéreo", command=self.plot_airspace).pack(fill='x')
        tk.Button(root, text="Camino más corto en el espacio aéreo", command=self.show_shortest_path_airspace).pack(fill='x')

    def load_example(self):
        self.graph = CreateGraph_1()
        messagebox.showinfo("Info", "Grafo de ejemplo cargado")

    def load_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.graph = LoadGraph(filepath)
            messagebox.showinfo("Info", "Grafo cargado desde archivo")

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            SaveGraph(self.graph, filepath)
            messagebox.showinfo("Info", "Grafo guardado correctamente")

    def plot_graph(self):
        Plot(self.graph)

    def plot_node(self):
        name = simpledialog.askstring("Nodo", "Nombre del nodo:")
        if name:
            if not PlotNode(self.graph, name):
                messagebox.showerror("Error", "Nodo no encontrado")

    def add_node(self):
        name = simpledialog.askstring("Nombre del nodo", "Introduce el nombre del nodo:")
        try:
            x = float(simpledialog.askstring("X", "Coordenada X:"))
            y = float(simpledialog.askstring("Y", "Coordenada Y:"))
        except:
            messagebox.showerror("Error", "Coordenadas inválidas")
            return
        if not AddNode(self.graph, Node(name, x, y)):
            messagebox.showerror("Error", "El nodo ya existe")

    def add_segment(self):
        name = simpledialog.askstring("Nombre del segmento", "Introduce el nombre del segmento:")
        origin = simpledialog.askstring("Origen", "Nombre del nodo de origen:")
        dest = simpledialog.askstring("Destino", "Nombre del nodo de destino:")
        if not AddSegment(self.graph, name, origin, dest):
            messagebox.showerror("Error", "Error al añadir segmento. Revisa nombres de nodos.")

    def delete_node(self):
        name = simpledialog.askstring("Eliminar nodo", "Nombre del nodo a eliminar:")
        if not DeleteNode(self.graph, name):
            messagebox.showerror("Error", "Nodo no encontrado")

    def reset_graph(self):
        self.graph = Graph()
        messagebox.showinfo("Info", "Grafo nuevo creado")

    def show_reachability(self):
        name = simpledialog.askstring("Alcanzables", "Nombre del nodo de origen:")
        node = next((n for n in self.graph.nodes if n.name == name), None)
        if not node:
            messagebox.showerror("Error", "Nodo no encontrado")
            return
        reached = set()
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in reached:
                reached.add(current)
                stack.extend(n for n in current.neighbors if n not in reached)
        path = Path()
        for n in reached:
            AddNodeToPath(path, n)
        PlotPath(self.graph, path)

    def show_shortest_path(self):
        origin = simpledialog.askstring("Camino mínimo", "Nodo de origen:")
        destination = simpledialog.askstring("Camino mínimo", "Nodo de destino:")
        path = FindShortestPath(self.graph, origin, destination)
        if path:
            PlotPath(self.graph, path)
        else:
            messagebox.showinfo("Sin camino", "No existe un camino entre los nodos seleccionados.")

    def load_airspace(self):
        nav = filedialog.askopenfilename(title="Selecciona archivo Cat_nav.txt")
        seg = filedialog.askopenfilename(title="Selecciona archivo Cat_seg.txt")
        aer = filedialog.askopenfilename(title="Selecciona archivo Cat_aer.txt")
        self.airspace = AirSpace()
        self.airspace.load_points(nav)
        self.airspace.load_segments(seg)
        self.airspace.load_airports(aer)
        messagebox.showinfo("Cargado", "Espacio aéreo cargado correctamente")

    def show_neighbors_navpoint(self):
        if not self.airspace:
            messagebox.showerror("Error", "No hay espacio aéreo cargado")
            return
        try:
            point_id = int(simpledialog.askstring("NavPoint", "ID del NavPoint:"))
            neighbors = self.airspace.get_neighbors(point_id)
            if neighbors:
                messagebox.showinfo("Vecinos", f"IDs alcanzables desde {point_id}: {neighbors}")
            else:
                messagebox.showinfo("Vecinos", f"Ningún vecino encontrado para {point_id}")
        except:
            messagebox.showerror("Error", "ID inválido")

    def show_reachables_navpoint(self):
        if not self.airspace:
            messagebox.showerror("Error", "No hay espacio aéreo cargado")
            return
        try:
            start_id = int(simpledialog.askstring("Alcanzables", "ID del NavPoint de origen:"))
            reached = set()
            stack = [start_id]
            while stack:
                current = stack.pop()
                if current not in reached:
                    reached.add(current)
                    stack.extend(n for n in self.airspace.get_neighbors(current) if n not in reached)

            from path import Path, AddNodeToPath, PlotPath
            path = Path()
            for nid in reached:
                np = self.airspace.navPoints.get(nid)
                if np:
                    AddNodeToPath(path, np)

            if path.nodes:
                PlotPath(self.airspace, path)
            else:
                messagebox.showinfo("Sin datos", "No se pudo generar ruta visual de alcanzables.")
        except Exception as e:
            messagebox.showerror("Error", f"ID inválido o error inesperado: {e}")

    def plot_airspace(self):
        if not self.airspace:
            messagebox.showerror("Error", "No hay espacio aéreo cargado")
            return
        PlotAirSpace(self.airspace)

    def show_shortest_path_airspace(self):
        if not self.airspace:
            messagebox.showerror("Error", "No hay espacio aéreo cargado")
            return
        try:
            origin_id = int(simpledialog.askstring("Origen", "ID del NavPoint origen:"))
            destination_id = int(simpledialog.askstring("Destino", "ID del NavPoint destino:"))
            from node import Distance
            from path import Path, AddNodeToPath, ContainsNode, PlotPath

            origin = self.airspace.navPoints.get(origin_id)
            destination = self.airspace.navPoints.get(destination_id)
            if not origin or not destination:
                raise ValueError("IDs inválidos")

            paths = []
            path = Path()
            AddNodeToPath(path, origin)
            paths.append(path)

            found = None
            while paths:
                paths.sort(key=lambda p: p.cost + Distance(p.nodes[-1], destination))
                best = paths.pop(0)
                last = best.nodes[-1]

                if last == destination:
                    found = best
                    break

                for nid in self.airspace.get_neighbors(last.number):
                    next_node = self.airspace.navPoints[nid]
                    if ContainsNode(best, next_node):
                        continue
                    newp = Path()
                    newp.nodes = best.nodes[:]
                    newp.cost = best.cost
                    AddNodeToPath(newp, next_node)
                    paths.append(newp)

            if found:
                PlotPath(self.airspace, found)
            else:
                messagebox.showinfo("Sin camino", "No se encontró un camino entre los puntos seleccionados.")
        except:
            messagebox.showerror("Error", "IDs inválidos")

if __name__ == '__main__':
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
