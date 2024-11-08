class Prestamo:
    def __init__(self, ID, usuario, libro, fechaPrestamo, fechaDevolucion):
        self.ID = ID
        self.usuario = usuario
        self.libro = libro
        self.fechaPrestamo = fechaPrestamo
        self.fechaDevolucion = fechaDevolucion

    def guardar(self, db):
        try:
            db.cursor.execute(
                """
                INSERT INTO Prestamo (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion) 
                VALUES (?, ?, ?, ?)
            """,
                (self.usuario, self.libro, self.fechaPrestamo, self.fechaDevolucion),
            )
            db.conexion.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def consultar(db, prestamo_id):
        try:
            db.cursor.execute("SELECT * FROM Prestamo WHERE id = ?", (prestamo_id,))
            resultado = db.cursor.fetchone()
            return resultado if resultado else None
        except Exception as e:
            return e

    def modificar(self, db):
        try:
            db.cursor.execute(
                """
                UPDATE Prestamo 
                SET usuario_id = ?, libro_isbn = ?, fecha_prestamo = ?, fecha_devolucion = ?
                WHERE id = ?
            """,
                (
                    self.usuario,
                    self.libro,
                    self.fechaPrestamo,
                    self.fechaDevolucion,
                    self.ID,
                ),
            )
            db.conexion.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def eliminar(db, prestamo_id):
        try:
            db.cursor.execute("DELETE FROM Prestamo WHERE id = ?", (prestamo_id,))
            db.conexion.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def registrar_devolucion(db, prestamo_id, en_condiciones=True):
        try:
            if not en_condiciones:
                print("El libro no está en buenas condiciones. Anotar para revisar.")

            # Actualizar la fecha de devolución en el préstamo
            db.cursor.execute(
                """
                UPDATE Prestamo
                SET fecha_devolucion = date('now')
                WHERE id = ?
            """,
                (prestamo_id,),
            )

            # Obtener el ISBN del libro del préstamo
            db.cursor.execute(
                "SELECT libro_isbn FROM Prestamo WHERE id = ?", (prestamo_id,)
            )
            libro_isbn = db.cursor.fetchone()[0]

            # Actualizar la cantidad disponible en el inventario de libros
            db.cursor.execute(
                """
                UPDATE Libro
                SET cantidad = cantidad + 1
                WHERE isbn = ?
            """,
                (libro_isbn,),
            )

            db.conexion.commit()
            return True
        except Exception as e:
            return e
