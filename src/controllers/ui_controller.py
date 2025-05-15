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