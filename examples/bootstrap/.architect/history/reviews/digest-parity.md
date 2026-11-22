# Digest parity review

> Historical artifact from the fictional `remindr` project. Current rationale: [ADR-001](../../DECISIONS.md#adr-001--cli-owns-digest-rendering-web-view-wraps-it).

On 2026-08-14, the design review considered a formatting mismatch between the CLI digest and the web preview. Patching the web template would fix the visible discrepancy, but the next format change would again require editing both templates. The alternative was to share the digest builder and leave HTML wrapping to the web layer.
