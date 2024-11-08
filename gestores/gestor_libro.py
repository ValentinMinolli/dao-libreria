from entidades.Libro import Libro

from base_de_datos.database_connection import DatabaseConnection
from entidades.notificador.notificador import Notificador


class Gestor_Libros(Notificador):
    _instance = None  # Singleton para Gestor_Libros

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Gestor_Libros, cls).__new__(cls)
            cls._instance.db = (
                DatabaseConnection()
            )  # Instancia única de la conexión a la BD
            from presentacion.interfaz_principal import Aplicacion

            cls._instance.suscriptor = Aplicacion()
        return cls._instance

    def notificar(self):
        self.suscriptor.recibir_notificacion()

    def registrar(self, isbn, titulo, genero, anio_publicacion, autor_id, cantidad):
        """
        Registra un libro en la base de datos si no existe previamente.
        """
        try:
            cursor = self.db.get_connection().cursor()

            # Comprobar si el libro ya existe
            cursor.execute("SELECT * FROM libro WHERE isbn = ?", (isbn,))
            if cursor.fetchone() is not None:
                print("El libro ya existe.")
                return False  # El libro ya existe

            # Registrar el nuevo libro
            cursor.execute(
                "INSERT INTO libro (isbn, titulo, genero, anio_publicacion, autor_id, cantidad) VALUES (?, ?, ?, ?, ?, ?)",
                (isbn, titulo, genero, anio_publicacion, autor_id, cantidad),
            )
            self.db.get_connection().commit()
            self.notificar()
            return True  # Inserción exitosa
        except Exception as e:
            print(f"Error al registrar el libro: {e}")
            self.db.get_connection().rollback()
            return False
        finally:
            cursor.close()

    def obtener_isbn_libros(self):
        """
        Retorna una lista de los isbns de los libros.
        """
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT isbn FROM libro")
        isbns = cursor.fetchall()
        cursor.close()

        # Transformar los resultados en instancias de Libros
        return [
            Libro(
                isbn=row[0],
                titulo=None,
                genero=None,
                anio_publicacion=None,
                autor_id=None,
                cantidad=None,
            )
            for row in isbns
        ]
