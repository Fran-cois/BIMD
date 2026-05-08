"""Humor engine — sarcastic boomer-dev commentary."""

from __future__ import annotations

import random

from bimd.data import Era

# Fallback quips when an era has no specific comments
_GENERIC_QUIPS = [
    "De mon temps, on n'avait pas de LLM. On avait Stack Overflow et de la volonté.",
    "Vous ne connaissez pas votre chance, les jeunes.",
    "Tout ça pour wrapper une API et appeler ça de l'innovation…",
]


def get_boomer_comment(era: Era) -> str:
    """Pick a random sarcastic remark for the given era."""
    pool = era.boomer_comments if era.boomer_comments else _GENERIC_QUIPS
    return random.choice(pool)
