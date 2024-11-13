from base_de_datos.database_connection import DatabaseConnection
from entidades.notificador.notificador import Notificador
from datetime import datetime
from gestores.gestor_libro import Gestor_Libros
from entidades.Libro import Libro
from entidades.Prestamo import Prestamo


class Gestor_Prestamos(Notificador):
    _instance = None  # Singleton para Gestor_Prestamos

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Gestor_Prestamos, cls).__new__(cls)
            cls._instance.db = (
                DatabaseConnection()
            )  # Instancia única de la conexión a la BD
            from presentacion.interfaz_principal import Aplicacion

            cls._instance.suscriptor = Aplicacion()
        return cls._instance

    def notificar(self):
        self.suscriptor.recibir_notificacion()

    def registrar(
        self,
        usuario_id,
        libro_isbn,
        fecha_prestamo,
        fecha_devolucion,
        estado="Pendiente de Devolución",
    ):
        """
        Registra un préstamo en la base de datos si no existe previamente.
        """
        try:
            gestor_libros = Gestor_Libros()

            # Obtener datos del libro
            cursor = self.db.get_connection().cursor()
            cursor.execute("SELECT * FROM libro WHERE isbn = ?", (libro_isbn,))
            libro_data = cursor.fetchone()

            if not libro_data:
                print("El libro con ese ISBN no existe.")
                return False

            # Crear una instancia de Libro a partir de los datos obtenidos
            libro = Libro(*libro_data)
            nueva_cantidad = libro.cantidad - 1

            if libro.cantidad <= 0:
                print("No hay cantidad disponible.")
                return False

            # Insertar el préstamo
            cursor.execute(
                "INSERT INTO prestamo (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion, estado) VALUES (?, ?, ?, ?, ?)",
                (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion, estado),
            )
            self.db.get_connection().commit()

            # Actualizar cantidad del libro con el orden correcto de parámetros
            gestor_libros.modificar(
                libro.titulo,
                libro.genero,
                libro.anio_publicacion,
                libro.autor_id,
                nueva_cantidad,
                libro.isbn,
            )

            self.notificar()  # Notificar, si aplica
            return True

        except Exception as e:
            print(f"Error al registrar el préstamo: {e}")
            self.db.get_connection().rollback()
            return False

    def obtener_prestamos_pendientes(self, usuario_id):
        """
        Obtiene todos los préstamos pendientes de devolución para un usuario.
        """
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                """
                SELECT * FROM Prestamo
                WHERE usuario_id = ? AND estado = 'Pendiente de Devolución'
                """,
                (usuario_id,),
            )
            prestamos_pendientes = cursor.fetchall()
            cursor.close()

            # Si hay préstamos pendientes, se devuelven como objetos de la clase Prestamo
            prestamos = []
            for prestamo in prestamos_pendientes:
                prestamos.append(
                    Prestamo(*prestamo)
                )  # Asumimos que Prestamo tiene un constructor que toma los datos

            # Verificar que se están obteniendo correctamente los préstamos
            print("Préstamos pendientes:", prestamos)

            return prestamos
        except Exception as e:
            print(f"Error al obtener los préstamos pendientes: {e}")
            return []

    def incrementar_cantidad(self, isbn):
        """
        Incrementa en 1 la cantidad de un libro en la base de datos
        """
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                """
                    UPDATE Libro
                    SET cantidad = cantidad + 1
                    WHERE isbn = ?
                    """,
                (isbn,),
            )
            self.db.get_connection().commit()

            if cursor.rowcount == 0:
                print(
                    f"Error: El libro con ISBN {isbn} no se encuentra en la base de datos."
                )
                return False
            return True
        except Exception as e:
            print(f"Error al incrementar la cantidad del libro: {e}")
            return False

    def registrar_devolucion(self, isbn, usuario_id, condiciones):
        try:
            # Verificar que el libro esté en condiciones
            if condiciones != "Sí":
                print("El libro no está en condiciones. No se puede registrar la devolución.")
                return False
            # Buscar el préstamo pendiente del usuario para el libro seleccionado
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                """
                SELECT * FROM Prestamo WHERE usuario_id = ? AND libro_isbn = ? AND estado = 'Pendiente de Devolución'
                """,
                (usuario_id, isbn),
            )
            prestamo = cursor.fetchone()

            if not prestamo:
                print("No se encontró un préstamo pendiente para este libro.")
                return False  # No se encontró el préstamo pendiente

            # Actualizar el estado del préstamo a "Devuelto" para ese préstamo específico
            cursor.execute(
                """
                UPDATE Prestamo SET estado = 'Devuelto' WHERE id = ? AND usuario_id = ? AND libro_isbn = ?
                """,
                (prestamo[0], usuario_id, isbn),
            )

            # Actualizar la cantidad del libro (sumar 1 al stock)
            cursor.execute(
                """
                UPDATE Libro SET cantidad = cantidad + 1 WHERE isbn = ?
                """,
                (isbn,),
            )

            # Confirmar la transacción
            self.db.get_connection().commit()
            cursor.close()

            return True
        except Exception as e:
            print(f"Error al registrar la devolución: {e}")
            self.db.get_connection().rollback()
            return False
