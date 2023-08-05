from dataclasses import dataclass
from datetime import date, datetime

from timeoff.model.base import Model


@dataclass
class Entry(Model):
    date: date
    rate: float

    @classmethod
    def rm(cls, date):
        data = {"date": str(date), "rate": 0}
        super(cls, cls)._write(data)

    @classmethod
    def get(cls):
        data = {}
        for entry in super(cls, cls)._load():
            entry["date"] = datetime.strptime(entry["date"], "%Y-%m-%d").date()
            entry["rate"] = float(entry["rate"])
            if entry["rate"] == 0:
                data.pop(entry["date"], None)
            else:
                data[entry["date"]] = cls(**entry)

        return data


@dataclass
class Absence(Entry):
    pass


@dataclass
class Accrued(Entry):
    pass