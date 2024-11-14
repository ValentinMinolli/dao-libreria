from tkinter import ttk, messagebox
import tkinter as tk
from gestores.gestor_prestamo import Gestor_Prestamos
from gestores.gestor_libro import Gestor_Libros
from gestores.gestor_usuario import Gestor_Usuarios


class Interfaz_Devolucion_Libro(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancias de los gestores
        self.gestor_prestamos = Gestor_Prestamos()  # Gestor para los préstamos
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

        # Crear los elementos de la interfaz para la devolución de libros
        ttk.Label(self, text="ID del Usuario:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.combo_usuario = ttk.Combobox(self, state="readonly")
        self.combo_usuario.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.cargar_usuarios()

        ttk.Label(self, text="Libro (ISBN):").grid(
            row=1, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.combo_isbn_libro = ttk.Combobox(self, state="readonly")
        self.combo_isbn_libro.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="ew")

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

        # Vincular la función para cargar los libros prestados al campo de ID de usuario
        self.combo_usuario.bind("<<ComboboxSelected>>", self.cargar_libros_prestados)

    def cargar_usuarios(self):
        """Carga los usuarios en el Combobox."""
        usuarios = self.gestor_usuarios.obtener_usuarios()  # Obtener todos los usuarios
        self.combo_usuario["values"] = [
            usuario.id for usuario in usuarios
        ]  # Usamos el id del objeto usuario

    def cargar_libros_prestados(self, event=None):
        """
        Carga los ISBN de los libros actualmente prestados que están en estado "Pendiente de Devolución".
        """
        usuario_id = self.combo_usuario.get()  # Obtener ID de usuario desde el ComboBox

        # Si no hay ID, no hacer nada
        if not usuario_id:
            self.combo_isbn_libro.set("")  # Limpiar la selección
            self.combo_isbn_libro["values"] = []  # Limpiar los valores
            return

        # Vaciar el ComboBox antes de cargar los nuevos ISBN
        self.combo_isbn_libro.set("")  # Limpiar selección previa
        self.combo_isbn_libro["values"] = []  # Limpiar los valores anteriores

        # Obtener los préstamos pendientes del usuario
        prestamos_pendientes = self.gestor_prestamos.obtener_prestamos_pendientes(
            usuario_id
        )

        # Si no se han encontrado préstamos pendientes, informarlo
        if not prestamos_pendientes:
            self.combo_isbn_libro["values"] = (
                []
            )  # Asegurarse de que el ComboBox se quede vacío
            return

        # Llenar el ComboBox con los ISBN de los libros
        self.combo_isbn_libro["values"] = [
            prestamo.libro_isbn for prestamo in prestamos_pendientes
        ]

        # Si hay préstamos, seleccionar el primer ISBN (opcional)
        if prestamos_pendientes:
            self.combo_isbn_libro.set(prestamos_pendientes[0].libro_isbn)

    def registrar_devolucion(self):
        """
        Registra la devolución de un libro.
        """
        usuario_id = self.combo_usuario.get()
        isbn = self.combo_isbn_libro.get()
        en_condiciones = self.condiciones_var.get()

        # Validar que todos los campos estén llenos
        if not usuario_id or not isbn or not en_condiciones:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Registrar la devolución usando el gestor de préstamos
            if self.gestor_prestamos.registrar_devolucion(
                isbn, usuario_id, en_condiciones
            ):
                messagebox.showinfo("Éxito", "Devolución registrada con éxito.")
                self.combo_usuario.set("")
                self.combo_isbn_libro.set("")
                self.condiciones_combo.set("")
            else:
                messagebox.showerror("Error", "No se pudo registrar la devolución.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar la devolución: {str(e)}")
