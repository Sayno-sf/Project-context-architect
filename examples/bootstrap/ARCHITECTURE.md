> Fictional example (`remindr`); illustrative architecture, not a real application.

# Architecture

`summarize.py` reads YAML from `reminders/`, validates reminders and builds a plain-text digest. `app.py` is the local Flask entry point and renders that digest as HTML. There is no database or notification sender; reminder files own persistent data and the web layer owns no separate reminder state.

The CLI entry point is `summarize.py`; the web entry point is `app.py`. Both use the same digest builder. See [ADR-001](DECISIONS.md#adr-001--cli-owns-digest-rendering-web-view-wraps-it) for ownership rationale, [Runbook](RUNBOOK.md) for commands and [Project State](PROJECT_STATE.md#current-status) for implementation limits.
