from __future__ import annotations

import numpy as np
import pandas as pd


def get_sample_datasets() -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", periods=120, freq="D")
    sales = pd.DataFrame({
        "date": dates,
        "region": rng.choice(["North", "South", "East", "West"], len(dates)),
        "product": rng.choice(["Platform", "Analytics", "Security"], len(dates)),
        "units_sold": rng.poisson(45, len(dates)) + 5,
        "discount": rng.uniform(0.02, 0.22, len(dates)).round(2),
        "channel": rng.choice(["Direct", "Partner", "Online"], len(dates)),
    })
    sales["revenue"] = (sales["units_sold"] * rng.normal(185, 20, len(dates)) * (1 - sales["discount"])).round(2)

    n = 250
    churn = pd.DataFrame({
        "customer_id": [f"C{i:04d}" for i in range(n)],
        "signup_date": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 600, n), unit="D"),
        "plan": rng.choice(["Basic", "Professional", "Enterprise"], n, p=[.45, .4, .15]),
        "monthly_fee": rng.choice([29, 79, 199], n, p=[.45, .4, .15]),
        "tenure_months": rng.integers(1, 48, n),
        "country": rng.choice(["India", "UK", "Germany", "USA"], n),
    })
    churn["churned"] = (((churn["tenure_months"] < 8) & (rng.random(n) < .45)) | (rng.random(n) < .12)).astype(int)

    n = 500
    fraud = pd.DataFrame({
        "transaction_id": [f"T{i:05d}" for i in range(n)],
        "timestamp": pd.Timestamp("2025-03-01") + pd.to_timedelta(rng.integers(0, 30 * 24 * 60, n), unit="m"),
        "amount": rng.lognormal(4, 1, n).round(2),
        "merchant_category": rng.choice(["Retail", "Travel", "Food", "Digital", "Gambling"], n),
        "country": rng.choice(["IN", "GB", "DE", "US"], n),
    })
    fraud["is_fraud"] = (fraud["amount"] > fraud["amount"].quantile(.96)).astype(int)
    return {"Sales performance": sales, "Customer churn": churn, "Fraud transactions": fraud}
