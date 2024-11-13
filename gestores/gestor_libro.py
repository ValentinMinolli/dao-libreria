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

    def registrar_con_autor(
        self,
        isbn,
        titulo,
        genero,
        anio_publicacion,
        nombre_autor,
        apellido_autor,
        cantidad,
    ):
        """
        Registra un libro en la base de datos y maneja la creación de un autor si no existe.
        """
        try:
            cursor = self.db.get_connection().cursor()

            # Verificar si el autor ya existe
            cursor.execute(
                "SELECT id FROM autor WHERE nombre = ? AND apellido = ?",
                (nombre_autor, apellido_autor),
            )
            autor = cursor.fetchone()

            # Si el autor no existe, lo insertamos
            if autor is None:
                cursor.execute(
                    "INSERT INTO autor (nombre, apellido) VALUES (?, ?)",
                    (nombre_autor, apellido_autor),
                )
                autor_id = cursor.lastrowid  # Obtiene el id del nuevo autor
            else:
                autor_id = autor[0]  # Usamos el id del autor existente

            # Comprobar si el libro ya existe
            cursor.execute("SELECT * FROM libro WHERE isbn = ?", (isbn,))
            if cursor.fetchone() is not None:
                print("El libro ya existe.")
                return False  # El libro ya existe

            # Registrar el nuevo libro con el autor_id obtenido
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

    @staticmethod
    def consultar(self, isbn):
        try:
            self.db.cursor.execute("SELECT * FROM Libro WHERE isbn = ?", (isbn,))
            resultado = self.db.cursor.fetchone()
            return resultado if resultado else None
        except Exception as e:
            return e

    def modificar(self, titulo, genero, anio_publicacion, autor_id, cantidad, isbn):
        try:
            # Verifica la conexión
            conexion = self.db.get_connection()
            cursor = conexion.cursor()

            print(
                f"Actualizando libro con ISBN {isbn}: cantidad a establecer = {cantidad}"
            )  # Debug

            # Ejecuta la consulta de actualización
            cursor.execute(
                """
                UPDATE libro
                SET titulo = ?, genero = ?, anio_publicacion = ?, autor_id = ?, cantidad = ?
                WHERE isbn = ?
                """,
                (titulo, genero, anio_publicacion, autor_id, cantidad, isbn),
            )

            # Commit y verificación del cambio
            conexion.commit()
            if cursor.rowcount == 0:
                print("No se actualizó ningún registro. Verifica el ISBN.")
            else:
                print("Registro actualizado exitosamente. Nueva cantidad:", cantidad)

            cursor.close()
            return True
        except Exception as e:
            print(f"Error al modificar el libro: {e}")
            return False

    @staticmethod
    def consultar_disponibilidad(db, isbn):
        try:
            db.cursor.execute("SELECT cantidad FROM Libro WHERE isbn = ?", (isbn,))
            cantidad = db.cursor.fetchone()
            return cantidad[0] > 0 if cantidad else False
        except Exception as e:
            return e
