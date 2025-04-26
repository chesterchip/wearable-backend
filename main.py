# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime, timedelta

from sensors import generate_sensor_data, historical_data, events_timeline
from events import build_event_list

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Wearable backend running with 24h history + events!"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("▶ Client connected")

    # Build your events list (with ISO‐strings inside build_event_list)
    events_list = build_event_list()

    try:
        # Send BOTH your 24h of samples and the event blocks in one payload:
        await ws.send_json({
            "type":   "historical",
            "data":   historical_data,
            "events": events_list
        })

        # Now stream live samples forever
        while True:
            # <-- NOTE: no timestamp argument! sensors.generate_sensor_data()  
            # will create its own ISO‐string timestamp internally.
            new_data = generate_sensor_data()
            historical_data.append(new_data)

            # keep 24h of data
            if len(historical_data) > 17280:
                historical_data.pop(0)

            await ws.send_json({"type": "live", "data": new_data})
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print("⏹ Client disconnected cleanly")
    except Exception as e:
        import traceback; traceback.print_exc()
        print("⚠️ WebSocket error:", e)
    finally:
        print("🔥 WebSocket handler done")
