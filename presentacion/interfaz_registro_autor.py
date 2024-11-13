from gestores.gestor_autor import Gestor_Autores

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Interfaz_Registro_Autor(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancia del gestor de autores
        self.gestor_autores = Gestor_Autores()

        # Crear los elementos de la interfaz con separación
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_apellido = ttk.Entry(self)
        self.entry_apellido.grid(row=1, column=1, padx=5, pady=5)

        #ttk.Label(self, text="Nacionalidad:").grid(row=2, column=0, padx=5, pady=5)
        #self.entry_nacionalidad = ttk.Entry(self)
        #self.entry_nacionalidad.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Nacionalidad:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.combo_nacionalidad = ttk.Combobox(
            self, state="readonly", values=["Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Antigua y Barbuda", "Arabia Saudita", "Argelia", "Argentina", 
    "Armenia", "Australia", "Austria", "Azerbaiyán", "Bahamas", "Bangladés", "Barbados", "Baréin", "Bélgica", 
    "Belice", "Benín", "Bielorrusia", "Birmania", "Bolivia", "Bosnia y Herzegovina", "Botsuana", "Brasil", "Brunéi", 
    "Bulgaria", "Burkina Faso", "Burundi", "Bután", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Catar", "Chad", 
    "Chile", "China", "Chipre", "Colombia", "Comoras", "Corea del Norte", "Corea del Sur", "Costa de Marfil", 
    "Costa Rica", "Croacia", "Cuba", "Dinamarca", "Dominica", "Ecuador", "Egipto", "El Salvador", "Emiratos Árabes Unidos", 
    "Eritrea", "Eslovaquia", "Eslovenia", "España", "Estados Unidos", "Estonia", "Esuatini", "Etiopía", "Filipinas", 
    "Finlandia", "Fiyi", "Francia", "Gabón", "Gambia", "Georgia", "Ghana", "Granada", "Grecia", "Guatemala", 
    "Guinea", "Guinea-Bisáu", "Guinea Ecuatorial", "Guyana", "Haití", "Honduras", "Hungría", "India", "Indonesia", 
    "Irak", "Irán", "Irlanda", "Islandia", "Islas Marshall", "Islas Salomón", "Israel", "Italia", "Jamaica", "Japón", 
    "Jordania", "Kazajistán", "Kenia", "Kirguistán", "Kiribati", "Kuwait", "Laos", "Lesoto", "Letonia", "Líbano", 
    "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", "Madagascar", "Malasia", "Malaui", "Maldivas", 
    "Malí", "Malta", "Marruecos", "Mauricio", "Mauritania", "México", "Micronesia", "Moldavia", "Mónaco", 
    "Mongolia", "Montenegro", "Mozambique", "Namibia", "Nauru", "Nepal", "Nicaragua", "Níger", "Nigeria", "Noruega", 
    "Nueva Zelanda", "Omán", "Países Bajos", "Pakistán", "Palaos", "Panamá", "Papúa Nueva Guinea", "Paraguay", 
    "Perú", "Polonia", "Portugal", "Reino Unido", "República Centroafricana", "República Checa", 
    "República de Macedonia del Norte", "República del Congo", "República Democrática del Congo", "República Dominicana", 
    "Ruanda", "Rumania", "Rusia", "Samoa", "San Cristóbal y Nieves", "San Marino", "San Vicente y las Granadinas", 
    "Santa Lucía", "Santo Tomé y Príncipe", "Senegal", "Serbia", "Seychelles", "Sierra Leona", "Singapur", 
    "Siria", "Somalia", "Sri Lanka", "Suazilandia", "Sudáfrica", "Sudán", "Sudán del Sur", "Suecia", "Suiza", 
    "Surinam", "Tailandia", "Tanzania", "Tayikistán", "Timor Oriental", "Togo", "Tonga", "Trinidad y Tobago", 
    "Túnez", "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", "Uganda", "Uruguay", "Uzbekistán", "Vanuatu", 
    "Venezuela", "Vietnam", "Yemen", "Yibuti", "Zambia", "Zimbabue"]
        )
        self.combo_nacionalidad.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Botón de registro con estilo y separación
        self.boton_registrar = ttk.Button(
            self, text="Registrar Autor", command=self.registrar
        )
        self.boton_registrar.grid(row=4, columnspan=2, pady=(20, 10))

        # Estilo del botón
        estilo = ttk.Style()
        estilo.configure(
            "TButton",
            background="lightblue",
            foreground="black",
            padding=10,
            font=("Arial", 10, "bold"),
        )
        self.boton_registrar.config(style="TButton")

    def validar_numero(self, nuevo_texto):
        # Verifica si el nuevo texto es vacío o si solo contiene números
        return nuevo_texto == "" or nuevo_texto.isdigit()

    def registrar(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        nacionalidad = self.entry_nacionalidad.get()

        # Validar campos obligatorios
        if not nombre or not apellido or not nacionalidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Registrar cliente usando el gestor
        if self.gestor_autores.registrar(nombre, apellido, nacionalidad):
            messagebox.showinfo("Éxito", "Cliente registrado con éxito.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_nacionalidad.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo registrar el autor.")
