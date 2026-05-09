import asyncio

import websockets

SERVER_URL = "ws://localhost:8000/ws"


async def receive_messages(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(f"\nBroadcast: {message}")
        except websockets.ConnectionClosed:
            print("Connection closed")
            break


async def send_messages(websocket):
    while True:
        message = await asyncio.to_thread(input, "You: ")
        await websocket.send(message)


async def main():
    async with websockets.connect(
        SERVER_URL, ping_interval=20, ping_timeout=20
    ) as websocket:
        receive_task = asyncio.create_task(receive_messages(websocket))
        send_task = asyncio.create_task(send_messages(websocket))

        await asyncio.gather(receive_task, send_task)


if __name__ == "__main__":
    asyncio.run(main())
