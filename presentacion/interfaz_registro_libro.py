from gestores.gestor_libro import Gestor_Libros

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Interfaz_Registro_Libro(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancia del gestor de autores
        self.gestor_libros = Gestor_Libros()

        # Crear los elementos de la interfaz con separación
        ttk.Label(self, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_isbn = ttk.Entry(self)
        self.entry_isbn.grid(row=0, column=1, padx=5, pady=5)

        # Crear un validador que solo permite números, 'X' y guiones
        vcmd_numero = (parent.register(self.validar_caracteres), "%S")
        self.entry_isbn.config(validate="key", validatecommand=vcmd_numero)

        ttk.Label(self, text="Titulo:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_titulo = ttk.Entry(self)
        self.entry_titulo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Genero:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_genero = ttk.Entry(self)
        self.entry_genero.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Año Publicacion:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_anio_publicacion = ttk.Entry(self)
        self.entry_anio_publicacion.grid(row=3, column=1, padx=5, pady=5)

        # Crear un validador que solo permite números para el año de publicacion
        vcmd_numero = (parent.register(self.validar_numero), "%P")
        self.entry_anio_publicacion.config(validate="key", validatecommand=vcmd_numero)

         # Crear los campos para Nombre y Apellido del Autor
        ttk.Label(self, text="Nombre del Autor:").grid(row=4, column=0, padx=5, pady=5)
        self.entry_nombre_autor = ttk.Entry(self)
        self.entry_nombre_autor.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Apellido del Autor:").grid(row=5, column=0, padx=5, pady=5)
        self.entry_apellido_autor = ttk.Entry(self)
        self.entry_apellido_autor.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text="Cantidad:").grid(row=6, column=0, padx=5, pady=5)
        self.entry_cantidad = ttk.Entry(self)
        self.entry_cantidad.grid(row=6, column=1, padx=5, pady=5)

        # Crear un validador que solo permite números para la cantidad
        vcmd_numero = (parent.register(self.validar_numero), "%P")
        self.entry_cantidad.config(validate="key", validatecommand=vcmd_numero)

        # Botón de registro con estilo y separación
        self.boton_registrar = ttk.Button(
            self, text="Registrar Libro", command=self.registrar
        )
        self.boton_registrar.grid(row=7, columnspan=2, pady=(20, 10))

        # Estilo del botón
        estilo = ttk.Style()
        estilo.configure(
            "TButton",
            background="lightblue",
            foreground="black",
            padding=10,
            font=("Arial", 10, "bold"),
        )
        self.boton_registrar.config(style="TButton")

    def validar_numero(self, nuevo_texto):
        # Verifica si el nuevo texto es vacío o si solo contiene números
        return nuevo_texto == "" or nuevo_texto.isdigit()

    def validar_caracteres(self, caracter):
        # Permitir solo números, 'X' o '-'
        if caracter.isdigit() or caracter == "X" or caracter == "-":
            return True
        return False

    def registrar(self):
        isbn = self.entry_isbn.get()
        titulo = self.entry_titulo.get()
        genero = self.entry_genero.get()
        anio_publicacion = self.entry_anio_publicacion.get()
        nombre_autor = self.entry_nombre_autor.get()
        apellido_autor = self.entry_apellido_autor.get()
        cantidad = self.entry_cantidad.get()

    # Validar campos obligatorios
        if not all([isbn, titulo, genero, anio_publicacion, nombre_autor, apellido_autor, cantidad]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

    # Registrar libro usando el gestor
        if self.gestor_libros.registrar_con_autor(
            isbn, titulo, genero, anio_publicacion, nombre_autor, apellido_autor, cantidad
    ):
            messagebox.showinfo("Éxito", "Libro registrado con éxito.")
            self.entry_isbn.delete(0, tk.END)
            self.entry_titulo.delete(0, tk.END)
            self.entry_genero.delete(0, tk.END)
            self.entry_anio_publicacion.delete(0, tk.END)
            self.entry_nombre_autor.delete(0, tk.END)
            self.entry_apellido_autor.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo registrar el libro.")
