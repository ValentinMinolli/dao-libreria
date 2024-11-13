from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generar_reporte_prestamos_vencidos(prestamos):
    # Crear el PDF
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
        isbn = prestamo['isbn']
        nombre_libro = prestamo['nombre_libro']
        fecha_prestamo = datetime.strptime(prestamo['fecha_prestamo'], "%Y-%m-%d")
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
    print(f"Reporte generado: {nombre_archivo}")

# Ejemplo de datos de préstamos (esto puede venir de la base de datos)
prestamos_vencidos = [
    {"isbn": "978-3-16-148410-0", "nombre_libro": "El Gran Libro", "fecha_prestamo": "2024-10-01"},
    {"isbn": "978-1-23-456789-7", "nombre_libro": "Python para Todos", "fecha_prestamo": "2024-08-15"},
]

# Llamada a la función para generar el reporte
generar_reporte_prestamos_vencidos(prestamos_vencidos)

