import random
from datetime import datetime, timedelta

# --- baseline & state ----------------------------------------------------
BASELINE_STATE = {
    "glucose_mg_dL": 90,
    "lactate_mmol_L": 1.0,
    "heart_rate_BPM": 65,
    "skin_temp_C": 34.5,
    "GSR_uS": 2.5,
}
current_state = BASELINE_STATE.copy()

# define your events here if you also want to share them to the client
events_timeline = [
    # {"hour_offset": ..., "type": "...", "desc": "..."},
]

historical_data = []

def smooth_adjust(current, target, rate):
    return current + (target - current) * rate

def decay_to_baseline(state):
    rates = {
        "glucose_mg_dL": 0.005,
        "lactate_mmol_L": 0.01,
        "heart_rate_BPM": 0.01,
        "skin_temp_C": 0.01,
        "GSR_uS": 0.01,
    }
    for k, r in rates.items():
        state[k] = smooth_adjust(state[k], BASELINE_STATE[k], r)

def apply_event_effects(state, event, mins_since):
    # ... your existing logic ...
    pass

def generate_sensor_data(timestamp: datetime):
    global current_state

    # 1) decay
    decay_to_baseline(current_state)

    # 2) apply events if you want
    for ev in events_timeline:
        ev_time = datetime.utcnow() + timedelta(hours=ev["hour_offset"])
        mins = (timestamp - ev_time).total_seconds() / 60
        apply_event_effects(current_state, ev, mins)

    # 3) clamp & package
    out = {
        "timestamp": timestamp.isoformat() + "Z",
        "biochemical": {
            "glucose_mg_dL": round(min(max(current_state["glucose_mg_dL"], 70), 150), 1),
            "lactate_mmol_L": round(min(max(current_state["lactate_mmol_L"], 0.5), 5), 2),
        },
        "physiological": {
            "heart_rate_BPM": round(min(max(current_state["heart_rate_BPM"], 45), 120), 1),
            "skin_temp_C": round(min(max(current_state["skin_temp_C"], 33), 36.5), 2),
        },
        "environmental": {
            "GSR_uS": round(min(max(current_state["GSR_uS"], 1), 6), 2)
        }
    }
    return out

def generate_historical_data():
    historical_data.clear()
    global current_state
    current_state = BASELINE_STATE.copy()
    t = datetime.utcnow() - timedelta(hours=24)
    for _ in range(17280):  # 24h at 5s intervals
        historical_data.append(generate_sensor_data(t))
        t += timedelta(seconds=5)
