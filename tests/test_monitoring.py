import pandas as pd

from src.monitoring.model_monitor import drift_alerts, feature_drift


def test_feature_drift_flags_large_shift():
    reference = pd.DataFrame({"elo_delta": [0.0, 1.0, -1.0]})
    current = pd.DataFrame({"elo_delta": [20.0, 21.0, 19.0]})
    drift = feature_drift(reference, current, ["elo_delta"])
    assert "elo_delta" in drift_alerts(drift, threshold=2.0)
