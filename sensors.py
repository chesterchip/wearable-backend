import random
from datetime import datetime, timedelta

sensor_state = {
    "glucose_mg_dL": 100,
    "lactate_mmol_L": 1.0,
    "ketones_mmol_L": 0.2,
    "proteins_g_dL": 7.0,
    "alcohol_BAC_pct": 0.0,
    "urea_mg_dL": 14,
    "heart_rate_BPM": 65,
    "skin_temp_C": 34.5,
}

historical_data = []

def random_walk(value, min_val, max_val, step):
    return max(min_val, min(max_val, value + random.uniform(-step, step)))

def generate_sensor_data(timestamp=None):
    if not timestamp:
        timestamp = datetime.utcnow().isoformat() + "Z"

    sensor_state["glucose_mg_dL"] = random_walk(sensor_state["glucose_mg_dL"], 80, 140, 1.0)
    sensor_state["lactate_mmol_L"] = random_walk(sensor_state["lactate_mmol_L"], 0.5, 2.0, 0.05)
    sensor_state["ketones_mmol_L"] = random_walk(sensor_state["ketones_mmol_L"], 0.1, 0.4, 0.01)
    sensor_state["proteins_g_dL"] = random_walk(sensor_state["proteins_g_dL"], 6.5, 7.5, 0.02)
    sensor_state["alcohol_BAC_pct"] = max(sensor_state["alcohol_BAC_pct"] - 0.00005, 0.0)
    sensor_state["urea_mg_dL"] = random_walk(sensor_state["urea_mg_dL"], 12, 18, 0.1)
    sensor_state["heart_rate_BPM"] = random_walk(sensor_state["heart_rate_BPM"], 60, 80, 1.0)
    sensor_state["skin_temp_C"] = random_walk(sensor_state["skin_temp_C"], 33.5, 35.5, 0.05)

    data = {
        "timestamp": timestamp,
        "biochemical": {
            "glucose_mg_dL": round(sensor_state["glucose_mg_dL"], 1),
            "lactate_mmol_L": round(sensor_state["lactate_mmol_L"], 2),
            "ketones_mmol_L": round(sensor_state["ketones_mmol_L"], 2),
            "proteins_g_dL": round(sensor_state["proteins_g_dL"], 2),
            "alcohol_BAC_pct": round(sensor_state["alcohol_BAC_pct"], 4),
            "urea_mg_dL": round(sensor_state["urea_mg_dL"], 1),
        },
        "physiological": {
            "heart_rate_BPM": round(sensor_state["heart_rate_BPM"], 1),
            "skin_temp_C": round(sensor_state["skin_temp_C"], 2),
        },
    }

    return data

def generate_historical_data():
    global historical_data
    historical_data.clear()

    now = datetime.utcnow()
    sensor_state.update({
        "glucose_mg_dL": 100,
        "lactate_mmol_L": 1.0,
        "ketones_mmol_L": 0.2,
        "proteins_g_dL": 7.0,
        "alcohol_BAC_pct": 0.0,
        "urea_mg_dL": 14,
        "heart_rate_BPM": 65,
        "skin_temp_C": 34.5,
    })

    for mins_ago in reversed(range(1440)):  # 1440 minutes = 24 hours
        timestamp = (now - timedelta(minutes=mins_ago)).isoformat() + "Z"
        data = generate_sensor_data(timestamp=timestamp)
        historical_data.append(data)

# Generate initial historical data once at startup
generate_historical_data()
