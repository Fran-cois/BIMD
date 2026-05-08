"""Humor engine — sarcastic boomer-dev commentary."""

from __future__ import annotations

import random

from bimd.data import Era

# Fallback quips when an era has no specific comments
_GENERIC_QUIPS = {
    "en": [
        "Back in my day, we didn't have LLMs. We had Stack Overflow and willpower.",
        "You kids don't know how good you have it.",
        "All this just to wrap an API and call it innovation…",
    ],
    "fr": [
        "De mon temps, on n'avait pas de LLM. On avait Stack Overflow et de la volonté.",
        "Vous ne connaissez pas votre chance, les jeunes.",
        "Tout ça pour wrapper une API et appeler ça de l'innovation…",
    ],
}


def get_boomer_comment(era: Era) -> str:
    """Pick a random sarcastic remark for the given era."""
    if era.boomer_comments:
        return random.choice(era.boomer_comments)
    from bimd.i18n import get_lang
    lang = get_lang()
    pool = _GENERIC_QUIPS.get(lang, _GENERIC_QUIPS["en"])
    return random.choice(pool)
