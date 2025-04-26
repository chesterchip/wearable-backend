# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime, timedelta

app = FastAPI()

#
# — your existing sensor‐generation machinery —
#
from sensors import generate_sensor_data, historical_data, events_timeline

# events_timeline is assumed to be a list of dicts like:
#   {"hour_offset": -20, "type": "exercise", "desc": "Gym", "color": "#ffcc80", ...}
# and historical_data is your 24 h sample generated at startup.

@app.get("/")
async def root():
    return {"status": "Wearable backend running with 24h history!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # 1) Immediately send your static events timeline, with real start/end timestamps:
    now = datetime.utcnow()
    events_payload = []
    for e in events_timeline:
        start = now + timedelta(hours=e["hour_offset"])
        # assume each event lasts 1 hour if no explicit duration:
        end   = start + timedelta(hours=e.get("duration_h", 1))
        events_payload.append({
            "desc":     e["desc"],
            "category": e["type"],
            "color":    e["color"],
            "start":    start.isoformat() + "Z",
            "end":      end.isoformat() + "Z"
        })

    await websocket.send_json({
        "type": "events",
        "data": events_payload
    })

    # 2) Then send the full 24 h history
    await websocket.send_json({
        "type": "historical",
        "data": historical_data
    })

    # 3) And stream live updates
    try:
        while True:
            new_data = generate_sensor_data()
            historical_data.append(new_data)
            if len(historical_data) > 1440:
                historical_data.pop(0)

            await websocket.send_json({
                "type": "live",
                "data": new_data
            })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected.")
