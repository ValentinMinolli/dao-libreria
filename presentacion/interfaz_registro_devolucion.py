from gestores.gestor_prestamo import Gestor_Prestamos
from gestores.gestor_libro import Gestor_Libros
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Interfaz_Devolucion_Libro(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancias de los gestores
        self.gestor_prestamos = Gestor_Prestamos()  # Gestor para los préstamos
        self.gestor_libros = Gestor_Libros()        # Gestor para los libros

        # Configuración del estilo
        estilo = ttk.Style()
        estilo.configure("TFrame", background="#f2f2f2")
        estilo.configure("TLabel", background="#f2f2f2", font=("Arial", 10, "bold"))
        estilo.configure("TEntry", padding=5, font=("Arial", 10))
        estilo.configure("TCombobox", padding=5, font=("Arial", 10))
        estilo.configure(
            "TButton",
            background="#007ACC",
            foreground="white",
            font=("Arial", 10, "bold"),
        )

        # Crear los elementos de la interfaz para la devolución de libros
        ttk.Label(self, text="Libro (ISBN):").grid(
            row=0, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.combo_isbn_libro = ttk.Combobox(self, state="readonly")
        self.combo_isbn_libro.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")
        self.cargar_libros_prestados()

        ttk.Label(self, text="ID del Usuario:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_usuario = ttk.Entry(self)
        self.entry_usuario.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self, text="¿En condiciones?:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.condiciones_var = tk.StringVar()
        self.condiciones_combo = ttk.Combobox(
            self, textvariable=self.condiciones_var, state="readonly"
        )
        self.condiciones_combo["values"] = ("Sí", "No")
        self.condiciones_combo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Botón para registrar devolución
        self.boton_devolver = ttk.Button(
            self, text="Registrar Devolución", command=self.registrar_devolucion
        )
        self.boton_devolver.grid(row=3, columnspan=2, pady=(20, 10), padx=10)

        # Expande la segunda columna para ajustarse al tamaño de la ventana
        self.columnconfigure(1, weight=1)

    def cargar_libros_prestados(self):
        """Carga los ISBN de los libros actualmente prestados."""
        libros_prestados = self.gestor_prestamos.obtener_libros_prestados()
        self.combo_isbn_libro["values"] = [libro.isbn for libro in libros_prestados]

    def registrar_devolucion(self):
        """Registra la devolución de un libro."""
        isbn = self.combo_isbn_libro.get()
        usuario = self.entry_usuario.get()
        en_condiciones = self.condiciones_var.get()

        # Validar que todos los campos estén llenos
        if not isbn or not usuario or not en_condiciones:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Registrar la devolución usando el gestor de préstamos
        if self.gestor_prestamos.registrar_devolucion(isbn, usuario, en_condiciones):
            messagebox.showinfo("Éxito", "Devolución registrada con éxito.")
            self.combo_isbn_libro.set("")
            self.entry_usuario.delete(0, tk.END)
            self.condiciones_combo.set("")
        else:
            messagebox.showerror("Error", "No se pudo registrar la devolución.")
