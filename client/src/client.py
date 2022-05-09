import asyncio
import websockets
import json
import math
import os
import sys
import numpy as np
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

            pos = np.random.rand(2) * 1000
            pos[0] = 100
            vel = (np.random.rand(2) - 0.5) * 10
            prey = []
            clients = []

            boid = Boid(pos[0], pos[1], vel[0], vel[1], width, height)

            async for message in websocket:
                data_in = json.loads(message)
                typekey = [list(x.keys())[0] for x in list(data_in)]
                data_in = [data for data in list(data_in) if list(data.keys())[0] == 'type']
                if typekey[0] == 'msgtype' and typekey[1] == 'type':
                    prey = list(filter(lambda x: x['type'] == 'prey', list(data_in)))
                    # prey = [prey for prey in list(data_in) if prey['type']=='prey']
                    clients = list(filter(lambda x: x['type'] == 'predator', list(data_in)))
                    boids = [Boid(b["x"],b["y"],b["dx"],b["dy"],width,height) for b in clients]
                    boid.edges()
                    boid.apply_behaviour(boids,prey)
                    boid.update()
                msg = {
                    "type": "predator",
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