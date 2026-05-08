"""Load and query the eras database."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Era:
    id: str
    name: str
    start_date: datetime.date
    end_date: datetime.date
    top_models: list[str]
    context_window: str
    badge_label: str
    badge_color: str
    boomer_comments: list[str]


_ERAS_FILE = Path(__file__).parent / "eras.yaml"


def load_eras(path: Path | None = None) -> list[Era]:
    """Parse eras.yaml and return a sorted list of Era objects."""
    path = path or _ERAS_FILE
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    eras: list[Era] = []
    for entry in raw["eras"]:
        eras.append(
            Era(
                id=entry["id"],
                name=entry["name"],
                start_date=datetime.date.fromisoformat(entry["start_date"]),
                end_date=datetime.date.fromisoformat(entry["end_date"]),
                top_models=entry["top_models"],
                context_window=entry["context_window"],
                badge_label=entry.get("badge_label", entry["name"]),
                badge_color=entry.get("badge_color", "blue"),
                boomer_comments=entry.get("boomer_comments", []),
            )
        )
    eras.sort(key=lambda e: e.start_date)
    return eras


def find_era(target: datetime.date, eras: list[Era] | None = None) -> Era | None:
    """Return the era matching a given date, or None."""
    if eras is None:
        eras = load_eras()
    for era in eras:
        if era.start_date <= target <= era.end_date:
            return era
    return None
