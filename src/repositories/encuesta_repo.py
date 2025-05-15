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
    
    def _serialize(self, poll: Poll):
        return {
            "id": str(poll.id),
            "pregunta": poll.pregunta,
            "opciones": poll.opciones,
            "votos": poll.votos,
            "tipo": poll.tipo,
            "estado": poll.estado.value,
            "timestamp_inicio": poll.timestamp_inicio.isoformat(),
            "duracion_segundos": poll.duracion.total_seconds(),
            "votantes": list(poll.votantes)
        }

    def _deserialize(self, data):
        from datetime import timedelta, datetime
        poll = Poll(data['pregunta'], data['opciones'], int(data['duracion_segundos']), data['tipo'])
        poll.id = UUID(data['id'])
        poll.votos = data['votos']
        poll.estado = poll.estado.__class__(data['estado'])
        poll.timestamp_inicio = datetime.fromisoformat(data['timestamp_inicio'])
        poll.duracion = timedelta(seconds=data['duracion_segundos'])
        poll.votantes = set(data['votantes'])
        return poll