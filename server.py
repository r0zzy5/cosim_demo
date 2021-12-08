import asyncio
import websockets
import json
import argparse
import math
import numpy as np

OBJECTS = {}
VIEWERS = set()
dt = 1/10
width = 1000
height = 1000

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
    pos = np.random.rand(2) * 1000
    vel = (np.random.rand(2) - 0.5) * 10
    OBJECTS[websocket] = {"x":pos[0],"y":pos[1],"dx":vel[0],"dy":vel[1]}
    msg = OBJECTS[websocket] | {"width": width,"height": height}
    await websocket.send(json.dumps(msg))

    try:
        async for message in websocket:
            data = json.loads(message)
            OBJECTS[websocket] = data
    finally:
        print("Client (object) disconnected")
        del OBJECTS[websocket]

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
        recipients = VIEWERS.union(set(OBJECTS.keys()))
        websockets.broadcast(recipients, json.dumps(list(OBJECTS.values())))
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