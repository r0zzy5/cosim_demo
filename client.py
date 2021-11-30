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
    websocker_server = os.environ.get('WEBSOCKET_SERVER')
    if websocker_server:
        async with websockets.connect(f'ws://{websocker_server}') as websocket:
            data_out = {"type":"object"}
            await websocket.send(json.dumps(data_out))

            message = await websocket.recv()
            data_in = json.loads(message)
            x0 = float(data_in["x"])
            y0 = float(data_in["y"])
            width = data_in["width"]
            height = data_in["height"]

            boid = Boid(x0, y0, width, height)

            async for message in websocket:
                data_in = json.loads(message)
                boids = [Boid(pos['x'],pos['x'],width,height) for pos in data_in]
                boid.edges()
                boid.apply_behaviour(boids)
                boid.update()
                msg = {
                    "x": boid.position[0],
                    "y": boid.position[1],
                }
                await websocket.send(json.dumps(msg))

    else:
        sys.exit('WEBSOCKET_SERVER environment variable not set')

if __name__ == "__main__":
    asyncio.run(main())