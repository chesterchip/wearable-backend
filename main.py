# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from sensors import generate_sensor_data, historical_data

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        # 1) Send full history immediately
        await ws.send_json({"type": "historical", "data": historical_data})

        # 2) Then stream one new data point every 5 seconds
        while True:
            point = generate_sensor_data()
            historical_data.append(point)
            if len(historical_data) > 1440:
                historical_data.pop(0)
            await ws.send_json({"type": "live", "data": point})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected")
