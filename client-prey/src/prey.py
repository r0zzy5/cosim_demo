class Prey():

    def __init__(self, x, y, z, dx, dy, dz, width, height):
        self.position = [x, y, z]
        self.velocity = [dx,dy,dz]
        self.acceleration = 0
        self.max_force = 0.3
        self.max_speed = 5
        self.perception = 100
        self.width = width
        self.height = height
