> Fictional example (`remindr`); illustrative claims, not measured test results.

# Project State

Last Updated: 2026-10-22

## Project

Internal daily-digest tool for the platform team, rendering YAML reminders as CLI text and an in-progress HTML view.

## Current Status

CLI implemented and tested in this fictional scenario. The local web wrapper renders simple digests; multi-line content is not ready. No shared web deployment or user acceptance is claimed.

## Current Work

Fix multi-line YAML block rendering in the web wrapper (PR #23). Stop when offline multiline rendering tests pass and the PR is ready for review; merging is a separate action.

## Implemented

- YAML validation, CLI digest rendering and per-source timezones.
- Local Flask wrapper for simple digest content.

## Known Issues

- The web wrapper drops multi-line blocks.
- A future `--from` date silently produces an empty CLI digest.

## Non-goals

Real notifications and multi-user authentication are outside the current scope.

## Next

Complete [Current Work](#current-work), then request review. Do not mark the web view shipped before review and acceptance.

## New Session Handoff

- Identity, delivery and work: [Project](#project), [Current Status](#current-status), [Current Work](#current-work).
- Composition and entry points: [Architecture](ARCHITECTURE.md).
- Constraints: [Project rules](AGENTS.md#project-rules), [Non-goals](#non-goals).
- Outstanding work and stopping point: [Known Issues](#known-issues), [Next](#next).
- Commands: [Runbook](RUNBOOK.md); enduring rationale: [Decisions](DECISIONS.md).
