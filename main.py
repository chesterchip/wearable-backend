import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from sensors import generate_sensor_data

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Wearable backend is live!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = generate_sensor_data()
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
