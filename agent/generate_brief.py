#!/usr/bin/env python3
"""Generate a prioritized daily brief for a PM from calendar, email and task data.

Usage:
    export ANTHROPIC_API_KEY=...        # or put it in a local .env (git-ignored)
    python agent/generate_brief.py                      # print the brief
    python agent/generate_brief.py --output brief.md    # save it to a file
    python agent/generate_brief.py --dry-run            # print the prompt, no API call
"""

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_DATA_DIR = Path(__file__).parent / "sample_data"
DEFAULT_MODEL = os.environ.get("BRIEF_MODEL", "claude-sonnet-5-5")

SYSTEM_PROMPT = """You are a chief-of-staff for a busy project manager. Each morning you turn raw \
calendar, email and task data into a daily brief that can be read and acted on in under two minutes.

Prioritization rules:
- Lead with the one to three decisions or risks that matter most today, not a list of everything.
- Meetings: flag missing agendas, overlapping events, and meetings whose outcome depends on \
another event earlier in the day. Say what the PM should prepare or decide, not just the time.
- Emails: rank by deadline and sender. Pending decisions and stakeholder deadlines come first; \
newsletters and routine reminders go last in a single line.
- Tasks: surface overdue items above everything else due later. Connect tasks to the meetings \
or emails they affect when there is a real link.
- Use only the data provided. Never invent people, dates, or facts.

Output format (Markdown):
# Daily Brief — <weekday>
## Focus for Today        (2-3 sentences)
## Meetings               (chronological bullets; mark conflicts and missing agendas with a warning emoji)
## Emails Needing a Response   (numbered, highest priority first; one low-priority line at the end)
## Action Items           (red = overdue, yellow = due today or soon, green = later)
Keep it tight. No preamble and no closing remarks."""


def load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(f"Missing data file: {path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"Invalid JSON in {path}: {exc}")


def to_minutes(hhmm: str) -> int:
    hours, minutes = hhmm.split(":")
    return int(hours) * 60 + int(minutes)


def find_conflicts(events: list[dict]) -> list[str]:
    """Detect overlapping meetings in code so the model doesn't have to infer them."""
    conflicts = []
    ordered = sorted(events, key=lambda e: to_minutes(e["start"]))
    for i, first in enumerate(ordered):
        for second in ordered[i + 1:]:
            if to_minutes(second["start"]) < to_minutes(first["end"]):
                conflicts.append(
                    f'"{first["title"]}" ({first["start"]}-{first["end"]}) overlaps with '
                    f'"{second["title"]}" ({second["start"]}-{second["end"]})'
                )
    return conflicts


def build_prompt(calendar: dict, emails: dict, tasks: dict) -> str:
    conflicts = find_conflicts(calendar["events"])
    no_agenda = [e["title"] for e in calendar["events"] if not e.get("agenda")]
    precomputed = {
        "meeting_conflicts": conflicts or "none",
        "meetings_without_agenda": no_agenda or "none",
    }
    return (
        f"Today is {calendar.get('day', '')} {calendar.get('date', '')}.\n\n"
        "<precomputed_checks>\n"
        f"{json.dumps(precomputed, indent=2)}\n"
        "</precomputed_checks>\n\n"
        "<calendar>\n"
        f"{json.dumps(calendar['events'], indent=2)}\n"
        "</calendar>\n\n"
        "<emails>\n"
        f"{json.dumps(emails['emails'], indent=2)}\n"
        "</emails>\n\n"
        "<tasks>\n"
        f"{json.dumps(tasks['tasks'], indent=2)}\n"
        "</tasks>\n\n"
        "Write today's brief."
    )


def generate_brief(prompt: str, model: str) -> str:
    try:
        import anthropic
    except ImportError:
        sys.exit("The 'anthropic' package is not installed. Run: pip install -r requirements.txt")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. See README for setup, or use --dry-run.")

    client = anthropic.Anthropic()
    try:
        response = client.messages.create(
            model=model,
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIError as exc:
        sys.exit(f"Anthropic API error: {exc}")
    return "".join(block.text for block in response.content if block.type == "text")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a prioritized daily PM brief.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="folder with calendar/emails/tasks JSON")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Claude model ID (default: %(default)s)")
    parser.add_argument("--output", type=Path, help="write the brief to this file instead of stdout")
    parser.add_argument("--dry-run", action="store_true", help="print the assembled prompt and exit without calling the API")
    args = parser.parse_args()

    calendar = load_json(args.data_dir / "calendar.json")
    emails = load_json(args.data_dir / "emails.json")
    tasks = load_json(args.data_dir / "tasks.json")
    prompt = build_prompt(calendar, emails, tasks)

    if args.dry_run:
        print(f"--- SYSTEM ---\n{SYSTEM_PROMPT}\n\n--- USER ---\n{prompt}")
        return

    brief = generate_brief(prompt, args.model)
    if args.output:
        args.output.write_text(brief + "\n", encoding="utf-8")
        print(f"Brief written to {args.output}")
    else:
        print(brief)


if __name__ == "__main__":
    main()
