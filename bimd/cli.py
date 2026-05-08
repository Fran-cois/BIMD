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

from bimd.data import Era, find_era, load_eras
from bimd.git_utils import get_commit_date, get_first_commit_date, get_repo
from bimd.humor import get_boomer_comment

app = typer.Typer(
    name="bimd",
    help="BackInMyDay — Archéologie logicielle de l'ère IA 👴",
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
            f"  📅  Date analysée : [bold yellow]{commit_date.isoformat()}[/]"
        )
    console.print(
        f"  🏷️   Ère détectée  : [bold magenta]{era.name}[/] ({era.id})\n"
    )

    # Models table
    table = Table(
        title="🤖 Modèles disponibles à l'époque",
        show_header=True,
        header_style="bold green",
    )
    table.add_column("Modèle", style="cyan")
    for model in era.top_models:
        table.add_row(model)
    console.print(table)

    console.print(
        f"\n  📏  Fenêtre de contexte : [bold]{era.context_window}[/]"
    )
    console.print(
        f"  📆  Période : {era.start_date.isoformat()} → {era.end_date.isoformat()}\n"
    )

    # Boomer panel
    quip = get_boomer_comment(era)
    console.print(
        Panel(
            Text(f"👴 {quip}", style="italic"),
            title="[bold red]Le Boomer du Prompt râle[/]",
            border_style="red",
            expand=False,
        )
    )


# ── Commands ─────────────────────────────────────────────────────────────────

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@app.command()
def scan(
    path: str = typer.Argument(
        ".", help="Chemin vers le dépôt Git à analyser."
    ),
) -> None:
    """Scanne un dépôt Git et affiche l'ère IA correspondant à son premier commit."""
    try:
        repo = get_repo(path)
    except Exception:
        console.print(
            "[bold red]Erreur :[/] le chemin spécifié n'est pas un dépôt Git valide.",
        )
        raise typer.Exit(code=1)

    try:
        commit_date = get_first_commit_date(repo)
    except ValueError as exc:
        console.print(f"[bold red]Erreur :[/] {exc}")
        raise typer.Exit(code=1)

    era = find_era(commit_date)
    if era is None:
        console.print(
            f"[yellow]Aucune ère trouvée pour la date {commit_date.isoformat()}.[/]"
        )
        raise typer.Exit(code=1)

    _render_era(era, commit_date)


@app.command()
def era(
    ref: str = typer.Argument(
        ...,
        help="Date (YYYY-MM-DD) ou hash de commit à analyser.",
    ),
    path: str = typer.Option(
        ".",
        "--path",
        "-p",
        help="Chemin du dépôt Git (nécessaire pour un hash de commit).",
    ),
) -> None:
    """Affiche l'ère IA correspondant à une date ou un commit donné."""
    target_date: datetime.date | None = None

    if _DATE_RE.match(ref):
        target_date = datetime.date.fromisoformat(ref)
    else:
        # Treat as commit hash
        try:
            repo = get_repo(path)
            target_date = get_commit_date(repo, ref)
        except Exception:
            console.print(
                f"[bold red]Erreur :[/] impossible de résoudre le commit '{ref}'.",
            )
            raise typer.Exit(code=1)

    matched = find_era(target_date)
    if matched is None:
        console.print(
            f"[yellow]Aucune ère trouvée pour la date {target_date.isoformat()}.[/]"
        )
        raise typer.Exit(code=1)

    _render_era(matched, target_date)


@app.command()
def badge(
    path: str = typer.Argument(
        ".", help="Chemin vers le dépôt Git."
    ),
) -> None:
    """Génère le Markdown pour un badge Shields.io de l'ère du projet."""
    try:
        repo = get_repo(path)
        commit_date = get_first_commit_date(repo)
    except Exception:
        console.print(
            "[bold red]Erreur :[/] impossible d'analyser le dépôt Git."
        )
        raise typer.Exit(code=1)

    matched = find_era(commit_date)
    if matched is None:
        console.print("[yellow]Aucune ère trouvée.[/]")
        raise typer.Exit(code=1)

    label = urllib.parse.quote(matched.badge_label)
    color = matched.badge_color
    badge_url = f"https://img.shields.io/badge/Era-{label}-{color}"
    markdown = f"![BackInMyDay Era]({badge_url})"

    console.print(
        Panel(
            f"[bold]{markdown}[/]",
            title="[bold green]Badge Markdown[/]",
            border_style="green",
            expand=False,
        )
    )
    console.print(
        "\n  Copiez la ligne ci-dessus dans votre README.md 🚀\n"
    )


if __name__ == "__main__":
    app()
