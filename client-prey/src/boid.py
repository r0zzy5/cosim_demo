#import numpy as np
from random import random
import math
from prey import Prey

add = lambda v1,v2: [x + y for x,y in zip(v1,v2)]
sub = lambda v1,v2: [x - y for x,y in zip(v1,v2)]
norm = lambda v: math.sqrt(sum([x**2 for x in v]))
scale = lambda v,sf: [(x / norm(v)) * sf for x in v]

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]
    
    return c

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

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

    def apply_behaviour(self, boids, prey):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        prey_cohesion = self.preyCohesion(prey)

        #self.acceleration += alignment
        #self.acceleration += cohesion
        #self.acceleration += separation
        self.acceleration = add(self.acceleration,alignment)
        self.acceleration = add(self.acceleration,cohesion)
        self.acceleration = add(self.acceleration,separation)
        self.acceleration = add(self.acceleration,prey_cohesion)
        

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
    
    def preyCohesion(self, prey):
        steering = [0,0]
        total = 0
        if prey:
            preypos = [prey[0]["x"], prey[0]["y"], 0]
            prey_obj = Prey(preypos[0], preypos[1], preypos[2], 0, 0, 0, 0, 0)
            misspos = [self.position[0],self.position[1], 0]
            vm = [self.velocity[0],self.velocity[1], 0]
            if norm(sub(preypos - misspos)) < self.perception + 500:
                if norm(sub(preypos-misspos)) > 10:
                    r = [prey_obj.position[0] - misspos[0], prey_obj.position[1] - misspos[1], prey_obj.position[2] - misspos[2]]
                    vr = [prey_obj.velocity[0] - vm[0], prey_obj.velocity[1] - vm[1], prey_obj.velocity[2] - vm[2]]
                    rotVec = (cross(r,vr)) / (r @ r)
                    steering = (-5 * norm(vr) * cross(vm,rotVec)) / (norm(vm))
                    steering = [steering[0],steering[1]]
                else:
                    vec_to_tar = [prey_obj.position[0] - misspos[0], prey_obj.position[1] - misspos[1], prey_obj.position[2] - misspos[2]]
                    if norm(vec_to_tar) > 0:
                        vec_to_tar = (vec_to_tar / norm(vec_to_tar)) * self.max_speed
                    steering = ([(vec_to_tar[0] - vm[0])*100, (vec_to_tar[1] - vm[1])*100, (vec_to_tar[2] - vm[2])*100)
                    steering = [steering[0],steering[1]]
        return steering
