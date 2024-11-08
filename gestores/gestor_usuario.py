from base_de_datos.database_connection import DatabaseConnection
from entidades.notificador.notificador import Notificador
from entidades.Usuario import Usuario


class Gestor_Usuarios(Notificador):
    _instance = None  # Singleton para Gestor_Usuarios

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Gestor_Usuarios, cls).__new__(cls)
            cls._instance.db = (
                DatabaseConnection()
            )  # Instancia única de la conexión a la BD
            from presentacion.interfaz_principal import Aplicacion

            cls._instance.suscriptor = Aplicacion()
        return cls._instance

    def notificar(self):
        self.suscriptor.recibir_notificacion()

    def registrar(self, nombre, apellido, tipo_usuario, direccion, telefono):
        """
        Registra un usuario en la base de datos si no existe previamente.
        """
        try:
            cursor = self.db.get_connection().cursor()

            # Comprobar si el usuario ya existe
            cursor.execute(
                "SELECT * FROM usuario WHERE nombre = ? AND apellido = ?",
                (nombre, apellido),
            )
            if cursor.fetchone() is not None:
                print("El usuario ya existe.")
                return False  # El usuario ya existe

            # Registrar el nuevo usuario
            cursor.execute(
                "INSERT INTO usuario (nombre, apellido, tipo_usuario, direccion, telefono) VALUES (?, ?, ?, ?, ?)",
                (nombre, apellido, tipo_usuario, direccion, telefono),
            )
            self.db.get_connection().commit()
            self.notificar()
            return True  # Inserción exitosa
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
            self.db.get_connection().rollback()
            return False
        finally:
            cursor.close()

    def obtener_usuarios(self):
        """
        Retorna una lista de los ids de los usuarios.
        """
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT id FROM usuario")
        ids = cursor.fetchall()
        cursor.close()

        # Transformar los resultados en instancias de Usuarios
        return [
            Usuario(
                id=row[0],
                nombre=None,
                apellido=None,
                direccion=None,
                telefono=None,
            )
            for row in ids
        ]
