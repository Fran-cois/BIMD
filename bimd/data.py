"""Load and query the eras database."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class ModelInfo:
    name: str
    released: str | None = None
    org: str | None = None


@dataclass
class Era:
    id: str
    name: str
    start_date: datetime.date
    end_date: datetime.date
    top_models: list[str]
    models: list[ModelInfo]
    context_window: str
    badge_label: str
    badge_color: str
    boomer_comments: list[str]


_ERAS_FILE = Path(__file__).parent / "eras.yaml"


def _resolve_str(value: str | dict, lang: str) -> str:
    """Resolve a possibly-multilingual string value."""
    if isinstance(value, dict):
        return value.get(lang, value.get("en", ""))
    return str(value)


def _resolve_list(value: list | dict, lang: str) -> list[str]:
    """Resolve a possibly-multilingual list value."""
    if isinstance(value, dict):
        return value.get(lang, value.get("en", []))
    if isinstance(value, list):
        return value
    return []


def load_eras(path: Path | None = None, lang: str | None = None) -> list[Era]:
    """Parse eras.yaml and return a sorted list of Era objects."""
    if lang is None:
        from bimd.i18n import get_lang
        lang = get_lang()
    path = path or _ERAS_FILE
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    eras: list[Era] = []
    for entry in raw["eras"]:
        raw_models = entry["top_models"]
        models: list[ModelInfo] = []
        model_names: list[str] = []
        for m in raw_models:
            if isinstance(m, dict):
                mi = ModelInfo(
                    name=m["name"],
                    released=m.get("released"),
                    org=m.get("org"),
                )
                models.append(mi)
                model_names.append(mi.name)
            else:
                models.append(ModelInfo(name=str(m)))
                model_names.append(str(m))
        eras.append(
            Era(
                id=entry["id"],
                name=_resolve_str(entry["name"], lang),
                start_date=datetime.date.fromisoformat(entry["start_date"]),
                end_date=datetime.date.fromisoformat(entry["end_date"]),
                top_models=model_names,
                models=models,
                context_window=_resolve_str(entry["context_window"], lang),
                badge_label=entry.get("badge_label", ""),
                badge_color=entry.get("badge_color", "blue"),
                boomer_comments=_resolve_list(entry.get("boomer_comments", {}), lang),
            )
        )
    eras.sort(key=lambda e: e.start_date)
    return eras


def find_era(
    target: datetime.date,
    eras: list[Era] | None = None,
    lang: str | None = None,
) -> Era | None:
    """Return the era matching a given date, or None."""
    if eras is None:
        eras = load_eras(lang=lang)
    for era in eras:
        if era.start_date <= target <= era.end_date:
            return era
    return None
