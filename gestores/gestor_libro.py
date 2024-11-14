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

    def registrar_libro(
        self, isbn, titulo, genero, anio_publicacion, autor_id, cantidad
    ):
        try:
            cursor = self.db.get_connection().cursor()

            # Verificar si el ISBN ya existe
            print(f"Verificando si el ISBN {isbn} ya existe...")
            cursor.execute("SELECT isbn FROM libro WHERE isbn = ?", (isbn,))
            if cursor.fetchone():
                print(f"Error: El ISBN {isbn} ya existe.")
                raise Exception(f"El ISBN {isbn} ya está registrado.")

            # Insertar libro
            print(f"Registrando libro con ISBN: {isbn}")
            cursor.execute(
                "INSERT INTO libro (isbn, titulo, genero, anio_publicacion, autor_id, cantidad) VALUES (?, ?, ?, ?, ?, ?)",
                (isbn, titulo, genero, anio_publicacion, autor_id, cantidad),
            )

            # Confirmar la transacción
            self.db.get_connection().commit()
            print(f"Libro con ISBN {isbn} registrado exitosamente.")
        except Exception as e:
            print(f"Error al registrar el libro: {e}")
            raise e
        finally:
            cursor.close()  # Asegurarnos de cerrar el cursor

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
            # Crear cursor para la base de datos
            cursor = db.get_connection().cursor()

            # Consultar la cantidad total de copias en stock
            cursor.execute("SELECT cantidad FROM libro WHERE isbn = ?", (isbn,))
            resultado_libro = cursor.fetchone()

            # Si el libro no existe, devolver que no está disponible y 0 copias prestadas
            if resultado_libro is None:
                return 0, False, 0  # No existe el libro en la base de datos

            cantidad_total = resultado_libro[0]
            disponible = cantidad_total > 0

            # Consultar la cantidad de copias actualmente prestadas y en estado pendiente de devolución
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM prestamo 
                WHERE libro_isbn = ? AND estado = 'Pendiente de Devolución'
            """,
                (isbn,),
            )
            copias_prestadas = cursor.fetchone()[0]

            # Calcular las copias disponibles como total - prestadas
            copias_disponibles = max(0, cantidad_total - copias_prestadas)

            return cantidad_total, copias_disponibles > 0, copias_prestadas
        except Exception as e:
            print(f"Error al consultar disponibilidad: {e}")
            return 0, False, 0  # Valores seguros en caso de error
        finally:
            cursor.close()
