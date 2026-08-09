from io import BytesIO
from zipfile import ZipFile

from security import validate_upload


def test_valid_csv_is_accepted_with_hash():
    report = validate_upload("sample.csv", b"name,amount\nA,10\nB,20\n")
    assert report["accepted"] is True
    assert len(report["sha256"]) == 64


def test_binary_csv_is_rejected():
    report = validate_upload("sample.csv", b"name,amount\nA,\x00\n")
    assert report["accepted"] is False


def test_unsupported_extension_is_rejected():
    report = validate_upload("macro.xlsm", b"not a workbook")
    assert report["accepted"] is False


def test_formula_like_csv_values_are_reported():
    report = validate_upload("sample.csv", b"name,value\nA,=SUM(1,2)\n")
    assert any("formula-like" in warning for warning in report["warnings"])


def test_corrupt_xlsx_is_rejected():
    report = validate_upload("sample.xlsx", b"PK-not-a-real-zip")
    assert report["accepted"] is False


def test_valid_minimal_xlsx_container_passes_structure():
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("xl/workbook.xml", "<workbook/>")
    report = validate_upload("sample.xlsx", buffer.getvalue())
    assert any(check["name"] == "xlsx_container" and check["status"] == "passed" for check in report["checks"])


def test_size_limit_is_enforced():
    report = validate_upload("large.csv", b"a" * (10 * 1024 * 1024 + 1))
    assert report["accepted"] is False
