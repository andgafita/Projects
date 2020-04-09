import pygame
from physical_object import *
from cronometer import *

class enemy:

    def __init__(self, height, width, pos_x, pos_y):

        color = (0, 255, 0)
        self.ph = physical_object(height, width, pos_x, pos_y, color)
        self.killed = False
        self.default_movement = (0.0, 0.25)


    def update(self):
        if self.ph.grounded and self.ph.velocity[1] == 0.0:
            self.ph.velocity = self.default_movement

        if self.ph.right_collision and self.default_movement[1] < 0.0:
            self.default_movement = (self.default_movement[0], self.default_movement[1] * -1.0)

        if self.ph.left_collision and self.default_movement[1] > 0.0:
            self.default_movement = (self.default_movement[0], self.default_movement[1] * -1.0)



    def draw (self, screen, grounds):
        self.update()
        self.ph.draw(screen, grounds)