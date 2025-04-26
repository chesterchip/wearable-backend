# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

from sensors import historical_data, generate_sensor_data, generate_historical_data
from events import events

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # build 24h of history on startup
    generate_historical_data()

@app.get("/")
async def root():
    return {"status": "Wearable backend running with 24h history!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # send the full 24h history once
        await websocket.send_json({
            "type": "historical",
            "data": historical_data,
            "events": events,               # include your events here too
        })

        # then stream live updates
        while True:
            new_point = generate_sensor_data()
            historical_data.append(new_point)
            # keep exactly 24h (if you generate every 5s, that's ~17k points)
            if len(historical_data) > 17280:
                historical_data.pop(0)

            await websocket.send_json({
                "type": "live",
                "data": new_point,
                "active_events": [
                    e for e in events
                    if e["start"] <= new_point["timestamp"] <= e["end"]
                ]
            })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected.")
