# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from sensors import generate_sensor_data, historical_data

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Wearable backend running with 24h history!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_json({"type": "historical", "data": historical_data})
        while True:
            new_data = generate_sensor_data()
            historical_data.append(new_data)
            if len(historical_data) > 1440:
                historical_data.pop(0)
            await websocket.send_json({"type": "live", "data": new_data})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected.")
