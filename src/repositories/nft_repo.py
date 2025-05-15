import json
import os 
from src.models.token_nft import TokenNFT
from datetime import datetime

class NFTRepository:
    def __init__(self, filepath="data/nfts.json"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.isfile(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def _load_all(self):
        with open(self.filepath, "r") as f:
            data = json.load(f)
        return data
    
    def _save_all(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save(self, token: TokenNFT):
        data = self._load_all()
        found = False
        for i, t in enumerate(data):
            if t["token_id"] == token.token_id:
                data[i] = self._token_to_dict(token)
                found = True
                break
        if not found:
            data.append(self._token_to_dict(token))
        self._save_all(data)

    def get_by_owner(self, owner: str):
        data = self._load_all()
        return [self._dict_to_token(t) for t in data if t["owner"] == owner]
    
    def  get_by_id(self, token_id: str):
        data = self._load_all()
        for t in data:
            if t["token_id"] == token_id:
                return self._dict_to_token(t)
        return None

    def _token_to_dict(self, token: TokenNFT):
        return {
            "token_id": token.token_id,
            "owner": token.owner,
            "poll_id": token.poll_id,
            "option": token.option,
            "issued_at": token.issued_at.isoformat()
        }
    
    def _dict_to_token(self, data):
        token = TokenNFT(data["owner"], data["poll_id"], data["option"])
        token.token_id = data["token_id"]
        token.issued_at = datetime.fromisoformat(data["issued_at"])
        return token

    def update_owner(self, token_id: str, new_owner: str):
        data = self._load_all()
        for t in data:
            if t["token_id"] == token_id:
                t["owner"] = new_owner
                self._save_all(data)
                return True
        return False