import random
from datetime import datetime, timedelta

# Define baseline values clearly for each sensor
BASELINE_STATE = {
    "glucose_mg_dL": 90,
    "lactate_mmol_L": 1.0,
    "heart_rate_BPM": 65,
    "skin_temp_C": 34.5,
    "alcohol_BAC_pct": 0.0,
    "GSR_uS": 2.5,
}

# Sensor state now persists over time
current_state = BASELINE_STATE.copy()

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

historical_data = []

# Smoothly adjust towards target with decay
def smooth_adjust(current, target, adjustment_rate):
    return current + (target - current) * adjustment_rate

# Gradually revert to baseline when no events are active
def decay_to_baseline(state):
    decay_rates = {
        "glucose_mg_dL": 0.005,
        "lactate_mmol_L": 0.01,
        "heart_rate_BPM": 0.01,
        "skin_temp_C": 0.01,
        "GSR_uS": 0.01,
        "alcohol_BAC_pct": 0.02,
    }
    for sensor in state:
        state[sensor] = smooth_adjust(state[sensor], BASELINE_STATE[sensor], decay_rates[sensor])

def apply_event_effects(state, event, mins_since_event):
    intensity = 0
    if event["type"] == "meal" and 0 <= mins_since_event <= 120:
        intensity = (1 - mins_since_event / 120)
        target = BASELINE_STATE["glucose_mg_dL"] + 25
        state["glucose_mg_dL"] = smooth_adjust(state["glucose_mg_dL"], target, 0.1 * intensity)
    
    elif event["type"] == "exercise" and 0 <= mins_since_event <= 60:
        intensity = (1 - mins_since_event / 60)
        state["lactate_mmol_L"] = smooth_adjust(state["lactate_mmol_L"], BASELINE_STATE["lactate_mmol_L"] + 3, 0.2 * intensity)
        state["heart_rate_BPM"] = smooth_adjust(state["heart_rate_BPM"], BASELINE_STATE["heart_rate_BPM"] + 30, 0.2 * intensity)
        state["skin_temp_C"] = smooth_adjust(state["skin_temp_C"], BASELINE_STATE["skin_temp_C"] + 0.5, 0.1 * intensity)
    
    elif event["type"] == "sleep" and 0 <= mins_since_event <= 480:
        intensity = (mins_since_event / 480)
        state["heart_rate_BPM"] = smooth_adjust(state["heart_rate_BPM"], 55, 0.05 * intensity)
        state["GSR_uS"] = smooth_adjust(state["GSR_uS"], 1.8, 0.05 * intensity)
    
    elif event["type"] == "wake" and 0 <= mins_since_event <= 30:
        intensity = (1 - mins_since_event / 30)
        state["heart_rate_BPM"] = smooth_adjust(state["heart_rate_BPM"], BASELINE_STATE["heart_rate_BPM"] + 15, 0.2 * intensity)
        state["GSR_uS"] = smooth_adjust(state["GSR_uS"], BASELINE_STATE["GSR_uS"] + 1, 0.2 * intensity)
    
    elif event["type"] == "coffee" and 0 <= mins_since_event <= 60:
        intensity = (1 - mins_since_event / 60)
        state["heart_rate_BPM"] = smooth_adjust(state["heart_rate_BPM"], BASELINE_STATE["heart_rate_BPM"] + 10, 0.1 * intensity)
        state["GSR_uS"] = smooth_adjust(state["GSR_uS"], BASELINE_STATE["GSR_uS"] + 0.5, 0.1 * intensity)

def generate_sensor_data(timestamp):
    global current_state

    # Gradually decay to baseline each cycle
    decay_to_baseline(current_state)

    for event in events_timeline:
        event_time = datetime.utcnow() + timedelta(hours=event["hour_offset"])
        mins_since_event = (timestamp - event_time).total_seconds() / 60
        apply_event_effects(current_state, event, mins_since_event)

    # Ensure values remain realistic
    sensor_output = {
        "timestamp": timestamp.isoformat() + "Z",
        "biochemical": {
            "glucose_mg_dL": round(min(max(current_state["glucose_mg_dL"], 70), 150), 1),
            "lactate_mmol_L": round(min(max(current_state["lactate_mmol_L"], 0.5), 5), 2),
            "alcohol_BAC_pct": round(current_state["alcohol_BAC_pct"], 3),
        },
        "physiological": {
            "heart_rate_BPM": round(min(max(current_state["heart_rate_BPM"], 45), 120), 1),
            "skin_temp_C": round(min(max(current_state["skin_temp_C"], 33.0), 36.5), 2),
        },
        "environmental": {
            "GSR_uS": round(min(max(current_state["GSR_uS"], 1.0), 6.0), 2),
        },
    }

    return sensor_output

def generate_historical_data():
    historical_data.clear()
    global current_state
    current_state = BASELINE_STATE.copy()
    timestamp = datetime.utcnow() - timedelta(hours=24)
    for _ in range(17280):  # every 5 seconds for 24 hours
        historical_data.append(generate_sensor_data(timestamp))
        timestamp += timedelta(seconds=5)

generate_historical_data()
