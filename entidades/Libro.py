from base_de_datos.database_connection import DatabaseConnection


class Libro:
    def __init__(self, isbn, titulo, genero, anio_publicacion, autor_id, cantidad):
        self.isbn = isbn
        self.titulo = titulo
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.autor_id = autor_id
        self.cantidad = cantidad


