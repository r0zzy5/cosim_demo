import asyncio
import json
import os
import sys

import websockets


async def main():
    websocker_server = os.environ.get('WEBSOCKET_SERVER')
    if websocker_server:
        async with websockets.connect(f'ws://{websocker_server}') as websocket:
            data_out = {"type":"viewer"}
            await websocket.send(json.dumps(data_out))

            async for message in websocket:
                data_in = json.loads(message)
                if data_in:
                    print(message)
    else:
        sys.exit('WEBSOCKET_SERVER environment variable not set')

if __name__ == "__main__":
    asyncio.run(main())
