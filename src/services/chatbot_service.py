from transformers import pipeline
from src.services.poll_service import PollService

class ChatbotService:
    def __init__(self, poll_service: PollService):
        self.poll_service = poll_service
        self.chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")
        self.historial = {}

    def chatbot_response(self, username: str, question: str) -> str:
        # Palabras clave para encuestas
        keys = ["quién va ganando", "cuánto falta", "resultado", "encuesta", "voto"]

        if any(key in question.lower() for key in keys):
            # Generar respuesta manual consultando PollService
            # Para simplificar, solo devolvemos la última encuesta activa o cerrada
            polls = self.poll_service.encuesta_repo.get_all_polls()
            if not polls:
                return "No hay encuestas disponibles ahora."
            poll = polls[-1]
            if poll.estado == "activa":
                resultados = self.poll_service.get_partial_results(poll.id)
                return f"La encuesta '{poll.pregunta}' va así: {resultados}"
            else:
                resultados = self.poll_service.get_final_results(poll.id)
                return f"Resultados finales de la encuesta '{poll.pregunta}': {resultados}"
        else:
            # Pregunta libre, responde con IA
            respuesta = self.chatbot(question)
            return respuesta[0]['generated_text']