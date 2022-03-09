import asyncio
import websockets
import json
import math
import os
import sys
from random import random
from boid import Boid

w = 2 * math.pi / 5
r = 0.5

async def main():
    websocket_server = os.getenv("WEBSOCKET_SERVER", "localhost:8001")
    if websocket_server:
        async with websockets.connect(f'ws://{websocket_server}') as websocket:
            data_out = {"type":"object"}
            await websocket.send(json.dumps(data_out))

            message = await websocket.recv()
            data_in = json.loads(message)
            width = data_in["width"]
            height = data_in["height"]

            pos = [random() * 1000 for _ in range(2)]
            vel = [(random() - 0.5) * 10 for _ in range(2)]

            boid = Boid(pos[0], pos[1], vel[0], vel[1], width, height)

            async for message in websocket:
                data_in = json.loads(message)
                boids = [Boid(b["x"],b["y"],b["dx"],b["dy"],width,height) for b in data_in]
                boid.edges()
                boid.apply_behaviour(boids)
                boid.update()
                msg = {
                    "x": boid.position[0],
                    "y": boid.position[1],
                    "dx": boid.velocity[0],
                    "dy": boid.velocity[1],
                }
                await websocket.send(json.dumps(msg))

    else:
        sys.exit('WEBSOCKET_SERVER environment variable not set')

if __name__ == "__main__":
    asyncio.run(main())