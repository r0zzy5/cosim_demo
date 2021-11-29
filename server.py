import asyncio
import websockets
import json
import random
import os
import sys

OBJECTS = {}
VIEWERS = set()
dt = 1/20

async def handler(websocket, path):
    message = await websocket.recv()
    data = json.loads(message)

    match data["type"]:
        case "object":
            await object(websocket)
        case "viewer":
            await viewer(websocket)

async def object(websocket):
    x = random.randint(2,19)
    y = random.randint(2,19)
    OBJECTS[websocket] = {"x":x, "y":y}
    await websocket.send(json.dumps(OBJECTS[websocket]))

    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            OBJECTS[websocket] = data
        except websockets.ConnectionClosed:
            del OBJECTS[websocket]
            break

async def viewer(websocket):
    VIEWERS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        VIEWERS.remove(websocket)

async def update():
    while True:
        websockets.broadcast(VIEWERS, json.dumps(list(OBJECTS.values())))
        await asyncio.sleep(dt)

async def main():
    websocket_port = os.environ.get('WEBSOCKET_PORT')
    if websocket_port:
        async with websockets.serve(handler,"",websocket_port):
            await update()
    else:
        sys.exit('WEBSOCKET_PORT environment variable not set')

if __name__ == "__main__":
    asyncio.run(main())