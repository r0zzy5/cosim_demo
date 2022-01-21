import names
import uuid

class Asset():
    def __init__(self,lat,lon):
        self.uuid = str(uuid.uuid1())
        assetname = names.get_full_name().replace(" ","_")
        self.name = assetname+"_asset"
        self.lat = lat
        self.lon = lon
        self.status = "Live"

    def killed(self):
        self.status = "Dead"

    def generate_msg(self):
        msg = {
            'uuid': self.uuid,
            'Asset_Name': self.name,
            'Latitude': self.lat,
            'Longitude': self.lon,
            'Status': self.status
        }
        return msg