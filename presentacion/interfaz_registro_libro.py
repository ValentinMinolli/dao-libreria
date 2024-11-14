from gestores.gestor_libro import Gestor_Libros
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Interfaz_Registro_Libro(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.gestor_libros = Gestor_Libros()

        # Crear los elementos de la interfaz
        ttk.Label(self, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_isbn = ttk.Entry(self)
        self.entry_isbn.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Titulo:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_titulo = ttk.Entry(self)
        self.entry_titulo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Genero:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_genero = ttk.Entry(self)
        self.entry_genero.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Año Publicacion:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_anio_publicacion = ttk.Entry(self)
        self.entry_anio_publicacion.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Autor:").grid(row=4, column=0, padx=5, pady=5)
        self.combo_autores = ttk.Combobox(self, state="readonly")
        self.combo_autores.grid(row=4, column=1, padx=5, pady=5)
        self.cargar_autores()

        ttk.Label(self, text="Cantidad:").grid(row=5, column=0, padx=5, pady=5)
        self.entry_cantidad = ttk.Entry(self)
        self.entry_cantidad.grid(row=5, column=1, padx=5, pady=5)

        self.boton_registrar = ttk.Button(
            self, text="Registrar Libro", command=self.registrar
        )
        self.boton_registrar.grid(row=6, columnspan=2, pady=(20, 10))

    def cargar_autores(self):
        cursor = self.gestor_libros.db.get_connection().cursor()
        cursor.execute("SELECT nombre, apellido FROM autor")
        autores = cursor.fetchall()
        print(
            "Autores cargados:", autores
        )  # Verificar que los autores se cargan correctamente
        self.combo_autores["values"] = [f"{autor[0]} {autor[1]}" for autor in autores]
        cursor.close()

    def registrar(self):
        isbn = self.entry_isbn.get()
        titulo = self.entry_titulo.get()
        genero = self.entry_genero.get()
        anio_publicacion = self.entry_anio_publicacion.get()
        autor_seleccionado = self.combo_autores.get()
        cantidad = self.entry_cantidad.get()

        # Validar campos obligatorios
        if not all(
            [isbn, titulo, genero, anio_publicacion, autor_seleccionado, cantidad]
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            anio_publicacion = int(anio_publicacion)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror(
                "Error", "El año de publicación y la cantidad deben ser números."
            )
            return

        # Obtener el autor seleccionado
        autor_nombre, autor_apellido = autor_seleccionado.split(" ", 1)
        autor_nombre = autor_nombre.strip()
        autor_apellido = autor_apellido.strip()

        cursor = self.gestor_libros.db.get_connection().cursor()
        cursor.execute(
            "SELECT id FROM autor WHERE nombre = ? AND apellido = ?",
            (autor_nombre, autor_apellido),
        )
        autor_resultado = cursor.fetchone()
        print(
            f"Resultado búsqueda autor: {autor_resultado}"
        )  # Verificar si el autor se encuentra

        if autor_resultado:
            autor_id = autor_resultado[0]
        else:
            print(f"Error: Autor no encontrado: {autor_nombre} {autor_apellido}")
            messagebox.showerror("Error", "Autor no encontrado en la base de datos.")
            cursor.close()
            return

        # Intentar registrar el libro
        try:
            print(f"Registrando libro con ISBN: {isbn}")
            self.gestor_libros.registrar_libro(
                isbn, titulo, genero, anio_publicacion, autor_id, cantidad
            )
            messagebox.showinfo("Éxito", "Libro registrado con éxito.")
            self.limpiar_campos()
        except Exception as e:
            print(f"Error al registrar el libro: {e}")
            messagebox.showerror("Error", "No se pudo registrar el libro.")

    def limpiar_campos(self):
        self.entry_isbn.delete(0, tk.END)
        self.entry_titulo.delete(0, tk.END)
        self.entry_genero.delete(0, tk.END)
        self.entry_anio_publicacion.delete(0, tk.END)
        self.combo_autores.set("")
        self.entry_cantidad.delete(0, tk.END)
