import uuid
import datetime
from src.models.token_nft import TokenNFT
from src.repositories.nft_repo import NFTRepository

class NFTService:
    def __init__(self, nft_repo: NFTRepository):
        self.nft_repo = nft_repo

    def mint_token(self, username: str, poll_id: uuid.UUID, option: str) -> TokenNFT:
        token_id = uuid.uuid4()
        issued_at = datetime.datetime.now()
        token = TokenNFT(
            token_id=token_id,
            owner=username,
            poll_id=poll_id,
            option=option,
            issued_at=issued_at
        )
        self.nft_repo.save_token(token)
        return token
    
    def transfer_token(self, token_id: uuid.UUID, current_owner: str, new_owner: str):
        token = self.nft_repo.get_token(token_id)
        if token is None:
            raise Exception("Token no encontrado.")
        if token.owner != current_owner:
            raise Exception("No eres el propietario de este token.")
        token.owner = new_owner
        self.nft_repo.save_token(token)

    def get_tokens_of_user(self, username: str):
        return self.nft_repo.get_tokens_by_owner(username)