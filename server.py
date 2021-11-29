import asyncio
import websockets
import json
import random
import argparse

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
    print("Client connected as 'object'")
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
            print("Client (object) disconnected")
            del OBJECTS[websocket]
            break

async def viewer(websocket):
    print("Client connected as 'viewer'")
    VIEWERS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        print("Client (viewer) disconnected")
        VIEWERS.remove(websocket)

async def update():
    while True:
        websockets.broadcast(VIEWERS, json.dumps(list(OBJECTS.values())))
        await asyncio.sleep(dt)

async def main():
    parser = argparse.ArgumentParser(description='Websocket Server')

    parser.add_argument("port",
        help="the port used to accept websocket connections [default 8001]",
        nargs='?',
        default=8001,
        type=int
    )

    args = parser.parse_args()
    print(f"Starting websocket server on port {args.port}")
    
    async with websockets.serve(handler,"",args.port):
        await update()

if __name__ == "__main__":
    asyncio.run(main())