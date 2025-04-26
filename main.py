# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from sensors import generate_historical_data, historical_data, generate_live_data

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Wearable backend running with 24h history!"}

# prepare 24 h of smoothed historical data at startup
generate_historical_data()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # 1) send full 24 h history immediately
        await websocket.send_json({"type": "historical", "data": historical_data})

        # 2) then stream live readings every 5 s
        while True:
            new_point = generate_live_data()
            historical_data.append(new_point)
            # keep exactly 24 h worth at 5 s intervals = 24*3600/5 = 17280 points
            if len(historical_data) > 17280:
                historical_data.pop(0)
            await websocket.send_json({"type": "live", "data": new_point})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected.")
