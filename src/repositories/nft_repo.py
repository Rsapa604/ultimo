import json
from pathlib import Path
from uuid import UUID
from src.models.token_nft import TokenNFT
from datetime import datetime

class NFTRepository:
    def __init__(self, filepath="nfts.json"):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self.filepath.write_text("[]")

    def guardar(self, token: TokenNFT):
        tokens = self._cargar_todos()
        tokens = [t for t in tokens if t['token_id'] != str(token.token_id)]
        tokens.append(self._serialize(token))
        self.filepath.write_text(json.dumps(tokens, indent=2))

    def listar_por_owner(self, owner):
        tokens = self._cargar_todos()
        return [self._deserialize(t) for t in tokens if t['owner'] == owner]

    def buscar_por_id(self, token_id: UUID):
        tokens = self._cargar_todos()
        for t in tokens:
            if t['token_id'] == str(token_id):
                return self._deserialize(t)
        return None

    def _cargar_todos(self):
        return json.loads(self.filepath.read_text())
    
    def _serialize(self, token: TokenNFT):
        return {
            "token_id": str(token.token_id),
            "owner": token.owner,
            "poll_id": str(token.poll_id),
            "option": token.option,
            "issued_at": token.issued_at.isoformat()
        }

    def _deserialize(self, data):
        token = TokenNFT(data['owner'], UUID(data['poll_id']), data['option'])
        token.token_id = UUID(data['token_id'])
        token.issued_at = datetime.fromisoformat(data['issued_at'])
        return token