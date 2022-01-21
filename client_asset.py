import asyncio
import os
import websockets
from asset import Asset
import json
import sys

async def main():
    websocket_server = os.getenv("WEBSOCKET_SERVER", "localhost:8002")
    if websocket_server:
        async with websockets.connect(f'ws://{websocket_server}') as websocket:
            shakehand = {"type":"asset"}
            await websocket.send(json.dumps(shakehand))

            message = await websocket.recv()
            location = json.loads(message)
            print('Shook hands:',location)
            latitude = location["latitude"]
            longitude = location["longitude"]

            asset = Asset(latitude,longitude)
            msg = asset.generate_msg()
            print("Registration is ",msg)
            await websocket.send(json.dumps(msg))
            
            try:
                async for message in websocket:
                    data = json.loads(message)
                    print('Killed')
                    if data['Status'] == 'hit':
                        asset.killed()
                    msg = asset.generate_msg()
                    print(msg)
                    await websocket.send(json.dumps(msg))
            finally:
                print("Client (object) disconnected")
        

    else:
        sys.exit('WEBSOCKET_SERVER environment variable not set')

if __name__ == "__main__":
    asyncio.run(main())