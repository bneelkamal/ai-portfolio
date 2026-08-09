from __future__ import annotations


def recommend_reports(schema: list[dict]) -> list[dict]:
    numeric = [item for item in schema if item["logical_type"] == "numeric"]
    categorical = [item for item in schema if item["logical_type"] in {"categorical", "boolean"}]
    dates = [item for item in schema if item["logical_type"] == "datetime"]
    missing = [item for item in schema if item["missing_pct"] > 0]
    reports = [{"name": "Dataset overview", "reason": "Always recommended to establish dataset size, fields, and structure."}, {"name": "Data quality", "reason": "Always recommended to review missing values and structural warnings."}]
    if numeric:
        reports.append({"name": "Numeric distributions", "reason": f"Recommended because {len(numeric)} numeric field(s) were detected."})
    if categorical:
        reports.append({"name": "Segment comparison", "reason": f"Recommended because {len(categorical)} categorical or boolean field(s) support group analysis."})
    if dates and numeric:
        reports.append({"name": "Time trends", "reason": "Recommended because date/time and numeric measures can be compared over time."})
    if len(numeric) >= 2:
        reports.append({"name": "Relationships", "reason": "Recommended because multiple numeric measures support correlation and scatter analysis."})
    if missing:
        reports.append({"name": "Missingness review", "reason": f"Recommended because {len(missing)} field(s) contain missing values."})
    return reports
