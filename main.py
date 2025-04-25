from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from sensors import generate_sensor_data

app = FastAPI()

connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # Receive event trigger from client if any (optional)
            event = await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
            data = generate_sensor_data(event=event)
            await websocket.send_json(data)
            await asyncio.sleep(1)  # Update every second
    except asyncio.TimeoutError:
        # No message received, keep streaming normal data
        while True:
            data = generate_sensor_data()
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)