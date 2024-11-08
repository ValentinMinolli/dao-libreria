from abc import abstractmethod


class Suscriptor:

    @abstractmethod
    def recibir_notificacion(self):
        pass
