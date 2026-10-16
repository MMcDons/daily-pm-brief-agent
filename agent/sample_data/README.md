# Sample Data

This POC uses fabricated data representing a realistic (but fictional) PM's Tuesday. No real names, companies, or personal information are used anywhere in this repo.

The raw data the agent reads is in `agent/sample_data/`:
- `calendar.json` — 4 sample meetings, including one with no agenda and one that conflicts with another
- `emails.json` — 6 sample emails, ranging from a routine newsletter to a stakeholder email with a pending decision
- `tasks.json` — 5 sample open action items, including two overdue

This mix was chosen deliberately so the agent has to actually exercise judgment — not just re-list the inputs in the order they arrived, but recognize what's urgent, what's overdue, and what's noise.
