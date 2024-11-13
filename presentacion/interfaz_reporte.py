import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Función para generar el reporte en PDF
def generar_reporte_prestamos_vencidos(prestamos):
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
        messagebox.showinfo("Éxito", f"Reporte generado: {nombre_archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al generar el reporte: {e}")

# Función para simular la consulta de préstamos vencidos
def obtener_prestamos_vencidos():
    # Datos simulados (deberían ser obtenidos de la base de datos)
    return [
        {"isbn": "978-3-16-148410-0", "nombre_libro": "El Gran Libro", "fecha_prestamo": "2024-10-01"},
        {"isbn": "978-1-23-456789-7", "nombre_libro": "Python para Todos", "fecha_prestamo": "2024-08-15"},
    ]

# Función para manejar el evento del botón
def generar_reporte():
    prestamos_vencidos = obtener_prestamos_vencidos()
    if prestamos_vencidos:
        generar_reporte_prestamos_vencidos(prestamos_vencidos)
    else:
        messagebox.showwarning("Sin Datos", "No hay préstamos vencidos para mostrar.")

# Crear la ventana principal
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Generador de Reporte de Préstamos Vencidos")
    ventana.geometry("400x200")

    # Título de la ventana
    label = tk.Label(ventana, text="Generar Reporte de Préstamos Vencidos", font=("Helvetica", 14))
    label.pack(pady=20)

    # Botón para generar el reporte
    boton_generar = tk.Button(ventana, text="Generar Reporte", font=("Helvetica", 12), command=generar_reporte)
    boton_generar.pack(pady=20)

    # Iniciar la interfaz
    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()
