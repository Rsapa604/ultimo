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