import uuid
import datetime
from src.models.encuesta import Poll
from src.models.voto import Vote
from src.repositories.encuesta_repo import EncuestaRepository
from src.patterns.observer import Observable
from src.patterns.strategy import DesempateStrategy

class PollService(Observable):
    def __init__(self, encuesta_repo: EncuestaRepository, desempate_strategy: DesempateStrategy):
        super().__init__()
        self.encuesta_repo = encuesta_repo
        self.desempate_strategy = desempate_strategy

    def create_poll(self, pregunta: str, opciones: list, duracion_segundos: int, tipo: str) -> Poll:
        poll_id = uuid.uuid4()
        ahora = datetime.datetime.now()
        poll = Poll(
            id=poll_id,
            pregunta=pregunta,
            opciones=opciones,
            votos=[],
            estado="activa",
            timestamp_inicio=ahora,
            duracion=datetime.timedelta(seconds=duracion_segundos),
            tipo=tipo
        )
        self.encuesta_repo.save_poll(poll)
        return poll

    def vote(self, poll_id: uuid.UUID, username: str, opcion):
        poll = self.encuesta_repo.get_poll(poll_id)
        if poll is None or poll.estado != "activa":
            raise Exception("Encuesta no activa o no existe.")
        if poll.has_voted(username):
            raise Exception("Usuario ya votó en esta encuesta.")

        # Registrar voto
        if poll.tipo == "multiple" and isinstance(opcion, list):
            for op in opcion:
                vote = Vote(username=username, opcion=op)
                poll.votos.append(vote)
        else:
            vote = Vote(username=username, opcion=opcion)
            poll.votos.append(vote)

        self.encuesta_repo.save_poll(poll)
        self.check_auto_close(poll)

    def check_auto_close(self, poll: Poll):
        ahora = datetime.datetime.now()
        if poll.estado == "activa" and ahora > poll.timestamp_inicio + poll.duracion:
            self.close_poll(poll.id)

    def close_poll(self, poll_id: uuid.UUID):
        poll = self.encuesta_repo.get_poll(poll_id)
        if poll is None or poll.estado != "activa":
            raise Exception("Encuesta no activa o no existe.")
        poll.estado = "cerrada"
        self.encuesta_repo.save_poll(poll)
        self.notify_observers(poll)

    def get_partial_results(self, poll_id: uuid.UUID):
        poll = self.encuesta_repo.get_poll(poll_id)
        if poll is None:
            raise Exception("Encuesta no encontrada.")
        return poll.count_votes()

    def get_final_results(self, poll_id: uuid.UUID):
        poll = self.encuesta_repo.get_poll(poll_id)
        if poll is None or poll.estado != "cerrada":
            raise Exception("Encuesta no cerrada o no existe.")
        resultados = poll.count_votes()
        if poll.has_tie():
            return self.desempate_strategy.resolve(poll)
        return resultados