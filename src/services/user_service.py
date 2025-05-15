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

    def login(self, username, password):
        user = self.repo.buscar_por_username(username)
        if not user:
            raise Exception("Usuario no existe")
        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            raise Exception("Contraseña incorrecta")
        token = str(uuid.uuid4())
        self.sessions[username] = token
        return token

    def is_logged_in(self, username, token):
        return self.sessions.get(username) == token