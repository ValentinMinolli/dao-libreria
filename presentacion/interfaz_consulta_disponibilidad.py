# interfaz_consulta_disponibilidad.py
from tkinter import ttk
from tkinter import messagebox

class Interfaz_Consulta_Disponibilidad(ttk.Frame):
    def __init__(self, parent, gestor_libros):
        super().__init__(parent)
        self.gestor_libros = gestor_libros  # Se espera que pases un gestor para consultar disponibilidad

        # Configuración de la interfaz
        ttk.Label(self, text="Consulta Disponibilidad de Libros", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="ISBN del Libro:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_isbn = ttk.Entry(self)
        self.entry_isbn.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.boton_consultar = ttk.Button(self, text="Consultar", command=self.consultar_disponibilidad)
        self.boton_consultar.grid(row=2, columnspan=2, pady=10)

        # Configurar la expansión de la columna
        self.columnconfigure(1, weight=1)

    def consultar_disponibilidad(self):
        isbn = self.entry_isbn.get()
        if not isbn:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el ISBN del libro.")
            return

        disponible = self.gestor_libros.consultar_disponibilidad(isbn)
        if disponible:
            messagebox.showinfo("Disponibilidad", f"El libro con ISBN {isbn} está disponible.")
        else:
            messagebox.showinfo("Disponibilidad", f"El libro con ISBN {isbn} no está disponible.")
