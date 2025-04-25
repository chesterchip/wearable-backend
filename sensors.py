import random
from datetime import datetime, timedelta

events_timeline = [
    {"hour_offset": -24, "type": "meal", "desc": "Lunch"},
    {"hour_offset": -20, "type": "exercise", "desc": "Yoga/Gym"},
    {"hour_offset": -18, "type": "meal", "desc": "Dinner"},
    {"hour_offset": -16, "type": "exercise", "desc": "Evening Walk"},
    {"hour_offset": -13, "type": "sleep", "desc": "Bedtime"},
    {"hour_offset": -5,  "type": "wake", "desc": "Wake Up"},
    {"hour_offset": -3,  "type": "coffee", "desc": "Coffee"},
    {"hour_offset": -2,  "type": "meal", "desc": "Breakfast"},
]

sensor_state = {
    "glucose_mg_dL": 90, "lactate_mmol_L": 1.0, "heart_rate_BPM": 65,
    "skin_temp_C": 34.5, "alcohol_BAC_pct": 0.0, "GSR_uS": 2.5,
}

historical_data = []

def apply_event_effects(sensor_state, event, mins_since_event):
    if event["type"] == "meal":
        if 0 <= mins_since_event <= 60:
            sensor_state["glucose_mg_dL"] += random.uniform(15, 30) * (1 - mins_since_event / 60)
    elif event["type"] == "exercise":
        if 0 <= mins_since_event <= 45:
            sensor_state["lactate_mmol_L"] += random.uniform(1, 5) * (1 - mins_since_event / 45)
            sensor_state["heart_rate_BPM"] += random.uniform(10, 30) * (1 - mins_since_event / 45)
            sensor_state["skin_temp_C"] += random.uniform(0.1, 0.5) * (1 - mins_since_event / 45)
    elif event["type"] == "sleep":
        if mins_since_event >= 0:
            sensor_state["heart_rate_BPM"] = max(50, sensor_state["heart_rate_BPM"] - 0.02 * mins_since_event)
            sensor_state["GSR_uS"] = max(1.5, sensor_state["GSR_uS"] - 0.005 * mins_since_event)
    elif event["type"] == "wake":
        if 0 <= mins_since_event <= 30:
            sensor_state["heart_rate_BPM"] += random.uniform(5, 15) * (1 - mins_since_event / 30)
            sensor_state["GSR_uS"] += random.uniform(0.5, 1.5) * (1 - mins_since_event / 30)
    elif event["type"] == "coffee":
        if 0 <= mins_since_event <= 60:
            sensor_state["heart_rate_BPM"] += random.uniform(5, 10) * (1 - mins_since_event / 60)
            sensor_state["GSR_uS"] += random.uniform(0.2, 0.8) * (1 - mins_since_event / 60)

def generate_sensor_data(timestamp):
    state_copy = sensor_state.copy()

    for event in events_timeline:
        event_time = datetime.utcnow() + timedelta(hours=event["hour_offset"])
        mins_since_event = (timestamp - event_time).total_seconds() / 60
        apply_event_effects(state_copy, event, mins_since_event)

    # Keep values within realistic ranges
    state_copy["glucose_mg_dL"] = min(max(state_copy["glucose_mg_dL"], 70), 150)
    state_copy["lactate_mmol_L"] = min(max(state_copy["lactate_mmol_L"], 0.5), 5)
    state_copy["heart_rate_BPM"] = min(max(state_copy["heart_rate_BPM"], 45), 120)
    state_copy["skin_temp_C"] = min(max(state_copy["skin_temp_C"], 33.0), 36.5)
    state_copy["GSR_uS"] = min(max(state_copy["GSR_uS"], 1.0), 6.0)

    return {
        "timestamp": timestamp.isoformat() + "Z",
        "biochemical": {
            "glucose_mg_dL": round(state_copy["glucose_mg_dL"], 1),
            "lactate_mmol_L": round(state_copy["lactate_mmol_L"], 2),
            "alcohol_BAC_pct": round(state_copy["alcohol_BAC_pct"], 3),
        },
        "physiological": {
            "heart_rate_BPM": round(state_copy["heart_rate_BPM"], 1),
            "skin_temp_C": round(state_copy["skin_temp_C"], 2),
        },
        "environmental": {
            "GSR_uS": round(state_copy["GSR_uS"], 2),
        },
    }

def generate_historical_data():
    historical_data.clear()
    now = datetime.utcnow() - timedelta(hours=24)
    for _ in range(17280):  # every 5s for 24h
        historical_data.append(generate_sensor_data(now))
        now += timedelta(seconds=5)

generate_historical_data()
