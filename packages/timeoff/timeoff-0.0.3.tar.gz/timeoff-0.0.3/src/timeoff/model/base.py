import json
import pickle
from dataclasses import fields
from pathlib import Path
from typing import List

from timeoff.config import DATA_DIR, DATA_VERSION


class Model:
    @classmethod
    def _data_file(cls) -> Path:
        filename = f"{cls.__name__}.pkl".lower()
        return Path(DATA_DIR) / str(DATA_VERSION) / filename

    @classmethod
    def _write(cls, data: dict) -> None:
        cls._data_file().parent.mkdir(parents=True, exist_ok=True)
        with cls._data_file().open("ab") as f:
            pickle.dump(json.dumps(data), f)

    @classmethod
    def _load(cls) -> List[dict]:
        if not cls._data_file().is_file():
            return []
        with cls._data_file().open("rb") as f:
            data = []
            while True:
                try:
                    entry = json.loads(pickle.load(f))
                    data.append(entry)
                except EOFError:
                    break
            return data

    def save(self) -> None:
        data = {}
        for field in fields(self):
            data[field.name] = str(getattr(self, field.name))
        self._write(data)
