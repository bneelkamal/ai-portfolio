# Ingestion Security

The portal follows a reject-first policy: validate a source before parsing it with pandas or passing it to the LangGraph workflow.

## Controls

- Maximum upload size: 10 MB.
- CSV and XLSX allowlist.
- SHA-256 integrity hash.
- CSV encoding, NUL-byte, shape, and formula-like-cell checks.
- XLSX ZIP signature and container validation.
- Rejection of VBA projects, embedded objects, and external links.
- Optional ClamAV scanning.
- `STRICT_SECURITY=1` rejects files when ClamAV is unavailable.

The Streamlit UI must display `scanner unavailable` rather than claiming a file is clean when no antivirus scanner is configured. Production deployments require quarantine storage, isolated parsing, access control, logging, and monitoring.
