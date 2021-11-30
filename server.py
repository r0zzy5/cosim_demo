import asyncio
import websockets
import json
import random
import argparse
import math

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
    x = random.randint(0,1000)
    y = random.randint(0,1000)
    OBJECTS[websocket] = {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
    }
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
        for websocket, pos1 in OBJECTS.items():
            objects = [pos2 for pos2 in OBJECTS.values() if check_distance(pos1, pos2)]
            await websocket.send(json.dumps(objects))
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

def check_distance(p1,p2):
    dx = p1['x'] - p2['x']
    dy = p1['y'] - p2['y']
    r = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
    return 0 < r <= 100

if __name__ == "__main__":
    asyncio.run(main())