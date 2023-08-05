
from dataclasses import dataclass
from datetime import date, datetime

from timeoff.model.base import Model


@dataclass
class Setting(Model):
    starting_balance: float
    starting_date: date

    @staticmethod
    def get():
        data = super(Setting, Setting)._load()[-1]
        data["starting_balance"] = float(data["starting_balance"])
        data["starting_date"] = datetime.strptime(
            data["starting_date"], "%Y-%m-%d",
        ).date()
        return Setting(**data)

