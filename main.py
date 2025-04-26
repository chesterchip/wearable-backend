# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime

from sensors import generate_sensor_data, historical_data
from events import build_event_list

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Wearable backend running with 24h history and events!"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("▶ Client connected")

    # Build the events list at connect
    events_list = build_event_list()

    try:
        # 1) Send both sensor history and events
        await ws.send_json({
            "type": "historical",
            "data": historical_data,
            "events": events_list
        })

        # 2) Stream live updates every 5 seconds
        while True:
            now = datetime.utcnow()
            new_data = generate_sensor_data(now)
            historical_data.append(new_data)
            
            # Keep exactly 24h of data (17280 samples at 5s intervals)
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
