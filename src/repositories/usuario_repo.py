import json
import os 
from src.models.usuario import User

class UsuarioRepository:
    def __init__(self, filepath="data/usuarios.json"):
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
            json.dump(data, f, indent=2)

    def save(self, user: User):
        data = self._load_all()
        found = False
        for i, u in enumerate(data):
            if u["username"] == user.username:
                data[i] = self._user_to_dict(user)
                found = True
                break
        if not found:
            data.append(self._user_to_dict(user))
        self._save_all(data)

    def get_by_username(self, username: str):
        data = self._load_all()
        for u in data:
            if u["username"] == username:
                return self._dict_to_user(u)
        return None

    def _user_to_dict(self, user: User):
        return {
            "id": user.id,
            "username": user.username,
            "password_hash": user.password_hash,
            "tokens": user.tokens
        }
    def _dict_to_user(self,data):
        user = User(data["username"], data["password_hash"])
        user.id = data["id"]
        user.tokens = data.get("tokens", [])
        return user