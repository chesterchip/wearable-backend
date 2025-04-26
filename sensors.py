# sensors.py
import random
from datetime import datetime, timedelta

# baseline values
BASELINE = {
    "glucose_mg_dL": 90,
    "lactate_mmol_L": 1.0,
    "heart_rate_BPM": 65,
    "skin_temp_C": 34.5,
    "GSR_uS": 2.5,
}

# stored history
historical_data = []
# persistent state
current = BASELINE.copy()

def smooth(val, target, rate):
    return val + (target - val) * rate

def decay_toward_baseline():
    rates = {
        "glucose_mg_dL": 0.002,
        "lactate_mmol_L": 0.01,
        "heart_rate_BPM": 0.01,
        "skin_temp_C": 0.005,
        "GSR_uS": 0.01,
    }
    for k, base in BASELINE.items():
        current[k] = smooth(current[k], base, rates[k])

def generate_sensor_data(timestamp=None):
    if not timestamp:
        timestamp = datetime.utcnow()
    else:
        # parse iso string
        timestamp = datetime.fromisoformat(timestamp.rstrip("Z"))

    # apply slow decay
    decay_toward_baseline()

    # tiny random walk
    for k in current:
        step = {"glucose_mg_dL":1.0,"lactate_mmol_L":0.02,"heart_rate_BPM":1.0,
                "skin_temp_C":0.02,"GSR_uS":0.05}[k]
        current[k] += random.uniform(-step, step)
        # clamp
        if k == "glucose_mg_dL":
            current[k] = max(70, min(150, current[k]))
        if k == "lactate_mmol_L":
            current[k] = max(0.5, min(5.0, current[k]))
        if k == "heart_rate_BPM":
            current[k] = max(45, min(120, current[k]))
        if k == "skin_temp_C":
            current[k] = max(33, min(37, current[k]))
        if k == "GSR_uS":
            current[k] = max(1.0, min(6.0, current[k]))

    point = {
        "timestamp": timestamp.isoformat() + "Z",
        "sensor": {
            "glucose":    round(current["glucose_mg_dL"], 1),
            "lactate":    round(current["lactate_mmol_L"], 2),
            "heart_rate": round(current["heart_rate_BPM"], 1),
            "skin_temp":  round(current["skin_temp_C"], 2),
            "gsr":        round(current["GSR_uS"], 2),
        }
    }
    return point

def generate_historical_data():
    historical_data.clear()
    # start 24h ago, step by 5s
    t = datetime.utcnow() - timedelta(hours=24)
    for _ in range(17280):
        historical_data.append(generate_sensor_data(t.isoformat()+"Z"))
        t += timedelta(seconds=5)
