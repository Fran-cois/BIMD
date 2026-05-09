# SKILL.md — BackInMyDay (`bimd`)

> Use this file to understand how to interact with the `bimd` CLI tool programmatically or via shell commands.

## What is bimd?

`bimd` is a Python CLI that performs "AI-era software archaeology" on Git repositories. Given a repo (or a date), it tells you which AI era the project belongs to, lists the models that existed at that time, and delivers a sarcastic boomer-developer comment.

## Installation

```bash
pip install backinmyday
```

Requires Python 3.10+.

## Commands

### `bimd scan [PATH]`

Scan a Git repository and display the AI era of its first commit.

```bash
bimd scan .                   # current directory
bimd scan /path/to/repo       # specific repo
```

**Output**: ASCII banner, era name, table of models (name / release date / org), context window range, era period, boomer comment.

### `bimd era <REF>`

Show the AI era for a specific date or commit hash.

```bash
bimd era 2023-03-15           # by date (YYYY-MM-DD)
bimd era abc1234 -p /my/repo  # by commit hash (needs --path/-p for the repo)
```

### `bimd badge [PATH]`

Generate a shields.io badge Markdown line for the repo's era.

```bash
bimd badge .
```

**Output**: A Markdown image link like `![BackInMyDay Era](https://img.shields.io/badge/Era-...-color)`.

## Global Options

| Flag | Description |
|------|-------------|
| `-l`, `--lang` | Set output language: `en` (default) or `fr` |

Language can also be set via the `BIMD_LANG` environment variable.

## Programmatic Usage (Python)

```python
from bimd.data import load_eras, find_era
import datetime

# Load all eras from eras.yaml
eras = load_eras()

# Find era for a specific date
era = find_era(datetime.date(2023, 3, 15))
print(era.name)            # "The GPT-4 Revolution"
print(era.id)              # "gpt4_era"
print(era.context_window)  # "8k - 32k tokens"
for model in era.models:
    print(f"{model.name} ({model.org}) — {model.released}")

# Get a boomer comment
from bimd.humor import get_boomer_comment
print(get_boomer_comment(era))
```

### Key classes

| Class | Module | Fields |
|-------|--------|--------|
| `Era` | `bimd.data` | `id`, `name`, `start_date`, `end_date`, `context_window`, `models: list[ModelInfo]`, `badge_label`, `badge_color`, `boomer_comments` |
| `ModelInfo` | `bimd.data` | `name`, `released`, `org` |

### Git utilities

```python
from bimd.git_utils import get_repo, get_first_commit_date, get_commit_date

repo = get_repo("/path/to/repo")
first_date = get_first_commit_date(repo)   # datetime.date
commit_date = get_commit_date(repo, "abc1234")  # datetime.date
```

## Era Database

The era definitions live in `bimd/eras.yaml`. There are **11 eras** spanning from 1900 (pre-Transformer) to 2099 (future unknown), with **42 verified models** total. Model release dates are sourced from official provider documentation — see `SOURCES.md` for full provenance.

### Era IDs

| ID | Period | Example Models |
|----|--------|----------------|
| `pre_transformer` | 1900–2017 | Word2Vec, LSTM |
| `transformer_dawn` | 2017–2018 | Transformer, GPT-1 |
| `bert_era` | 2018–2020 | BERT, GPT-2, XLNet |
| `gpt3_era` | 2020–2022 | GPT-3, Codex, DALL-E |
| `chatgpt_era` | 2022–2023 | ChatGPT, GPT-3.5 |
| `gpt4_era` | 2023–2023 | GPT-4, Claude, PaLM 2 |
| `open_source_era` | 2023–2024 | Llama 2, Mistral, Mixtral |
| `multimodal_era` | 2024–2024 | GPT-4o, Gemini 1.5, Claude 3 |
| `reasoning_era` | 2024–2025 | o1, DeepSeek-R1 |
| `agent_era` | 2025–2026 | Claude 4, GPT-5, Gemini 2.5 |
| `future_unknown` | 2027–2099 | ??? |

## Error Handling

- Exit code `1`: not a Git repo, no commits, unresolvable commit hash, or no matching era.
- All errors are printed to stdout via Rich panels.

## Environment

| Variable | Description |
|----------|-------------|
| `BIMD_LANG` | Override output language (`en` or `fr`) |
