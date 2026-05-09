<div align="center">

# 👴 BackInMyDay

**AI-era software archaeology** — Find out what the LLM landscape looked like when your code was written.

[![PyPI](https://img.shields.io/pypi/v/backinmyday?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/backinmyday/)
[![Python](https://img.shields.io/pypi/pyversions/backinmyday?logo=python&logoColor=white)](https://pypi.org/project/backinmyday/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/Fran-cois/BIMD/actions/workflows/ci.yml/badge.svg)](https://github.com/Fran-cois/BIMD/actions/workflows/ci.yml)
[![Publish](https://github.com/Fran-cois/BIMD/actions/workflows/publish.yml/badge.svg)](https://github.com/Fran-cois/BIMD/actions/workflows/publish.yml)
[![GitHub Pages](https://github.com/Fran-cois/BIMD/actions/workflows/pages.yml/badge.svg)](https://fran-cois.github.io/BIMD/)

</div>

---

`bimd` scans a Git repository, finds its first commit date, and tells you which **AI era** your project was born in — complete with the models that existed at the time and sarcastic boomer-developer commentary.

## Installation

```bash
pip install backinmyday
```

> **Requires Python 3.10+**

## Getting Started

### Scan the current repo

```bash
bimd scan .
```

```
 ____             _    ___       __  __       ____
| __ )  __ _  ___| | _|_ _|_ __ |  \/  |_   _|  _ \  __ _ _   _
|  _ \ / _` |/ __| |/ /| || '_ \| |\/| | | | | | | |/ _` | | | |
| |_) | (_| | (__|   < | || | | | |  | | |_| | |_| | (_| | |_| |
|____/ \__,_|\___|_|\_\___|_| |_|_|  |_|\__, |____/ \__,_|\__, |
                                         |___/             |___/

  📅  Date analysed  : 2026-05-09
  🏷️   Era detected   : The Agentic Era (agent_era)

       🤖 Models available at the time
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Model                  ┃ Released   ┃ Organization    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ o3-mini                │ 2025-01-31 │ OpenAI          │
│ Claude 3.7 Sonnet      │ 2025-02-24 │ Anthropic       │
│ GPT-4.5                │ 2025-02-27 │ OpenAI          │
│ ...                    │            │                 │
└────────────────────────┴────────────┴─────────────────┘

  👴 "Vibe coding 2.0: now the agent vibe-codes for you
      while you sip your coffee."
```

### Time-travel to any date

```bash
bimd era 2019-06-15
```

Shows the BERT era with GPT-2, XLNet, and a grumpy reminder that "GPT-2 was too dangerous to release."

### Generate a badge for your README

```bash
bimd badge .
```

Outputs a shields.io Markdown snippet you can paste into your README:

![BackInMyDay Era](https://img.shields.io/badge/Era-Agent%20Orchestrator-9cf)

### Switch language

```bash
bimd -l fr scan .          # French output
export BIMD_LANG=fr        # or set it globally
```

Supported: `en` (default), `fr`.

## Commands

| Command | Description |
|---------|-------------|
| `bimd scan [PATH]` | Scan a Git repo and display its AI era |
| `bimd era <DATE\|HASH>` | Show the AI era for any date or commit hash |
| `bimd badge [PATH]` | Generate a shields.io badge for the repo's era |

## How it works

1. Reads the **first commit date** from your Git history
2. Matches it against **11 AI eras** (pre-Transformer → Agentic Era)
3. Shows **42 verified models** with release dates, orgs, and context window sizes
4. Delivers a sarcastic boomer-developer quip for good measure

The era database lives in [`bimd/eras.yaml`](bimd/eras.yaml). Model dates are sourced from official provider docs — see [`SOURCES.md`](SOURCES.md) for full provenance.

## Contributing

PRs welcome! To add models or eras, edit `bimd/eras.yaml` and run the tests:

```bash
pip install -e ".[dev]"
pytest
```

## Links

- **PyPI**: [pypi.org/project/backinmyday](https://pypi.org/project/backinmyday/)
- **Docs**: [fran-cois.github.io/BIMD](https://fran-cois.github.io/BIMD/)
- **Sources**: [`SOURCES.md`](SOURCES.md) — per-model provenance for all 42 models

## License

[MIT](LICENSE)
