import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
from graph import *
from test_graph import *
from path import *
from airSpace import AirSpace, PlotAirSpace

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Interface")
        self.root.geometry("1080x720")
        self.graph = Graph()
        self.airspace = None
        
        # Variables para interacción con clicks
        self.click_mode = None  # 'add_node', 'add_segment', None
        self.selected_nodes = []  # Para almacenar nodos seleccionados para segmentos
        self.node_counter = 1  # Contador automático para nombres de nodos
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=3)  # Columna izquierda (60%)
        self.root.grid_columnconfigure(1, weight=2)  # Columna derecha (40%)
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1)
        
        # Frame para la columna izquierda con botones
        self.left_frame = tk.Frame(self.root, bg='#f0f0f0', relief='ridge', bd=2)
        self.left_frame.grid(row=0, column=0, rowspan=8, sticky='nsew', padx=5, pady=5)
        
        # Configurar grid del frame izquierdo
        for i in range(17):
            self.left_frame.grid_rowconfigure(i, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para la columna derecha (gráficos y información)
        self.right_frame = tk.Frame(self.root, bg='#e8f4f8', relief='ridge', bd=2)
        self.right_frame.grid(row=0, column=1, rowspan=8, sticky='nsew', padx=5, pady=5)
        
        # Configurar grid del frame derecho
        self.right_frame.grid_rowconfigure(0, weight=0)  # Título
        self.right_frame.grid_rowconfigure(1, weight=1)  # Gráfico
        self.right_frame.grid_rowconfigure(2, weight=0)  # Info
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        # Título en la columna derecha
        self.info_label = tk.Label(self.right_frame, text="Visualización y Estado", 
                                  font=('Arial', 12, 'bold'), bg='#e8f4f8')
        self.info_label.grid(row=0, column=0, sticky='ew', pady=5)
        
        # Frame para el gráfico
        self.plot_frame = tk.Frame(self.right_frame, bg='white', relief='sunken', bd=1)
        self.plot_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Configurar matplotlib
        self.figure = Figure(figsize=(4, 3), dpi=80, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Conectar evento de click
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        
        # Área de texto para información
        self.info_text = tk.Text(self.right_frame, height=6, wrap='word', bg='white', 
                                relief='sunken', bd=1, font=('Arial', 8))
        self.info_text.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        
        # Botones en la columna izquierda
        self.create_buttons()
        
        # Mensaje inicial
        self.update_info("Sistema iniciado. Selecciona una opción del menú.")
        self.show_welcome_plot()

    def calculate_distance(self, node1, node2):
        """Calcula la distancia euclidiana entre dos nodos"""
        return math.sqrt((node2.x - node1.x)**2 + (node2.y - node1.y)**2)

    def create_buttons(self):
        buttons_config = [
            ("Cargar grafo de ejemplo", self.load_example),
            ("Cargar grafo desde archivo", self.load_file),
            ("Guardar grafo", self.save_file),
            ("Mostrar grafo", self.plot_graph),
            ("Mostrar vecinos de un nodo", self.plot_node),
            ("🖱️ Añadir nodo (click)", self.enable_add_node_mode),
            ("Añadir nodo (manual)", self.add_node_manual),
            ("🖱️ Añadir segmento (click)", self.enable_add_segment_mode),
            ("Añadir segmento (manual)", self.add_segment_manual),
            ("Eliminar nodo", self.delete_node),
            ("Diseñar grafo desde cero", self.reset_graph),
            ("Ver alcanzables desde nodo", self.show_reachability),
            ("Camino más corto entre nodos", self.show_shortest_path),
            ("Cargar espacio aéreo (3 archivos)", self.load_airspace),
            ("Mostrar vecinos NavPoint", self.show_neighbors_navpoint),
            ("Ver alcanzables desde NavPoint", self.show_reachables_navpoint),
            ("Mostrar mapa del espacio aéreo", self.plot_airspace),
            ("Camino más corto en el espacio aéreo", self.show_shortest_path_airspace)
        ]
        
        for i, (text, command) in enumerate(buttons_config):
            btn = tk.Button(self.left_frame, text=text, command=command, 
                           font=('Arial', 9), relief='raised', bd=1)
            btn.grid(row=i, column=0, sticky='ew', padx=5, pady=2)

    def on_canvas_click(self, event):
        """Maneja los clicks en el canvas según el modo activo"""
        if event.inaxes is None:
            return
            
        if self.click_mode == 'add_node':
            self.add_node_by_click(event.xdata, event.ydata)
        elif self.click_mode == 'add_segment':
            self.select_node_for_segment(event.xdata, event.ydata)

    def enable_add_node_mode(self):
        """Activa el modo de añadir nodos por click"""
        self.click_mode = 'add_node'
        self.selected_nodes = []
        self.update_info("🖱️ Modo añadir nodo activado. Haz click en el gráfico para añadir un nodo.")
        self.update_info("Para salir del modo, selecciona otra opción.")

    def enable_add_segment_mode(self):
        """Activa el modo de añadir segmentos por click"""
        if len(self.graph.nodes) < 2:
            self.update_info("✗ Error: Necesitas al menos 2 nodos para crear un segmento")
            messagebox.showerror("Error", "Necesitas al menos 2 nodos para crear un segmento")
            return
            
        self.click_mode = 'add_segment'
        self.selected_nodes = []
        self.update_info("🖱️ Modo añadir segmento activado. Haz click en dos nodos para conectarlos.")
        self.update_info("Para salir del modo, selecciona otra opción.")
        self.plot_graph_in_panel()

    def add_node_by_click(self, x, y):
        """Añade un nodo en las coordenadas del click"""
        if x is None or y is None:
            return
            
        node_name = f"N{self.node_counter}"
        new_node = Node(node_name, x, y)
        
        if AddNode(self.graph, new_node):
            self.node_counter += 1
            self.update_info(f"✓ Nodo '{node_name}' añadido en ({x:.2f}, {y:.2f})")
            self.plot_graph_in_panel()
        else:
            self.update_info(f"✗ Error al añadir nodo '{node_name}'")

    def select_node_for_segment(self, x, y):
        """Selecciona nodos para crear un segmento"""
        if x is None or y is None or not self.graph.nodes:
            return
            
        closest_node = GetClosest(self.graph, x, y)
        distance = math.sqrt((closest_node.x - x)**2 + (closest_node.y - y)**2)
        if distance > 1.0:
            self.update_info(f"✗ Click demasiado lejos de cualquier nodo (distancia: {distance:.2f})")
            return
        
        if closest_node in self.selected_nodes:
            self.update_info(f"✗ Nodo '{closest_node.name}' ya seleccionado")
            return
            
        self.selected_nodes.append(closest_node)
        self.update_info(f"✓ Nodo '{closest_node.name}' seleccionado ({len(self.selected_nodes)}/2)")
        
        if len(self.selected_nodes) == 2:
            self.create_segment_from_selected()

    def create_segment_from_selected(self):
        """Crea un segmento con los nodos seleccionados"""
        if len(self.selected_nodes) != 2:
            return
            
        node1, node2 = self.selected_nodes
        segment_name = f"S{node1.name}-{node2.name}"
        
        if AddSegment(self.graph, segment_name, node1.name, node2.name):
            distance = self.calculate_distance(node1, node2)
            self.update_info(f"✓ Segmento '{segment_name}' creado: {node1.name} ↔ {node2.name}")
            self.update_info(f"  📏 Distancia: {distance:.2f} unidades")
            self.plot_graph_in_panel()
        else:
            self.update_info(f"✗ Error al crear segmento entre {node1.name} y {node2.name}")
        
        self.selected_nodes = []
        self.update_info("🖱️ Selecciona otros dos nodos para crear otro segmento.")

    def clear_plot(self):
        """Limpia el área de gráfico"""
        self.figure.clear()
        self.canvas.draw()

    def show_welcome_plot(self):
        """Muestra un gráfico de bienvenida"""
        self.clear_plot()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, 'Gráficos aparecerán aquí', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12, color='gray')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.canvas.draw()

    def plot_graph_in_panel(self):
        """Dibuja el grafo en el panel derecho con distancias en los segmentos"""
        self.clear_plot()
        ax = self.figure.add_subplot(111)
        
        # Dibujar nodos
        for node in self.graph.nodes:
            if self.click_mode == 'add_segment' and node in self.selected_nodes:
                color = 'red'
                size = 150
            else:
                color = 'lightblue'
                size = 100
                
            ax.scatter(node.x, node.y, s=size, c=color, edgecolors='black')
            ax.annotate(node.name, (node.x, node.y), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8, fontweight='bold')
        
        # Dibujar segmentos con distancias
        for segment in self.graph.segments:
            origin = segment.origin
            dest = segment.destination
            
            ax.plot([origin.x, dest.x], [origin.y, dest.y], 'b-', alpha=0.6, linewidth=2)
            
            mid_x = (origin.x + dest.x) / 2
            mid_y = (origin.y + dest.y) / 2
            distance = self.calculate_distance(origin, dest)
            
            dx = dest.x - origin.x
            dy = dest.y - origin.y
            length = math.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                perp_x = -dy / length
                perp_y = dx / length
                
                name_offset = 0.3
                name_x = mid_x + perp_x * name_offset
                name_y = mid_y + perp_y * name_offset
                
                dist_offset = -0.3
                dist_x = mid_x + perp_x * dist_offset
                dist_y = mid_y + perp_y * dist_offset
            else:
                name_x = name_y = mid_x
                dist_x = dist_y = mid_y
            
            ax.annotate(segment.name, (name_x, name_y), fontsize=7, 
                       ha='center', va='center', color='red', fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
            
            ax.annotate(f'{distance:.2f}', (dist_x, dist_y), fontsize=7, 
                       ha='center', va='center', color='blue', fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.8))
        
        if self.click_mode == 'add_node':
            title = 'Modo: Añadir Nodo (click para añadir)'
        elif self.click_mode == 'add_segment':
            title = f'Modo: Añadir Segmento ({len(self.selected_nodes)}/2 seleccionados)'
        else:
            title = 'Grafo Actual'
            
        ax.set_title(title, fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        self.canvas.draw()

    def plot_node_neighbors_in_panel(self, node_name):
        """Dibuja un nodo y sus vecinos en el panel derecho con distancias"""
        node = next((n for n in self.graph.nodes if n.name == node_name), None)
        if not node:
            return False
            
        self.clear_plot()
        ax = self.figure.add_subplot(111)
        
        ax.scatter(node.x, node.y, s=150, c='red', edgecolors='black')
        ax.annotate(node.name, (node.x, node.y), xytext=(5, 5), 
                   textcoords='offset points', fontsize=10, fontweight='bold')
        
        for neighbor in node.neighbors:
            ax.scatter(neighbor.x, neighbor.y, s=100, c='lightgreen', edgecolors='black')
            ax.annotate(neighbor.name, (neighbor.x, neighbor.y), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8)
            
            ax.plot([node.x, neighbor.x], [node.y, neighbor.y], 'g-', alpha=0.7, linewidth=2)
            
            distance = self.calculate_distance(node, neighbor)
            mid_x = (node.x + neighbor.x) / 2
            mid_y = (node.y + neighbor.y) / 2
            
            ax.annotate(f'{distance:.2f}', (mid_x, mid_y), fontsize=8, 
                       ha='center', va='center', color='blue', fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.8))
        
        ax.set_title(f'Vecinos de {node_name}', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        self.canvas.draw()
        return True

    def plot_path_in_panel(self, path):
        """Dibuja un camino en el panel derecho con distancias"""
        if not path or not path.nodes:
            return
            
        self.clear_plot()
        ax = self.figure.add_subplot(111)
        
        for node in self.graph.nodes:
            ax.scatter(node.x, node.y, s=50, c='lightgray', edgecolors='gray', alpha=0.5)
        
        path_x = [node.x for node in path.nodes]
        path_y = [node.y for node in path.nodes]
        ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.8)
        
        total_distance = 0
        for i, node in enumerate(path.nodes):
            if i == 0:
                ax.scatter(node.x, node.y, s=120, c='green', edgecolors='black')
            elif i == len(path.nodes) - 1:
                ax.scatter(node.x, node.y, s=120, c='red', edgecolors='black')
            else:
                ax.scatter(node.x, node.y, s=100, c='orange', edgecolors='black')
            
            ax.annotate(node.name, (node.x, node.y), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8, fontweight='bold')
            
            if i < len(path.nodes) - 1:
                next_node = path.nodes[i + 1]
                distance = self.calculate_distance(node, next_node)
                total_distance += distance
                
                mid_x = (node.x + next_node.x) / 2
                mid_y = (node.y + next_node.y) / 2
                
                ax.annotate(f'{distance:.2f}', (mid_x, mid_y), fontsize=8, 
                           ha='center', va='center', color='blue', fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.9))
        
        ax.set_title(f'Camino (Distancia Total: {total_distance:.2f})', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        self.canvas.draw()

    def plot_airspace_in_panel(self):
        """Dibuja el espacio aéreo en el panel derecho"""
        if not self.airspace:
            return False
            
        self.clear_plot()
        ax = self.figure.add_subplot(111)
        
        # Dibujar NavPoints
        nav_x = []
        nav_y = []
        nav_labels = []
        for nav_id, nav_point in self.airspace.navPoints.items():
            nav_x.append(nav_point.longitude)  # Usar longitude en lugar de x
            nav_y.append(nav_point.latitude)   # Usar latitude en lugar de y
            nav_labels.append(str(nav_id))
        
        if nav_x:
            ax.scatter(nav_x, nav_y, s=30, c='blue', alpha=0.7, label='NavPoints')
            for i, label in enumerate(nav_labels):
                ax.annotate(label, (nav_x[i], nav_y[i]), xytext=(2, 2), 
                        textcoords='offset points', fontsize=6)
        
        # Dibujar aeropuertos
        aer_x = []
        aer_y = []
        aer_labels = []
        for aer_name, airport in self.airspace.airports.items():
            # Buscar las coordenadas del aeropuerto en los NavPoints
            # Asumiendo que el aeropuerto tiene un NavPoint asociado
            for nav_id, nav_point in self.airspace.navPoints.items():
                if nav_point.name == aer_name:  # O alguna otra lógica de asociación
                    aer_x.append(nav_point.longitude)
                    aer_y.append(nav_point.latitude)
                    aer_labels.append(aer_name)
                    break
        
        if aer_x:
            ax.scatter(aer_x, aer_y, s=80, c='red', marker='s', alpha=0.8, label='Aeropuertos')
            for i, label in enumerate(aer_labels):
                ax.annotate(label, (aer_x[i], aer_y[i]), xytext=(2, 2), 
                        textcoords='offset points', fontsize=8, fontweight='bold')
        
        # Dibujar segmentos del espacio aéreo
        for segment in self.airspace.segments:
            origin_id = segment.origin_number      # ← Cambio aquí
            dest_id = segment.destination_number   # ← Cambio aquí
            
            origin_point = self.airspace.navPoints.get(origin_id)
            dest_point = self.airspace.navPoints.get(dest_id)
            
            if origin_point and dest_point:
                ax.plot([origin_point.longitude, dest_point.longitude], 
                    [origin_point.latitude, dest_point.latitude], 
                    'gray', alpha=0.5, linewidth=1)
        
        ax.set_title('Espacio Aéreo', fontsize=10)
        ax.grid(True, alpha=0.3)
        if nav_x or aer_x:  # Solo mostrar leyenda si hay datos
            ax.legend()
        ax.axis('equal')
        self.canvas.draw()
        return True

    def plot_airspace_path_in_panel(self, path):
        """Dibuja un camino del espacio aéreo en el panel derecho"""
        if not path or not path.nodes:
            return
            
        self.clear_plot()
        ax = self.figure.add_subplot(111)
        
        # Dibujar todos los NavPoints en gris claro
        for nav_id, nav_point in self.airspace.navPoints.items():
            ax.scatter(nav_point.x, nav_point.y, s=20, c='lightgray', alpha=0.5)
        
        # Dibujar aeropuertos
        for aer_id, airport in self.airspace.airports.items():
            ax.scatter(airport.x, airport.y, s=60, c='lightcoral', marker='s', alpha=0.6)
        
        # Dibujar el camino
        path_x = [node.x for node in path.nodes]
        path_y = [node.y for node in path.nodes]
        ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.8)
        
        # Dibujar nodos del camino
        for i, node in enumerate(path.nodes):
            if i == 0:
                ax.scatter(node.x, node.y, s=100, c='green', edgecolors='black')
            elif i == len(path.nodes) - 1:
                ax.scatter(node.x, node.y, s=100, c='red', edgecolors='black')
            else:
                ax.scatter(node.x, node.y, s=80, c='orange', edgecolors='black')
            
            ax.annotate(str(node.number), (node.x, node.y), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8, fontweight='bold')
        
        ax.set_title(f'Camino en Espacio Aéreo (Costo: {path.cost:.2f})', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        self.canvas.draw()

    def update_info(self, message):
        """Actualiza el área de información en la columna derecha"""
        self.info_text.insert(tk.END, f"{message}\n")
        self.info_text.see(tk.END)

    # Métodos principales (sin cambios significativos)
    def load_example(self):
        self.graph = CreateGraph_1()
        self.click_mode = None
        self.selected_nodes = []
        self.update_info("✓ Grafo de ejemplo cargado correctamente")
        messagebox.showinfo("Info", "Grafo de ejemplo cargado")

    def load_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.graph = LoadGraph(filepath)
            self.click_mode = None
            self.selected_nodes = []
            self.update_info(f"✓ Grafo cargado desde archivo: {filepath}")
            messagebox.showinfo("Info", "Grafo cargado desde archivo")

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            SaveGraph(self.graph, filepath)
            self.update_info(f"✓ Grafo guardado en: {filepath}")
            messagebox.showinfo("Info", "Grafo guardado correctamente")

    def plot_graph(self):
        self.click_mode = None
        self.selected_nodes = []
        self.plot_graph_in_panel()
        self.update_info("✓ Grafo visualizado en panel derecho")

    def plot_node(self):
        name = simpledialog.askstring("Nodo", "Nombre del nodo:")
        if name:
            self.click_mode = None
            self.selected_nodes = []
            if self.plot_node_neighbors_in_panel(name):
                self.update_info(f"✓ Vecinos del nodo '{name}' mostrados")
            else:
                self.update_info(f"✗ Error: Nodo '{name}' no encontrado")
                messagebox.showerror("Error", "Nodo no encontrado")

    def add_node_manual(self):
        self.click_mode = None
        self.selected_nodes = []
        
        name = simpledialog.askstring("Nombre del nodo", "Introduce el nombre del nodo:")
        if not name:
            return
            
        try:
            x = float(simpledialog.askstring("X", "Coordenada X:"))
            y = float(simpledialog.askstring("Y", "Coordenada Y:"))
        except:
            self.update_info("✗ Error: Coordenadas inválidas")
            messagebox.showerror("Error", "Coordenadas inválidas")
            return
            
        if AddNode(self.graph, Node(name, x, y)):
            self.update_info(f"✓ Nodo '{name}' añadido en ({x}, {y})")
        else:
            self.update_info(f"✗ Error: El nodo '{name}' ya existe")
            messagebox.showerror("Error", "El nodo ya existe")

    def add_segment_manual(self):
        self.click_mode = None
        self.selected_nodes = []
        
        name = simpledialog.askstring("Nombre del segmento", "Introduce el nombre del segmento:")
        if not name:
            return
            
        origin = simpledialog.askstring("Origen", "Nombre del nodo de origen:")
        if not origin:
            return
            
        dest = simpledialog.askstring("Destino", "Nombre del nodo de destino:")
        if not dest:
            return
            
        if AddSegment(self.graph, name, origin, dest):
            origin_node = next((n for n in self.graph.nodes if n.name == origin), None)
            dest_node = next((n for n in self.graph.nodes if n.name == dest), None)
            if origin_node and dest_node:
                distance = self.calculate_distance(origin_node, dest_node)
                self.update_info(f"✓ Segmento '{name}' añadido: {origin} → {dest}")
                self.update_info(f"  📏 Distancia: {distance:.2f} unidades")
        else:
            self.update_info(f"✗ Error al añadir segmento '{name}'")
            messagebox.showerror("Error", "Error al añadir segmento. Revisa nombres de nodos.")

    def delete_node(self):
        self.click_mode = None
        self.selected_nodes = []
        
        name = simpledialog.askstring("Eliminar nodo", "Nombre del nodo a eliminar:")
        if name and DeleteNode(self.graph, name):
            self.update_info(f"✓ Nodo '{name}' eliminado")
        else:
            self.update_info(f"✗ Error: Nodo '{name}' no encontrado")
            messagebox.showerror("Error", "Nodo no encontrado")

    def reset_graph(self):
        self.graph = Graph()
        self.click_mode = None
        self.selected_nodes = []
        self.node_counter = 1
        self.show_welcome_plot()
        self.update_info("✓ Nuevo grafo creado (grafo vacío)")
        messagebox.showinfo("Info", "Grafo nuevo creado")

    def show_reachability(self):
        self.click_mode = None
        self.selected_nodes = []
        
        name = simpledialog.askstring("Alcanzables", "Nombre del nodo de origen:")
        node = next((n for n in self.graph.nodes if n.name == name), None)
        if not node:
            self.update_info(f"✗ Error: Nodo '{name}' no encontrado")
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
        self.plot_path_in_panel(path)
        self.update_info(f"✓ Nodos alcanzables desde '{name}': {len(reached)} nodos")

    def show_shortest_path(self):
        self.click_mode = None
        self.selected_nodes = []
        
        origin = simpledialog.askstring("Camino mínimo", "Nodo de origen:")
        destination = simpledialog.askstring("Camino mínimo", "Nodo de destino:")
        path = FindShortestPath(self.graph, origin, destination)
        if path:
            self.plot_path_in_panel(path)
            self.update_info(f"✓ Camino más corto encontrado: {origin} → {destination}")
        else:
            self.update_info(f"✗ No existe camino entre '{origin}' y '{destination}'")
            messagebox.showinfo("Sin camino", "No existe un camino entre los nodos seleccionados.")

    # Métodos del espacio aéreo corregidos
    def load_airspace(self):
        try:
            nav = filedialog.askopenfilename(title="Selecciona archivo Cat_nav.txt")
            if not nav:
                return
                
            seg = filedialog.askopenfilename(title="Selecciona archivo Cat_seg.txt")
            if not seg:
                return
                
            aer = filedialog.askopenfilename(title="Selecciona archivo Cat_aer.txt")
            if not aer:
                return
                
            self.airspace = AirSpace()
            self.airspace.load_points(nav)
            self.airspace.load_segments(seg)
            self.airspace.load_airports(aer)
            
            self.update_info("✓ Espacio aéreo cargado correctamente")
            self.update_info(f"  - NavPoints: {len(self.airspace.navPoints)} puntos")
            self.update_info(f"  - Segmentos: {len(self.airspace.segments)} conexiones")
            self.update_info(f"  - Aeropuertos: {len(self.airspace.airports)} aeropuertos")
            messagebox.showinfo("Cargado", "Espacio aéreo cargado correctamente")
            
        except Exception as e:
            self.update_info(f"✗ Error al cargar espacio aéreo: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar espacio aéreo: {str(e)}")

    def show_neighbors_navpoint(self):
        if not self.airspace:
            self.update_info("✗ Error: No hay espacio aéreo cargado")
            messagebox.showerror("Error", "No hay espacio aéreo cargado")
            return
        try:
            point_id = int(simpledialog.askstring("NavPoint", "ID del NavPoint:"))
            neighbors = self.airspace.get_neighbors(point_id)
            if neighbors:
                self.update_info(f"✓ Vecinos del NavPoint {point_id}: {neighbors}")
                messagebox.showinfo("Vecinos", f"IDs alcanzables desde {point_id}: {neighbors}")
            else:
                self.update_info(f"✓ NavPoint {point_id} no tiene vecinos")
                messagebox.showinfo("Vecinos", f"Ningún vecino encontrado para {point_id}")
        except:
            self.update_info("✗ Error: ID inválido")
            messagebox.showerror("Error", "ID inválido")

    def show_reachables_navpoint(self):
        if not self.airspace:
            self.update_info("✗ Error: No hay espacio aéreo cargado")
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

            # Crear path para visualización
            path = Path()
            for nid in reached:
                np = self.airspace.navPoints.get(nid)
                if np:
                    AddNodeToPath(path, np)

            if path.nodes:
                self.plot_airspace_path_in_panel(path)
                self.update_info(f"✓ NavPoints alcanzables desde {start_id}: {len(reached)} puntos")
            else:
                self.update_info("✗ No se pudo generar ruta visual de alcanzables")
                messagebox.showinfo("Sin datos", "No se pudo generar ruta visual de alcanzables.")
        except Exception as e:
            self.update_info(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"ID inválido o error inesperado: {e}")

    def plot_airspace(self):
        if not self.airspace:
            self.update_info("✗ Error: No hay espacio aéreo cargado")
            messagebox.showerror("Error", "No hay espacio aéreo cargado")
            return
        
        if self.plot_airspace_in_panel():
            self.update_info("✓ Mapa del espacio aéreo visualizado")
        else:
            self.update_info("✗ Error al visualizar espacio aéreo")

    def show_shortest_path_airspace(self):
        if not self.airspace:
            self.update_info("✗ Error: No hay espacio aéreo cargado")
            messagebox.showerror("Error", "No hay espacio aéreo cargado")
            return
        try:
            origin_id = int(simpledialog.askstring("Origen", "ID del NavPoint origen:"))
            destination_id = int(simpledialog.askstring("Destino", "ID del NavPoint destino:"))
            
            from node import Distance
            from path import Path, AddNodeToPath, ContainsNode

            origin = self.airspace.navPoints.get(origin_id)
            destination = self.airspace.navPoints.get(destination_id)
            if not origin or not destination:
                raise ValueError("IDs inválidos")

            # Algoritmo A* adaptado para espacio aéreo
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
                self.plot_airspace_path_in_panel(found)
                self.update_info(f"✓ Camino más corto en espacio aéreo: {origin_id} → {destination_id}")
                self.update_info(f"  📏 Costo total: {found.cost:.2f}")
            else:
                self.update_info(f"✗ No se encontró camino entre {origin_id} y {destination_id}")
                messagebox.showinfo("Sin camino", "No se encontró un camino entre los puntos seleccionados.")
        except Exception as e:
            self.update_info(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
