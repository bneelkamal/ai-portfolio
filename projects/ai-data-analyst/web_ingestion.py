from __future__

from io import BytesIO, StringIO
from ipaddress import ip_address
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

MAX_BYTES = 8 * 1024 * 1024
TIMEOUT_SECONDS = 15


def _validate_url(url: str) -> None:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Enter a valid public HTTP(S) URL.")
    host = parsed.hostname.lower()
    if host in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Local URLs are not allowed.")
    try:
        address = ip_address(host)
        if address.is_private or address.is_loopback or address.is_link_local:
            raise ValueError("Private-network URLs are not allowed.")
    except ValueError:
        if host.replace(".", "").isdigit():
            raise ValueError("The URL host is not allowed.")


def _response(url: str) -> requests.Response:
    _validate_url(url)
    response = requests.get(
        url,
        timeout=TIMEOUT_SECONDS,
        headers={"User-Agent": "AI-Portfolio-Data-Analyst/0.1"},
    )
    response.raise_for_status()
    if len(response.content) > MAX_BYTES:
        raise ValueError("The response is larger than the 8 MB demo limit.")
    return response


def _file_dataframe(response: requests.Response, url: str) -> pd.DataFrame | None:
    content_type = response.headers.get("content-type", "").lower()
    lower_url = url.lower().split("?", 1)[0]
    if "csv" in content_type or lower_url.endswith(".csv"):
        return pd.read_csv(StringIO(response.text))
    if "spreadsheet" in content_type or "excel" in content_type or lower_url.endswith((".xlsx", ".xls")):
        return pd.read_excel(BytesIO(response.content))
    if "json" in content_type or lower_url.endswith(".json"):
        payload = response.json()
        return pd.json_normalize(payload if isinstance(payload, list) else payload.get("data", payload))
    return None


def extract_public_url(url: str) -> dict:
    response = _response(url.strip())
    direct = _file_dataframe(response, url)
    if direct is not None:
        return {"kind": "tabular", "dataframe": direct, "title": url, "warning": None}

    soup = BeautifulSoup(response.text, "html.parser")
    tables = pd.read_html(StringIO(response.text), flavor="lxml")
    if tables:
        frame = max(tables, key=lambda table: table.shape[0] * table.shape[1]).copy()
        return {
            "kind": "html_table",
            "dataframe": frame,
            "title": soup.title.get_text(strip=True) if soup.title else url,
            "warning": f"Found {len(tables)} HTML table(s); selected the largest table.",
        }

    text = soup.get_text(" ", strip=True)
    words = text.split()
    metadata = pd.DataFrame({
        "metric": ["characters", "words", "paragraphs", "links"],
        "value": [len(text), len(words), len(soup.find_all("p")), len(soup.find_all("a"))],
    })
    return {
        "kind": "text",
        "dataframe": metadata,
        "title": soup.title.get_text(strip=True) if soup.title else url,
        "warning": "No structured table was found; showing page-level text metadata.",
        "text_preview": text[:1000],
    }
