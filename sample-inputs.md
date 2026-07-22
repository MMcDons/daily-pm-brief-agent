# Architecture

## Overview

```
 ┌─────────────────┐     ┌──────────────────┐     ┌────────────────────┐
 │  Calendar data   │     │   Email data     │     │   Task list data   │
 │ (sample_data/    │     │  (sample_data/   │     │  (sample_data/     │
 │  calendar.json)  │     │   emails.json)   │     │   tasks.json)      │
 └────────┬─────────┘     └────────┬─────────┘     └──────────┬─────────┘
          │                        │                          │
          └────────────────────────┼──────────────────────────┘
                                    ▼
                     ┌──────────────────────────┐
                     │   generate_brief.py       │
                     │  (assembles prompt,        │
                     │   calls Claude API)        │
                     └──────────────┬─────────────┘
                                    ▼
                     ┌──────────────────────────┐
                     │   Formatted daily brief    │
                     │   (Markdown / email-ready) │
                     └──────────────────────────┘
```

## How It Works

1. **Data ingestion** — the script loads three JSON files representing a day's calendar events, unread/flagged emails, and open task items.
2. **Prompt assembly** — the script builds a single prompt that gives the model all three data sources plus explicit instructions on how a PM would want them prioritized (e.g., meetings with prep needs first, emails from leadership or with deadlines flagged, overdue tasks surfaced above routine ones).
3. **Generation** — the prompt is sent to the Anthropic API (Claude), which synthesizes the inputs into a single structured brief.
4. **Output** — the brief is returned as formatted Markdown, suitable for saving as a doc or pasting into an email to yourself.

## Why This Prioritization Logic

The prompt encodes judgment a PM already applies manually: a meeting with no agenda and three overdue action items feeding into it matters more than a routine standup; an email from a stakeholder with a decision pending matters more than a newsletter. The point of the agent isn't to replace that judgment — it's to apply it consistently, every morning, before the PM has even opened their inbox.

## Path to Live Integration (not built in this POC)

To move from sample data to a live version:

- **Calendar:** Google Calendar API (`calendar.events.list`) or Microsoft Graph API for Outlook/Teams calendars
- **Email:** Gmail API (`users.messages.list`) or Microsoft Graph for Outlook
- **Tasks:** integration with whatever tracker is in use (Asana, Planner, Jira) via their respective APIs
- **Auth:** OAuth 2.0 for each service, with tokens scoped to read-only access
- **Scheduling:** a daily trigger (cron job, or a scheduled cloud function) to run the brief automatically each morning and deliver it by email or Slack DM

The core synthesis logic in `generate_brief.py` wouldn't change — only the data-loading functions would be swapped from reading local JSON files to calling live APIs.

## Tools Used
- Python 3
- Anthropic API (Claude) for synthesis
- JSON for sample data structure
