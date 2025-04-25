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
        # Immediately send historical data upon connection
        await websocket.send_json({"type": "historical", "data": historical_data})

        # Stream new live data every few seconds
        while True:
            new_data = generate_sensor_data()
            historical_data.append(new_data)

            # Keep exactly 24h of data
            if len(historical_data) > 1440:
                historical_data.pop(0)

            await websocket.send_json({"type": "live", "data": new_data})
            await asyncio.sleep(5)  # adjust this timing if needed
    except WebSocketDisconnect:
        print("Client disconnected.")
