import bcrypt
import uuid
from src.repositories.usuario_repo import UsuarioRepository
from src.models.usuario import User

class UserService:
    def __init__(self):
        self.repo = UsuarioRepository()
        self.sessions = {}  # username -> token sesión

    def register(self, username, password):
        if self.repo.buscar_por_username(username):
            raise Exception("Usuario ya existe")
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User(username, pw_hash.decode())
        self.repo.guardar(user)