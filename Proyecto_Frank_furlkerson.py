import tkinter as tk
import PIL as pl
import PIL.Image
import PIL.ImageTk

def mostrar_presentacion(root):
    ruta_imagen = r"C:\Users\Oga_8\OneDrive\Documentos\Matematica_Computacional\logo_de_upc(1).png"
    imagen = pl.Image.open(ruta_imagen)
    logo = pl.ImageTk.PhotoImage(imagen)

    label = tk.Label(root, image=logo)
    label.image = logo 
    label.pack()

    titulo = tk.Label(
        root,
        text="Curso: Matemática Computacional",
        font=("Arial", 24, "bold"),
        bg="#f0f0f0"
    )
    titulo.pack(pady=20)

    Proyecto = tk.Label(
        root,
        text="Nombre del proyecto: Flujo Maximo con Algoritmo de Frank Furlkerson",
        font=("Arial",20,"bold"),
        bg="#f0f0f0"
    )
    Proyecto.pack(pady=20)

    integrantes_frame = tk.Frame(root, bg="#f0f0f0")
    integrantes_frame.pack(pady=20)

    integrantes = [
        "Integrante 1: Leonardo Williams Chavez Corrales",
        "Integrante 2: Carlos Alberto Masias Espinoza",
        "Integrante 3: Andy Alfredo Hipolito Salcedo Muñoz",
        "Integrante 4: Joaquín Estuardo Valera Herrera",
        "Integrante 5: Piero Benjamin Acevedo Chavez"
    ]

    for i in integrantes:
        lbl = tk.Label(integrantes_frame, text=i, font=("Arial", 16), bg="#f0f0f0")
        lbl.pack(anchor="center")

    boton = tk.Button(
        root,
        text="Ingresar a la Aplicación",
        font=("Arial", 18, "bold"),
        bg="#4CAF50", fg="white",
        padx=30, pady=15,
        command=lambda: mostrar_app(root)
    )
    boton.pack(side="bottom", pady=60)


def mostrar_app(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Bienvenido a la aplicación 👋", font=("Arial", 20), bg="#f0f0f0").pack(pady=50)


def main():
    root = tk.Tk()
    root.title("Aplicación")
    root.attributes("-fullscreen", True)
    root.configure(bg="#f0f0f0")

    def toggle_fullscreen(event=None):
        state = not root.attributes("-fullscreen")
        root.attributes("-fullscreen", state)
        if not state:
            root.geometry("800x600")

    root.bind("<Escape>", toggle_fullscreen)

    mostrar_presentacion(root)

    root.mainloop()

main()