class Prestamo:
    def __init__(
        self, id, usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion, estado
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.libro_isbn = libro_isbn
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado
