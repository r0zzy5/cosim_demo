
import pandas as pd
import asyncio
import websockets
import argparse
import json
import random




# initialise the dataframes

df_assets = pd.DataFrame(data={},columns=['Asset_Name','Latitude','Longitude','Status'])
df_radars = pd.DataFrame(data={},columns=['Radar_Name','Latitude','Longitude','Tracked_list'])
df_launchers = pd.DataFrame(data={},columns=['Parent_Radar','Latitude','Longitude','Status'])
df_missiles = pd.DataFrame(data={},columns=['Missile_name','Colour','Target','Status','Latitude','Longitude'])
df_ships = pd.DataFrame(data={},columns=['Ship_name','Latitude','Longitude','Currently_attacking'])

# variable initialisations

dt = 1/10 # update time step for viewers
VIEWERS = set()
ASSETS = {}
RADARS = {}
LAUNCHERS = {}
MISSILES = {}
SHIPS = {}


async def service_asset(websocket):
    print("Client connected as 'asset'")
    latitude = random.uniform(51.16257108745399,51.181182648808075) #  51.181182648808075, -3.2781141919515755
    longitude = random.uniform(-3.210264681344032,-3.2781141919515755) # 51.16257108745399, -3.210264681344032
    msg = {"latitude": latitude, "longitude": longitude}
    await websocket.send(json.dumps(msg))
    registration = await websocket.recv()
    data = json.loads(registration)
    # print("registration is ",registration)
    assetuuid = data['uuid']
    # print(assetuuid)
    del data['uuid']
    df_newasset = pd.Series(data)
    # print(df_newasset)
    df_assets.loc[assetuuid] = df_newasset
    print(df_assets.head())
    await asyncio.sleep(5) # replace this with kill criteria

    data['Status'] = 'hit'
    await websocket.send(json.dumps(data))
    confirmation = await websocket.recv()
    data = json.loads(confirmation)
    print("Confirming",data['Asset_Name'],data['Status'])
    del data['uuid']
    df_newasset = pd.Series(data)
    df_assets.loc[assetuuid] = df_newasset
    print(df_assets)
    
async def service_radar(websocket):
    pass

async def service_missile(websocket):
    pass

async def service_ship(websocket):
    print("Client connected as 'ship'")
    latitude = random.uniform(51.18713124449443,51.1904221056704) #  51.1904221056704, -3.2826495634164115
    longitude = random.uniform(-3.2692339838586832,-3.2826495634164115) # 51.18713124449443, -3.2692339838586832
    reloadtime = 3
    msg = {"latitude": latitude, "longitude": longitude,'reloadtime':reloadtime}
    await websocket.send(json.dumps(msg))
    registration = await websocket.recv()
    data = json.loads(registration)
    print("registration is ",registration)
    shipuuid = data['uuid']
    # print(assetuuid)
    del data['uuid']
    df_newship= pd.Series(data)
    # print(df_newasset)
    df_ships.loc[shipuuid] = df_newship
    print(df_newship.head())

    try:
        async for message in websocket:
            data = json.loads(message)
            print('Request from ship recieved')
            if data['message'] == 'request live asset':
                df_available_assets = df_assets[['Status']=='Live']
                if len(df_available_assets):
                    target_asset = df_available_assets.head(0).to_dict()
                else:
                    target_asset = 'None'
                msg = {'target_asset':target_asset}
                await websocket.send(json.dumps(msg))
    finally:
        print("Client (object) disconnected")

async def service_viewer(websocket):
    print("Client connected as 'viewer'")
    VIEWERS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        print("Client (viewer) disconnected")
        VIEWERS.remove(websocket)

async def handler(websocket,path):
    message = await websocket.recv()
    data = json.loads(message)

    match data["type"]:
        case "asset":
            await service_asset(websocket)
        case "radar":
            await service_radar(websocket)
        case "missile":
            await service_missile(websocket)
        case "ship":
            await service_ship(websocket)
        case "viewer":
            await service_viewer(websocket)

async def update():
    while True:
        jsonbroadcast = json.dumps({"data":[df_assets.to_json(),df_radars.to_json(),df_launchers.to_json(),df_missiles.to_json(),df_ships.to_json()]})
        websockets.broadcast(VIEWERS, jsonbroadcast)
        await asyncio.sleep(dt)




#using main in async mode 
async def main():
    parser = argparse.ArgumentParser(description='System of systems server')

    parser.add_argument("port",
        help="the port used to accept websocket connections [default 8002]",
        nargs='?',
        default=8002,
        type=int
    )

    args = parser.parse_args()
    print(f"Starting websocket server on port {args.port}")
    
    async with websockets.serve(handler,"",args.port):
        await update()

if __name__ == "__main__":
    asyncio.run(main())