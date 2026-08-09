# Ingestion Security

The portal follows a reject-first policy: validate the source before parsing it with pandas or passing it to the LangGraph workflow.

## Current controls

- Maximum upload size: 10 MB.
- CSV and XLSX allowlist.
- SHA-256 integrity hash.
- CSV UTF-8, NUL-byte, shape, and formula-like-cell checks.
- XLSX ZIP signature and container validation.
- Rejection of VBA projects, embedded objects, and external links.
- Optional ClamAV scanning.
- Strict mode through `STRICT_SECURITY=1` rejects files when ClamAV is unavailable.

## Important limitation

Structural validation is not equivalent to antivirus protection. The application must display `scanner unavailable` rather than claiming that a file is clean. Production deployments should run ClamAV or another approved malware scanner in a separate quarantine service.

## CSV injection

Values beginning with `=`, `+`, `-`, or `@` can become formulas when exported to spreadsheet software. The portal warns about these values and must sanitize them before generating downloadable spreadsheet files.

## Future URL controls

The URL ingestion layer must validate every redirect, resolve DNS before connecting, block private and metadata networks, restrict content types, enforce timeouts and response limits, and reject executable or macro-enabled downloads. It must never bypass authentication, paywalls, CAPTCHAs, or anti-bot controls.

## Threat model

This is a portfolio prototype, not a certified malware-analysis service. Public demonstrations should use synthetic or non-sensitive data. Sensitive production files require private hosting, access control, quarantine storage, antivirus scanning, isolated parsing, audit logging, and operational monitoring.
