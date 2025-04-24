import tkinter as tk
from tkinter import messagebox
from graph import *
from path import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Initialize GUI ---
root = tk.Tk()
root.title("Airspace Graph Explorer")

# Create the default graph
graph = CreateGraph_1()
node_names = [node.name for node in graph.nodes]

# --- Create Matplotlib Figure ---
fig, ax = plt.subplots(figsize=(6, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

def redraw_plot(draw_func):
    ax.clear()
    draw_func()
    canvas.draw()

# --- Plot Buttons ---
frame_top = tk.Frame(root)
frame_top.pack()

tk.Button(frame_top, text="Show Example Graph", command=lambda: redraw_plot(lambda: Plot(graph))).pack(side=tk.LEFT, padx=5)

tk.Button(frame_top, text="Show Node C Neighbors", command=lambda: redraw_plot(lambda: PlotNode(graph, "C"))).pack(side=tk.LEFT, padx=5)

# --- Reachability UI ---
tk.Label(root, text="Reachability from node:").pack()
reachability_var = tk.StringVar(value=node_names[0])
tk.OptionMenu(root, reachability_var, *node_names).pack()

def on_reachability():
    selected = reachability_var.get()
    if not selected:
        messagebox.showerror("Error", "Please select a node.")
        return
    redraw_plot(lambda: PlotReachability(graph, selected))

tk.Button(root, text="Show Reachable Nodes", command=on_reachability).pack(pady=5)

# --- Shortest Path UI ---
tk.Label(root, text="Shortest Path - Origin:").pack()
origin_var = tk.StringVar(value=node_names[0])
tk.OptionMenu(root, origin_var, *node_names).pack()

tk.Label(root, text="Destination:").pack()
dest_var = tk.StringVar(value=node_names[1])
tk.OptionMenu(root, dest_var, *node_names).pack()

def on_shortest_path():
    orig = origin_var.get()
    dest = dest_var.get()
    if orig == dest:
        messagebox.showerror("Error", "Origin and destination must be different.")
        return
    path = FindShortestPath(graph, orig, dest)
    if path:
        redraw_plot(lambda: PlotPath(graph, path))
    else:
        messagebox.showinfo("No Path", "There is no path between these nodes.")

tk.Button(root, text="Find Shortest Path", command=on_shortest_path).pack(pady=5)

# --- Launch App ---
root.mainloop()

