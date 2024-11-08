from gestores.gestor_autor import Gestor_Autores

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Interfaz_Registro_Autor(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancia del gestor de autores
        self.gestor_autores = Gestor_Autores()

        # Crear los elementos de la interfaz con separación
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_apellido = ttk.Entry(self)
        self.entry_apellido.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Nacionalidad:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_nacionalidad = ttk.Entry(self)
        self.entry_nacionalidad.grid(row=2, column=1, padx=5, pady=5)

        # Botón de registro con estilo y separación
        self.boton_registrar = ttk.Button(
            self, text="Registrar Autor", command=self.registrar
        )
        self.boton_registrar.grid(row=4, columnspan=2, pady=(20, 10))

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

    def registrar(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        nacionalidad = self.entry_nacionalidad.get()

        # Validar campos obligatorios
        if not nombre or not apellido or not nacionalidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Registrar cliente usando el gestor
        if self.gestor_autores.registrar(nombre, apellido, nacionalidad):
            messagebox.showinfo("Éxito", "Cliente registrado con éxito.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_nacionalidad.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo registrar el autor.")
