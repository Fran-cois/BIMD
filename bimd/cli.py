"""bimd — BackInMyDay CLI entry point."""

from __future__ import annotations

import datetime
import re
import urllib.parse
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from bimd.data import Era, ModelInfo, find_era, load_eras
from bimd.git_utils import get_commit_date, get_first_commit_date, get_repo
from bimd.humor import get_boomer_comment
from bimd.i18n import get_lang, set_lang, t

app = typer.Typer(
    name="bimd",
    help="BackInMyDay — AI-era software archaeology 👴",
    add_completion=False,
)
console = Console()

# ── ASCII banner ─────────────────────────────────────────────────────────────

BANNER = r"""
 ____             _    ___       __  __       ____
| __ )  __ _  ___| | _|_ _|_ __ |  \/  |_   _|  _ \  __ _ _   _
|  _ \ / _` |/ __| |/ /| || '_ \| |\/| | | | | | | |/ _` | | | |
| |_) | (_| | (__|   < | || | | | |  | | |_| | |_| | (_| | |_| |
|____/ \__,_|\___|_|\_\___|_| |_|_|  |_|\__, |____/ \__,_|\__, |
                                         |___/             |___/
"""


def _render_era(era: Era, commit_date: datetime.date | None = None) -> None:
    """Pretty-print an era report to the console."""
    console.print(BANNER, style="bold cyan")

    # Date info
    if commit_date:
        console.print(
            f"{t('date_analysed')}[bold yellow]{commit_date.isoformat()}[/]"
        )
    console.print(
        f"{t('era_detected')}[bold magenta]{era.name}[/] ({era.id})\n"
    )

    # Models table
    table = Table(
        title=t("models_table_title"),
        show_header=True,
        header_style="bold green",
    )
    table.add_column(t("model_col"), style="cyan")
    table.add_column(t("released_col"), style="yellow")
    table.add_column(t("org_col"), style="white")
    for mi in era.models:
        table.add_row(
            mi.name,
            mi.released or "—",
            mi.org or "—",
        )
    console.print(table)

    console.print(
        f"\n{t('context_window')}[bold]{era.context_window}[/]"
    )
    console.print(
        f"{t('period')}{era.start_date.isoformat()} → {era.end_date.isoformat()}\n"
    )

    # Boomer panel
    quip = get_boomer_comment(era)
    console.print(
        Panel(
            Text(f"👴 {quip}", style="italic"),
            title=t("boomer_panel_title"),
            border_style="red",
            expand=False,
        )
    )


# ── Commands ─────────────────────────────────────────────────────────────────

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@app.callback()
def main(
    lang: Optional[str] = typer.Option(
        None,
        "--lang",
        "-l",
        help="Language: en or fr. Auto-detected from locale by default.",
    ),
) -> None:
    """BackInMyDay — AI-era software archaeology 👴"""
    if lang:
        set_lang(lang)


@app.command()
def scan(
    path: str = typer.Argument(
        ".", help="Path to the Git repository / Chemin vers le dépôt Git."
    ),
) -> None:
    """Scan a Git repo and show the AI era of its first commit."""
    try:
        repo = get_repo(path)
    except Exception:
        console.print(t("err_not_git"))
        raise typer.Exit(code=1)

    try:
        commit_date = get_first_commit_date(repo)
    except ValueError as exc:
        console.print(f"{t('err_prefix')}{exc}")
        raise typer.Exit(code=1)

    era = find_era(commit_date)
    if era is None:
        console.print(t("no_era_for_date", date=commit_date.isoformat()))
        raise typer.Exit(code=1)

    _render_era(era, commit_date)


@app.command()
def era(
    ref: str = typer.Argument(
        ...,
        help="Date (YYYY-MM-DD) or commit hash / Date ou hash de commit.",
    ),
    path: str = typer.Option(
        ".",
        "--path",
        "-p",
        help="Path to the Git repo (for commit hashes) / Chemin du dépôt Git.",
    ),
) -> None:
    """Show the AI era for a given date or commit."""
    target_date: datetime.date | None = None

    if _DATE_RE.match(ref):
        target_date = datetime.date.fromisoformat(ref)
    else:
        # Treat as commit hash
        try:
            repo = get_repo(path)
            target_date = get_commit_date(repo, ref)
        except Exception:
            console.print(t("err_resolve_commit", ref=ref))
            raise typer.Exit(code=1)

    matched = find_era(target_date)
    if matched is None:
        console.print(t("no_era_for_date", date=target_date.isoformat()))
        raise typer.Exit(code=1)

    _render_era(matched, target_date)


@app.command()
def badge(
    path: str = typer.Argument(
        ".", help="Path to the Git repository / Chemin vers le dépôt Git."
    ),
) -> None:
    """Generate a Shields.io badge Markdown for the project era."""
    try:
        repo = get_repo(path)
        commit_date = get_first_commit_date(repo)
    except Exception:
        console.print(t("err_analyse_repo"))
        raise typer.Exit(code=1)

    matched = find_era(commit_date)
    if matched is None:
        console.print(t("no_era_found"))
        raise typer.Exit(code=1)

    label = urllib.parse.quote(matched.badge_label)
    color = matched.badge_color
    badge_url = f"https://img.shields.io/badge/Era-{label}-{color}"
    markdown = f"![BackInMyDay Era]({badge_url})"

    console.print(
        Panel(
            f"[bold]{markdown}[/]",
            title=t("badge_panel_title"),
            border_style="green",
            expand=False,
        )
    )
    console.print(t("badge_copy_msg"))


if __name__ == "__main__":
    app()
