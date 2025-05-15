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
    
    def vote(self, poll_id, username, opcion):
        poll = self.repo.buscar_por_id(poll_id)
        if not poll or not poll.esta_activa():
            raise Exception("Encuesta no disponible o cerrada")
        poll.agregar_voto(username, opcion)
        self.repo.guardar(poll)
        # Generar NFT token por voto
        self.nft_service.mint_token(username, poll_id, opcion)

    def get_partial_results(self, poll_id):
        poll = self.repo.buscar_por_id(poll_id)
        if not poll:
            raise Exception("Encuesta no encontrada")
        total = sum(poll.votos.values())
        porcentajes = {k: (v / total) * 100 if total > 0 else 0 for k, v in poll.votos.items()}
        return {"conteo": poll.votos, "porcentajes": porcentajes}

    def close_poll(self, poll_id):
        poll = self.repo.buscar_por_id(poll_id)
        if not poll:
            raise Exception("Encuesta no encontrada")
        poll.cerrar()
        self.repo.guardar(poll)