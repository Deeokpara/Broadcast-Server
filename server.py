import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

clients = {}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Ask for username
    await websocket.send_text("Enter your username:")
    username = await websocket.receive_text()

    clients[websocket] = username

    print(f"{username} connected")

    try:
        while True:
            message = await websocket.receive_text()

            print(f"{username}: {message}")

            disconnected = []

            for client in clients.keys():
                try:
                    await client.send_text(f"{username}: {message}")
                except:
                    disconnected.append(client)

            for dc in disconnected:
                del clients[dc]

    except WebSocketDisconnect:
        print(f"{username} disconnected")

        if websocket in clients:
            del clients[websocket]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ws_ping_interval=20, ws_ping_timeout=20)
