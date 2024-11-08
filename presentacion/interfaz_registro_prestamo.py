from gestores.gestor_prestamo import (
    Gestor_Prestamos,
)  # Asegúrate de importar los gestores correspondientes
from gestores.gestor_libro import Gestor_Libros
from gestores.gestor_usuario import Gestor_Usuarios

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re
from datetime import datetime


class Interfaz_Registro_Prestamo(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancias de los gestores
        self.gestor_prestamos = Gestor_Prestamos()  # Gestor para los prestamos
        self.gestor_libros = Gestor_Libros()  # Gestor para los libros
        self.gestor_usuarios = Gestor_Usuarios()  # Gestor para los usuarios

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

        # Crear los elementos de la interfaz con estilo y espaciado
        ttk.Label(self, text="Libro (ISBN):").grid(
            row=0, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.combo_isbn_libro = ttk.Combobox(self, state="readonly")
        self.combo_isbn_libro.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")
        self.cargar_libros()

        # Combobox para seleccionar "ID de Usuario"
        ttk.Label(self, text="ID de Usuario:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.combo_usuarios = ttk.Combobox(self, state="readonly")
        self.combo_usuarios.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="ew")
        self.cargar_usuarios()

        # Campo de entrada para la fecha de prestamo
        ttk.Label(self, text="Fecha de entrega (dd/mm/yyyy):").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_fecha_prestamo = ttk.Entry(self)
        self.entry_fecha_prestamo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Campo de entrada para la fecha de devolucion
        ttk.Label(self, text="Fecha de devolución (dd/mm/yyyy):").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_fecha_devolucion = ttk.Entry(self)
        self.entry_fecha_devolucion.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Botón de registro con estilo
        self.boton_registrar = ttk.Button(
            self, text="Registrar Prestamo", command=self.registrar
        )
        self.boton_registrar.grid(row=4, columnspan=2, pady=(20, 10), padx=10)

        # Expande la segunda columna para ajustarse al tamaño de la ventana
        self.columnconfigure(1, weight=1)

    def cargar_libros(self):
        """Carga los libros en el Combobox."""
        libros = (
            self.gestor_libros.obtener_isbn_libros()
        )  # Llamada al gestor para obtener los isbn de los libros
        self.combo_isbn_libro["values"] = [
            libro.isbn for libro in libros
        ]  # Usamos el isbn del objeto libro

    def cargar_usuarios(self):
        """Carga los usuarios en el Combobox."""
        usuarios = (
            self.gestor_usuarios.obtener_usuarios()
        )  # Llamada al gestor para obtener los ids de los usuarios
        self.combo_usuarios["values"] = [
            usuario.id for usuario in usuarios
        ]  # Usamos el id del objeto usuario

    def registrar(self):
        """Registra un servicio para un auto."""
        isbn = self.combo_isbn_libro.get()
        usuario = self.combo_usuarios.get()
        fecha_prestamo = self.entry_fecha_prestamo.get()
        fecha_devolucion = self.entry_fecha_devolucion.get()

        # Validar que todos los campos estén llenos
        if not isbn or not usuario or not fecha_prestamo or not fecha_devolucion:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Registrar el prestamo usando el gestor de prestamos
        if self.gestor_prestamos.registrar(
            usuario, isbn, fecha_prestamo, fecha_devolucion
        ):
            messagebox.showinfo("Éxito", "Prestamo registrado con éxito.")
            self.combo_isbn_libro.set("")
            self.combo_usuarios.set("")
            self.entry_fecha_prestamo.delete(0, tk.END)
            self.entry_fecha_devolucion.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo registrar el prestamo.")
