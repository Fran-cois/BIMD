#!/usr/bin/env python3
"""Build a verified model-launch-dates reference from Epoch AI data.

Downloads the Epoch AI "Notable AI Models" CSV and extracts publication
dates for every model referenced in bimd's eras.yaml.

Usage:
    python scripts/build_model_dates.py          # prints report
    python scripts/build_model_dates.py --patch   # updates eras.yaml in-place
"""
from __future__ import annotations

import csv
import io
import re
import zipfile
from datetime import date, datetime
from pathlib import Path
from urllib.request import urlretrieve

EPOCH_ZIP_URL = "https://epoch.ai/data/ai_models.zip"
CACHE_DIR = Path(__file__).resolve().parent.parent / ".data"
CSV_NAME = "notable_ai_models.csv"
ERAS_FILE = Path(__file__).resolve().parent.parent / "bimd" / "eras.yaml"

# ── Model aliases → Epoch AI CSV "Model" patterns ───────────────────────────
# Keys = names used in eras.yaml's top_models, values = regex on CSV "Model"
MODEL_PATTERNS: dict[str, str] = {
    # Pre-Transformer
    "Word2Vec": r"^Word2Vec",
    "GloVe": r"^GloVe",
    "LSTM (Basic)": r"^Seq2Seq LSTM",
    "Seq2Seq": r"^Seq2Seq LSTM",
    # Transformer birth
    "Transformer (Original)": r"^Transformer$",
    "ELMo": r"^ELMo$",
    # BERT era
    "BERT": r"^BERT-Large$",
    "GPT-2": r"^GPT-2 \(1\.5B\)$",
    "XLNet": r"^XLNet$",
    "RoBERTa": r"^RoBERTa Large$",
    # GPT-3 dawn
    "GPT-3 (davinci)": r"^GPT-3 175B",
    "Codex": r"^Codex$",
    "PaLM": r"^PaLM \(540B\)$",
    "DALL-E": r"^DALL-E$",
    # ChatGPT explosion
    "ChatGPT (GPT-3.5-turbo)": r"^GPT-3\.5",
    "Flan-T5": r"^FLAN",
    "LLaMA (Leaked)": r"^LLaMA 65B$",
    # GPT-4 revolution
    "GPT-4 (Original)": r"^GPT-4$",
    "Claude 1": r"^Claude$",
    "Llama 1": r"^LLaMA 65B$",
    "PaLM 2": r"^PaLM 2",
    # Open source wave
    "GPT-4 Turbo": r"^GPT-4 Turbo",
    "Claude 2.1": r"^Claude 2\.1$",
    "Mixtral 8x7B": r"^Mixtral 8x7B$",
    "Llama 2": r"^Llama 2",
    # Multimodal era
    "Claude 3 (Opus/Sonnet/Haiku)": r"^Claude 3 Opus$",
    "GPT-4o": r"^GPT-4o$",
    "Gemini 1.5 Pro": r"^Gemini 1\.5 Pro$",
    "Llama 3": r"^Llama 3-70B$",
    # Reasoning age
    "o1 / o1-mini": r"^o1-preview$",
    "Claude 3.5 Sonnet": r"^Claude 3\.5 Sonnet$",
    "Gemini 2.0": r"^Gemini 2\.0",
    "DeepSeek V3": r"^DeepSeek.V3",
    "Llama 3.1 405B": r"^Llama 3\.1.405B$",
    # Agent era
    "Claude 3.7 Sonnet": r"^Claude 3\.7 Sonnet$",
    "Claude 4 Opus/Sonnet": r"^Claude (Opus 4|Sonnet 4)$",
    "GPT-4.5": r"^GPT-4\.5$",
    "o3 / o4-mini": r"^o3",
    "Gemini 2.5 Pro": r"^Gemini 2\.5 Pro",
    "Llama 4 (Scout/Maverick)": r"^Llama 4 Scout$",
}


def _download_csv() -> Path:
    """Download and cache the Epoch AI CSV."""
    CACHE_DIR.mkdir(exist_ok=True)
    zip_path = CACHE_DIR / "ai_models.zip"
    csv_path = CACHE_DIR / CSV_NAME
    if not csv_path.exists():
        print(f"Downloading {EPOCH_ZIP_URL} …")
        urlretrieve(EPOCH_ZIP_URL, zip_path)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extract(CSV_NAME, CACHE_DIR)
    return csv_path


def _load_epoch_models(csv_path: Path) -> list[dict]:
    """Load relevant rows from the Epoch AI CSV."""
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "name": row["Model"].strip(),
                    "date": row.get("Publication date", "").strip(),
                    "org": row.get("Organization", "").strip(),
                    "params": row.get("Parameters", "").strip(),
                }
            )
    return rows


def match_models(epoch_rows: list[dict]) -> dict[str, dict]:
    """Match eras.yaml model names to Epoch AI entries."""
    results: dict[str, dict] = {}
    for alias, pattern in MODEL_PATTERNS.items():
        regex = re.compile(pattern, re.IGNORECASE)
        for row in epoch_rows:
            if regex.search(row["name"]):
                results[alias] = row
                break
    return results


def main() -> None:
    csv_path = _download_csv()
    epoch_rows = _load_epoch_models(csv_path)
    matches = match_models(epoch_rows)

    print(f"\n{'Model (eras.yaml)':<35} {'Epoch AI Match':<45} {'Date':<12} {'Org'}")
    print("─" * 120)
    for alias in MODEL_PATTERNS:
        m = matches.get(alias)
        if m:
            print(f"{alias:<35} {m['name']:<45} {m['date']:<12} {m['org']}")
        else:
            print(f"{alias:<35} {'*** NOT FOUND ***':<45}")

    # Summary
    found = len(matches)
    total = len(MODEL_PATTERNS)
    print(f"\nMatched {found}/{total} models from Epoch AI dataset.")
    if found < total:
        missing = set(MODEL_PATTERNS) - set(matches)
        print(f"Missing: {', '.join(sorted(missing))}")


if __name__ == "__main__":
    main()
