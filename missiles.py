import names

class Missile():
    def __init__(self,colour,parent_name,target_name):
        missilename = names.get_full_name().replace(" ","_")
        self.name = missilename+"_missile"
        self.colour = colour
        self.parent = parent_name
        self.target = target_name
        self.lat = 0
        self.long = 0
        self.lastlat = 0
        self.lastlon = 0

    def update_position(self):
        pass

