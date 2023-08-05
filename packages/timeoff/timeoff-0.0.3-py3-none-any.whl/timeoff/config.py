from pathlib import Path

from timeoff.model.schedule import SemiMonthly

SCHEDULES = {
    "semi-monthly": SemiMonthly,
}

DATA_DIR = Path("~/.timeoff").expanduser()
DATA_VERSION = 0
