from .database_connection import DatabaseConnection


def crear_base_de_datos():
    db = DatabaseConnection()
    cursor = db.get_connection().cursor()

    # Crear tabla Autor
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Autor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            nacionalidad TEXT NOT NULL
            )
    """
    )

    # Crear tabla Libro
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Libro (
            isbn TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            anio_publicacion INTEGER NOT NULL,
            autor_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            FOREIGN KEY(autor_id) REFERENCES Autor(id)
            )
        """
    )

    # Crear tabla Usuario
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono INTEGER NOT NULL
            )
        """
    )

    # Crear tabla Prestamo
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Prestamo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            libro_isbn TEXT NOT NULL,
            fecha_prestamo DATE NOT NULL,
            fecha_devolucion DATE NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente de Devolución',
            FOREIGN KEY(usuario_id) REFERENCES Usuario(id),
            FOREIGN KEY(libro_isbn) REFERENCES Libro(isbn)
            )
    """
    )

    db.get_connection().commit()


def cargar_datos_mock():
    db = DatabaseConnection()
    cursor = db.get_connection().cursor()

    # Verificar si ya hay datos en la tabla autores
    cursor.execute("SELECT COUNT(*) FROM autor")
    if cursor.fetchone()[0] == 0:  # Si la tabla está vacía, insertar autores
        autores = [
            ("Brian", "Tracy", "Estados Unidos"),
            ("Mario", "Puzo", "Italia"),
            ("Eckhart", "Tolle", "Alemania"),
        ]
        cursor.executemany(
            "INSERT INTO autor (nombre, apellido, nacionalidad) VALUES (?, ?, ?)",
            autores,
        )

    # Verificar si ya hay datos en la tabla libros
    cursor.execute("SELECT COUNT(*) FROM libro")
    if cursor.fetchone()[0] == 0:  # Si la tabla está vacía, insertar libros
        libros = [
            ("0-306-40615-2", "Si lo Crees, lo Creas", "Autoayuda", "2018", "1", "18"),
            ("0-395-19395-8", "El Padrino", "Novela", "1969", "2", "3"),
            ("0-436-23312-4", "El Poder del Ahora", "Autoayuda", "1997", "3", "35"),
            (
                "0-341-78421-1",
                "¡Traguese ese Sapo!",
                "Autoayuda",
                "2001",
                "1",
                "65",
            ),
            ("3-212-64331-3", "El Siciliano", "Novela", "1984", "2", "354"),
            ("0-671-74251-2", "Una Nueva Tierra", "Autoayuda", "2005", "3", "53"),
        ]
        cursor.executemany(
            "INSERT INTO libro (isbn, titulo, genero, anio_publicacion, autor_id, cantidad) VALUES (?, ?, ?, ?, ?, ?)",
            libros,
        )

    # Verificar si ya hay datos en la tabla usuarios
    cursor.execute("SELECT COUNT(*) FROM usuario")
    if cursor.fetchone()[0] == 0:  # Si la tabla está vacía, insertar usuarios
        usuarios = [
            ("Valentin", "Minolli", "Estudiante", "Las Heras 285", "3571527817"),
            ("Agustin", "Aron", "Estudiante", "Antartida Argentina 119", "3543313674"),
            ("Olivia", "Pacheco", "Estudiante", "Paul Groussac 112", "3513895464"),
            ("Milagros", "Diaz", "Estudiante", "Dean Funes 732", "3514591847"),
        ]
        cursor.executemany(
            "INSERT INTO usuario (nombre, apellido, tipo_usuario, direccion, telefono) VALUES (?, ?, ?, ?, ?)",
            usuarios,
        )

        # fecha_prestamo
        # fecha_devolucion
    cursor.execute("SELECT COUNT(*) FROM prestamo")
    if cursor.fetchone()[0] == 0:  # Si la tabla está vacía, insertar prestamos
        prestamos = [
            (
                "1",
                "0-306-40615-2",
                "2024-11-07",
                "2024-11-15",
                "Pendiente de Devolución",
            ),
            (
                "1",
                "0-395-19395-8",
                "2024-11-07",
                "2024-11-16",
                "Pendiente de Devolución",
            ),
            ("2", "0-436-23312-4", "2024-11-07", "2024-11-16", "Devuelto"),
            ("3", "0-341-78421-1", "2024-11-07", "2024-11-17", "Devuelvo"),
            (
                "4",
                "3-212-64331-3",
                "2024-11-07",
                "2024-11-18",
                "Pendiente de Devolución",
            ),
        ]
        cursor.executemany(
            "INSERT INTO prestamo (usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion, estado) VALUES (?, ?, ?, ?, ?)",
            prestamos,
        )

    db.get_connection().commit()


# Crear la base de datos
crear_base_de_datos()

# Cargar datos de prueba
cargar_datos_mock()
