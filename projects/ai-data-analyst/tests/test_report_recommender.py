from report_recommender import recommend_reports


def test_numeric_schema_recommends_distributions():
    schema = [{"column": "amount", "logical_type": "numeric", "missing_pct": 0}]
    names = {item["name"] for item in recommend_reports(schema)}
    assert "Numeric distributions" in names


def test_datetime_numeric_schema_recommends_time_trends():
    schema = [
        {"column": "date", "logical_type": "datetime", "missing_pct": 0},
        {"column": "revenue", "logical_type": "numeric", "missing_pct": 0},
    ]
    names = {item["name"] for item in recommend_reports(schema)}
    assert "Time trends" in names


def test_categorical_schema_recommends_segments():
    schema = [{"column": "region", "logical_type": "categorical", "missing_pct": 0}]
    names = {item["name"] for item in recommend_reports(schema)}
    assert "Segment comparison" in names


def test_missingness_is_explained():
    schema = [{"column": "discount", "logical_type": "numeric", "missing_pct": 12.5}]
    recommendations = recommend_reports(schema)
    assert any(item["name"] == "Missingness review" for item in recommendations)
