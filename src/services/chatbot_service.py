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