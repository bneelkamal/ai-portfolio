from __future__ import annotations

import numpy as np
import pandas as pd


def get_sample_datasets() -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(42)
    n = 240
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    regions = rng.choice(["North", "South", "East", "West"], n)
    segments = rng.choice(["Retail", "SME", "Corporate"], n, p=[0.55, 0.3, 0.15])
    banking = pd.DataFrame({
        "application_date": dates,
        "region": regions,
        "customer_segment": segments,
        "loan_amount": rng.lognormal(11.0, 0.55, n).round(2),
        "annual_income": rng.lognormal(12.0, 0.45, n).round(2),
        "credit_score": np.clip(rng.normal(700, 55, n), 420, 850).round(),
        "default_flag": rng.binomial(1, 0.12, n),
    })
    claims = pd.DataFrame({
        "claim_date": dates,
        "product": rng.choice(["Motor", "Health", "Property", "Travel"], n),
        "channel": rng.choice(["Agent", "Web", "Branch"], n),
        "claim_amount": rng.gamma(2.2, 18000, n).round(2),
        "processing_days": np.maximum(rng.normal(11, 5, n), 1).round(1),
        "fraud_flag": rng.binomial(1, 0.08, n),
    })
    sales = pd.DataFrame({
        "order_date": dates,
        "category": rng.choice(["Electronics", "Home", "Fashion", "Grocery"], n),
        "region": regions,
        "units": rng.integers(1, 15, n),
        "revenue": rng.lognormal(7.4, 0.7, n).round(2),
        "discount_pct": rng.uniform(0, 35, n).round(1),
    })
    trend_dates = pd.date_range("2022-01-01", periods=36, freq="MS")
    trend = pd.DataFrame({
        "month": trend_dates,
        "revenue": (100000 + np.arange(36) * 4200 + rng.normal(0, 9000, 36)).round(2),
        "expenses": (65000 + np.arange(36) * 2500 + rng.normal(0, 6500, 36)).round(2),
        "customers": (1200 + np.arange(36) * 35 + rng.normal(0, 45, 36)).round().astype(int),
    })
    return {
        "Banking risk portfolio": banking,
        "Insurance claims": claims,
        "Retail sales": sales,
        "Monthly business trend": trend,
    }
