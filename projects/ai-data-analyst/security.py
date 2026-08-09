from __future__ import annotations

import csv
import hashlib
import io
import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_ROWS = 250_000
MAX_COLUMNS = 250
FORMULA_PREFIXES = ("=", "+", "-", "@")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _scan_clamav(data: bytes) -> dict:
    scanner = shutil.which("clamscan")
    if not scanner:
        return {"status": "unavailable", "detail": "ClamAV is not installed."}
    with tempfile.NamedTemporaryFile(suffix=".upload", delete=False) as handle:
        handle.write(data)
        path = handle.name
    try:
        result = subprocess.run([scanner, "--no-summary", path], capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            return {"status": "passed", "detail": "ClamAV reported no detections."}
        return {"status": "rejected", "detail": result.stdout.strip() or result.stderr.strip() or "ClamAV detected a threat."}
    except Exception as exc:
        return {"status": "unavailable", "detail": f"ClamAV scan failed: {exc}"}
    finally:
        Path(path).unlink(missing_ok=True)


def validate_upload(filename: str, data: bytes, strict: bool | None = None) -> dict:
    strict = os.getenv("STRICT_SECURITY", "0") == "1" if strict is None else strict
    suffix = Path(filename).suffix.lower()
    report = {"accepted": True, "filename": filename, "sha256": _sha256(data), "checks": [], "warnings": []}

    if len(data) == 0 or len(data) > MAX_UPLOAD_BYTES:
        report["accepted"] = False
        report["checks"].append({"name": "size", "status": "failed"})
        return report
    if suffix not in {".csv", ".xlsx"}:
        report["accepted"] = False
        report["checks"].append({"name": "extension", "status": "failed", "detail": "Only CSV and XLSX are accepted."})
        return report

    if suffix == ".csv":
        if b"\x00" in data:
            report["accepted"] = False
            report["checks"].append({"name": "csv_text", "status": "failed", "detail": "Binary NUL byte detected."})
            return report
        try:
            text = data.decode("utf-8-sig")
            rows = list(csv.reader(io.StringIO(text)))
            width = max((len(row) for row in rows), default=0)
            formula_cells = sum(1 for row in rows for cell in row if cell.lstrip().startswith(FORMULA_PREFIXES))
            if len(rows) > MAX_ROWS or width > MAX_COLUMNS:
                report["accepted"] = False
                report["checks"].append({"name": "csv_shape", "status": "failed", "detail": "Row or column limit exceeded."})
                return report
            report["checks"].append({"name": "csv_structure", "status": "passed", "rows": len(rows), "columns": width})
            if formula_cells:
                report["warnings"].append(f"{formula_cells} formula-like cell(s) detected; sanitize before export.")
        except UnicodeDecodeError:
            report["accepted"] = False
            report["checks"].append({"name": "encoding", "status": "failed", "detail": "CSV is not valid UTF-8."})
            return report
    else:
        if not data.startswith(b"PK"):
            report["accepted"] = False
            report["checks"].append({"name": "xlsx_signature", "status": "failed"})
            return report
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                names = set(archive.namelist())
                bad_member = archive.testzip()
                suspicious = [name for name in names if "vbaProject.bin" in name or name.startswith("xl/embeddings/") or name.startswith("xl/externalLinks/")]
                if bad_member or "[Content_Types].xml" not in names or suspicious:
                    report["accepted"] = False
                    report["checks"].append({"name": "xlsx_container", "status": "failed", "detail": "Corrupt, incomplete, or active-content workbook detected."})
                    return report
                report["checks"].append({"name": "xlsx_container", "status": "passed", "members": len(names)})
        except zipfile.BadZipFile:
            report["accepted"] = False
            report["checks"].append({"name": "xlsx_container", "status": "failed", "detail": "Invalid XLSX container."})
            return report

    av = _scan_clamav(data)
    report["checks"].append({"name": "antivirus", **av})
    if av["status"] == "rejected" or (strict and av["status"] != "passed"):
        report["accepted"] = False
    if av["status"] == "unavailable":
        report["warnings"].append("Antivirus scanner unavailable; structural checks are not a malware guarantee.")
    return report
