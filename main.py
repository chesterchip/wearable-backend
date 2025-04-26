from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from sensors import generate_sensor_data, generate_historical_data, historical_data
from datetime import datetime

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Build 24h of history at server start
    generate_historical_data()
    print(f"[{datetime.utcnow().isoformat()}] Historical data generated, {len(historical_data)} points")

@app.get("/")
async def root():
    return {"status": "Wearable backend running with 24h history!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"[{datetime.utcnow().isoformat()}] Client connected")
    try:
        # 1) Send the full historical dump
        await websocket.send_json({"type": "historical", "data": {
            "sensor": historical_data,
            # if you have an events_timeline to share, include it here:
            # "events": events_timeline
        }})
        print(f"[{datetime.utcnow().isoformat()}] Sent historical")

        # 2) Now stream live points every 5s
        while True:
            now = datetime.utcnow()
            new_data = generate_sensor_data(now)
            historical_data.append(new_data)

            # keep at most 24h @ 5s => 17280 points
            if len(historical_data) > 17280:
                historical_data.pop(0)

            await websocket.send_json({"type": "live", "data": new_data})
            print(f"[{now.isoformat()}] Sent live")
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print(f"[{datetime.utcnow().isoformat()}] Client disconnected")
    except Exception as err:
        # catch any other error so you can inspect it
        print(f"[{datetime.utcnow().isoformat()}] ERROR in websocket loop:", err)
        await websocket.close()
