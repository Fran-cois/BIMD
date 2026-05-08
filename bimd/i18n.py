"""Internationalisation — English / French string tables."""

from __future__ import annotations

import locale
import os

SUPPORTED_LANGS = ("en", "fr")

_current_lang: str | None = None


def get_lang() -> str:
    """Return the active language (``en`` or ``fr``).

    Resolution order: explicit ``set_lang()`` → ``BIMD_LANG`` env var → system
    locale → ``en`` fallback.
    """
    if _current_lang:
        return _current_lang
    env = os.environ.get("BIMD_LANG", "").lower()
    if env in SUPPORTED_LANGS:
        return env
    try:
        loc = locale.getlocale()[0] or ""
    except ValueError:
        loc = ""
    if loc.lower().startswith("fr"):
        return "fr"
    return "en"


def set_lang(lang: str) -> None:
    """Override the active language for this process."""
    global _current_lang
    _current_lang = lang


# fmt: off
_STRINGS: dict[str, dict[str, str]] = {
    "date_analysed": {
        "en": "  📅  Date analysed  : ",
        "fr": "  📅  Date analysée  : ",
    },
    "era_detected": {
        "en": "  🏷️   Era detected   : ",
        "fr": "  🏷️   Ère détectée   : ",
    },
    "models_table_title": {
        "en": "🤖 Models available at the time",
        "fr": "🤖 Modèles disponibles à l'époque",
    },
    "model_col": {
        "en": "Model",
        "fr": "Modèle",
    },
    "released_col": {
        "en": "Released",
        "fr": "Publié",
    },
    "org_col": {
        "en": "Organization",
        "fr": "Organisation",
    },
    "context_window": {
        "en": "  📏  Context window : ",
        "fr": "  📏  Fenêtre de contexte : ",
    },
    "period": {
        "en": "  📆  Period : ",
        "fr": "  📆  Période : ",
    },
    "boomer_panel_title": {
        "en": "[bold red]The Prompt Boomer grumbles[/]",
        "fr": "[bold red]Le Boomer du Prompt râle[/]",
    },
    "err_not_git": {
        "en": "[bold red]Error:[/] the specified path is not a valid Git repository.",
        "fr": "[bold red]Erreur :[/] le chemin spécifié n'est pas un dépôt Git valide.",
    },
    "err_prefix": {
        "en": "[bold red]Error:[/] ",
        "fr": "[bold red]Erreur :[/] ",
    },
    "no_era_for_date": {
        "en": "[yellow]No era found for date {date}.[/]",
        "fr": "[yellow]Aucune ère trouvée pour la date {date}.[/]",
    },
    "err_resolve_commit": {
        "en": "[bold red]Error:[/] unable to resolve commit '{ref}'.",
        "fr": "[bold red]Erreur :[/] impossible de résoudre le commit '{ref}'.",
    },
    "err_analyse_repo": {
        "en": "[bold red]Error:[/] unable to analyse the Git repository.",
        "fr": "[bold red]Erreur :[/] impossible d'analyser le dépôt Git.",
    },
    "no_era_found": {
        "en": "[yellow]No era found.[/]",
        "fr": "[yellow]Aucune ère trouvée.[/]",
    },
    "badge_panel_title": {
        "en": "[bold green]Badge Markdown[/]",
        "fr": "[bold green]Badge Markdown[/]",
    },
    "badge_copy_msg": {
        "en": "\n  Copy the line above into your README.md 🚀\n",
        "fr": "\n  Copiez la ligne ci-dessus dans votre README.md 🚀\n",
    },
}
# fmt: on


def t(key: str, **kwargs: str) -> str:
    """Translate *key* to the active language.

    Extra *kwargs* are passed to ``str.format()`` on the resulting string.
    """
    lang = get_lang()
    entry = _STRINGS.get(key, {})
    text = entry.get(lang, entry.get("en", key))
    if kwargs:
        text = text.format(**kwargs)
    return text
