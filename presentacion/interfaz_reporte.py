import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# from gestores.gestorServicio import GestorDeServicios
# from gestores.gestorAuto import GestorDeAutos
# from gestores.gestorVenta import GestorDeVentas


class Interfaz_Reportes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configuración de estilo para los botones
        estilo = ttk.Style()
        estilo.configure("TButton", padding=10, font=("Arial", 10, "bold"))

        # Título de la interfaz
        ttk.Label(self, text="Consultas de Reportes", font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(10, 20)
        )

        self.boton_listado_ventas = ttk.Button(
            self,
            text="Listado de préstamos vencidos",
            command=self.listado_prestamos_vencidos,
        )
        self.boton_listado_ventas.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )

        self.boton_ingresos_totales = ttk.Button(
            self,
            text="Listado de libros más prestados en el último mes (PDF) (PDF)",
            command=self.listado_libros_mas_prestados,
        )
        self.boton_ingresos_totales.grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )

        self.boton_autos_mas_vendidos = ttk.Button(
            self,
            text="Listado de usuarios que han tomado más libros en préstamo (PDF)",
            command=self.cant_libros_prestados_a_usuario,
        )
        self.boton_autos_mas_vendidos.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )

    # Función para generar el reporte en PDF
    def listado_prestamos_vencidos(self, prestamos):
        try:
            nombre_archivo = "reporte_prestamos_vencidos.pdf"
            c = canvas.Canvas(nombre_archivo, pagesize=letter)
            width, height = letter

            # Título del PDF
            c.setFont("Helvetica-Bold", 16)
            c.drawString(200, height - 50, "Reporte de Préstamos Vencidos")

            # Detalles del préstamo
            c.setFont("Helvetica", 10)
            y_position = height - 80

            for prestamo in prestamos:
                isbn = prestamo["isbn"]
                nombre_libro = prestamo["nombre_libro"]
                fecha_prestamo = datetime.strptime(
                    prestamo["fecha_prestamo"], "%Y-%m-%d"
                )
                fecha_actual = datetime.now()

                # Calcular el tiempo vencido
                tiempo_vencido = (fecha_actual - fecha_prestamo).days

                c.drawString(50, y_position, f"ISBN: {isbn}")
                c.drawString(200, y_position, f"Nombre: {nombre_libro}")
                c.drawString(400, y_position, f"Vencido por: {tiempo_vencido} días")

                y_position -= 20

                # Si llegamos al final de la página, comenzamos una nueva página
                if y_position < 40:
                    c.showPage()
                    y_position = height - 50

            # Guardar el archivo PDF
            c.save()
            messagebox.showinfo("Éxito", f"Reporte generado: {nombre_archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al generar el reporte: {e}")

    def listado_libros_mas_prestados(self):
        pass

    def cant_libros_prestados_a_usuario(self):
        pass
