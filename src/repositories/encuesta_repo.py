import json
from pathlib import Path
from uuid import UUID
from src.models.encuesta import Poll

class EncuestaRepository:
    def __init__(self, filepath="encuestas.json"):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self.filepath.write_text("[]")

    def guardar(self, encuesta: Poll):
        encuestas = self._cargar_todos()
        encuestas = [e for e in encuestas if e['id'] != str(encuesta.id)]
        encuestas.append(self._serialize(encuesta))
        self.filepath.write_text(json.dumps(encuestas, indent=2))

    def buscar_por_id(self, poll_id: UUID):
        encuestas = self._cargar_todos()
        for e in encuestas:
            if e['id'] == str(poll_id):
                return self._deserialize(e)
        return None

    def listar_todos(self):
        encuestas = self._cargar_todos()
        return [self._deserialize(e) for e in encuestas]

    def _cargar_todos(self):
        return json.loads(self.filepath.read_text())