# daily-pm-brief-agent

AI agent that consolidates calendar, email, and task data into a prioritized daily brief — sample-data proof of concept.

## Quick start

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here   # never commit this
python agent/generate_brief.py           # prints the brief
```

Options:

- `--dry-run` prints the assembled prompt without calling the API (no key needed)
- `--output brief.md` saves the brief to a file
- `--model <id>` or the `BRIEF_MODEL` env var overrides the default model
- `--data-dir <path>` points at a different folder of `calendar.json`, `emails.json`, `tasks.json`

## Layout

| Path | What it is |
|---|---|
| `agent/generate_brief.py` | Loads the data, assembles the prompt, calls the Claude API |
| `agent/sample_data/` | Fabricated calendar, email and task data for one PM's Tuesday |
| `docs/project-charter.md` | Problem, scope, success criteria and risks |
| `docs/architecture.md` | How it works and the path to live Gmail/Calendar integration |
| `docs/sample-brief.md` | Example output |

All sample data is fictional. No real names, companies or personal information are used.

## License

MIT — see `LICENSE`.
