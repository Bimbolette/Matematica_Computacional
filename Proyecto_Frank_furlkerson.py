import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import os
from collections import defaultdict, deque

class FordFulkersonApp:
    def __init__(self, root):
        self.root = root
        self.matriz_capacidad = None
        self.num_nodos = 0
        self.rutas_encontradas = []
        
    def mostrar_presentacion(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both")
        
        titulo = tk.Label(
            frame_principal,
            text="Curso: Matemática Computacional",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        titulo.pack(pady=20)
        
        proyecto = tk.Label(
            frame_principal,
            text="Proyecto: Flujo Máximo con Algoritmo de Ford-Fulkerson",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        )
        proyecto.pack(pady=10)
        
        integrantes_frame = tk.Frame(frame_principal, bg="#f0f0f0")
        integrantes_frame.pack(pady=20)
        
        integrantes = [
            "Integrante 1: Leonardo Williams Chavez Corrales",
            "Integrante 2: Carlos Alberto Masias Espinoza",
            "Integrante 3: Andy Alfredo Hipolito Salcedo Muñoz",
            "Integrante 4: Joaquín Estuardo Valera Herrera",
            "Integrante 5: Piero Benjamin Acevedo Chavez"
        ]
        
        for i in integrantes:
            lbl = tk.Label(integrantes_frame, text=i, font=("Arial", 14), bg="#f0f0f0")
            lbl.pack(anchor="center", pady=2)
        
        boton = tk.Button(
            frame_principal,
            text="Ingresar a la Aplicación",
            font=("Arial", 18, "bold"),
            bg="#4CAF50", fg="white",
            padx=30, pady=15,
            command=self.mostrar_menu_principal
        )
        boton.pack(pady=40)
    
    def mostrar_menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both")
        
        titulo = tk.Label(
            frame_principal,
            text="Aplicación de Flujo Máximo",
            font=("Arial", 28, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        titulo.pack(pady=40)
        
        botones_frame = tk.Frame(frame_principal, bg="#f0f0f0")
        botones_frame.pack(expand=True)
        
        btn1 = tk.Button(
            botones_frame,
            text="1. Ingresar Matriz de Conexiones",
            font=("Arial", 16, "bold"),
            bg="#3498db", fg="white",
            width=35, height=2,
            command=self.ingresar_matriz
        )
        btn1.pack(pady=15)
        
        btn2 = tk.Button(
            botones_frame,
            text="2. Mostrar Matriz Actual",
            font=("Arial", 16, "bold"),
            bg="#9b59b6", fg="white",
            width=35, height=2,
            command=self.mostrar_matriz
        )
        btn2.pack(pady=15)
        
        btn3 = tk.Button(
            botones_frame,
            text="3. Calcular Flujo Máximo",
            font=("Arial", 16, "bold"),
            bg="#e74c3c", fg="white",
            width=35, height=2,
            command=self.calcular_flujo_maximo
        )
        btn3.pack(pady=15)
        
        btn4 = tk.Button(
            botones_frame,
            text="4. Salir",
            font=("Arial", 16, "bold"),
            bg="#95a5a6", fg="white",
            width=35, height=2,
            command=self.pantalla_despedida
        )
        btn4.pack(pady=15)
    
    def ingresar_matriz(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both", padx=20, pady=20)
        
        titulo = tk.Label(
            frame_principal,
            text="Ingresar Matriz de Capacidades",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        titulo.pack(pady=20)
        
        frame_nodos = tk.Frame(frame_principal, bg="#f0f0f0")
        frame_nodos.pack(pady=20)
        
        tk.Label(
            frame_nodos,
            text="Número de nodos (almacenes):",
            font=("Arial", 14),
            bg="#f0f0f0"
        ).pack(side="left", padx=10)
        
        entry_nodos = tk.Entry(frame_nodos, font=("Arial", 14), width=10)
        entry_nodos.pack(side="left")
        
        def crear_matriz():
            try:
                n = int(entry_nodos.get())
                if n < 8 or n > 16:
                    messagebox.showerror("Error", "El número de nodos debe estar entre 8 y 16")
                    return
                
                self.num_nodos = n
                self.mostrar_formulario_matriz(n)
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

        def generar_matriz_aleatoria():
            try:
                n = int(entry_nodos.get())
                if n < 8 or n > 16:
                    messagebox.showerror("Error", "El número de nodos debe estar entre 8 y 16")
                    return
                
                self.num_nodos = n
                self.crear_matriz_aleatoria(n)
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")
        
        botones_frame = tk.Frame(frame_principal, bg="#f0f0f0")
        botones_frame.pack(pady=20)
        
        btn_crear = tk.Button(
            botones_frame,
            text="Crear Matriz Manual",
            font=("Arial", 14, "bold"),
            bg="#27ae60", fg="white",
            padx=30, pady=15,
            command=crear_matriz
        )
        btn_crear.pack(pady=10)
        
        btn_random = tk.Button(
            botones_frame,
            text="Generar Matriz Aleatoria",
            font=("Arial", 14, "bold"),
            bg="#e67e22", fg="white",
            padx=30, pady=15,
            command=generar_matriz_aleatoria
        )
        btn_random.pack(pady=10)
        
        desc = tk.Label(
            frame_principal,
            text="La matriz aleatoria generará conexiones y flujos automáticamente",
            font=("Arial", 11, "italic"),
            bg="#f0f0f0",
            fg="#555"
        )
        desc.pack(pady=10)
        
        btn_volver = tk.Button(
            frame_principal,
            text="Volver al Menú",
            font=("Arial", 12),
            bg="#95a5a6", fg="white",
            padx=20, pady=10,
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(side="bottom", pady=20)
    
    def crear_matriz_aleatoria(self, n):
        """Genera una matriz de capacidades aleatoria"""
        import random
        
        matriz = [[0 for _ in range(n)] for _ in range(n)]
        
        num_conexiones_fuente = random.randint(1, min(3, n-1))
        nodos_conectados = random.sample(range(1, n), num_conexiones_fuente)
        
        for nodo in nodos_conectados:
            matriz[0][nodo] = random.randint(1, 15)
        
        num_conexiones_sumidero = random.randint(1, min(3, n-1))
        nodos_hacia_sumidero = random.sample(range(1, n-1), min(num_conexiones_sumidero, n-2))
        
        for nodo in nodos_hacia_sumidero:
            matriz[nodo][n-1] = random.randint(1, 15)
        
        for i in range(1, n-1):
            num_conexiones = random.randint(0, min(3, n-i-1))
            if num_conexiones > 0:
                posibles_destinos = list(range(i+1, n))
                destinos = random.sample(posibles_destinos, num_conexiones)
                
                for destino in destinos:
                    if matriz[i][destino] == 0:  # Evitar sobrescribir
                        matriz[i][destino] = random.randint(1, 15)
        
        conexiones_extra = random.randint(0, n)
        for _ in range(conexiones_extra):
            i = random.randint(0, n-2)
            j = random.randint(i+1, n-1)
            if matriz[i][j] == 0 and i != j:
                matriz[i][j] = random.randint(1, 15)
        
        self.matriz_capacidad = matriz
        messagebox.showinfo("Éxito", f"Matriz aleatoria generada con {n} nodos")
        self.mostrar_matriz()
    
    def mostrar_formulario_matriz(self, n):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both")
        
        titulo = tk.Label(
            frame_principal,
            text=f"Matriz de Capacidades ({n} nodos)",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0"
        )
        titulo.pack(pady=10)
        
        instrucciones = tk.Label(
            frame_principal,
            text="Ingrese las capacidades de flujo entre nodos (0 si no hay conexión)\nNodo 1 es la fuente, Nodo {} es el sumidero".format(n),
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#555"
        )
        instrucciones.pack(pady=5)
        
        canvas = tk.Canvas(frame_principal, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        entries = []
        
        tk.Label(scrollable_frame, text="", bg="#f0f0f0", width=8).grid(row=0, column=0)
        for j in range(n):
            tk.Label(
                scrollable_frame,
                text=f"Nodo {j+1}",
                font=("Arial", 10, "bold"),
                bg="#f0f0f0",
                width=8
            ).grid(row=0, column=j+1, padx=2, pady=2)
        
        for i in range(n):
            tk.Label(
                scrollable_frame,
                text=f"Nodo {i+1}",
                font=("Arial", 10, "bold"),
                bg="#f0f0f0",
                width=8
            ).grid(row=i+1, column=0, padx=2, pady=2)
            
            fila = []
            for j in range(n):
                entry = tk.Entry(scrollable_frame, width=8, font=("Arial", 10))
                entry.grid(row=i+1, column=j+1, padx=2, pady=2)
                entry.insert(0, "0")
                if i == j:
                    entry.config(state="disabled", bg="#ddd")
                fila.append(entry)
            entries.append(fila)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        def guardar_matriz():
            try:
                matriz = []
                for i in range(n):
                    fila = []
                    for j in range(n):
                        if i == j:
                            fila.append(0)
                        else:
                            val = int(entries[i][j].get())
                            if val < 0:
                                messagebox.showerror("Error", "Las capacidades deben ser >= 0")
                                return
                            fila.append(val)
                    matriz.append(fila)
                
                self.matriz_capacidad = matriz
                messagebox.showinfo("Éxito", "Matriz guardada correctamente")
                self.mostrar_menu_principal()
            except ValueError:
                messagebox.showerror("Error", "Ingrese solo números enteros")
        
        frame_botones = tk.Frame(frame_principal, bg="#f0f0f0")
        frame_botones.pack(side="bottom", pady=20)
        
        btn_guardar = tk.Button(
            frame_botones,
            text="Guardar Matriz",
            font=("Arial", 14, "bold"),
            bg="#27ae60", fg="white",
            padx=30, pady=10,
            command=guardar_matriz
        )
        btn_guardar.pack(side="left", padx=10)
        
        btn_volver = tk.Button(
            frame_botones,
            text="Volver",
            font=("Arial", 14),
            bg="#95a5a6", fg="white",
            padx=30, pady=10,
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(side="left", padx=10)
    
    def mostrar_matriz(self):
        if self.matriz_capacidad is None:
            messagebox.showwarning("Advertencia", "Primero debe ingresar una matriz")
            return
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both", padx=20, pady=20)
        
        titulo = tk.Label(
            frame_principal,
            text="Matriz de Capacidades Actual",
            font=("Arial", 22, "bold"),
            bg="#f0f0f0"
        )
        titulo.pack(pady=20)
        
        matriz_frame = tk.Frame(frame_principal, bg="white", relief="solid", borderwidth=2)
        matriz_frame.pack(pady=10)
        
        n = len(self.matriz_capacidad)
        
        tk.Label(matriz_frame, text="", bg="white", width=8).grid(row=0, column=0, padx=5, pady=5)
        for j in range(n):
            tk.Label(
                matriz_frame,
                text=f"N{j+1}",
                font=("Arial", 11, "bold"),
                bg="#3498db",
                fg="white",
                width=6
            ).grid(row=0, column=j+1, padx=2, pady=2)
        
        for i in range(n):
            tk.Label(
                matriz_frame,
                text=f"N{i+1}",
                font=("Arial", 11, "bold"),
                bg="#3498db",
                fg="white",
                width=6
            ).grid(row=i+1, column=0, padx=2, pady=2)
            
            for j in range(n):
                valor = self.matriz_capacidad[i][j]
                bg_color = "#ecf0f1" if i == j else "white"
                tk.Label(
                    matriz_frame,
                    text=str(valor),
                    font=("Arial", 11),
                    bg=bg_color,
                    width=6,
                    relief="solid",
                    borderwidth=1
                ).grid(row=i+1, column=j+1, padx=2, pady=2)
        
        btn_grafo = tk.Button(
            frame_principal,
            text="Mostrar Grafo de Conexiones",
            font=("Arial", 14, "bold"),
            bg="#e67e22", fg="white",
            padx=30, pady=15,
            command=self.mostrar_grafo
        )
        btn_grafo.pack(pady=20)
        
        btn_volver = tk.Button(
            frame_principal,
            text="Volver al Menú",
            font=("Arial", 12),
            bg="#95a5a6", fg="white",
            padx=20, pady=10,
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(side="bottom", pady=10)
    
    def mostrar_grafo(self):
        if self.matriz_capacidad is None:
            messagebox.showwarning("Advertencia", "No hay matriz para mostrar")
            return
            
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both")
        
        titulo = tk.Label(
            frame_principal,
            text="Grafo de Conexiones",
            font=("Arial", 22, "bold"),
            bg="#f0f0f0"
        )
        titulo.pack(pady=20)
        
        canvas = tk.Canvas(frame_principal, bg="white", width=900, height=550)
        canvas.pack(pady=20)
        
        n = len(self.matriz_capacidad)
        
        import math
        posiciones = []
        
        if n <= 2:
            posiciones = [(150, 275), (750, 275)]
        elif n == 3:
            posiciones = [(150, 275), (450, 275), (750, 275)]
        elif n == 4:
            posiciones = [(200, 200), (200, 350), (700, 200), (700, 350)]
        elif n == 5:
            posiciones = [(150, 275), (350, 180), (350, 370), (650, 180), (650, 370)]
        elif n == 6:
            posiciones = [(150, 200), (150, 350), (450, 180), (450, 370), (750, 200), (750, 350)]
        else:
            layers = 3
            nodes_per_layer = (n + layers - 1) // layers
            x_spacing = 700 / (layers + 1)
            
            for i in range(n):
                layer = i // nodes_per_layer
                pos_in_layer = i % nodes_per_layer
                nodes_in_this_layer = min(nodes_per_layer, n - layer * nodes_per_layer)
                
                x = 150 + (layer + 1) * x_spacing
                y_spacing = 400 / (nodes_in_this_layer + 1)
                y = 100 + (pos_in_layer + 1) * y_spacing
                
                posiciones.append((x, y))
        
        for i in range(n):
            for j in range(n):
                if self.matriz_capacidad[i][j] > 0:
                    x1, y1 = posiciones[i]
                    x2, y2 = posiciones[j]
                    
                    dx = x2 - x1
                    dy = y2 - y1
                    dist = math.sqrt(dx*dx + dy*dy)
                    
                    if dist > 0:
                        ratio = 30 / dist
                        x1_adj = x1 + dx * ratio
                        y1_adj = y1 + dy * ratio
                        x2_adj = x2 - dx * ratio
                        y2_adj = y2 - dy * ratio
                    else:
                        x1_adj, y1_adj = x1, y1
                        x2_adj, y2_adj = x2, y2
                    
                    mx = x1 + dx * 0.4
                    my = y1 + dy * 0.4
                    
                    canvas.create_line(x1_adj, y1_adj, x2_adj, y2_adj, arrow=tk.LAST, 
                                     width=2, fill="#5271ff", arrowshape=(12,15,6), smooth=True)
                    
                    canvas.create_rectangle(mx-18, my-12, mx+18, my+12, fill="white", outline="")
                    canvas.create_text(
                        mx, my,
                        text=str(self.matriz_capacidad[i][j]),
                        font=("Arial", 11, "bold"),
                        fill="#000000"
                    )
        
        for i, (x, y) in enumerate(posiciones):
            if i == 0:
                color = "#b8c5ff" 
                outline_color = "#5271ff"
            elif i == n-1:
                color = "#b8c5ff" 
                outline_color = "#5271ff"
            else:
                color = "#b8c5ff"  
                outline_color = "#5271ff"
            
            canvas.create_oval(x-30, y-30, x+30, y+30, fill=color, outline=outline_color, width=3)
            canvas.create_text(x, y, text=f"{i+1}", font=("Arial", 18, "bold"), fill="#000000")
        
        leyenda_frame = tk.Frame(frame_principal, bg="#f0f0f0")
        leyenda_frame.pack(pady=10)
        
        tk.Label(leyenda_frame, text="● Fuente", font=("Arial", 12), bg="#f0f0f0", fg="#e74c3c").pack(side="left", padx=10)
        tk.Label(leyenda_frame, text="● Sumidero", font=("Arial", 12), bg="#f0f0f0", fg="#27ae60").pack(side="left", padx=10)
        tk.Label(leyenda_frame, text="● Nodo intermedio", font=("Arial", 12), bg="#f0f0f0", fg="#3498db").pack(side="left", padx=10)
        
        botones_frame = tk.Frame(frame_principal, bg="#f0f0f0")
        botones_frame.pack(pady=20)
        
        btn_matriz = tk.Button(
            botones_frame,
            text="Volver a Matriz",
            font=("Arial", 12, "bold"),
            bg="#3498db", fg="white",
            padx=20, pady=10,
            command=self.mostrar_matriz
        )
        btn_matriz.pack(side="left", padx=10)
        
        btn_menu = tk.Button(
            botones_frame,
            text="Menú Principal",
            font=("Arial", 12, "bold"),
            bg="#95a5a6", fg="white",
            padx=20, pady=10,
            command=self.mostrar_menu_principal
        )
        btn_menu.pack(side="left", padx=10)
    
    def bfs(self, grafo_residual, fuente, sumidero, padre):
        """BFS para encontrar camino aumentante"""
        n = len(grafo_residual)
        visitado = [False] * n
        cola = deque([fuente])
        visitado[fuente] = True
        
        while cola:
            u = cola.popleft()
            
            for v in range(n):
                if not visitado[v] and grafo_residual[u][v] > 0:
                    cola.append(v)
                    visitado[v] = True
                    padre[v] = u
                    if v == sumidero:
                        return True
        return False
    
    def ford_fulkerson(self):
        """Implementación del algoritmo de Ford-Fulkerson"""
        n = len(self.matriz_capacidad)
        fuente = 0
        sumidero = n - 1
        
        grafo_residual = [fila[:] for fila in self.matriz_capacidad]
        
        padre = [-1] * n
        flujo_maximo = 0
        self.rutas_encontradas = []
        
        while self.bfs(grafo_residual, fuente, sumidero, padre):
            flujo_camino = float('inf')
            s = sumidero
            camino = []
            
            while s != fuente:
                camino.append(s)
                flujo_camino = min(flujo_camino, grafo_residual[padre[s]][s])
                s = padre[s]
            camino.append(fuente)
            camino.reverse()
            
            v = sumidero
            while v != fuente:
                u = padre[v]
                grafo_residual[u][v] -= flujo_camino
                grafo_residual[v][u] += flujo_camino
                v = padre[v]
            
            flujo_maximo += flujo_camino
            
            ruta_str = "-".join(str(nodo + 1) for nodo in camino)
            self.rutas_encontradas.append((ruta_str, flujo_camino))
            
            padre = [-1] * n
        
        return flujo_maximo
    
    def calcular_flujo_maximo(self):
        if self.matriz_capacidad is None:
            messagebox.showwarning("Advertencia", "Primero debe ingresar una matriz")
            return
        
        flujo_max = self.ford_fulkerson()
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both", padx=20, pady=20)
        
        titulo = tk.Label(
            frame_principal,
            text="Resultado: Flujo Máximo",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        titulo.pack(pady=20)
        
        resultado_frame = tk.Frame(frame_principal, bg="#27ae60", relief="solid", borderwidth=3)
        resultado_frame.pack(pady=20)
        
        tk.Label(
            resultado_frame,
            text=f"Flujo Máximo Total: {flujo_max}",
            font=("Arial", 28, "bold"),
            bg="#27ae60",
            fg="white",
            padx=40,
            pady=20
        ).pack()
        
        tk.Label(
            frame_principal,
            text="Caminos Aumentantes Utilizados:",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        rutas_text = scrolledtext.ScrolledText(
            frame_principal,
            width=70,
            height=15,
            font=("Courier", 12),
            bg="white"
        )
        rutas_text.pack(pady=10)
        
        for i, (ruta, flujo) in enumerate(self.rutas_encontradas, 1):
            rutas_text.insert(tk.END, f"Camino {i}: {ruta}  →  Flujo: {flujo}\n")
        
        rutas_text.config(state="disabled")
        
        btn_volver = tk.Button(
            frame_principal,
            text="Volver al Menú",
            font=("Arial", 14, "bold"),
            bg="#95a5a6", fg="white",
            padx=30, pady=15,
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def pantalla_despedida(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#2c3e50")
        frame_principal.pack(expand=True, fill="both")
        
        tk.Label(
            frame_principal,
            text="¡Gracias por usar la aplicación!",
            font=("Arial", 32, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=50)
        
        tk.Label(
            frame_principal,
            text="Proyecto de Matemática Computacional",
            font=("Arial", 18),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(pady=20)
        
        tk.Label(
            frame_principal,
            text="Algoritmo de Ford-Fulkerson",
            font=("Arial", 16),
            bg="#2c3e50",
            fg="#95a5a6"
        ).pack(pady=10)
        
        btn_cerrar = tk.Button(
            frame_principal,
            text="Cerrar Aplicación",
            font=("Arial", 16, "bold"),
            bg="#e74c3c", fg="white",
            padx=40, pady=20,
            command=self.root.quit
        )
        btn_cerrar.pack(pady=50)
        
        btn_volver = tk.Button(
            frame_principal,
            text="Volver al Menú",
            font=("Arial", 12),
            bg="#3498db", fg="white",
            padx=20, pady=10,
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(pady=10)


def main():
    root = tk.Tk()
    root.title("Flujo Máximo - Ford-Fulkerson")
    root.attributes("-fullscreen", True)
    root.configure(bg="#f0f0f0")
    
    def toggle_fullscreen(event=None):
        state = not root.attributes("-fullscreen")
        root.attributes("-fullscreen", state)
        if not state:
            root.geometry("1000x700")
    
    root.bind("<Escape>", toggle_fullscreen)
    
    app = FordFulkersonApp(root)
    app.mostrar_presentacion()
    
    root.mainloop()

if __name__ == "__main__":
    main()