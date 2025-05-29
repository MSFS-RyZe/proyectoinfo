import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from graph import *
from test_graph import *
from path import *
from airSpace import *
from test_graph import *
from kml_export import *
from PIL import Image, ImageTk
import pygame
import threading
import tkinter.font as font
import time

pygame.mixer.init()


class BotonRedondeado(tk.Canvas):
    def __init__(self, parent, width, height, border_radius, color, text='', text_color='black', command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0, relief="flat", 
                          highlightthickness=0, bg=parent.cget('bg'))
        self.command = command
        self.color = color
        self.text_color = text_color
        self.width = width
        self.height = height
        self.border_radius = border_radius
        
        # Configurar tamaño del canvas
        self.configure(width=width, height=height)
        
        # Dibujar el botón redondeado
        self._dibujar_boton()
        
        # Añadir texto
        self.font = font.Font(size=14, family='Arial', weight="bold")
        self.create_text(width/2, height/2, text=text, fill=text_color, 
                        font=self.font, justify='center')
        
        # Eventos de clic
        self.bind("<Button-1>", self._on_click)
    
    def _dibujar_boton(self):
        # Dibujar las esquinas redondeadas usando arcos
        rad = 2 * self.border_radius
        
        # Esquinas redondeadas
        self.create_arc((0, rad, rad, 0), start=90, extent=90, 
                       fill=self.color, outline=self.color)
        self.create_arc((self.width-rad, 0, self.width, rad), start=0, extent=90, 
                       fill=self.color, outline=self.color)
        self.create_arc((self.width, self.height-rad, self.width-rad, self.height), 
                       start=270, extent=90, fill=self.color, outline=self.color)
        self.create_arc((0, self.height-rad, rad, self.height), start=180, extent=90, 
                       fill=self.color, outline=self.color)
        
        # Rectángulos para completar el botón
        self.create_rectangle(self.border_radius, 0, self.width-self.border_radius, 
                            self.height, fill=self.color, outline=self.color)
        self.create_rectangle(0, self.border_radius, self.width, 
                            self.height-self.border_radius, fill=self.color, outline=self.color)
    
    def _on_click(self, event):
        if self.command:
            self.command()

# Inicializar pygame mixer
pygame.mixer.init()

def reproducir_sonido_y_cerrar():
    # Reproduce el sonido en un hilo para no bloquear la interfaz
    def play_and_quit():
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.load("jijijija.mp3")# Cambia por tu archivo de sonido
        pygame.mixer.music.play()
        # Espera a que termine el sonido antes de cerrar la ventana
        while pygame.mixer.music.get_busy():
            pass
        root.destroy()
    threading.Thread(target=play_and_quit, daemon=True).start()

root = tk.Tk()
root.title("El maravilloso trabajo del grupo CR7")
root.geometry("800x800")
root.configure(bg='white')  # Fondo para el canvas

imagen = Image.open("Adam.png")
imagen = imagen.resize((800, 800))
imagen_tk = ImageTk.PhotoImage(imagen)

# Mostrar la imagen de fondo
label_imagen = tk.Label(root, image=imagen_tk)
label_imagen.place(x=0, y=0, relwidth=1, relheight=1)

# Botón redondeado superpuesto sobre la imagen
boton_curvo = BotonRedondeado(
    parent=root,
    width=400,
    height=120,
    border_radius=100,
    color="#ffffff",
    text="Bienvenidos a nuestro proyecto\n\nPulse para CONTINUAR!",
    text_color="black",
    command=reproducir_sonido_y_cerrar
)
boton_curvo.place(x=120, y=250)

root.mainloop()

# Inicializar pygame mixer
pygame.mixer.init()
# Configurar volumen de la música al 15%
pygame.mixer.music.set_volume(0.25)

