from src.services.user_service import UserService
from src.services.poll_service import PollService
from src.services.nft_service import NFTService

class CLIController:
    def __init__(self):
        self.user_service = UserService()
        self.poll_service = PollService()
        self.nft_service = NFTService()
        self.current_user = None
        self.session_token = None
