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

    def add_vote(self, username: str, opcion: str):
        if opcion not in self.opciones:
            raise ValueError("Opción inválida")
        if username in self.get_all_voters():
            raise ValueError("Usuario ya votó")
        self.votos[opcion].append(username)

    def get_all_voters(self):
        voters = set()
        for vots in self.votos.values():
            voters.update(vots)
        return voters

    def get_partial_results(self):
        total = sum(len(v) for v in self.votos.values())
        if total == 0:
            return {op: (0, 0) for op in self.opciones}  # (count, percentage)
        return {op: (len(v), len(v)/total*100) for op, v in self.votos.items()}

    def get_final_results(self):
        if self.estado != PollStatus.CLOSED:
            raise Exception("Encuesta no cerrada")
        return self.get_partial_results()