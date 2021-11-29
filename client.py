import asyncio
import websockets
import json
import math
import os
import sys

dt = 1/10
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
            xo = data_in["x"]
            yo = data_in["y"]

            t = 0
            while True:
                msg = {
                    "x": r * math.cos(w*t) + xo,
                    "y": r * math.sin(w*t) + yo,
                }
                await websocket.send(json.dumps(msg))
                await asyncio.sleep(dt)
                t += dt
    else:
        sys.exit('WEBSOCKET_SERVER environment variable not set')

if __name__ == "__main__":
    asyncio.run(main())