# Cargar y reproducir música de fondo
pygame.mixer.music.load('Menu 03.mp3')
pygame.mixer.music.play(-1)  # -1 

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Interface")
        self.root.geometry("1080x720")
        self.graph = Graph()
        self.show_only_airports = False
        
        # Variables para interacción con clicks
        self.click_mode = None  # 'add_node', 'add_segment', None
        self.selected_nodes = []  # Para almacenar nodos seleccionados para segmentos
        self.node_counter = 1  # Contador automático para nombres de nodos
        
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=3)  # Columna izquierda (60%)
        self.root.grid_columnconfigure(1, weight=2)  # Columna derecha (40%)
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1)
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=1)  # Columna izquierda (botones, menos espacio)
        self.root.grid_columnconfigure(1, weight=5)  # Columna derecha (gráfico, más espacio)
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
        
        # Frame para la columna izquierda con botones
        self.left_frame = tk.Frame(self.root, bg='#f0f0f0', relief='ridge', bd=2)
        self.left_frame.grid(row=0, column=0, rowspan=8, sticky='nsew', padx=5, pady=5)

        # Frame para botones de grafo
        self.graph_buttons_frame = tk.LabelFrame(self.left_frame, text="Grafo", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        self.graph_buttons_frame.pack(fill='x', padx=5, pady=(5, 2))

        # Frame para botones de espacio aéreo
        self.airspace_buttons_frame = tk.LabelFrame(self.left_frame, text="Espacio Aéreo", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        self.airspace_buttons_frame.pack(fill='x', padx=5, pady=(10, 5))

        # Título en la columna derecha
        self.info_label = tk.Label(self.right_frame, text="Visualización y Estado", 
                                  font=('Arial', 12, 'bold'), bg='#e8f4f8')
        self.info_label.grid(row=0, column=0, sticky='ew', pady=5)
        self.create_graph_buttons()
        self.create_airspace_buttons()
        boton_sorpresa = tk.Button(
            self.left_frame,
            text="Botón Sorpresa",
            command=abrir_sorpresa,
            font=('Arial', 10, 'bold'),
            bg="#ffde59",  
            fg="black",
            cursor="hand2"
        )
        boton_sorpresa.pack(side='bottom', fill='x', padx=10, pady=10)
        funcionalidades = tk.Button(
                self.left_frame,
                text="funcionalidades extra",
                command=funcionalidad,
                font=('Arial', 10, 'bold'),
                bg="#ffde59",  
                fg="black",
                cursor="hand2"
        )
        funcionalidades.pack(side='bottom', fill='x', padx=10, pady=10)

        # Frame para el gráfico
        self.plot_frame = tk.Frame(self.right_frame, bg='white', relief='sunken', bd=1)
        self.plot_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Configurar matplotlib
        self.figure = Figure(figsize=(4, 3), dpi=80, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Conectar evento de click
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press_pan)  # override
        self.canvas.mpl_connect('button_release_event', self.on_release_pan)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion_pan)
        
        # Área de texto para información
        self.info_text = tk.Text(self.right_frame, height=6, wrap='word', bg='white', 
                                relief='sunken', bd=1, font=('Arial', 8))
        self.info_text.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        
        # Botones en la columna izquierda
        
        # Mensaje inicial
        self.update_info("Sistema iniciado. Selecciona una opción del menú.")
        self.show_welcome_plot()


    def calculate_distance(self, node1, node2):
        return math.sqrt((node2.x - node1.x)**2 + (node2.y - node1.y)**2)

    def enable_add_node_mode(self):
        #Activa o desactiva el modo de añadir nodos por click
        if self.click_mode == 'add_node':
            self.click_mode = None
            self.selected_nodes = []
            self.update_info("Modo añadir nodo desactivado.")
            self.plot_graph_in_panel()
        else:
            self.click_mode = 'add_node'
            self.selected_nodes = []
            self.update_info("🖱️ Modo añadir nodo activado. Haz click en el gráfico para añadir un nodo.")
            self.update_info("Para salir del modo, selecciona otra opción o vuelve a pulsar este botón.")

    def enable_add_segment_mode(self):
        # Activa o desactiva el modo de añadir segmentos por click
        if self.click_mode == 'add_segment':
            self.click_mode = None
            self.selected_nodes = []
            self.update_info("Modo añadir segmento desactivado.")
            self.plot_graph_in_panel()
            return

        if len(self.graph.nodes) < 2:
            self.update_info("✗ Error: Necesitas al menos 2 nodos para crear un segmento")
            messagebox.showerror("Error", "Necesitas al menos 2 nodos para crear un segmento")
            return
            
        self.click_mode = 'add_segment'
        self.selected_nodes = []
        self.update_info("🖱️ Modo añadir segmento activado. Haz click en dos nodos para conectarlos.")
        self.update_info("Para salir del modo, selecciona otra opción o vuelve a pulsar este botón.")
        self.plot_graph_in_panel()

    def create_graph_buttons(self):
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
            ("Ver alcanzables desde nodo", self.show_reachability),
            ("Camino más corto entre nodos", self.show_shortest_path),
        ]
        for i, (text, command) in enumerate(buttons_config):
            btn = tk.Button(self.graph_buttons_frame, text=text, command=command, 
                font=('Arial', 8), relief='raised', bd=1, height=1, padx=2, pady=1)
            btn.pack(fill='x', padx=5, pady=2)

    def create_airspace_buttons(self):
        buttons_config = [
            ("Cargar espacio aéreo (3 archivos)", self.load_airspace),
            ("Mostrar vecinos NavPoint", self.show_neighbors_navpoint),
            ("Ver alcanzables desde NavPoint", self.show_reachables_navpoint),
            ("Mostrar mapa del espacio aéreo", self.plot_airspace),
            ("Camino más corto en el espacio aéreo", self.show_shortest_path_airspace),
            ("Exportar espacio aéreo a KML", self.export_airspace_kml),
            ("Exportar camino a KML", self.export_path_kml),
            ("🔁 Ver solo aeropuertos / todo", self.toggle_airspace_view),
        ]
        for i, (text, command) in enumerate(buttons_config):
            btn = tk.Button(self.airspace_buttons_frame, text=text, command=command, 
                font=('Arial', 8), relief='raised', bd=1, height=1, padx=2, pady=1)
            btn.pack(fill='x', padx=5, pady=2)
        
    
    def on_canvas_click(self, event):
        # Maneja los clicks en el canvas según el modo activo
        if event.inaxes is None:
            return
            
        if self.click_mode == 'add_node':
            self.add_node_by_click(event.xdata, event.ydata)
        elif self.click_mode == 'add_segment':
            self.select_node_for_segment(event.xdata, event.ydata)

    def enable_add_node_mode(self):
        # Activa el modo de añadir nodos por click
        self.click_mode = 'add_node'
        self.selected_nodes = []
        self.update_info("🖱️ Modo añadir nodo activado. Haz click en el gráfico para añadir un nodo.")
        self.update_info("Para salir del modo, selecciona otra opción.")

    def enable_add_segment_mode(self):
        # Activa el modo de añadir segmentos por click
        if len(self.graph.nodes) < 2:
            self.update_info("✗ Error: Necesitas al menos 2 nodos para crear un segmento")
            messagebox.showerror("Error", "Necesitas al menos 2 nodos para crear un segmento")
            return
            
        self.click_mode = 'add_segment' # Activa el modo de añadir segmentos
        self.selected_nodes = []
        self.update_info("🖱️ Modo añadir segmento activado. Haz click en dos nodos para conectarlos.")
        self.update_info("Para salir del modo, selecciona otra opción.")
        self.plot_graph_in_panel()

    def add_node_by_click(self, x, y):
        # Añade un nodo en las coordenadas del click
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
        # Selecciona nodos para crear un segmento
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
        # Crea un segmento con los nodos seleccionados
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
        # Limpia el área de gráfico
        self.figure.clear()
        self.canvas.draw()

    def show_welcome_plot(self):
        # Muestra un gráfico de bienvenida
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
        # Dibuja el grafo en el panel derecho con distancias en los segmentos
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
        # Dibuja un nodo y sus vecinos en el panel derecho con distancias
        node = next((n for n in self.graph.nodes if n.name == node_name), None)
        if not node:
            return False
            
        self.clear_plot()
        ax = self.figure.add_subplot(111)
        
        ax.scatter(node.x, node.y, s=150, c='red', edgecolors='black')
        ax.annotate(node.name, (node.x, node.y), xytext=(5, 5), 
                   textcoords='offset points', fontsize=10, fontweight='bold')
        
        for neighbor in node.neighbors: # Asumiendo que neighbor es un objeto Node
            ax.scatter(neighbor.x, neighbor.y, s=100, c='lightgreen', edgecolors='black')
            ax.annotate(neighbor.name, (neighbor.x, neighbor.y), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8)
            
            ax.plot([node.x, neighbor.x], [node.y, neighbor.y], 'g-', alpha=0.7, linewidth=2)
            
            distance = self.calculate_distance(node, neighbor)
            mid_x = (node.x + neighbor.x) / 2
            mid_y = (node.y + neighbor.y) / 2
            
            ax.annotate(f'{distance:.2f}', (mid_x, mid_y), fontsize=8, # añade distancia
                       ha='center', va='center', color='blue', fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.8))
        
        ax.set_title(f'Vecinos de {node_name}', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        self.canvas.draw()
        return True

    def plot_path_in_panel(self, path):
        # Dibuja un camino en el panel derecho con distancias
        if not path or not path.nodes:
            return
            
        self.clear_plot() # Limpia el área de gráfico
        ax = self.figure.add_subplot(111)
        
        for node in self.graph.nodes: # Asumiendo que graph tiene un atributo nodes
            ax.scatter(node.x, node.y, s=50, c='lightgray', edgecolors='gray', alpha=0.5)
        
        path_x = [node.x for node in path.nodes]
        path_y = [node.y for node in path.nodes]
        ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.8)
        
        total_distance = 0
        for i, node in enumerate(path.nodes): # Asumiendo que path tiene un atributo nodes
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
        # Dibuja el espacio aéreo en el panel derecho, mostrando distancias en los segmentos
        if not self.airspace:
            return False
            
        self.clear_plot()
        ax = self.figure.add_subplot(111)
        
        # Dibujar NavPoints
        # Dibujar NavPoints (con filtro de aeropuertos si es necesario)
        nav_x = []
        nav_y = []
        nav_labels = []
        for nav_id, nav_point in self.airspace.navPoints.items():
            is_airport = nav_id in self.airspace.airports

            if self.show_only_airports and not is_airport:
                continue

            ax.scatter(nav_point.longitude, nav_point.latitude, s=20, c='lightgray', alpha=0.5)
            nav_x.append(nav_point.longitude)
            nav_y.append(nav_point.latitude)
            nav_labels.append(nav_point.name)

        
        if nav_x:
            ax.scatter(nav_x, nav_y, s=30, c='blue', alpha=0.7, label='NavPoints')
            for i, label in enumerate(nav_labels):
                ax.annotate(label, (nav_x[i], nav_y[i]), xytext=(2, 2), 
                        textcoords='offset points', fontsize=6)
        
        # Dibujar aeropuertos
        # Dibujar aeropuertos
        aer_x = []
        aer_y = []
        aer_labels = []
        for aer_id in self.airspace.airports:
            nav_point = self.airspace.navPoints.get(aer_id)
            if nav_point:
                aer_x.append(nav_point.longitude)
                aer_y.append(nav_point.latitude)
                aer_labels.append(nav_point.name)


                if self.show_only_airports and nav_id not in self.airspace.airports:
                    continue  # Enseñar solo aeropuertos si está activado
                    ax.scatter(nav_point.longitude, nav_point.latitude, s=20, c='lightgray', alpha=0.5)
                
        if aer_x:
            ax.scatter(aer_x, aer_y, s=80, c='red', marker='s', alpha=0.8, label='Aeropuertos')
            for i, label in enumerate(aer_labels):
                ax.annotate(label, (aer_x[i], aer_y[i]), xytext=(2, 2), 
                        textcoords='offset points', fontsize=8, fontweight='bold')
        
        # Dibujar segmentos del espacio aéreo con distancias
        if not self.show_only_airports:
            for segment in self.airspace.segments:
                origin_id = segment.origin_number
                dest_id = segment.destination_number
                origin_point = self.airspace.navPoints.get(origin_id)
                dest_point = self.airspace.navPoints.get(dest_id)

                if origin_point and dest_point:
                    x1, y1 = origin_point.longitude, origin_point.latitude
                    x2, y2 = dest_point.longitude, dest_point.latitude
                    ax.plot([x1, x2], [y1, y2], 'gray', alpha=0.5, linewidth=1)

                    distance = haversine(origin_point.latitude, origin_point.longitude,
                                 dest_point.latitude, dest_point.longitude)
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    ax.annotate(f'{distance:.2f}', (mid_x, mid_y), fontsize=6,
                        ha='center', va='center', color='#333333', fontweight='normal',
                        bbox=dict(boxstyle="round,pad=0.05", facecolor='white', alpha=0.4, edgecolor='none'))

        ax.set_title('Espacio Aéreo', fontsize=10) # Título del gráfico
        ax.grid(True, alpha=0.3)
        if nav_x or aer_x:
            ax.legend()
        ax.axis('equal')
        self.canvas.draw()
        return True

    def plot_airspace_path_in_panel(self, path):
        # Dibuja un camino del espacio aéreo en el panel derecho
        if not path or not path.nodes:
            return

        self.clear_plot()
        ax = self.figure.add_subplot(111)

        # Dibujar todos los NavPoints en gris claro
        for nav_id, nav_point in self.airspace.navPoints.items():
            ax.scatter(nav_point.longitude, nav_point.latitude, s=20, c='lightgray', alpha=0.5)

        # Dibujar aeropuertos
        for aer_id, airport in self.airspace.airports.items():
            # Si tienes lat/lon en airport, usa eso; si no, busca el navpoint correspondiente
            nav_point = self.airspace.navPoints.get(aer_id)
            if nav_point:
                ax.scatter(nav_point.longitude, nav_point.latitude, s=60, c='lightcoral', marker='s', alpha=0.6)

        # Dibujar el camino
        path_x = [node.longitude for node in path.nodes]
        path_y = [node.latitude for node in path.nodes]
        ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.8)

        # Dibujar nodos del camino
        for i, node in enumerate(path.nodes):
            if i == 0:
                ax.scatter(node.longitude, node.latitude, s=100, c='green', edgecolors='black')
            elif i == len(path.nodes) - 1:
                ax.scatter(node.longitude, node.latitude, s=100, c='red', edgecolors='black')
            else:
                ax.scatter(node.longitude, node.latitude, s=80, c='orange', edgecolors='black')

            ax.annotate(str(node.number), (node.longitude, node.latitude), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8, fontweight='bold')

        ax.set_title(f'Camino en Espacio Aéreo (Costo: {path.cost:.2f})', fontsize=10) # Título del gráfico
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        self.canvas.draw()
    def export_path_kml(self):
        if not hasattr(self, 'last_path') or not self.last_path: # Verifica si hay un camino reciente
            self.update_info("✗ No hay camino reciente para exportar")
            messagebox.showerror("Error", "Primero genera un camino para exportar")
            return
        path = filedialog.asksaveasfilename(defaultextension=".kml", title="Guardar KML del camino")
        if path:
            export_path_to_kml(self.last_path, path)
            self.update_info(f"✓ Camino exportado a KML en: {path}") # Actualiza el mensaje de estado
            messagebox.showinfo("Exportado", f"Camino exportado a: {path}")
    def export_airspace_kml(self):
        if not self.airspace:
            self.update_info("✗ No hay espacio aéreo cargado para exportar")
            messagebox.showerror("Error", "No hay espacio aéreo cargado")
            return
        path = filedialog.asksaveasfilename(defaultextension=".kml", title="Guardar KML del espacio aéreo") 
        if path:
            export_airspace_to_kml(self.airspace, path)
            self.update_info(f"✓ Espacio aéreo exportado a KML en: {path}")
            messagebox.showinfo("Exportado", f"Espacio aéreo exportado a: {path}")
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
        self.play_audio("sonido/click1.wav")
        messagebox.showinfo("Info", "Grafo de ejemplo cargado")

    def load_file(self): # Carga un grafo desde un archivo
        filepath = filedialog.askopenfilename()
        if filepath:
            self.graph = LoadGraph(filepath)
            self.click_mode = None
            self.selected_nodes = []
            self.update_info(f"✓ Grafo cargado desde archivo: {filepath}")
            self.play_audio("sonido/click1.wav")
            messagebox.showinfo("Info", "Grafo cargado desde archivo")

    def save_file(self): # Guarda el grafo actual en un archivo
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            SaveGraph(self.graph, filepath)
            self.update_info(f"✓ Grafo guardado en: {filepath}")
            messagebox.showinfo("Info", "Grafo guardado correctamente")

    def plot_graph(self): # Muestra el grafo actual en el panel derecho
        self.click_mode = None
        self.selected_nodes = []
        self.plot_graph_in_panel()
        self.update_info("✓ Grafo visualizado en panel derecho")

    def plot_node(self): # Muestra los vecinos de un nodo específico en el panel derecho
        name = simpledialog.askstring("Nodo", "Nombre del nodo:")
        if name:
            self.click_mode = None
            self.selected_nodes = []
            if self.plot_node_neighbors_in_panel(name):
                self.update_info(f"✓ Vecinos del nodo '{name}' mostrados")
            else:
                self.update_info(f"✗ Error: Nodo '{name}' no encontrado")
                messagebox.showerror("Error", "Nodo no encontrado")

    def add_node_manual(self): # Añade un nodo manualmente con coordenadas
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
            self.plot_graph_in_panel()
        else:
            self.update_info(f"✗ Error: El nodo '{name}' ya existe")
            messagebox.showerror("Error", "El nodo ya existe")

    def add_segment_manual(self): # Añade un segmento manualmente entre dos nodos
        self.click_mode = None
        self.selected_nodes = []
        
        name = simpledialog.askstring("Nombre del segmento", "Introduce el nombre del segmento:") # nombre del segmento
        if not name:
            return
            
        origin = simpledialog.askstring("Origen", "Nombre del nodo de origen:")
        if not origin:
            return
            
        dest = simpledialog.askstring("Destino", "Nombre del nodo de destino:")
        if not dest:
            return
            
        if AddSegment(self.graph, name, origin, dest): # añade el segmento
            origin_node = next((n for n in self.graph.nodes if n.name == origin), None)
            dest_node = next((n for n in self.graph.nodes if n.name == dest), None)
            if origin_node and dest_node: # verifica que los nodos existen
                distance = self.calculate_distance(origin_node, dest_node)
            self.plot_graph_in_panel()
            self.update_info(f"✓ Segmento '{name}' añadido: {origin} → {dest}")
            self.update_info(f"  📏 Distancia: {distance:.2f} unidades")
        else:
            self.update_info(f"✗ Error al añadir segmento '{name}'")
            messagebox.showerror("Error", "Error al añadir segmento. Revisa nombres de nodos.")

    def delete_node(self): # Elimina un nodo del grafo
        self.click_mode = None
        self.selected_nodes = []
        
        name = simpledialog.askstring("Eliminar nodo", "Nombre del nodo a eliminar:")
        if name and DeleteNode(self.graph, name):
            self.update_info(f"✓ Nodo '{name}' eliminado")
            self.plot_graph_in_panel()  # Actualiza el gráfico tras eliminar
        else:
            self.update_info(f"✗ Error: Nodo '{name}' no encontrado")
            messagebox.showerror("Error", "Nodo no encontrado")

    def reset_graph(self): # Reinicia el grafo a un estado vacío
        self.graph = Graph()
        self.click_mode = None
        self.selected_nodes = []
        self.node_counter = 1
        self.show_welcome_plot()
        self.update_info("✓ Nuevo grafo creado (grafo vacío)")
        messagebox.showinfo("Info", "Grafo nuevo creado")

    def show_reachability(self): # Muestra los nodos alcanzables desde un nodo dado
        self.click_mode = None
        self.selected_nodes = []
        
        name = simpledialog.askstring("Alcanzables", "Nombre del nodo de origen:")
        node = next((n for n in self.graph.nodes if n.name == name), None)
        if not node:
            self.update_info(f"✗ Error: Nodo '{name}' no encontrado")
            messagebox.showerror("Error", "Nodo no encontrado") # mensaje de error
            return
        reached = set()
        stack = [node]
        while stack: # DFS para encontrar nodos alcanzables
            current = stack.pop()
            if current not in reached:
                reached.add(current)
                stack.extend(n for n in current.neighbors if n not in reached)
        path = Path()
        for n in reached:
            AddNodeToPath(path, n)
        self.plot_path_in_panel(path)
        self.update_info(f"✓ Nodos alcanzables desde '{name}': {len(reached)} nodos")

    def show_shortest_path(self): # Muestra el camino más corto entre dos nodos
        self.click_mode = None
        self.selected_nodes = []

        origin = simpledialog.askstring("Camino mínimo", "Nodo de origen:")
        destination = simpledialog.askstring("Camino mínimo", "Nodo de destino:")
        # Depuración: mostrar nodos existentes
        self.update_info(f"Nodos disponibles: {[n.name for n in self.graph.nodes]}")
        self.update_info(f"Buscando camino de '{origin}' a '{destination}'")
        path = FindShortestPath(self.graph, origin, destination)
        if path:
            self.last_path = path
            self.plot_path_in_panel(path)
            self.update_info(f"✓ Camino más corto encontrado: {origin} → {destination}")
        else:
            self.update_info(f"✗ No existe camino entre '{origin}' y '{destination}'")
            messagebox.showinfo("Sin camino", "No existe un camino entre los nodos seleccionados.")
    # Métodos del espacio aéreo corregidos
    def load_airspace(self):
        try:
            nav = filedialog.askopenfilename(title="Selecciona archivo _nav.txt")
            if not nav:
                return
                
            seg = filedialog.askopenfilename(title="Selecciona archivo _seg.txt")
            if not seg:
                return
                
            aer = filedialog.askopenfilename(title="Selecciona archivo _aer.txt")
            if not aer:
                return
                
            self.airspace = AirSpace()
            self.airspace.load_points(nav)
            self.airspace.load_segments(seg)
            self.airspace.load_airports(aer)
            print("Aeropuertos cargados:")
            for a in self.airspace.airports:
                print(f" - {a}")
            
            self.update_info("✓ Espacio aéreo cargado correctamente")
            self.update_info(f"  - NavPoints: {len(self.airspace.navPoints)} puntos")
            self.update_info(f"  - Segmentos: {len(self.airspace.segments)} conexiones")
            self.update_info(f"  - Aeropuertos: {len(self.airspace.airports)} aeropuertos")
            messagebox.showinfo("Cargado", "Espacio aéreo cargado correctamente")
            
        except Exception as e:
            self.update_info(f"✗ Error al cargar espacio aéreo: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar espacio aéreo: {str(e)}")

    def show_neighbors_navpoint(self): # Muestra los vecinos de un NavPoint
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

    def show_reachables_navpoint(self): # Muestra los NavPoints alcanzables desde un NavPoint dado
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

    def plot_airspace(self): # Muestra el espacio aéreo en el panel derecho
        if not self.airspace:
            self.update_info("✗ Error: No hay espacio aéreo cargado")
            messagebox.showerror("Error", "No hay espacio aéreo cargado")
            return
        
        if self.plot_airspace_in_panel():
            self.update_info("✓ Mapa del espacio aéreo visualizado")
        else:
            self.update_info("✗ Error al visualizar espacio aéreo")

    def show_shortest_path_airspace(self): # Muestra el camino más corto en el espacio aéreo entre dos NavPoints
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
                self.last_path = found

            else:
                self.update_info(f"✗ No se encontró camino entre {origin_id} y {destination_id}")
                messagebox.showinfo("Sin camino", "No se encontró un camino entre los puntos seleccionados.")
        except Exception as e:
            self.update_info(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")

    def on_scroll(self, event): # Maneja el zoom con la rueda del ratón
        ax = self.figure.gca()
        xdata, ydata = event.xdata, event.ydata
        if xdata is None or ydata is None:
            return

        scale_factor = 1.2 if event.button == 'down' else 0.8

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        new_xlim = [xdata - (xdata - xlim[0]) * scale_factor,
                    xdata + (xlim[1] - xdata) * scale_factor]
        new_ylim = [ydata - (ydata - ylim[0]) * scale_factor,
                    ydata + (ylim[1] - ydata) * scale_factor]

        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        self.canvas.draw_idle()

    def on_press_pan(self, event): # Inicia el modo de panorámica al presionar el botón izquierdo del ratón
        ax = self.figure.gca()
        if event.button == 1 and event.inaxes:
            self._pan_start = (event.xdata, event.ydata)
            self._xlim_on_press = ax.get_xlim()
            self._ylim_on_press = ax.get_ylim()

    def on_motion_pan(self, event): # Actualiza la vista al mover el ratón mientras se mantiene presionado el botón izquierdo
        ax = self.figure.gca()
        if not hasattr(self, '_pan_start') or event.xdata is None or event.ydata is None:
            return
        dx = self._pan_start[0] - event.xdata
        dy = self._pan_start[1] - event.ydata
        ax.set_xlim(self._xlim_on_press[0] + dx, self._xlim_on_press[1] + dx)
        ax.set_ylim(self._ylim_on_press[0] + dy, self._ylim_on_press[1] + dy)
        self.canvas.draw_idle()

    def on_release_pan(self, event): # Finaliza el modo de panorámica al soltar el botón izquierdo del ratón
        self._pan_start = None

    def toggle_airspace_view(self): # Alterna entre mostrar solo aeropuertos o todos los puntos del espacio aéreo
        self.show_only_airports = not self.show_only_airports
        status = "solo aeropuertos" if self.show_only_airports else "todos los puntos"
        self.update_info(f"🔁 Mostrando: {status}")
        self.plot_airspace()


if __name__ == '__main__':
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
