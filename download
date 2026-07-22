# Project Charter: Daily PM Brief Agent

## Problem Statement
Project managers routinely start the day by manually cross-referencing three disconnected sources — calendar, email, and task tracker — to figure out what actually needs attention. This is low-value, repetitive cognitive overhead that delays getting to real work, and it's the kind of task well-suited to AI-assisted automation.

## Objective
Design and build a proof-of-concept agent that ingests calendar, email, and task data, and produces a single prioritized daily brief a PM could act on in under two minutes of reading.

## Scope

**In scope:**
- Sample/mock data representing a realistic PM's calendar, inbox, and task list
- An agent (via the Anthropic API) that synthesizes this into a structured brief
- A polished, formatted sample output demonstrating the concept
- Documentation of architecture and a path to live-data integration

**Out of scope (for this POC):**
- Live Gmail/Calendar API connections (documented as a next step, not built here)
- Multi-user support or persistent storage
- Mobile or web front-end (output is a formatted document, not an app)

## Success Criteria
- Agent reliably produces a brief that correctly prioritizes urgent items over routine ones
- Output is genuinely usable — something a PM would actually want to read, not a data dump
- Architecture is documented clearly enough that a technical reviewer could see how live integration would work

## Stakeholders
- **Primary user:** PMs managing multiple concurrent workstreams
- **Secondary audience:** technical reviewers/hiring managers evaluating this as a portfolio piece

## Risks & Mitigations
| Risk | Mitigation |
|---|---|
| Public repo containing real personal/client data | Use only fabricated sample data throughout |
| Agent output feels generic or low-value | Ground the prompt in realistic PM scenarios (conflicting meetings, vague emails, overdue tasks) rather than trivial examples |
| Scope creep into a full live-integration build | Explicitly cap this phase at POC with sample data; document — don't build — the live-data path |
