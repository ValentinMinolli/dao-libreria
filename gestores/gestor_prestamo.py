from base_de_datos.database_connection import DatabaseConnection
from entidades.notificador.notificador import Notificador
from datetime import datetime

class Gestor_Prestamos(Notificador):
    _instance = None  # Singleton para Gestor_Prestamos

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Gestor_Prestamos, cls).__new__(cls)
            cls._instance.db = DatabaseConnection()  # Instancia única de la conexión a la BD
            from presentacion.interfaz_principal import Aplicacion
            cls._instance.suscriptor = Aplicacion()
        return cls._instance

    def notificar(self):
        self.suscriptor.recibir_notificacion()

    def registrar(self, usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion):
        """
        Registra un prestamo en la base de datos si no existe previamente.
        """
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                "SELECT * FROM prestamo WHERE usuario_id = ? AND libro_isbn = ?",
                (usuario_id, libro_isbn),
            )
            if cursor.fetchone() is not None:
                print("El prestamo ya existe.")
                return False

            cursor.execute(
                "INSERT INTO prestamo (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion) VALUES (?, ?, ?, ?)",
                (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion),
            )
            self.db.get_connection().commit()
            self.notificar()
            return True
        except Exception as e:
            print(f"Error al registrar el prestamo: {e}")
            self.db.get_connection().rollback()
            return False
        finally:
            cursor.close()

    def registrar_devolucion(self, isbn, usuario_id, en_condiciones):
        """
        Registra la devolución de un libro en el sistema.
        """
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id FROM prestamo WHERE isbn = ? AND usuario_id = ? AND fecha_devolucion IS NULL",
                (isbn, usuario_id),
            )
            prestamo = cursor.fetchone()
            if prestamo is None:
                print("El préstamo no existe o ya fue devuelto.")
                return False

            fecha_devolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "UPDATE prestamo SET fecha_devolucion = ?, en_condiciones = ? WHERE id = ?",
                (fecha_devolucion, en_condiciones, prestamo[0]),
            )
            connection.commit()

            if en_condiciones.lower() != "sí":
                cursor.execute(
                    "UPDATE libro SET disponible = 0 WHERE isbn = ?", (isbn,)
                )
                connection.commit()

            self.notificar()
            return True
        except Exception as e:
            print(f"Error al registrar la devolución: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()

    def obtener_libros_prestados(self):
        """
        Obtiene una lista de libros actualmente prestados (no devueltos).
        """
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT libro_isbn, usuario_id, fecha_prestamo FROM prestamo WHERE fecha_devolucion IS NULL"
            )
            libros_prestados = cursor.fetchall()

            # Retornar una lista de diccionarios con la información de cada préstamo
            return [
                {"isbn": libro[0], "usuario_id": libro[1], "fecha_prestamo": libro[2]}
                for libro in libros_prestados
            ]
        except Exception as e:
            print(f"Error al obtener libros prestados: {e}")
            return []
        finally:
            cursor.close()

