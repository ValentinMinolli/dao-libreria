from gestores.gestor_usuario import Gestor_Usuarios  # Importa la clase del gestor

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Interfaz_Registro_Usuario(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancia del gestor de usuarios
        self.gestor_usuarios = Gestor_Usuarios()

        # Crear los elementos de la interfaz con separación
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_apellido = ttk.Entry(self)
        self.entry_apellido.grid(row=1, column=1, padx=5, pady=5)

        # Combobox para seleccionar "Descripción del Servicio"
        ttk.Label(self, text="Tipo de Usuario:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.combo_tipo_usuario = ttk.Combobox(
            self, state="readonly", values=["Profesor", "Estudiante"]
        )
        self.combo_tipo_usuario.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_direccion = ttk.Entry(self)
        self.entry_direccion.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Teléfono:").grid(row=4, column=0, padx=5, pady=5)
        self.entry_telefono = ttk.Entry(self, validate="key")
        self.entry_telefono.grid(row=4, column=1, padx=5, pady=5)

        # Crear un validador que solo permite números para el teléfono
        vcmd_numero = (parent.register(self.validar_numero), "%P")
        self.entry_telefono.config(validate="key", validatecommand=vcmd_numero)

        # Botón de registro con estilo y separación
        self.boton_registrar = ttk.Button(
            self, text="Registrar Usuario", command=self.registrar
        )
        self.boton_registrar.grid(row=5, columnspan=2, pady=(20, 10))

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
        tipo_usuario = self.combo_tipo_usuario.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()

        # Validar campos obligatorios
        if (
            not nombre
            or not apellido
            or not tipo_usuario
            or not direccion
            or not telefono
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Registrar usuario usando el gestor
        if self.gestor_usuarios.registrar(
            nombre, apellido, tipo_usuario, direccion, telefono
        ):
            messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.combo_tipo_usuario.set("")  # Limpiar la selección de tipo de usuario
            self.entry_direccion.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario.")
