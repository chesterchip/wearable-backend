# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from sensors import generate_sensor_data, historical_sensor_data
from device_status import generate_device_status, historical_device_status

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Wearable backend running with simulated data!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_json({
            "type": "historical",
            "data": {
                "sensor_data": historical_sensor_data,
                "device_status": historical_device_status
            }
        })
        while True:
            sensor_data = generate_sensor_data()
            device_status = generate_device_status()

            historical_sensor_data.append(sensor_data)
            historical_device_status.append(device_status)

            if len(historical_sensor_data) > 1440:
                historical_sensor_data.pop(0)
            if len(historical_device_status) > 1440:
                historical_device_status.pop(0)

            await websocket.send_json({
                "type": "live",
                "data": {
                    "sensor_data": sensor_data,
                    "device_status": device_status
                }
            })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected.")
