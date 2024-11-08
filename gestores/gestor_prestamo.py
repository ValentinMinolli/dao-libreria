from base_de_datos.database_connection import DatabaseConnection
from entidades.notificador.notificador import Notificador


class Gestor_Prestamos(Notificador):
    _instance = None  # Singleton para Gestor_Autores

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

    def registrar(self, usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion):
        """
        Registra un prestamo en la base de datos si no existe previamente.
        """
        try:
            cursor = self.db.get_connection().cursor()

            # Comprobar si el prestamo ya existe
            cursor.execute(
                "SELECT * FROM prestamo WHERE usuario_id = ? AND libro_isbn = ?",
                (usuario_id, libro_isbn),
            )
            if cursor.fetchone() is not None:
                print("El prestamo ya existe.")
                return False  # El prestamo ya existe

            # Registrar el nuevo prestamo
            cursor.execute(
                "INSERT INTO prestamo (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion) VALUES (?, ?, ?, ?)",
                (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion),
            )
            self.db.get_connection().commit()
            self.notificar()
            return True  # Inserción exitosa
        except Exception as e:
            print(f"Error al registrar el prestamo: {e}")
            self.db.get_connection().rollback()
            return False
        finally:
            cursor.close()
