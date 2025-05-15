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