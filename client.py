import asyncio
import websockets
import json
import math
import os
import sys
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
            x0 = float(data_in["x"])
            y0 = float(data_in["y"])
            dx0 = float(data_in["dx"])
            dy0 = float(data_in["dy"])
            width = data_in["width"]
            height = data_in["height"]

            boid = Boid(x0, y0, width, height, dx0, dy0)

            async for message in websocket:
                data_in = json.loads(message)
                boids = [Boid(b["x"],b["y"],width,height,b["dx"],b["dy"]) for b in data_in]
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