# Deployment

## Streamlit entrypoint

Deploy the repository with this main file:

```text
projects/ai-data-analyst/app.py
```

The application is designed to run without an API key in deterministic mode.

## Streamlit configuration

The project limits uploads to 10 MB and uses a wide, light dashboard theme through `.streamlit/config.toml`.

## Secrets

Never commit API keys to GitHub. If an optional hosted LLM is added later, configure its key through the deployment platform's secrets manager. The app must continue to work when the key is missing.

## Security mode

Set the following environment variable for stricter deployments:

```text
STRICT_SECURITY=1
```

Strict mode rejects uploaded files when ClamAV is unavailable. A production deployment should provide a separate quarantine and antivirus service rather than relying only on in-process checks.

## Before publishing the live link

1. Run `pytest` locally.
2. Test each built-in sample dataset.
3. Test a valid CSV and XLSX file.
4. Test malformed and oversized files.
5. Test a public CSV or HTML-table URL.
6. Confirm that no secrets or sensitive files are committed.
7. Add the actual deployed URL to the portfolio README.
