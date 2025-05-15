import uuid
from datetime import datetime, timedelta
from enum import Enum

class PollState(Enum):
    ACTIVE = "activa"
    CLOSED = "cerrada"

class Poll:
    def __init__(self, pregunta: str, opciones: list, duracion_segundos: int, tipo: str ="simple"):
        self.id = str(uuid.uuid4())
        self.pregunta = pregunta
        self.opciones = opciones
        self.votos = {opcion: [] for opcion in opciones} 
        self.tipo = tipo
        self.estado = PollState.ACTIVE
        self.timestamp_inicio = datetime.utcnow()
        self.duracion = timedelta(seconds=duracion_segundos)
        

    def esta_activa(self):
        if self.estado == PollState.CLOSED:
            return False
        if datetime.utcnow() > self.timestamp_inicio + self.duracion:
            self.estado = PollState.CLOSED
            return False
        return True


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
        if self.estado != PollState.CLOSED:
            raise Exception("Encuesta no cerrada")
        return self.get_partial_results()