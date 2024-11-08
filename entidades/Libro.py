class Libro:
    def __init__(self, isbn, titulo, genero, anio_publicacion, autor_id, cantidad):
        self.isbn = isbn
        self.titulo = titulo
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.autor_id = autor_id
        self.cantidad = cantidad

    def guardar(self, db):
        try:
            db.cursor.execute(
                """
                INSERT INTO Libro (isbn, titulo, genero, anio_publicacion, autor_id, cantidad) 
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    self.isbn,
                    self.titulo,
                    self.genero,
                    self.anio_publicacion,
                    self.autor_id,
                    self.cantidad,
                ),
            )
            db.conexion.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def consultar(db, isbn):
        try:
            db.cursor.execute("SELECT * FROM Libro WHERE isbn = ?", (isbn,))
            resultado = db.cursor.fetchone()
            return resultado if resultado else None
        except Exception as e:
            return e

    def modificar(self, db):
        try:
            db.cursor.execute(
                """
                UPDATE Libro 
                SET titulo = ?, genero = ?, anio_publicacion = ?, autor_id = ?, cantidad = ?
                WHERE isbn = ?
            """,
                (
                    self.titulo,
                    self.genero,
                    self.anio_publicacion,
                    self.autor_id,
                    self.cantidad,
                    self.isbn,
                ),
            )
            db.conexion.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def eliminar(db, isbn):
        try:
            db.cursor.execute("DELETE FROM Libro WHERE isbn = ?", (isbn,))
            db.conexion.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def consultar_disponibilidad(db, isbn):
        try:
            db.cursor.execute("SELECT cantidad FROM Libro WHERE isbn = ?", (isbn,))
            cantidad = db.cursor.fetchone()
            return cantidad[0] > 0 if cantidad else False
        except Exception as e:
            return e
