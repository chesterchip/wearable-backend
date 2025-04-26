# backend.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime, timedelta
import random
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# --- 1a) Define your events timeline up front
class Event(BaseModel):
    start: datetime
    end:   datetime
    category: str
    desc:     str
    color:    str

events: List[Event] = [
    Event(start=datetime.utcnow().replace(hour=12, minute=0) - timedelta(hours=24),
          end=  datetime.utcnow().replace(hour=12, minute=30) - timedelta(hours=24),
          category="Eating & Drinking", desc="Lunch",        color="#4caf50"),
    Event(start=datetime.utcnow().replace(hour=17, minute=30) - timedelta(hours=24),
          end=  datetime.utcnow().replace(hour=18, minute=0)  - timedelta(hours=24),
          category="Exercise",          desc="Gym",          color="#ff9800"),
    Event(start=datetime.utcnow().replace(hour=8, minute=45)  - timedelta(hours=24),
          end=  datetime.utcnow().replace(hour=9, minute=0)   - timedelta(hours=24),
          category="Caffeine",         desc="Coffee",       color="#4caf50"),
    Event(start=datetime.utcnow().replace(hour=22, minute=30) - timedelta(hours=24),
          end=  datetime.utcnow().replace(hour=23, minute=30) - timedelta(hours=24),
          category="Sleep",            desc="Night Sleep",  color="#9fa8da"),
]

# --- 1b) Simulate your generators
historical_data: List[Dict] = []
sensor_state = {
    "glucose":    90.0,
    "lactate":    1.0,
    "heart_rate": 65.0,
    "skin_temp":  34.5,
    "GSR":        2.5,
}
def random_walk(v, low, high, step=0.5):
    return max(low, min(high, v + random.uniform(-step, step)))

def generate_point(ts: datetime):
    # gently decay toward baseline between events...
    sensor_state["glucose"]    = random_walk(sensor_state["glucose"],    80, 110, 0.3)
    sensor_state["lactate"]    = random_walk(sensor_state["lactate"],    0.5, 5,    0.05)
    sensor_state["heart_rate"] = random_walk(sensor_state["heart_rate"], 45, 120, 0.5)
    sensor_state["skin_temp"]  = random_walk(sensor_state["skin_temp"],  33,  37,  0.05)
    sensor_state["GSR"]        = random_walk(sensor_state["GSR"],        1,   6,   0.1)

    return {
        "timestamp": ts.isoformat() + "Z",
        "sensor": { **sensor_state },
        "active_events": []
    }

def make_history():
    historical_data.clear()
    t0 = datetime.utcnow() - timedelta(hours=24)
    for _ in range(24 * 60 * 12):  # 5-second steps in 24h
        historical_data.append(generate_point(t0))
        t0 += timedelta(seconds=5)

make_history()


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()

    # 2) on connect, send your three payloads in order
    await ws.send_json({ "type": "events",     "data": [e.dict() for e in events] })
    await ws.send_json({ "type": "historical", "data": historical_data })

    try:
        while True:
            await asyncio.sleep(5)
            pt = generate_point(datetime.utcnow())
            historical_data.append(pt)
            if len(historical_data) > 24*60*12:  # keep 24h worth
                historical_data.pop(0)
            await ws.send_json({ "type": "live", "data": pt })
    except WebSocketDisconnect:
        print("Client disconnected")
