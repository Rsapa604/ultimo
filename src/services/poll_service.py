from src.models.encuesta import Poll
from src.repositories.encuesta_repo import EncuestaRepository
from src.services.nft_service import NFTService

class PollService:
    def __init__(self):
        self.repo = EncuestaRepository()
        self.nft_service = NFTService()

    def create_poll(self, pregunta, opciones, duracion_segundos, tipo="simple"):
        poll = Poll(pregunta, opciones, duracion_segundos, tipo)
        self.repo.guardar(poll)
        return poll