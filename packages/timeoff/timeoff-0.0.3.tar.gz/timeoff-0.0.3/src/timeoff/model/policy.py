import json
from dataclasses import dataclass
from datetime import date, datetime

from timeoff.model.base import Model
from timeoff.model.schedule import (
    SemiMonthly,  # noqa: F401
)


@dataclass
class Policy(Model):
    date: date
    schedule: str
    schedule_args: list
    rate: float

    @staticmethod
    def rm(date):
        data = {"date": str(date), "schedule": "", "schedule_args": [], "rate": 0}
        super(Policy, Policy)._write(data)

    @staticmethod
    def get():
        data = {}
        for entry in super(Policy, Policy)._load():
            entry["date"] = datetime.strptime(entry["date"], "%Y-%m-%d").date()
            args = json.loads(entry["schedule_args"])
            schedule = globals()[entry["schedule"]]
            entry["schedule"] = schedule(*args)
            entry["rate"] = float(entry["rate"])
            if entry["rate"] == 0:
                entry.pop(entry["date"], None)
            else:
                data[entry["date"]] = Policy(**entry)
        return data
    