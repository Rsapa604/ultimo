import json
import os
from datetime import datetime
from src.models.encuesta import Poll

class EncuestaRepository:
    def __init__(self, filepath="encuestas.json"):
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
            json.dump(data, f, default=str, indent=2)

    def save(self):
        data = self._load_all()
        # Reemplaza o agrega
        found = False
        for i, p in enumerate(data):
            if p["id"] == poll.id:
                data[i] = self._poll_to_dict(Poll)
                found = True
                break
        if not found:
            data.append(self._poll_to_dict(Poll))
        self._save_all(data)

    def get_by_id(self, poll_id: str):
        data = self._load_all()
        for p in data:
            if p["id"] == poll_id:
                return self._dict_to_poll(p)
        return None
    
    def list_all(self):
        data = self._load_all()
        return [self._dict_to_poll(p) for p in data]
    
    def _poll_to_dict(self, poll: Poll):
        return {
            "id": poll.id,
            "pregunta": poll.pregunta,
            "opciones": poll.opciones,
            "votos": poll.votos,
            "estado": poll.estado.value,
            "timestamp_inicio": poll.timestamp_inicio.isoformat(),
            "duracion": poll.duracion.total_seconds(),
            "tipo": poll.tipo
        }

    def _dict_to_poll(self, data):
        poll = Poll(data["pregunta"], data["opciones"], int(data["duracion"]), data.get("tipo", "simple"))
        poll.id = data["id"]
        poll.votos = data["votos"]
        poll.estado = Poll(data["estado"])
        poll.timestamp_inicio = datetime.fromisoformat(data["timestamp_inicio"])
        return poll