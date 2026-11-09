> Fictional example (`remindr`). Verification labels demonstrate format only; these commands were not executed by this skill repository.

# Runbook

Run commands from the project root, not from `.architect/`.

## Setup

Python 3.11+, Flask and PyYAML. Create a virtual environment with `python -m venv .venv`, activate it using the platform's command, then run `pip install -r requirements.txt`.

## Run

- CLI: `python summarize.py digest reminders/ --out digest.txt`.
- Local web: `python app.py --port 8080`; bind only to localhost.

## Test

- Offline: `python -m pytest tests/`.
- Coverage is unverified and requires a separately installed coverage plugin.

In the fictional scenario, the basic commands above were exercised locally; this is not evidence of a running deployment. Current limitations live in [Known Issues](PROJECT_STATE.md#known-issues).

## Common failures

YAML parse failure: check indentation and tabs. Port 8080 busy: choose a free local port with `--port`.
