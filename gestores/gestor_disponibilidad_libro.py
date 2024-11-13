from base_de_datos.database_connection import DatabaseConnection

class Gestor_Disponibilidad_Libro:
    _instance = None  # Singleton para Gestor_Disponibilidad_Libro

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Gestor_Disponibilidad_Libro, cls).__new__(cls)
            cls._instance.db = DatabaseConnection()  # Instancia única de la conexión a la BD
        return cls._instance

    def consultar_disponibilidad(self, isbn):
        """
        Consulta si un libro está disponible para préstamo según su ISBN.
        Retorna True si está disponible, False si no lo está.
        """
        try:
            cursor = self.db.get_connection().cursor()

            # Consultar la disponibilidad del libro
            cursor.execute("SELECT disponible FROM libro WHERE isbn = ?", (isbn,))
            resultado = cursor.fetchone()

            if resultado is not None:
                disponible = resultado[0]
                return disponible == 1  # Retorna True si disponible es 1, False si es 0
            else:
                print("El libro con ISBN proporcionado no existe en la base de datos.")
                return None
        except Exception as e:
            print(f"Error al consultar la disponibilidad del libro: {e}")
            return None
        finally:
            cursor.close()
