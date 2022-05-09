import asyncio
import websockets
import json
import argparse
import math
import numpy as np
import os

OBJECTS = {}
PREY = {}
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
        case "prey":
            await prey(websocket)

async def object(websocket):
    print("Client connected as 'object'")
    
    msg = {"width": width, "height": height}
    await websocket.send(json.dumps(msg))

    OBJECTS[websocket] = {"x": 0, "y": 0, "dx": 0, "dy": 0}

    try:
        async for message in websocket:
            data = json.loads(message)
            OBJECTS[websocket] = data
            # print(PREY.values())
            # await websocket.send(json.dumps(PREY.values()))
            objects = [{"msgtype":"alldata"}]
            for obj in OBJECTS.values(): objects.append({"type":"predator","x":obj["x"],"y":obj["y"],"dx":obj["dx"],"dy":obj["dy"]})
            for obj in PREY.values(): objects.append({"type":"prey","x":obj["x"],"y":obj["y"]})
            if objects:
                await websocket.send(json.dumps(objects))
            await websocket.recv()
    finally:
        print("Client (object) disconnected")
        del OBJECTS[websocket]

async def prey(websocket):
    print("Prey connected as 'object'")
    
    msg = {"width": width, "height": height}
    await websocket.send(json.dumps(msg))

    PREY[websocket] = {"x": 0, "y": 0, "dx": 0, "dy": 0}

    try:
        async for message in websocket:
            data = json.loads(message)
            PREY[websocket] = data
    finally:
        print("Prey (object) disconnected")
        del PREY[websocket]

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

        websockets.broadcast(list(OBJECTS.keys()), json.dumps(list(OBJECTS.values())))
        websockets.broadcast(list(PREY.keys()), json.dumps(list(PREY.values())))
        # objects = [{"x":obj["x"],"y":obj["y"]} for obj in OBJECTS.values()]
        objects = [{"type":"predator","x":obj["x"],"y":obj["y"]} for obj in OBJECTS.values()]
        for obj in PREY.values(): objects.append({"type":"prey","x":obj["x"],"y":obj["y"]})
        websockets.broadcast(VIEWERS, json.dumps(objects))

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