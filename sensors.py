# backend/sensors.py
import random, math
from datetime import datetime, timedelta

# 1) a simple circadian‐rhythm modifier
def circadian_modulation(ts: datetime):
    # ts.hour → seconds since midnight
    secs = ts.hour*3600 + ts.minute*60 + ts.second
    phase = (secs / 86400.0) * 2*math.pi
    # body temp swings ±0.5°C, lowest ~4 AM, highest ~4 PM
    temp_mod = 0.5 * math.sin(phase - math.pi/2)
    # heart rate swings ±5 BPM, peak midday
    hr_mod = 5 * math.sin(phase)
    return temp_mod, hr_mod

# 2) your event timeline, now recorded as absolute datetimes
raw_events = [
    {"hour_offset": -20, "type": "meal",      "desc": "Lunch"},
    {"hour_offset": -18, "type": "exercise",  "desc": "Yoga/Gym"},
    {"hour_offset": -16, "type": "meal",      "desc": "Dinner"},
    {"hour_offset": -14, "type": "exercise",  "desc": "Evening Walk"},
    {"hour_offset": -12, "type": "sleep",     "desc": "Light Sleep"},  # will nest deeper
    {"hour_offset": -8,  "type": "sleep_deep","desc": "Deep Sleep"},
    {"hour_offset": -6,  "type": "sleep_rem", "desc": "REM Sleep"},
    {"hour_offset": -5,  "type": "meal",      "desc": "Breakfast"},
    {"hour_offset": -4,  "type": "caffeine",  "desc": "Coffee"},
]
# convert into absolute datetimes at module load
now = datetime.utcnow()
events = []
for e in raw_events:
    start = now + timedelta(hours=e["hour_offset"])
    # assume fixed durations
    if e["type"] == "meal":       end = start + timedelta(minutes=30)
    elif e["type"] == "exercise": end = start + timedelta(minutes=45)
    elif e["type"].startswith("sleep"): end = start + timedelta(hours=1.5)
    elif e["type"] == "caffeine": end = start + timedelta(minutes=15)
    else:                         end = start + timedelta(minutes=15)
    events.append({
        "start": start,
        "end":   end,
        "type":  e["type"],
        "desc":  e["desc"]
    })

# 3) baseline and mutable current state
BASELINE = {
    "glucose_mg_dL":  90,   "lactate_mmol_L": 1.0,
    "heart_rate_BPM": 65,   "skin_temp_C":    34.5,
    "GSR_uS":         2.5
}
current_state = BASELINE.copy()

historical_data = []

def smooth(current, target, rate):
    return current + (target - current)*rate

def apply_event_effects(state, event, minutes_since):
    # only consider if within event window
    if not (0 <= minutes_since <= (event["end"]-event["start"]).total_seconds()/60):
        return
    frac = minutes_since / ((event["end"]-event["start"]).total_seconds()/60)
    if event["type"] == "meal":
        # glycemic rise then fall: peak at mid‐meal
        peak = BASELINE["glucose_mg_dL"] + 30
        target = peak if frac < 0.5 else BASELINE["glucose_mg_dL"]
        rate   = 0.2
        state["glucose_mg_dL"] = smooth(state["glucose_mg_dL"], target, rate)
    elif event["type"] == "exercise":
        targetL = BASELINE["lactate_mmol_L"]+3
        targetH = BASELINE["heart_rate_BPM"]+30
        state["lactate_mmol_L"]   = smooth(state["lactate_mmol_L"],   targetL, 0.3)
        state["heart_rate_BPM"]   = smooth(state["heart_rate_BPM"],   targetH, 0.3)
    elif event["type"] == "sleep_deep":
        state["heart_rate_BPM"] = smooth(state["heart_rate_BPM"],  55,   0.05)
        state["GSR_uS"]         = smooth(state["GSR_uS"],          1.8,  0.05)
    elif event["type"] == "sleep_rem":
        state["heart_rate_BPM"] = smooth(state["heart_rate_BPM"],  60,   0.02)
        state["skin_temp_C"]    = smooth(state["skin_temp_C"],     BASELINE["skin_temp_C"], 0.02)
    elif event["type"] == "caffeine":
        state["heart_rate_BPM"] = smooth(state["heart_rate_BPM"], BASELINE["heart_rate_BPM"]+10, 0.2)

def decay_to_baseline(state):
    for k,v in BASELINE.items():
        state[k] = smooth(state[k], v, 0.01)

def generate_sensor_point(dt: datetime):
    global current_state
    # 1) circadian
    temp_mod, hr_mod = circadian_modulation(dt)
    current_state["skin_temp_C"] = BASELINE["skin_temp_C"] + temp_mod
    current_state["heart_rate_BPM"] = BASELINE["heart_rate_BPM"] + hr_mod

    # 2) decay + event effects
    decay_to_baseline(current_state)
    for ev in events:
        mins = (dt - ev["start"]).total_seconds()/60
        apply_event_effects(current_state, ev, mins)

    # 3) clamp + add tiny noise
    out = {
        "timestamp": dt.isoformat()+"Z",
        "biochemical": {
            "glucose_mg_dL": round(max(70, min(150, current_state["glucose_mg_dL"] + random.uniform(-1,1))),1),
            "lactate_mmol_L": round(max(0.5, min(5.0,  current_state["lactate_mmol_L"] + random.uniform(-0.1,0.1))),2),
        },
        "physiological": {
            "heart_rate_BPM": round(max(45, min(120, current_state["heart_rate_BPM"] + random.uniform(-2,2))),1),
            "skin_temp_C":    round(max(33, min(36.5, current_state["skin_temp_C"] + random.uniform(-0.2,0.2))),2),
        },
        "environmental": {
            "GSR_uS":         round(max(1, min(6, current_state["GSR_uS"] + random.uniform(-0.1,0.1))),2),
        }
    }
    return out

def generate_historical_data():
    """Replays 24h in 5s steps, so live picks up seamlessly."""
    historical_data.clear()
    start = datetime.utcnow() - timedelta(hours=24)
    t = start
    while t <= datetime.utcnow():
        historical_data.append(generate_sensor_point(t))
        t += timedelta(seconds=5)

def generate_live_data():
    """Called every 5s for a new reading."""
    return generate_sensor_point(datetime.utcnow())
