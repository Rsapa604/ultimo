import uuid
from typing import List

class User:
    def __init__(self, username: str, password_hash: str):
        self.id = uuid.uuid4()
        self.username = username
        self.password_hash = password_hash
        self.tokens = []