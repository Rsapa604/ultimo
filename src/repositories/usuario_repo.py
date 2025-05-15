import json
from pathlib import Path
from src.models.usuario import User

class UsuarioRepository:
    def __init__(self, filepath="usuarios.json"):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self.filepath.write_text("[]")

    def guardar(self, user: User):
        usuarios = self._cargar_todos()
        usuarios = [u for u in usuarios if u['username'] != user.username]
        usuarios.append(self._serialize(user))
        self.filepath.write_text(json.dumps(usuarios, indent=2))
