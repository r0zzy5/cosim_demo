import holoviews as hv
from holoviews import opts
from datashader.utils import lnglat_to_meters as webm
import pandas as pd
import panel as pn
import numpy as np
import asyncio
import websockets
import os
import json
import sys

# for testing only
import names
import uuid
import random

hv.extension('bokeh')



def create_block(row):
    return pd.Series([[
                        (row['easting']-50,row['northing']-50),
                        (row['easting']+50,row['northing']-50),
                        (row['easting']+50,row['northing']+50),
                        (row['easting']-50,row['northing']+50),
                        (row['easting']-50,row['northing']-50)
    ]])

worldmap = hv.element.tiles.EsriImagery().opts(width=1200, height=1080)


df_assets = pd.DataFrame(data={},columns=['Asset_Name','Latitude','Longitude','Status'])
df_radars = pd.DataFrame(data={},columns=['Radar_Name','Latitude','Longitude','Tracked_list'])
df_launchers = pd.DataFrame(data={},columns=['Parent_Radar','Latitude','Longitude','Status'])
df_missiles = pd.DataFrame(data={},columns=['Missile_name','Colour','Target','Status','Latitude','Longitude'])
df_ships = pd.DataFrame(data={},columns=['Ship_name','Latitude','Longitude','Currently_attacking'])

def populate_assets():
    n_assets = 20
    for i in range(n_assets):
        asset_uuid = str(uuid.uuid1())
        assetname = names.get_full_name().replace(" ","_")
        name = assetname+"_asset"
        latitude = random.uniform(51.162571,51.181182) #  51.181182648808075, -3.2781141919515755
        longitude = random.uniform(-3.210264,-3.278114) # 51.16257108745399, -3.210264681344032
        status = "Live"
        df_assets.loc[asset_uuid] = {'Asset_Name':name ,
                                'Latitude': latitude,
                                'Longitude': longitude,
                                'Status': status}
    print(df_assets.head())






# populate_assets()
# df_assets_wgs84 = df_assets.apply(towgs84,axis=1)
# df_assets['Latitude'], df_assets['Longitude'] = df_assets_wgs84[0].to_list(),df_assets_wgs84[1].to_list(),

df_assets.loc[:,'easting'],df_assets.loc[:,'northing'] = webm(df_assets['Longitude'],df_assets['Latitude'])
# df_assets.loc[:,'block'] = df_assets.apply(create_block,axis=1)
# print(df_assets.head(20))

asset_locs = hv.Points(df_assets,kdims=['easting','northing'],vdims=['Status'])
# asset_blocks = hv.Path(df_assets['block'].to_list()).opts(line_width=4)

asset_locs.opts(color='blue',marker='+')

# layout = pn.panel(worldmap*asset_locs*asset_blocks)
layout = pn.panel(worldmap*asset_locs)

layout.servable(title='System of systems visualisation')


async def main():
    websocket_server = os.getenv("WEBSOCKET_SERVER", "localhost:8002")
    if websocket_server:
        async with websockets.connect(f'ws://{websocket_server}') as websocket:
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
