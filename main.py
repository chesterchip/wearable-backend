# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("▶ Client connected")
    try:
        # A single ping so you can test immediately
        await ws.send_json({"type":"ping","msg":"hello"})
        while True:
            # every 5 seconds send a timestamp
            await ws.send_json({"type":"live", "now": __import__("time").time()})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("⏹ Client disconnected cleanly")
    except Exception as e:
        # catch everything so you can see the stack
        import traceback; traceback.print_exc()
        print("⚠️  WebSocket error:", e)
    finally:
        print("🔥 WebSocket handler shutting down")

@app.get("/")
async def root():
    return {"status":"ok"}
