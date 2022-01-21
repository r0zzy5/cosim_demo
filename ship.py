import names
import uuid
import time
from missiles import Missile

class Ship():
    def __init__(self,lat,lon,reloadtime):
        self.uuid = str(uuid.uuid1())
        assetname = names.get_full_name().replace(" ","_")
        self.name = assetname+"_ship"
        self.lat = lat
        self.lon = lon
        self.reload_time = reloadtime
        self.status = "Live"

    def reload(self):
        self.status = "Reloading"
        time.sleep(self.reload_time)
        self.status = "Live"
    
    def check_ready(self):
        while True:
            if self.status == "Reloading":
                time.sleep(1)
            else:
                return True

    def generate_msg(self):
        msg = {
            'uuid': self.uuid,
            'Asset_Name': self.name,
            'Latitude': self.lat,
            'Longitude': self.lon,
            'Reload_time': self.reload_time,
            'Status': self.status
        }
        return msg
    
    def generate_target_request_message(self):
        msg = {
            'uuid': self.uuid,
           'Asset_Name': self.name,
            'message': 'request live asset'
        }

    def load_missile(self,target_name):
        new_missile = Missile("Red",self.name,target_name)
        new_missile.lat = self.lat
        new_missile.lon = self.lon
        new_missile.lastlat = self.lat
        new_missile.lastlon = self.lon
        ready = self.check_ready()
        if ready:
            return new_missile
        
