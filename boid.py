#import numpy as np
from random import random
import math

add = lambda v1,v2: [x + y for x,y in zip(v1,v2)]
sub = lambda v1,v2: [x - y for x,y in zip(v1,v2)]
norm = lambda v: math.sqrt(sum([x**2 for x in v]))
scale = lambda v,sf: [(x / norm(v)) * sf for x in v]

class Boid():
    
    def __init__(self, x, y, dx, dy, width, height):
        #self.position = np.array([x, y])
        self.position = [x,y]
        #self.velocity = np.array([dx,dy])
        self.velocity = [dx,dy]
        #self.acceleration = (np.random.rand(2) - 0.5) / 2
        self.acceleration = [(random() - 0.5) / 2 for _ in range(2)]
        self.max_force = 0.3
        self.max_speed = 5
        self.perception = 100
        self.width = width
        self.height = height

    def update(self):
        #self.position += self.velocity
        self.position = add(self.position,self.velocity)
        #self.velocity += self.acceleration
        self.velocity = add(self.velocity,self.acceleration)
        #limit
        #if np.linalg.norm(self.velocity) > self.max_speed:
        if norm(self.velocity) > self.max_speed:
            #self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
            self.velocity = scale(self.velocity,self.max_speed)

        self.acceleration = [0,0]

    def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        #self.acceleration += alignment
        #self.acceleration += cohesion
        #self.acceleration += separation
        self.acceleration = add(self.acceleration,alignment)
        self.acceleration = add(self.acceleration,cohesion)
        self.acceleration = add(self.acceleration,separation)
        

    def edges(self):
        if self.position[0] > self.width:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = self.width

        if self.position[1] > self.height:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = self.height

    def align(self, boids):
        #steering = np.zeros(2)
        steering = [0,0]
        total = 0
        #avg_vector = np.zeros(2)
        avg_vector = [0,0]
        for boid in boids:
            #if np.linalg.norm(boid.position - self.position) < self.perception:
            if norm(sub(boid.position,self.position)) < self.perception:
                #avg_vector += boid.velocity
                avg_vector = add(avg_vector,boid.velocity)
                total += 1
        if total > 0:
            #avg_vector /= total
            avg_vector = [x / total for x in avg_vector]
            #avg_vector = (avg_vector / np.linalg.norm(avg_vector)) * self.max_speed
            avg_vector = scale(avg_vector,self.max_speed)
            #steering = avg_vector - self.velocity
            steering = sub(avg_vector,self.velocity)

        return steering

    def cohesion(self, boids):
        #steering = np.zeros(2)
        steering = [0,0]
        total = 0
        #center_of_mass = np.zeros(2)
        center_of_mass = [0,0]
        for boid in boids:
            #if np.linalg.norm(boid.position - self.position) < self.perception:
            if norm(sub(boid.position,self.position)) < self.perception:
                #center_of_mass += boid.position
                center_of_mass = add(center_of_mass,boid.position)
                total += 1
        if total > 0:
            #center_of_mass /= total
            center_of_mass = [x / total for x in center_of_mass]
            #vec_to_com = center_of_mass - self.position
            vec_to_com = sub(center_of_mass,self.position)
            #if np.linalg.norm(vec_to_com) > 0:
            if norm(vec_to_com) > 0:
                #vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
                vec_to_com = scale(vec_to_com,self.max_speed)
            #steering = vec_to_com - self.velocity
            steering = sub(vec_to_com,self.velocity)
            #if np.linalg.norm(steering)> self.max_force:
            if norm(steering) > self.max_force:
                #steering = (steering /np.linalg.norm(steering)) * self.max_force
                steering = scale(steering,self.max_force)

        return steering

    def separation(self, boids):
        #steering = np.zeros(2)
        steering = [0,0]
        total = 0
        #avg_vector = np.zeros(2)
        avg_vector = [0,0]
        for boid in boids:
            #distance = np.linalg.norm(boid.position - self.position)
            rel_pos = sub(self.position,boid.position)
            distance = norm(rel_pos)
            #if (self.position != boid.position).any() and distance < self.perception:
            if (self.position != boid.position) and distance < self.perception:
                #diff = self.position - boid.position
                #diff /= distance
                diff = scale(rel_pos,1)
                #avg_vector += diff
                avg_vector = add(avg_vector,diff)
                total += 1
        if total > 0:
            #avg_vector /= total
            avg_vector = [x / total for x in avg_vector]
            #if np.linalg.norm(steering) > 0:
            if norm(steering) > 0:
                #avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
                avg_vector = scale(avg_vector,self.max_speed)
            #steering = avg_vector - self.velocity
            steering = sub(avg_vector,self.velocity)
            if norm(steering) > self.max_force:
                #steering = (steering /np.linalg.norm(steering)) * self.max_force
                steering = scale(steering,self.max_force)

        return steering