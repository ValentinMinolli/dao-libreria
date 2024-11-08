from base_de_datos.database_connection import DatabaseConnection
from entidades.notificador.notificador import Notificador


class Gestor_Autores(Notificador):
    _instance = None  # Singleton para Gestor_Autores

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Gestor_Autores, cls).__new__(cls)
            cls._instance.db = (
                DatabaseConnection()
            )  # Instancia única de la conexión a la BD
            from presentacion.interfaz_principal import Aplicacion

            cls._instance.suscriptor = Aplicacion()
        return cls._instance

    def notificar(self):
        self.suscriptor.recibir_notificacion()

    def registrar(self, nombre, apellido, nacionalidad):
        """
        Registra un autor en la base de datos si no existe previamente.
        """
        try:
            cursor = self.db.get_connection().cursor()

            # Comprobar si el autor ya existe
            cursor.execute(
                "SELECT * FROM autor WHERE nombre = ? AND apellido = ?",
                (nombre, apellido),
            )
            if cursor.fetchone() is not None:
                print("El autor ya existe.")
                return False  # El autor ya existe

            # Registrar el nuevo autor
            cursor.execute(
                "INSERT INTO autor (nombre, apellido, nacionalidad) VALUES (?, ?, ?)",
                (nombre, apellido, nacionalidad),
            )
            self.db.get_connection().commit()
            self.notificar()
            return True  # Inserción exitosa
        except Exception as e:
            print(f"Error al registrar el autor: {e}")
            self.db.get_connection().rollback()
            return False
        finally:
            cursor.close()
