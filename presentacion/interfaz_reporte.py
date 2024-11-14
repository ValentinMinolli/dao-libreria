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

        # Botón para generar el PDF de préstamos vencidos
        self.boton_generar_pdf = ttk.Button(
            self,
            text="Generar PDF de Préstamos Vencidos",
            command=self.generar_pdf_prestamos_vencidos,
        )
        self.boton_generar_pdf.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        # Botón para generar el reporte de libros más prestados
        self.boton_reporte_libros_mas_prestados = ttk.Button(
            self,
            text="Generar PDF de Libros Más Prestados en el Último Mes",
            command=self.generar_reporte_libros_mas_prestados,
        )
        self.boton_reporte_libros_mas_prestados.grid(
            row=3, column=0, columnspan=2, pady=(10, 10)
        )

        # **Nuevo Botón** para generar el reporte de usuarios con cantidad de préstamos
        self.boton_reporte_usuarios_con_prestamos = ttk.Button(
            self,
            text="Generar PDF de Usuarios y Cantidad de Préstamos",
            command=self.generar_reporte_usuarios_con_prestamos,
        )
        self.boton_reporte_usuarios_con_prestamos.grid(
            row=4, column=0, columnspan=2, pady=(10, 10)
        )

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

    def generar_reporte_libros_mas_prestados(self):
        try:
            # Obtener los datos de libros más prestados del último mes
            libros_mas_prestados = (
                self.gestor_prestamos.obtener_libros_mas_prestados_ultimo_mes()
            )

            if not libros_mas_prestados:
                print("No hay préstamos en el último mes para generar el reporte.")
                return

            # Crear el archivo PDF del reporte de libros más prestados
            file_name = "reporte_libros_mas_prestados.pdf"
            c = canvas.Canvas(file_name, pagesize=letter)
            c.setFont("Helvetica", 20)

            # Título del reporte
            c.drawString(100, 750, "Reporte de Libros Más Prestados en el Último Mes")
            c.setFont("Helvetica", 10)

            # Encabezado de las columnas
            c.drawString(50, 720, "ISBN")
            c.drawString(250, 720, "Título")
            c.drawString(450, 720, "Cantidad de Préstamos")

            # Posición vertical para los registros
            y_position = 700
            for libro in libros_mas_prestados:
                c.drawString(50, y_position, libro["isbn"])  # ISBN
                c.drawString(250, y_position, libro["titulo"])  # Título
                c.drawString(450, y_position, str(libro["cantidad"]))  # Cantidad

                y_position -= 20
                if y_position < 50:
                    c.showPage()  # Nueva página si se llena la actual
                    c.setFont("Helvetica", 10)  # Mantener la misma fuente
                    y_position = 750

            # Guardar el archivo PDF
            c.save()
            print(f"Reporte de libros más prestados generado exitosamente: {file_name}")

        except Exception as e:
            print(f"No se pudo generar el reporte de libros más prestados: {e}")

    # Función para generar el reporte de usuarios con cantidad de préstamos
    def generar_reporte_usuarios_con_prestamos(self):
        try:
            # Obtener los datos de usuarios y cantidad de préstamos desde el gestor
            usuarios_con_prestamos = (
                self.gestor_prestamos.obtener_historial_prestamos_usuario()
            )

            if not usuarios_con_prestamos:
                print("No hay usuarios con préstamos para generar el reporte.")
                return

            # Crear el archivo PDF del reporte de usuarios con cantidad de préstamos
            file_name = "reporte_usuarios_con_prestamos.pdf"
            c = canvas.Canvas(file_name, pagesize=letter)
            c.setFont("Helvetica", 20)

            # Título del reporte
            c.drawString(100, 750, "Reporte de Usuarios y Cantidad de Préstamos")
            c.setFont("Helvetica", 10)

            # Encabezado de las columnas
            c.drawString(50, 720, "Nombre")
            c.drawString(250, 720, "Apellido")
            c.drawString(450, 720, "Cantidad de Préstamos")

            # Posición vertical para los registros
            y_position = 700
            for usuario in usuarios_con_prestamos:
                c.drawString(50, y_position, usuario["nombre"])  # Nombre
                c.drawString(250, y_position, usuario["apellido"])  # Apellido
                c.drawString(
                    450, y_position, str(usuario["cantidad_prestamos"])
                )  # Cantidad

                y_position -= 20
                if y_position < 50:
                    c.showPage()  # Nueva página si se llena la actual
                    c.setFont("Helvetica", 10)  # Mantener la misma fuente
                    y_position = 750

            # Guardar el archivo PDF
            c.save()
            print(
                f"Reporte de usuarios con préstamos generado exitosamente: {file_name}"
            )

        except Exception as e:
            print(f"No se pudo generar el reporte de usuarios con préstamos: {e}")
