import sqlite3
from sqlite3 import Connection


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect("biblioteca.db")
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance

    def get_connection(self) -> Connection:
        return self.conn

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.__class__._instance = None  # Resetear la instancia al cerrar
