import names
from missiles import Missile

class Radar():
    def __init__(self,lat,lon,trackradius):
        radarname = names.get_first_name().replace(" ","_")
        self.name = radarname+"_radar"
        self.lat = lat
        self.lon = lon
        self.trackradius = trackradius
        self.tracking = []
        
    
    def add_to_tracked(self, target_name):
        self.tracking.append(target_name)

    def remove_from_tracked(self,target_name):
        self.tracking.remove(target_name)

    def launch_missile(self,target_name):
        new_missile = Missle(self.name,target_name)
        return new_missile

