import numpy as np
from random import random
import math

from prey import Prey

class Boid():

    def __init__(self, x, y, dx, dy, width, height):
        self.position = [x, y]
        self.velocity = [dx,dy]
        self.acceleration = [random() - 0.5) / 2 for _ in range(2)]
        self.max_force = 0.3
        self.max_speed = 5
        self.perception = 100
        self.width = width
        self.height = height

    def update(self):
        self.position = add(self.position,self.velocity)
        self.velocity = add(self.velocity,self.acceleration)
        #limit
        if norm(self.velocity) > self.max_speed:
            self.velocity = scale(self.velocity, self.max_speed)

        self.acceleration = np.zeros(2)

    def apply_behaviour(self, boids, prey):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        prey_cohesion = self.preyCohesion(prey)

        self.acceleration = add(self.acceleration,alignment)
        self.acceleration = add(self.acceleration,cohesion)
        self.acceleration = add(self.acceleration,separation)
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
        steering = [0,0]
        total = 0
        avg_vector = [0,0]
        for boid in boids:
            if norm(sub(boid.position,self.position) < self.perception:
                avg_vector = add(avg_vector,boid.velocity)
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = (avg_vector / np.linalg.norm(avg_vector)) * self.max_speed
            steering = avg_vector - self.velocity

        return steering

    def cohesion(self, boids):
        steering = np.zeros(2)
        total = 0
        center_of_mass = np.zeros(2)
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            vec_to_com = center_of_mass - self.position
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.velocity
            if np.linalg.norm(steering)> self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering

    def separation(self, boids):
        steering = np.zeros(2)
        total = 0
        avg_vector = np.zeros(2)
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if (self.position != boid.position).any() and distance < self.perception:
                diff = self.position - boid.position
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
            steering = avg_vector - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force

        return steering

    def preyCohesion(self, prey):
        steering = np.zeros(2)
        total = 0
        if prey:
            preypos = np.array([prey[0]["x"], prey[0]["y"], 0])
            prey_obj = Prey(preypos[0], preypos[1], preypos[2], 0, 0, 0, 0, 0)
            misspos = np.append(self.position, 0)
            vm = np.append(self.velocity, 0)
            if np.linalg.norm(preypos - misspos) < self.perception + 500:
                if np.linalg.norm(preypos-misspos) > 10:
                    r = prey_obj.position - misspos
                    vr = prey_obj.velocity - vm
                    rotVec = (np.cross(r,vr)) / (np.dot(r,r))
                    steering = (-5 * np.linalg.norm(vr) * np.cross(vm,rotVec)) / (np.linalg.norm(vm))
                    steering = np.delete(steering, 2)
                else:
                    vec_to_tar = prey_obj.position - misspos
                    if np.linalg.norm(vec_to_tar) > 0:
                        vec_to_tar = (vec_to_tar / np.linalg.norm(vec_to_tar)) * self.max_speed
                    steering = (vec_to_tar - vm) * 100
                    steering = np.delete(steering, 2)
        return steering
