import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from graph import *

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Interface")
        self.graph = Graph()

        # Botones
        tk.Button(root, text="Cargar grafo de ejemplo", command=self.load_example).pack(fill='x')
        tk.Button(root, text="Cargar grafo desde archivo", command=self.load_file).pack(fill='x')
        tk.Button(root, text="Guardar grafo", command=self.save_file).pack(fill='x')
        tk.Button(root, text="Mostrar grafo", command=self.plot_graph).pack(fill='x')
        tk.Button(root, text="Mostrar vecinos de un nodo", command=self.plot_node).pack(fill='x')
        tk.Button(root, text="Añadir nodo", command=self.add_node).pack(fill='x')
        tk.Button(root, text="Añadir segmento", command=self.add_segment).pack(fill='x')
        tk.Button(root, text="Eliminar nodo", command=self.delete_node).pack(fill='x')
        tk.Button(root, text="Diseñar grafo desde cero", command=self.reset_graph).pack(fill='x')

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


if __name__ == '__main__':
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()

