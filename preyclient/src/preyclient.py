import asyncio
import websockets
import json
import math
import os
import sys
import numpy as np
from boid import Boid
from prey import Prey

w = 2 * math.pi / 5
r = 0.5

async def main():
    websocket_server = os.getenv("WEBSOCKET_SERVER", "localhost:8001")
    if websocket_server:
        async with websockets.connect(f'ws://{websocket_server}') as websocket:
            data_out = {"type":"prey"}
            await websocket.send(json.dumps(data_out))

            message = await websocket.recv()
            data_in = json.loads(message)
            width = data_in["width"]
            height = data_in["height"]

            vel = np.zeros(3)
            preypos = np.array([800, 500, 0])
            prey_obj = Prey(preypos[0], preypos[1], preypos[2], vel[0], vel[1], vel[2], width, height)

            async for message in websocket:
                data_in = json.loads(message)
                msg = {
                    "x": int(prey_obj.position[0]),
                    "y": int(prey_obj.position[1]),
                    "dx": int(prey_obj.velocity[0]),
                    "dy": int(prey_obj.velocity[1]),
                }
                # print(data_in)
                await websocket.send(json.dumps(msg))

    else:
        sys.exit('WEBSOCKET_SERVER environment variable not set')

if __name__ == "__main__":
    asyncio.run(main())