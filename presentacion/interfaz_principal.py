from tkinter import ttk

from presentacion.interfaz_registro_autor import Interfaz_Registro_Autor
from presentacion.interfaz_registro_libro import Interfaz_Registro_Libro
from presentacion.interfaz_registro_usuario import Interfaz_Registro_Usuario
from presentacion.interfaz_registro_prestamo import Interfaz_Registro_Prestamo

# from gui.interfaz_consulta_autos_vendidos import InterfazConsultaAutosVendidos
# from gui.interfaz_consulta_servicios import InterfazConsultaServiciosAuto
# from gui.interfaz_reportes import InterfazReportes
from entidades.notificador.suscriptor import Suscriptor


class Aplicacion(Suscriptor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def cargar_ventanas(self, active_index=0):
        for tab in self.contenedor.tabs():
            self.contenedor.forget(tab)

        # Crear las diferentes páginas
        self.frame_auto = Interfaz_Registro_Autor(self.contenedor)
        self.frame_libro = Interfaz_Registro_Libro(self.contenedor)
        self.frame_usuario = Interfaz_Registro_Usuario(self.contenedor)
        self.frame_prestamo = Interfaz_Registro_Prestamo(self.contenedor)
        # self.frame_servicio = InterfazRegistroServicio(self.contenedor)
        # self.frame_autos_vendidos = InterfazConsultaAutosVendidos(self.contenedor)
        # self.frame_servicio_auto = InterfazConsultaServiciosAuto(self.contenedor)
        # self.frame_reportes = InterfazReportes(self.contenedor)

        # Agregar las páginas al contenedor
        self.contenedor.add(self.frame_auto, text="Registrar Autor")
        self.contenedor.add(self.frame_libro, text="Registrar Libro")
        self.contenedor.add(self.frame_usuario, text="Registrar Usuario")
        self.contenedor.add(self.frame_prestamo, text="Registrar Prestamo")
        # self.contenedor.add(self.frame_servicio, text="Registrar Servicio")
        # self.contenedor.add(self.frame_autos_vendidos, text="Consultar Autos")
        # self.contenedor.add(self.frame_servicio_auto, text="Consultar Servicio")
        # self.contenedor.add(self.frame_reportes, text="Reportes")

        # Volver a la pestaña activa antes de recargar
        self.contenedor.select(active_index)

    def _initialize(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")

        # Crear estilo
        style = ttk.Style()
        style.configure(
            "TButton",
            padding=6,
            relief="flat",
            background="#4CAF50",
            foreground="white",
        )
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TEntry", padding=5)

        # Crear el contenedor principal (Notebook)
        self.contenedor = ttk.Notebook(root)
        self.contenedor.pack(expand=1, fill="both")

        self.cargar_ventanas()

    def recibir_notificacion(self):
        # Guardar la pestaña activa actual
        active_index = self.contenedor.index(self.contenedor.select())
        # Recargar ventanas manteniendo la pestaña activa
        self.cargar_ventanas(active_index)
