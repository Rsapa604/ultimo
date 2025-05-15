from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

class UIController:
    def __init__(self):
        self.user_service = UserService()
        self.poll_service = PollService()
        self.nft_service = NFTService()
        self.chatbot_service = ChatbotService()

    def registrar_usuario(self, username, password):
        try:
            self.user_service.register(username, password)
            return f"Usuario '{username}' registrado con éxito."
        except Exception as e:
            return f"Error: {e}"

    def login_usuario(self, username, password):
        try:
            token = self.user_service.login(username, password)
            return token
        except Exception as e:
            return f"Error: {e}"
        
    def obtener_encuestas_activas(self):
        return self.poll_service.get_active_polls()

    def votar(self, poll_id, username, opcion):
        try:
            self.poll_service.vote(poll_id, username, opcion)
            return "Voto registrado."
        except Exception as e:
            return f"Error: {e}"

    def obtener_tokens_usuario(self, username):
        try:
            return self.nft_service.get_tokens_by_owner(username)
        except Exception as e:
            return f"Error: {e}"

    def transferir_token(self, token_id, owner, nuevo_owner):
        try:
            self.nft_service.transfer_token(token_id, owner, nuevo_owner)
            return "Token transferido."
        except Exception as e:
            return f"Error: {e}"

    def chatbot_responder(self, username, pregunta):
        try:
            respuesta = self.chatbot_service.respond(username, pregunta)
            return respuesta
        except Exception as e:
            return f"Error: {e}"