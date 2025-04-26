# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime, timedelta

from sensors import generate_sensor_data, historical_data, events_timeline
# └─> assume events_timeline is your list of
#     { "hour_offset": …, "type": …, "desc": …, "color": …, "duration_h"?: … }

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Wearable backend running with 24h history!"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    # Build a one‐off events array with real ISO timestamps:
    now = datetime.utcnow()
    evs = []
    for e in events_timeline:
        start = now + timedelta(hours=e["hour_offset"])
        dur   = timedelta(hours=e.get("duration_h", 1))
        evs.append({
            "desc":     e["desc"],
            "category": e["type"],
            "color":    e["color"],
            "start":    start.isoformat() + "Z",
            "end":      (start + dur).isoformat() + "Z",
        })

    # Send **one** combined “historical” message that carries BOTH
    #  • your 24h of samples
    #  • your events timeline
    await ws.send_json({
        "type":   "historical",
        "data":   historical_data,
        "events": evs
    })

    # Now the exact same live‐stream loop you already had
    try:
        while True:
            new = generate_sensor_data()
            historical_data.append(new)
            if len(historical_data) > 1440:
                historical_data.pop(0)

            await ws.send_json({ "type": "live", "data": new })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected.")
