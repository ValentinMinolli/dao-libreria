import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

from gestores.gestor_prestamo import Gestor_Prestamos


class Interfaz_Reportes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancia del gestor de préstamos
        self.gestor_prestamos = Gestor_Prestamos()

        # Configuración de estilo
        estilo = ttk.Style()
        estilo.configure("TFrame", background="#f2f2f2")
        estilo.configure("TLabel", background="#f2f2f2", font=("Arial", 10, "bold"))
        estilo.configure(
            "TButton",
            background="#007ACC",
            foreground="white",
            font=("Arial", 10, "bold"),
        )

        # Crear un canvas para agregar la línea divisoria
        self.canvas = tk.Canvas(self, bg="#f2f2f2", height=1, width=500)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=(10, 10))

        # Título centrado y más grande
        titulo = ttk.Label(
            self, text="Reporte de Préstamos Vencidos", font=("Arial", 14, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(10))

        # Línea divisoria
        self.canvas.create_line(0, 0, 500, 0, width=2, fill="black")

        # Botón para generar el PDF
        self.boton_generar_pdf = ttk.Button(
            self,
            text="Generar PDF de Préstamos Vencidos",
            command=self.generar_pdf_prestamos_vencidos,
        )
        self.boton_generar_pdf.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        # Configuración del frame
        self.columnconfigure(0, weight=1)

    def generar_pdf_prestamos_vencidos(self):
        try:
            # Obtener los préstamos vencidos desde el gestor de préstamos
            prestamos_vencidos = self.gestor_prestamos.obtener_prestamos_vencidos()

            # Si no hay préstamos vencidos, mostrar mensaje y salir
            if not prestamos_vencidos:
                print("No hay préstamos vencidos para generar el reporte.")
                return

            # Crear el archivo PDF
            file_name = "reporte_prestamos_vencidos.pdf"
            c = canvas.Canvas(file_name, pagesize=letter)
            c.setFont("Helvetica", 25)

            # Título del reporte
            c.drawString(100, 750, "Reporte de Préstamos Vencidos")
            c.setFont("Helvetica", 8)  # Reducir tamaño de fuente para más espacio

            # Definir márgenes y longitud de la línea divisoria
            margen_izquierdo = 50  # Inicia donde empieza la primera columna
            margen_derecho = 550  # Termina antes de pasar el margen derecho

            # Ajustar la línea divisoria para que respete los márgenes
            c.setLineWidth(0.5)
            c.line(
                margen_izquierdo, 735, margen_derecho, 735
            )  # Línea divisoria ajustada

            # Encabezado de las columnas (ajustar espaciado entre columnas)
            c.drawString(margen_izquierdo, 720, "Nombre del Usuario")
            c.drawString(margen_izquierdo + 130, 720, "Apellido del Usuario")
            c.drawString(margen_izquierdo + 260, 720, "ISBN del Libro")
            c.drawString(margen_izquierdo + 390, 720, "Días Vencidos")

            # Mostrar los préstamos vencidos
            y_position = 700  # Posición vertical para los registros
            for prestamo in prestamos_vencidos:
                nombre_usuario = prestamo["nombre_usuario"]
                apellido_usuario = prestamo["apellido_usuario"]
                libro_isbn = prestamo["libro_isbn"]
                dias_vencidos = prestamo["dias_vencidos"]

                # Dibujar los valores de las columnas directamente en posiciones fijas
                c.drawString(margen_izquierdo, y_position, nombre_usuario)
                c.drawString(margen_izquierdo + 130, y_position, apellido_usuario)
                c.drawString(margen_izquierdo + 260, y_position, libro_isbn)
                c.drawString(margen_izquierdo + 390, y_position, str(dias_vencidos))

                # Ajustar la posición para el siguiente registro
                y_position -= 15  # Espacio entre filas

                # Verificar si llegamos al final de la página
                if y_position < 50:
                    c.showPage()  # Crear una nueva página
                    c.setFont("Helvetica", 8)  # Mantener la misma fuente
                    y_position = 750  # Restablecer la posición

            # Guardar el archivo PDF
            c.save()

            print(f"Reporte generado exitosamente: {file_name}")

        except Exception as e:
            print(f"No se pudo generar el PDF: {e}")
