import asyncio
import os
from time import sleep
import websockets
from ship import Ship
import json
import sys

async def main():
    websocket_server = os.getenv("WEBSOCKET_SERVER", "localhost:8002")
    if websocket_server:
        async with websockets.connect(f'ws://{websocket_server}') as websocket:
            shakehand = {"type":"asset"}
            await websocket.send(json.dumps(shakehand))

            message = await websocket.recv()
            parameters = json.loads(message)
            print('Shook hands:',parameters)
            latitude = parameters["latitude"]
            longitude = parameters["longitude"]
            reloadtime = parameters["reloadtime"]
            ship = Ship(latitude,longitude,reloadtime)
            msg = ship.generate_msg()
            print("Registration is ",msg)
            await websocket.send(json.dumps(msg))

            while ship.status == "Live":
                msg = ship.generate_target_request_message()
                await websocket.send(json.dumps(msg))
                message = await websocket.recv()
                targetmessage = json.loads(message)
                if targetmessage['target_asset'] == 'None':
                    sleep(5)
                else:
                    targetname = targetmessage['target_asset']['Asset_Name']
                    newmissile = ship.load_missile(targetname)



    else:
        sys.exit('WEBSOCKET_SERVER environment variable not set')

if __name__ == "__main__":
    asyncio.run(main())