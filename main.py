# main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import random
from datetime import datetime, timedelta

app = FastAPI()

#
# 1) Define your “real” events timeline
#
events_timeline = [
    {"hour_offset": -24, "type": "meal",      "desc": "Breakfast"},
    {"hour_offset": -20, "type": "exercise",  "desc": "Morning Run"},
    {"hour_offset": -18, "type": "coffee",    "desc": "Coffee"},
    {"hour_offset": -12, "type": "meal",      "desc": "Lunch"},
    {"hour_offset": -8,  "type": "exercise",  "desc": "Afternoon Gym"},
    {"hour_offset": -6,  "type": "caffeine",  "desc": "Afternoon Coffee"},
    {"hour_offset": -4,  "type": "meal",      "desc": "Dinner"},
    {"hour_offset": -2,  "type": "sleep",     "desc": "Night Sleep"},
]

#
# 2) Historical data store
#
historical_data = []

#
# 3) Sensor state + generators
#
BASELINE = {
    "glucose_mg_dL":   90,
    "lactate_mmol_L":  1.0,
    "heart_rate_BPM":  65,
    "skin_temp_C":    34.5,
    "GSR_uS":          2.5,
}
current_state = BASELINE.copy()

def smooth_adj(cur, tgt, rate):
    return cur + (tgt - cur)*rate

def decay_to_baseline(state):
    rates = {
        "glucose_mg_dL":  0.002, "lactate_mmol_L": 0.005,
        "heart_rate_BPM": 0.005, "skin_temp_C":  0.005,
        "GSR_uS":         0.005,
    }
    for k,r in rates.items():
        state[k] = smooth_adj(state[k], BASELINE[k], r)

def apply_event(state, evt, mins):
    if evt["type"]=="meal" and 0<=mins<=120:
        rate = (1-mins/120)*0.1
        state["glucose_mg_dL"] = smooth_adj(state["glucose_mg_dL"], BASELINE["glucose_mg_dL"]+25, rate)
    if evt["type"]=="exercise" and 0<=mins<=60:
        rate = (1-mins/60)*0.2
        state["heart_rate_BPM"] = smooth_adj(state["heart_rate_BPM"], BASELINE["heart_rate_BPM"]+30, rate)
        state["lactate_mmol_L"] = smooth_adj(state["lactate_mmol_L"], BASELINE["lactate_mmol_L"]+3, rate)
    if evt["type"]=="coffee" and 0<=mins<=30:
        rate = (1-mins/30)*0.1
        state["heart_rate_BPM"] = smooth_adj(state["heart_rate_BPM"], BASELINE["heart_rate_BPM"]+10, rate)
    if evt["type"]=="sleep" and 0<=mins<=480:
        rate = (mins/480)*0.05
        state["heart_rate_BPM"] = smooth_adj(state["heart_rate_BPM"], 55, rate)
        state["GSR_uS"]         = smooth_adj(state["GSR_uS"], 1.8, rate)

def generate_sensor_data(ts: datetime):
    global current_state
    decay_to_baseline(current_state)
    for evt in events_timeline:
        evt_time = datetime.utcnow() + timedelta(hours=evt["hour_offset"])
        mins_since = (ts - evt_time).total_seconds()/60
        apply_event(current_state, evt, mins_since)

    # clamp & round
    out = {
        "timestamp": ts.isoformat() + "Z",
        "biochemical": {
            "glucose_mg_dL":  round(max(70,min(150, current_state["glucose_mg_dL"])),1),
            "lactate_mmol_L": round(max(0.5,min(5,   current_state["lactate_mmol_L"])),2),
        },
        "physiological": {
            "heart_rate_BPM": round(max(45,min(120, current_state["heart_rate_BPM"])),1),
            "skin_temp_C":    round(max(33,min(36.5,  current_state["skin_temp_C"])),2),
        },
        "environmental": {
            "GSR_uS": round(max(1,min(6, current_state["GSR_uS"])),2),
        },
    }
    return out

def generate_historical_data():
    historical_data.clear()
    t0 = datetime.utcnow() - timedelta(hours=24)
    for i in range(int(24*60*60/5)):
        dp = generate_sensor_data(t0)
        historical_data.append(dp)
        t0 += timedelta(seconds=5)

# pre-fill
generate_historical_data()

#
# 4) WebSocket endpoint
#
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("▶ Client connected")
    try:
        # send history + events
        await ws.send_json({
            "type": "historical",
            "data": historical_data,
            "events": events_timeline
        })

        # now live updates every 5s
        while True:
            new_dp = generate_sensor_data(datetime.utcnow())
            historical_data.append(new_dp)
            if len(historical_data)>1440:  # keep 24h @5s = 17280 points, or adjust as needed
                historical_data.pop(0)

            await ws.send_json({"type":"live", "data": new_dp})
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print("⏹ Client disconnected cleanly")
    except Exception as e:
        import traceback; traceback.print_exc()
        print("⚠️ WebSocket error:", e)
    finally:
        print("🔥 WebSocket handler done")

@app.get("/")
async def root():
    return {"status": "Wearable backend with 24h history + events!"}
