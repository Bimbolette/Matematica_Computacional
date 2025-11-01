import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
import os
from collections import defaultdict, deque
import math

class FordFulkersonApp:
    def __init__(self, root):
        self.root = root
        self.matriz_capacidad = None
        self.num_nodos = 0
        self.rutas_encontradas = []
        self.corte_minimo = []
        self.grafo_residual_final = None
        
        # Para el editor interactivo
        self.nodos_grafo = []
        self.aristas_grafo = []
        
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
            text="1. Crear Grafo Interactivamente",
            font=("Arial", 16, "bold"),
            bg="#3498db", fg="white",
            width=35, height=2,
            command=self.editor_interactivo
        )
        btn1.pack(pady=15)
        
        btn2 = tk.Button(
            botones_frame,
            text="2. Generar Grafo Aleatorio",
            font=("Arial", 16, "bold"),
            bg="#e67e22", fg="white",
            width=35, height=2,
            command=self.menu_grafo_aleatorio
        )
        btn2.pack(pady=15)
        
        btn3 = tk.Button(
            botones_frame,
            text="3. Mostrar Grafo Actual",
            font=("Arial", 16, "bold"),
            bg="#9b59b6", fg="white",
            width=35, height=2,
            command=self.mostrar_grafo
        )
        btn3.pack(pady=15)
        
        btn4 = tk.Button(
            botones_frame,
            text="4. Calcular Flujo Máximo",
            font=("Arial", 16, "bold"),
            bg="#e74c3c", fg="white",
            width=35, height=2,
            command=self.calcular_flujo_maximo
        )
        btn4.pack(pady=15)
        
        btn5 = tk.Button(
            botones_frame,
            text="5. Salir",
            font=("Arial", 16, "bold"),
            bg="#95a5a6", fg="white",
            width=35, height=2,
            command=self.pantalla_despedida
        )
        btn5.pack(pady=15)
    
    def editor_interactivo(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both")
        
        titulo = tk.Label(
            frame_principal,
            text="Editor Interactivo de Grafo",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        titulo.pack(pady=10)
        
        # Panel izquierdo: Controles
        frame_izq = tk.Frame(frame_principal, bg="#f0f0f0", width=300)
        frame_izq.pack(side="left", fill="both", padx=20, pady=10)
        
        # Sección: Nodos
        tk.Label(frame_izq, text="GESTIÓN DE NODOS", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        
        frame_nodos = tk.LabelFrame(frame_izq, text="Agregar Nodos", bg="#f0f0f0", font=("Arial", 11, "bold"))
        frame_nodos.pack(pady=10, padx=10, fill="x")
        
        tk.Label(frame_nodos, text="Cantidad de nodos:", bg="#f0f0f0").pack(pady=5)
        entry_num_nodos = tk.Entry(frame_nodos, font=("Arial", 12), width=10)
        entry_num_nodos.pack(pady=5)
        entry_num_nodos.insert(0, "8")
        
        def agregar_nodos():
            try:
                n = int(entry_num_nodos.get())
                if n < 2 or n > 16:
                    messagebox.showerror("Error", "El número de nodos debe estar entre 2 y 16")
                    return
                
                self.num_nodos = n
                self.nodos_grafo = list(range(n))
                self.aristas_grafo = []
                actualizar_vista()
                messagebox.showinfo("Éxito", f"Se crearon {n} nodos")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")
        
        btn_crear_nodos = tk.Button(
            frame_nodos,
            text="Crear Nodos",
            font=("Arial", 11, "bold"),
            bg="#27ae60", fg="white",
            command=agregar_nodos
        )
        btn_crear_nodos.pack(pady=10)
        
        # Sección: Aristas
        tk.Label(frame_izq, text="GESTIÓN DE CANALES", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        
        frame_aristas = tk.LabelFrame(frame_izq, text="Agregar Canal de Flujo", bg="#f0f0f0", font=("Arial", 11, "bold"))
        frame_aristas.pack(pady=10, padx=10, fill="x")
        
        tk.Label(frame_aristas, text="Desde Nodo:", bg="#f0f0f0").pack()
        entry_origen = tk.Entry(frame_aristas, font=("Arial", 11), width=10)
        entry_origen.pack(pady=3)
        
        tk.Label(frame_aristas, text="Hacia Nodo:", bg="#f0f0f0").pack()
        entry_destino = tk.Entry(frame_aristas, font=("Arial", 11), width=10)
        entry_destino.pack(pady=3)
        
        tk.Label(frame_aristas, text="Capacidad:", bg="#f0f0f0").pack()
        entry_capacidad = tk.Entry(frame_aristas, font=("Arial", 11), width=10)
        entry_capacidad.pack(pady=3)
        
        def agregar_arista():
            if not self.nodos_grafo:
                messagebox.showerror("Error", "Primero debe crear los nodos")
                return
            
            try:
                origen = int(entry_origen.get()) - 1
                destino = int(entry_destino.get()) - 1
                capacidad = int(entry_capacidad.get())
                
                if origen < 0 or origen >= self.num_nodos or destino < 0 or destino >= self.num_nodos:
                    messagebox.showerror("Error", f"Los nodos deben estar entre 1 y {self.num_nodos}")
                    return
                
                if origen == destino:
                    messagebox.showerror("Error", "No se permiten ciclos (mismo nodo)")
                    return
                
                if capacidad <= 0:
                    messagebox.showerror("Error", "La capacidad debe ser mayor a 0")
                    return
                
                # Verificar si ya existe la arista
                for i, (o, d, _) in enumerate(self.aristas_grafo):
                    if o == origen and d == destino:
                        self.aristas_grafo[i] = (origen, destino, capacidad)
                        messagebox.showinfo("Actualizado", f"Canal {origen+1}→{destino+1} actualizado")
                        actualizar_vista()
                        return
                
                self.aristas_grafo.append((origen, destino, capacidad))
                actualizar_vista()
                messagebox.showinfo("Éxito", f"Canal agregado: {origen+1}→{destino+1} (Cap: {capacidad})")
                
                entry_origen.delete(0, tk.END)
                entry_destino.delete(0, tk.END)
                entry_capacidad.delete(0, tk.END)
                
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores válidos")
        
        btn_agregar_arista = tk.Button(
            frame_aristas,
            text="Agregar Canal",
            font=("Arial", 11, "bold"),
            bg="#3498db", fg="white",
            command=agregar_arista
        )
        btn_agregar_arista.pack(pady=10)
        
        # Lista de aristas
        frame_lista = tk.LabelFrame(frame_izq, text="Canales Creados", bg="#f0f0f0", font=("Arial", 11, "bold"))
        frame_lista.pack(pady=10, padx=10, fill="both", expand=True)
        
        lista_aristas = tk.Listbox(frame_lista, height=8, font=("Courier", 10))
        lista_aristas.pack(fill="both", expand=True, padx=5, pady=5)
        
        def eliminar_arista():
            sel = lista_aristas.curselection()
            if sel:
                idx = sel[0]
                arista = self.aristas_grafo[idx]
                self.aristas_grafo.pop(idx)
                actualizar_vista()
                messagebox.showinfo("Eliminado", f"Canal {arista[0]+1}→{arista[1]+1} eliminado")
        
        btn_eliminar = tk.Button(
            frame_lista,
            text="Eliminar Seleccionado",
            font=("Arial", 10),
            bg="#e74c3c", fg="white",
            command=eliminar_arista
        )
        btn_eliminar.pack(pady=5)
        
        # Panel derecho: Vista previa del grafo
        frame_der = tk.Frame(frame_principal, bg="white")
        frame_der.pack(side="right", fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(frame_der, text="Vista Previa del Grafo", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        canvas_preview = tk.Canvas(frame_der, bg="white", width=700, height=500, relief="solid", borderwidth=2)
        canvas_preview.pack(pady=10)
        
        def actualizar_vista():
            canvas_preview.delete("all")
            lista_aristas.delete(0, tk.END)
            
            if not self.nodos_grafo:
                canvas_preview.create_text(350, 250, text="Cree nodos primero", font=("Arial", 14), fill="gray")
                return
            
            # Calcular posiciones
            n = len(self.nodos_grafo)
            posiciones = self.calcular_posiciones(n, 700, 500)
            
            # Dibujar aristas
            for origen, destino, capacidad in self.aristas_grafo:
                x1, y1 = posiciones[origen]
                x2, y2 = posiciones[destino]
                
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
                
                canvas_preview.create_line(x1_adj, y1_adj, x2_adj, y2_adj, arrow=tk.LAST, 
                                 width=2, fill="#5271ff", arrowshape=(10,12,5), smooth=True)
                
                canvas_preview.create_rectangle(mx-18, my-12, mx+18, my+12, fill="white", outline="")
                canvas_preview.create_text(mx, my, text=str(capacidad), font=("Arial", 10, "bold"), fill="#000000")
                
                lista_aristas.insert(tk.END, f"  {origen+1:2d} → {destino+1:2d}  [Cap: {capacidad:2d}]")
            
            # Dibujar nodos
            for i, (x, y) in enumerate(posiciones):
                if i == 0:
                    color = "#ffcccb"
                    outline = "#e74c3c"
                elif i == n-1:
                    color = "#c8e6c9"
                    outline = "#27ae60"
                else:
                    color = "#b8c5ff"
                    outline = "#5271ff"
                
                canvas_preview.create_oval(x-25, y-25, x+25, y+25, fill=color, outline=outline, width=3)
                canvas_preview.create_text(x, y, text=f"{i+1}", font=("Arial", 14, "bold"), fill="#000000")
        
        # Botones finales
        frame_botones = tk.Frame(frame_der, bg="white")
        frame_botones.pack(pady=10)
        
        def generar_matriz():
            if not self.nodos_grafo:
                messagebox.showerror("Error", "Primero debe crear nodos")
                return
            
            n = len(self.nodos_grafo)
            matriz = [[0 for _ in range(n)] for _ in range(n)]
            
            for origen, destino, capacidad in self.aristas_grafo:
                matriz[origen][destino] = capacidad
            
            self.matriz_capacidad = matriz
            messagebox.showinfo("Éxito", f"Matriz generada con {n} nodos y {len(self.aristas_grafo)} canales")
            self.mostrar_menu_principal()
        
        btn_generar = tk.Button(
            frame_botones,
            text="Generar Matriz y Continuar",
            font=("Arial", 14, "bold"),
            bg="#27ae60", fg="white",
            padx=20, pady=10,
            command=generar_matriz
        )
        btn_generar.pack(side="left", padx=10)
        
        btn_volver = tk.Button(
            frame_botones,
            text="Cancelar",
            font=("Arial", 14),
            bg="#95a5a6", fg="white",
            padx=20, pady=10,
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(side="left", padx=10)
        
        actualizar_vista()
    
    def calcular_posiciones(self, n, width, height):
        """Calcula posiciones para los nodos en el canvas"""
        posiciones = []
        margin = 80
        
        if n <= 2:
            posiciones = [(margin + 50, height//2), (width - margin - 50, height//2)]
        elif n == 3:
            posiciones = [(margin + 50, height//2), (width//2, height//2), (width - margin - 50, height//2)]
        elif n == 4:
            posiciones = [(margin + 50, height//3), (margin + 50, 2*height//3), 
                         (width - margin - 50, height//3), (width - margin - 50, 2*height//3)]
        else:
            layers = min(3, (n + 2) // 3)
            nodes_per_layer = (n + layers - 1) // layers
            x_spacing = (width - 2*margin) / (layers + 1)
            
            for i in range(n):
                layer = i // nodes_per_layer
                pos_in_layer = i % nodes_per_layer
                nodes_in_this_layer = min(nodes_per_layer, n - layer * nodes_per_layer)
                
                x = margin + (layer + 1) * x_spacing
                y_spacing = (height - 2*margin) / (nodes_in_this_layer + 1)
                y = margin + (pos_in_layer + 1) * y_spacing
                
                posiciones.append((x, y))
        
        return posiciones
    
    def menu_grafo_aleatorio(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both", padx=20, pady=20)
        
        titulo = tk.Label(
            frame_principal,
            text="Generar Grafo Aleatorio",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        titulo.pack(pady=20)
        
        frame_nodos = tk.Frame(frame_principal, bg="#f0f0f0")
        frame_nodos.pack(pady=20)
        
        tk.Label(
            frame_nodos,
            text="Número de nodos (8-16):",
            font=("Arial", 14),
            bg="#f0f0f0"
        ).pack(side="left", padx=10)
        
        entry_nodos = tk.Entry(frame_nodos, font=("Arial", 14), width=10)
        entry_nodos.pack(side="left")
        entry_nodos.insert(0, "8")
        
        def generar():
            try:
                n = int(entry_nodos.get())
                if n < 8 or n > 16:
                    messagebox.showerror("Error", "El número de nodos debe estar entre 8 y 16")
                    return
                
                self.num_nodos = n
                self.crear_matriz_aleatoria(n)
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")
        
        btn_generar = tk.Button(
            frame_principal,
            text="Generar Grafo Aleatorio",
            font=("Arial", 14, "bold"),
            bg="#e67e22", fg="white",
            padx=30, pady=15,
            command=generar
        )
        btn_generar.pack(pady=20)
        
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
                    if matriz[i][destino] == 0:
                        matriz[i][destino] = random.randint(1, 15)
        
        conexiones_extra = random.randint(0, n)
        for _ in range(conexiones_extra):
            i = random.randint(0, n-2)
            j = random.randint(i+1, n-1)
            if matriz[i][j] == 0 and i != j:
                matriz[i][j] = random.randint(1, 15)
        
        self.matriz_capacidad = matriz
        
        # Actualizar nodos y aristas para visualización
        self.num_nodos = n
        self.nodos_grafo = list(range(n))
        self.aristas_grafo = []
        
        for i in range(n):
            for j in range(n):
                if matriz[i][j] > 0:
                    self.aristas_grafo.append((i, j, matriz[i][j]))
        
        messagebox.showinfo("Éxito", f"Grafo aleatorio generado con {n} nodos y {len(self.aristas_grafo)} canales")
        self.mostrar_grafo()
    
    def mostrar_grafo(self):
        if self.matriz_capacidad is None:
            messagebox.showwarning("Advertencia", "No hay grafo para mostrar")
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
        posiciones = self.calcular_posiciones(n, 900, 550)
        
        # Dibujar aristas
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
        
        # Dibujar nodos
        for i, (x, y) in enumerate(posiciones):
            if i == 0:
                color = "#ffcccb"
                outline_color = "#e74c3c"
            elif i == n-1:
                color = "#c8e6c9"
                outline_color = "#27ae60"
            else:
                color = "#b8c5ff"
                outline_color = "#5271ff"
            
            canvas.create_oval(x-30, y-30, x+30, y+30, fill=color, outline=outline_color, width=3)
            canvas.create_text(x, y, text=f"{i+1}", font=("Arial", 18, "bold"), fill="#000000")
        
        leyenda_frame = tk.Frame(frame_principal, bg="#f0f0f0")
        leyenda_frame.pack(pady=10)
        
        tk.Label(leyenda_frame, text="● Fuente (Origen)", font=("Arial", 12), bg="#f0f0f0", fg="#e74c3c").pack(side="left", padx=10)
        tk.Label(leyenda_frame, text="● Sumidero (Destino)", font=("Arial", 12), bg="#f0f0f0", fg="#27ae60").pack(side="left", padx=10)
        tk.Label(leyenda_frame, text="● Nodo intermedio", font=("Arial", 12), bg="#f0f0f0", fg="#3498db").pack(side="left", padx=10)
        
        botones_frame = tk.Frame(frame_principal, bg="#f0f0f0")
        botones_frame.pack(pady=20)
        
        btn_menu = tk.Button(
            botones_frame,
            text="Volver al Menú",
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
    
    def encontrar_corte_minimo(self, grafo_residual, fuente):
        """Encuentra el corte mínimo usando BFS en el grafo residual final"""
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
        
        # El corte está formado por las aristas que van desde nodos visitados a no visitados
        corte = []
        for u in range(n):
            if visitado[u]:
                for v in range(n):
                    if not visitado[v] and self.matriz_capacidad[u][v] > 0:
                        corte.append((u, v, self.matriz_capacidad[u][v]))
        
        return corte, visitado
    
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
            
            ruta_str = " → ".join(str(nodo + 1) for nodo in camino)
            self.rutas_encontradas.append((ruta_str, flujo_camino))
            
            padre = [-1] * n
        
        # Guardar el grafo residual final y encontrar el corte mínimo
        self.grafo_residual_final = grafo_residual
        self.corte_minimo, self.nodos_lado_fuente = self.encontrar_corte_minimo(grafo_residual, fuente)
        
        return flujo_maximo
    
    def calcular_flujo_maximo(self):
        if self.matriz_capacidad is None:
            messagebox.showwarning("Advertencia", "Primero debe crear un grafo")
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
        
        # Crear notebook con pestañas
        notebook = ttk.Notebook(frame_principal)
        notebook.pack(fill="both", expand=True, pady=10)
        
        # Pestaña 1: Caminos aumentantes
        tab_caminos = tk.Frame(notebook, bg="white")
        notebook.add(tab_caminos, text="Caminos Aumentantes")
        
        tk.Label(
            tab_caminos,
            text="Caminos Aumentantes Utilizados:",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=10)
        
        rutas_text = scrolledtext.ScrolledText(
            tab_caminos,
            width=80,
            height=12,
            font=("Courier", 12),
            bg="#f9f9f9"
        )
        rutas_text.pack(pady=10, padx=20, fill="both", expand=True)
        
        for i, (ruta, flujo) in enumerate(self.rutas_encontradas, 1):
            rutas_text.insert(tk.END, f"Camino {i}: {ruta}  →  Flujo: {flujo}\n")
        
        rutas_text.config(state="disabled")
        
        # Pestaña 2: Corte Mínimo
        tab_corte = tk.Frame(notebook, bg="white")
        notebook.add(tab_corte, text="Corte Mínimo")
        
        tk.Label(
            tab_corte,
            text="Corte Mínimo (Separación Fuente-Sumidero)",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=10)
        
        info_corte = tk.Label(
            tab_corte,
            text="El corte mínimo divide el grafo en dos conjuntos:\n"
                 "• Conjunto S: Nodos alcanzables desde la fuente\n"
                 "• Conjunto T: Nodos no alcanzables desde la fuente\n\n"
                 "Las aristas del corte van de S hacia T y están saturadas o no existen.",
            font=("Arial", 11),
            bg="white",
            fg="#555",
            justify="left"
        )
        info_corte.pack(pady=10)
        
        # Mostrar conjuntos
        n = len(self.matriz_capacidad)
        conjunto_s = [i+1 for i in range(n) if self.nodos_lado_fuente[i]]
        conjunto_t = [i+1 for i in range(n) if not self.nodos_lado_fuente[i]]
        
        conjuntos_frame = tk.Frame(tab_corte, bg="white")
        conjuntos_frame.pack(pady=10)
        
        tk.Label(
            conjuntos_frame,
            text=f"Conjunto S (con Fuente): {conjunto_s}",
            font=("Arial", 12, "bold"),
            bg="#ffe6e6",
            fg="#c0392b",
            padx=20,
            pady=10,
            relief="solid",
            borderwidth=2
        ).pack(pady=5)
        
        tk.Label(
            conjuntos_frame,
            text=f"Conjunto T (con Sumidero): {conjunto_t}",
            font=("Arial", 12, "bold"),
            bg="#e6ffe6",
            fg="#27ae60",
            padx=20,
            pady=10,
            relief="solid",
            borderwidth=2
        ).pack(pady=5)
        
        # Mostrar aristas del corte
        tk.Label(
            tab_corte,
            text="Aristas que forman el Corte Mínimo:",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=10)
        
        corte_text = scrolledtext.ScrolledText(
            tab_corte,
            width=80,
            height=8,
            font=("Courier", 12),
            bg="#fff9e6"
        )
        corte_text.pack(pady=10, padx=20, fill="both", expand=True)
        
        capacidad_total_corte = 0
        for i, (u, v, cap) in enumerate(self.corte_minimo, 1):
            corte_text.insert(tk.END, f"Arista {i}: Nodo {u+1} → Nodo {v+1}  (Capacidad: {cap})\n")
            capacidad_total_corte += cap
        
        corte_text.insert(tk.END, f"\n{'='*60}\n")
        corte_text.insert(tk.END, f"Capacidad Total del Corte: {capacidad_total_corte}\n")
        corte_text.insert(tk.END, f"(Igual al Flujo Máximo: {flujo_max})\n")
        
        corte_text.config(state="disabled")
        
        # Teorema del flujo máximo - corte mínimo
        teorema_label = tk.Label(
            tab_corte,
            text="✓ Teorema verificado: Flujo Máximo = Capacidad del Corte Mínimo",
            font=("Arial", 12, "bold"),
            bg="#d4edda",
            fg="#155724",
            padx=20,
            pady=10,
            relief="solid",
            borderwidth=2
        )
        teorema_label.pack(pady=10)
        
        # Botón para visualizar el corte
        btn_visualizar_corte = tk.Button(
            tab_corte,
            text="Visualizar Corte en el Grafo",
            font=("Arial", 13, "bold"),
            bg="#f39c12", fg="white",
            padx=30, pady=12,
            command=self.mostrar_grafo_con_corte
        )
        btn_visualizar_corte.pack(pady=15)
        
        btn_volver = tk.Button(
            frame_principal,
            text="Volver al Menú",
            font=("Arial", 14, "bold"),
            bg="#95a5a6", fg="white",
            padx=30, pady=15,
            command=self.mostrar_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def mostrar_grafo_con_corte(self):
        """Muestra el grafo con el corte mínimo resaltado"""
        if self.matriz_capacidad is None:
            messagebox.showwarning("Advertencia", "No hay grafo para mostrar")
            return
            
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both")
        
        titulo = tk.Label(
            frame_principal,
            text="Visualización del Corte Mínimo",
            font=("Arial", 22, "bold"),
            bg="#f0f0f0"
        )
        titulo.pack(pady=20)
        
        info = tk.Label(
            frame_principal,
            text="Las aristas ROJAS representan el corte mínimo que separa la fuente del sumidero",
            font=("Arial", 12, "italic"),
            bg="#f0f0f0",
            fg="#c0392b"
        )
        info.pack(pady=5)
        
        canvas = tk.Canvas(frame_principal, bg="white", width=900, height=550)
        canvas.pack(pady=20)
        
        n = len(self.matriz_capacidad)
        posiciones = self.calcular_posiciones(n, 900, 550)
        
        # Crear conjunto de aristas del corte para búsqueda rápida
        aristas_corte = {(u, v) for u, v, _ in self.corte_minimo}
        
        # Dibujar aristas
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
                    
                    # Verificar si es parte del corte
                    es_corte = (i, j) in aristas_corte
                    color = "#e74c3c" if es_corte else "#5271ff"
                    ancho = 4 if es_corte else 2
                    
                    canvas.create_line(x1_adj, y1_adj, x2_adj, y2_adj, arrow=tk.LAST, 
                                     width=ancho, fill=color, arrowshape=(12,15,6), smooth=True)
                    
                    # Etiqueta de capacidad
                    bg_color = "#ffe6e6" if es_corte else "white"
                    canvas.create_rectangle(mx-20, my-12, mx+20, my+12, fill=bg_color, outline=color if es_corte else "")
                    canvas.create_text(
                        mx, my,
                        text=str(self.matriz_capacidad[i][j]),
                        font=("Arial", 11, "bold"),
                        fill=color if es_corte else "#000000"
                    )
        
        # Dibujar nodos con colores según el conjunto
        for i, (x, y) in enumerate(posiciones):
            if self.nodos_lado_fuente[i]:
                # Conjunto S (lado de la fuente)
                if i == 0:
                    color = "#ffcccb"
                    outline_color = "#c0392b"
                else:
                    color = "#ffe6e6"
                    outline_color = "#e74c3c"
            else:
                # Conjunto T (lado del sumidero)
                if i == n-1:
                    color = "#c8e6c9"
                    outline_color = "#229954"
                else:
                    color = "#e6ffe6"
                    outline_color = "#27ae60"
            
            canvas.create_oval(x-30, y-30, x+30, y+30, fill=color, outline=outline_color, width=3)
            canvas.create_text(x, y, text=f"{i+1}", font=("Arial", 18, "bold"), fill="#000000")
        
        # Dibujar línea de corte que atraviesa las aristas del corte
        if len(self.corte_minimo) > 0:
            # Calcular puntos medios de todas las aristas del corte
            puntos_corte = []
            for u, v, _ in self.corte_minimo:
                x1, y1 = posiciones[u]
                x2, y2 = posiciones[v]
                # Punto medio de la arista
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                puntos_corte.append((mx, my))
            
            if len(puntos_corte) > 0:
                # Encontrar el rango de la línea de corte
                min_x = min(p[0] for p in puntos_corte) - 50
                max_x = max(p[0] for p in puntos_corte) + 50
                min_y = min(p[1] for p in puntos_corte) - 50
                max_y = max(p[1] for p in puntos_corte) + 50
                
                # Determinar la orientación de la línea (vertical, horizontal o diagonal)
                rango_x = max_x - min_x
                rango_y = max_y - min_y
                
                if rango_x > rango_y:
                    # Línea más horizontal - calcular ecuación de línea
                    x_medio = sum(p[0] for p in puntos_corte) / len(puntos_corte)
                    # Dibujar línea vertical en el punto medio
                    canvas.create_line(x_medio, 30, x_medio, 520, 
                                     fill="#ff0000", width=4, dash=(15, 10))
                    canvas.create_text(x_medio, 15, text="✂ CORTE MÍNIMO", 
                                     font=("Arial", 13, "bold"), fill="#ff0000")
                else:
                    # Línea más vertical o diagonal
                    y_medio = sum(p[1] for p in puntos_corte) / len(puntos_corte)
                    
                    # Intentar ajustar una línea que pase por los puntos
                    if len(puntos_corte) >= 2:
                        # Calcular pendiente promedio
                        x_vals = [p[0] for p in puntos_corte]
                        y_vals = [p[1] for p in puntos_corte]
                        
                        x_prom = sum(x_vals) / len(x_vals)
                        y_prom = sum(y_vals) / len(y_vals)
                        
                        # Calcular pendiente
                        numerador = sum((x_vals[i] - x_prom) * (y_vals[i] - y_prom) for i in range(len(x_vals)))
                        denominador = sum((x_vals[i] - x_prom) ** 2 for i in range(len(x_vals)))
                        
                        if abs(denominador) > 0.001:
                            pendiente = numerador / denominador
                            intercepto = y_prom - pendiente * x_prom
                            
                            # Dibujar línea con la pendiente calculada
                            x1_linea = 50
                            y1_linea = pendiente * x1_linea + intercepto
                            x2_linea = 850
                            y2_linea = pendiente * x2_linea + intercepto
                            
                            canvas.create_line(x1_linea, y1_linea, x2_linea, y2_linea,
                                             fill="#ff0000", width=4, dash=(15, 10))
                        else:
                            # Línea horizontal
                            canvas.create_line(50, y_medio, 850, y_medio,
                                             fill="#ff0000", width=4, dash=(15, 10))
                    else:
                        # Solo un punto - línea horizontal
                        canvas.create_line(50, y_medio, 850, y_medio,
                                         fill="#ff0000", width=4, dash=(15, 10))
                    
                    canvas.create_text(450, max(30, min_y - 30), text="✂ CORTE MÍNIMO", 
                                     font=("Arial", 13, "bold"), fill="#ff0000")
                
                # Marcar con X las aristas del corte
                for u, v, _ in self.corte_minimo:
                    x1, y1 = posiciones[u]
                    x2, y2 = posiciones[v]
                    mx = (x1 + x2) / 2
                    my = (y1 + y2) / 2
                    
                    # Dibujar una X sobre la arista
                    size = 12
                    canvas.create_line(mx-size, my-size, mx+size, my+size, 
                                     fill="#ff0000", width=3)
                    canvas.create_line(mx-size, my+size, mx+size, my-size, 
                                     fill="#ff0000", width=3)
        
        leyenda_frame = tk.Frame(frame_principal, bg="#f0f0f0")
        leyenda_frame.pack(pady=10)
        
        tk.Label(leyenda_frame, text="● Conjunto S (con Fuente)", font=("Arial", 11), bg="#f0f0f0", fg="#c0392b").pack(side="left", padx=10)
        tk.Label(leyenda_frame, text="● Conjunto T (con Sumidero)", font=("Arial", 11), bg="#f0f0f0", fg="#27ae60").pack(side="left", padx=10)
        tk.Label(leyenda_frame, text="━ Aristas del Corte", font=("Arial", 11), bg="#f0f0f0", fg="#e74c3c").pack(side="left", padx=10)
        
        botones_frame = tk.Frame(frame_principal, bg="#f0f0f0")
        botones_frame.pack(pady=20)
        
        btn_resultados = tk.Button(
            botones_frame,
            text="Ver Resultados Completos",
            font=("Arial", 12, "bold"),
            bg="#3498db", fg="white",
            padx=20, pady=10,
            command=self.calcular_flujo_maximo
        )
        btn_resultados.pack(side="left", padx=10)
        
        btn_menu = tk.Button(
            botones_frame,
            text="Menú Principal",
            font=("Arial", 12, "bold"),
            bg="#95a5a6", fg="white",
            padx=20, pady=10,
            command=self.mostrar_menu_principal
        )
        btn_menu.pack(side="left", padx=10)
    
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
            root.geometry("1200x800")
    
    root.bind("<Escape>", toggle_fullscreen)
    
    app = FordFulkersonApp(root)
    app.mostrar_presentacion()
    
    root.mainloop()

if __name__ == "__main__":
    main()