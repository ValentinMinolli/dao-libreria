from tkinter import ttk
from tkinter import messagebox
from gestores.gestor_libro import Gestor_Libros

class Interfaz_Consulta_Disponibilidad(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.gestor_libros = Gestor_Libros()

        # Configuración de la interfaz
        ttk.Label(
            self, text="Consulta Disponibilidad de Libros", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="ISBN del Libro:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_isbn = ttk.Entry(self)
        self.entry_isbn.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.boton_consultar = ttk.Button(
            self, text="Consultar", command=self.consultar_disponibilidad
        )
        self.boton_consultar.grid(row=2, columnspan=2, pady=10)

        # Configurar la expansión de la columna
        self.columnconfigure(1, weight=1)

    # En Interfaz_Consulta_Disponibilidad

    # En Interfaz_Consulta_Disponibilidad

    def consultar_disponibilidad(self):
        isbn = self.entry_isbn.get()
        if not isbn:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el ISBN del libro.")
            return

    # Llamada al método actualizado para obtener cantidad, disponibilidad y copias prestadas
        cantidad_total, disponible, copias_prestadas = self.gestor_libros.consultar_disponibilidad(
            self.gestor_libros.db, isbn
        )
    
        if disponible:
            messagebox.showinfo(
                "Disponibilidad",
                f"El libro con ISBN {isbn} está disponible.\n"
                f"Copias en stock: {cantidad_total}\n"
                f"Copias prestadas: {copias_prestadas}"
            )
        else:
            messagebox.showinfo(
                "Disponibilidad",
                f"El libro con ISBN {isbn} no está disponible.\n"
                f"Copias en stock: {cantidad_total}\n"
                f"Copias prestadas: {copias_prestadas}"
            )



