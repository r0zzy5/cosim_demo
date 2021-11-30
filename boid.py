import numpy as np

class Boid:
    def __init__(self, x, y, width, height):
        self.position = np.array([x, y])
        self.velocity = (np.random.rand(2) - 0.5) * 10
        self.acceleration = (np.random.rand(2) - 0.5) / 2
        self.max_force = 0.3
        self.max_speed = 5
        self.perception = 100
        self.width = width
        self.height = height
    
    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = self.velocity / speed * self.max_speed
    
    def edges(self):
        if self.position[0] > self.width:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = self.width

        if self.position[1] > self.height:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = self.height
    
    def apply_behaviour(self,boids):
        steering = np.zeros(2)
        total = 0
        avg_vel = np.zeros(2)
        center_of_mass = np.zeros(2)
        avg_rel_pos = np.zeros(2)

        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if np.linalg.norm(boid.position - self.position) < self.perception:
                avg_vel += boid.velocity
                center_of_mass += boid.position
                avg_rel_pos = (self.position - boid.position) / distance
                total += 1
        
        if total > 0:
            steering += self.align(avg_vel, total)
            steering += self.cohesion(center_of_mass, total)
            steering += self.separation(avg_rel_pos, total)

    def align(self,avg_vel,total):
        avg_vel /= total
        avg_vel = (avg_vel / np.linalg.norm(avg_vel)) * self.max_speed
        steering = avg_vel - self.velocity
        return steering
    
    def cohesion(self,center_of_mass,total):
        center_of_mass /= total
        vec_to_com = center_of_mass - self.position
        if np.linalg.norm(vec_to_com) > 0:
            vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
        steering = vec_to_com - self.velocity
        if np.linalg.norm(steering) > self.max_force:
            steering = (steering /np.linalg.norm(steering)) * self.max_force
        
        return steering
    
    def separation(self,avg_rel_pos,total):
        avg_rel_pos /= total
        steering = avg_rel_pos - self.velocity
        if np.linalg.norm(steering)> self.max_force:
            steering = (steering /np.linalg.norm(steering)) * self.max_force
        
        return steering