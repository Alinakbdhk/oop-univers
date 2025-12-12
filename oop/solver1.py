import tkinter as tk
import math
from tkinter import messagebox
from itertools import permutations


class DoGraph:
    def __init__(self, v, canvas, table_frame=None):
        self.v = v
        self.canvas = canvas
        self.table_frame = table_frame
        self.vertices = {}
        self.edges = []
        self.edge_creation = False
        self.first_vertex = None
        self.matrix_entries = []
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        if self.table_frame:
            self.create_adjacency_table()

    def create_adjacency_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.matrix_entries = []

        headers = [str(i + 1) for i in range(self.v)]

        for j in range(self.v):
            header_label = tk.Label(self.table_frame, text=headers[j], width=5,
                                    relief="solid", bg="lightgray", font=('Arial', 10, 'bold'))
            header_label.grid(row=0, column=j + 1, sticky="nsew")

        for i in range(self.v):
            header_label = tk.Label(self.table_frame, text=headers[i], width=5,
                                    relief="solid", bg="lightgray", font=('Arial', 10, 'bold'))
            header_label.grid(row=i + 1, column=0, sticky="nsew")

        for i in range(self.v):
            row_entries = []
            for j in range(self.v):
                if i == j:
                    entry = tk.Entry(self.table_frame, width=5, justify='center',
                                     state='disabled', disabledbackground='gray')
                    entry.insert(0, "0")
                else:
                    entry = tk.Entry(self.table_frame, width=5, justify='center')
                    entry.insert(0, "0")
                    vcmd = (self.table_frame.register(self.validate_number), '%P')
                    entry.config(validate="key", validatecommand=vcmd)

                    entry.bind('<FocusOut>', lambda e, row=i, col=j: self.sync_symmetric_cell(row, col))
                    entry.bind('<Return>', lambda e, row=i, col=j: self.sync_symmetric_cell(row, col))

                entry.grid(row=i + 1, column=j + 1, sticky="nsew")
                row_entries.append(entry)

            self.matrix_entries.append(row_entries)

        table_label = tk.Label(self.table_frame, text="Матрица смежности",
                               font=('Arial', 12, 'bold'))
        table_label.grid(row=self.v + 1, column=0, columnspan=self.v + 1, pady=5)

    def sync_symmetric_cell(self, row, col):
        if row == col:
            return

        value = self.matrix_entries[row][col].get()
        if value == "":
            value = "0"
            self.matrix_entries[row][col].delete(0, tk.END)
            self.matrix_entries[row][col].insert(0, value)

        self.matrix_entries[col][row].delete(0, tk.END)
        self.matrix_entries[col][row].insert(0, value)

    def validate_number(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def draw_v(self):
        self.canvas.delete("all")
        self.vertices = {}
        self.edges = []
        self.edge_creation = False
        self.first_vertex = None
        name_ver = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(self.v):
            angle = 2 * math.pi * i / self.v - math.pi / 2
            x = 150 + 80 * math.cos(angle)
            y = 150 + 80 * math.sin(angle)
            vertex_name = name_ver[i]
            self.vertices[vertex_name] = (x, y)
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='red', outline='darkred', width=2)
            self.canvas.create_text(x, y + 15, text=name_ver[i], font=('Arial', 12, 'bold'))

        if self.table_frame:
            self.create_adjacency_table()

    def enable_edge_creation(self):
        self.edge_creation = True
        self.first_vertex = None
        self.canvas.config(cursor="crosshair")

    def disable_edge_creation(self):
        self.edge_creation = False
        self.first_vertex = None
        self.canvas.config(cursor="")

    def on_canvas_click(self, event):
        if not self.edge_creation:
            return

        clicked_vertex = None
        min_distance = float('inf')

        for vertex, (x, y) in self.vertices.items():
            distance = ((x - event.x) ** 2 + (y - event.y) ** 2) ** 0.5
            if distance < min_distance and distance < 15:
                min_distance = distance
                clicked_vertex = vertex

        if clicked_vertex:
            if self.first_vertex is None:
                self.first_vertex = clicked_vertex
                x, y = self.vertices[clicked_vertex]
                self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6, outline='blue', width=2)
            else:
                if self.first_vertex != clicked_vertex:
                    edge_exists = False
                    for edge in self.edges:
                        if (edge[0] == self.first_vertex and edge[1] == clicked_vertex) or \
                                (edge[0] == clicked_vertex and edge[1] == self.first_vertex):
                            edge_exists = True
                            break

                    if not edge_exists:
                        x1, y1 = self.vertices[self.first_vertex]
                        x2, y2 = self.vertices[clicked_vertex]
                        edge_id = self.canvas.create_line(x1, y1, x2, y2, width=2, fill='black')
                        self.edges.append((self.first_vertex, clicked_vertex, edge_id))

                self.first_vertex = None
                self.redraw_vertices()

    def redraw_vertices(self):
        for vertex, (x, y) in self.vertices.items():
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='red', outline='darkred', width=2)
            self.canvas.create_text(x, y + 15, text=vertex, font=('Arial', 12, 'bold'))

    def delete_last_edge(self):
        if self.edges:
            last_edge = self.edges.pop()
            self.canvas.delete(last_edge[2])
            self.redraw_vertices()

    def get_table_graph(self):
        table_graph = {}
        for i in range(self.v):
            table_graph[str(i + 1)] = {}
            for j in range(self.v):
                value = self.matrix_entries[i][j].get()
                if value and value != "0":
                    table_graph[str(i + 1)][str(j + 1)] = int(value)
        return table_graph

    def get_visual_graph(self):
        visual_graph = {}
        for vertex in self.vertices:
            visual_graph[vertex] = set()

        for edge in self.edges:
            visual_graph[edge[0]].add(edge[1])
            visual_graph[edge[1]].add(edge[0])

        return visual_graph

    def calculate_degrees(self, graph):
        degrees = {}
        for vertex in graph:
            degrees[vertex] = len(graph[vertex])
        return degrees

    def find_isomorphism(self, table_graph, visual_graph):
        table_vertices = list(table_graph.keys())
        visual_vertices = list(visual_graph.keys())

        table_degrees = self.calculate_degrees(table_graph)
        visual_degrees = self.calculate_degrees(visual_graph)

        table_sorted = sorted(table_vertices, key=lambda x: table_degrees[x])
        visual_sorted = sorted(visual_vertices, key=lambda x: visual_degrees[x])

        table_degree_seq = [table_degrees[v] for v in table_sorted]
        visual_degree_seq = [visual_degrees[v] for v in visual_sorted]

        if table_degree_seq != visual_degree_seq:
            return None

        table_degree_groups = {}
        for v in table_sorted:
            deg = table_degrees[v]
            if deg not in table_degree_groups:
                table_degree_groups[deg] = []
            table_degree_groups[deg].append(v)

        visual_degree_groups = {}
        for v in visual_sorted:
            deg = visual_degrees[v]
            if deg not in visual_degree_groups:
                visual_degree_groups[deg] = []
            visual_degree_groups[deg].append(v)

        for deg in table_degree_groups:
            if deg not in visual_degree_groups or len(table_degree_groups[deg]) != len(visual_degree_groups[deg]):
                return None

        mappings = [{}]
        for deg in sorted(table_degree_groups.keys()):
            table_group = table_degree_groups[deg]
            visual_group = visual_degree_groups[deg]

            new_mappings = []
            for mapping in mappings:
                for visual_perm in permutations(visual_group):
                    new_mapping = mapping.copy()
                    for i, table_v in enumerate(table_group):
                        new_mapping[table_v] = visual_perm[i]
                    new_mappings.append(new_mapping)
            mappings = new_mappings

        for mapping in mappings:
            if self.check_isomorphism(table_graph, visual_graph, mapping):
                return mapping

        return None

    def check_isomorphism(self, table_graph, visual_graph, mapping):
        for table_v1 in table_graph:
            visual_v1 = mapping[table_v1]
            for table_v2 in table_graph[table_v1]:
                visual_v2 = mapping[table_v2]
                if visual_v2 not in visual_graph[visual_v1]:
                    return False
        return True

    def solve_problem(self):
        if self.v < 2 or self.v > 8:
            messagebox.showerror("Ошибка", "Количество вершин должно быть от 2 до 8")
            return

        table_graph = self.get_table_graph()
        visual_graph = self.get_visual_graph()

        mapping = self.find_isomorphism(table_graph, visual_graph)

        if not mapping:
            messagebox.showerror("Ошибка", "Не удалось найти соответствие между таблицей и графом")
            return

        self.show_solution_result(mapping)

    def show_solution_result(self, mapping):
        result_window = tk.Toplevel(root)
        result_window.title("Сопоставление вершин")
        result_window.geometry("400x300")

        result_text = "Сопоставление вершин таблицы и графа:\n\n"
        for table_vertex, graph_vertex in sorted(mapping.items()):
            result_text += f"Вершина {table_vertex} → {graph_vertex}\n"

        text_frame = tk.Frame(result_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Arial', 12))
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.insert(tk.END, result_text)
        text_widget.config(state=tk.DISABLED)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        close_button = tk.Button(result_window, text="Закрыть", command=result_window.destroy)
        close_button.pack(pady=10)

current_graph = None


def draw_vertices():
    global current_graph
    try:
        v = int(entry.get())
        if 2 <= v <= 8:
            current_graph = DoGraph(v, canvas, table_frame)
            current_graph.draw_v()
        else:
            messagebox.showerror("Ошибка", "Количество вершин должно быть от 2 до 8")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите целое число")


def enable_edge_mode():
    if current_graph:
        current_graph.enable_edge_creation()


def disable_edge_mode():
    if current_graph:
        current_graph.disable_edge_creation()


def delete_last_edge():
    if current_graph:
        current_graph.delete_last_edge()


def normal_mode():
    if current_graph:
        current_graph.disable_edge_creation()
        current_graph.canvas.bind("<Button-1>", current_graph.on_canvas_click)


def solve_problem():
    if current_graph:
        current_graph.solve_problem()
    else:
        messagebox.showwarning("Предупреждение", "Сначала постройте граф!")

root = tk.Tk()
root.title("Сопоставление вершин графа и таблицы")
root.geometry("1000x800")

frame = tk.Frame(root, bg='light blue')
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Количество вершин (2-8):")
label.pack(side=tk.LEFT)

entry = tk.Entry(frame, width=10)
entry.pack(side=tk.LEFT, padx=5)
entry.insert(0, "5")

button = tk.Button(frame, text="Построить вершины", command=draw_vertices)
button.pack(side=tk.LEFT, padx=5)

edge_frame = tk.Frame(root, bg='light blue')
edge_frame.pack(pady=10)

btn_create_edges = tk.Button(edge_frame, text="Режим создания рёбер", command=enable_edge_mode)
btn_create_edges.pack(side=tk.LEFT, padx=5)

btn_normal_mode = tk.Button(edge_frame, text="Обычный режим", command=normal_mode)
btn_normal_mode.pack(side=tk.LEFT, padx=5)

btn_delete_last = tk.Button(edge_frame, text="Удалить последнее ребро", command=delete_last_edge)
btn_delete_last.pack(side=tk.LEFT, padx=5)

btn_solve = tk.Button(edge_frame, text="Сопоставить вершины", command=solve_problem)
btn_solve.pack(side=tk.LEFT, padx=5)

main_frame = tk.Frame(root)
main_frame.pack(pady=10)

canvas = tk.Canvas(main_frame, width=400, height=400, bg='white')
canvas.pack(side=tk.LEFT, padx=10)

table_frame = tk.Frame(main_frame, bg='white')
table_frame.pack(side=tk.RIGHT, padx=10)

root.mainloop()