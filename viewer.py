import asyncio
import websockets
import json

async def main():
    async with websockets.connect("ws://localhost:8001") as websocket:
        data_out = {"type":"viewer"}
        await websocket.send(json.dumps(data_out))

        async for message in websocket:
            data_in = json.loads(message)
            if data_in:
                print(message)

if __name__ == "__main__":
    asyncio.run(main())