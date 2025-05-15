import uuid
from datetime import datetime, timedelta
from enum import Enum

class PollState(Enum):
    ACTIVE = "activa"
    CLOSED = "cerrada"

class Poll:
    def __init__(self, pregunta, opciones, duracion_segundos, tipo="simple"):
        self.id = uuid.uuid4()
        self.pregunta = pregunta
        self.opciones = opciones
        self.votos = {opcion: 0 for opcion in opciones}
        self.tipo = tipo
        self.estado = PollState.ACTIVE
        self.timestamp_inicio = datetime.now()
        self.duracion = timedelta(seconds=duracion_segundos)
        self.votantes = set()

    def esta_activa(self):
        if self.estado == PollState.CLOSED:
            return False
        if datetime.now() > self.timestamp_inicio + self.duracion:
            self.estado = PollState.CLOSED
            return False
        return True

    def agregar_voto(self, username, opcion):
        if not self.esta_activa():
            raise Exception("Encuesta cerrada")
        if username in self.votantes:
            raise Exception("Usuario ya votó")
        if opcion not in self.opciones:
            raise Exception("Opción inválida")
        self.votos[opcion] += 1
        self.votantes.add(username)

    def cerrar(self):
        self.estado = PollState.CLOSED