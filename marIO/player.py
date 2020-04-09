import pygame
from physical_object import *
from controller import *
from cronometer import *

class player:

    def __init__(self, height, width, pos_x, pos_y):
        color = (250, 0, 0)
        self.ph = physical_object(height, width, pos_x, pos_y, color)

        self.killed = False
        self.won = False

        self.clock = cronometer()
        self.sum = 0.0
        self.reward = 0.0
        self.bottom_edge = 410

        self.right_movement_reward = 0.0
        self.X = 0.0


    def jump(self):
        if self.ph.grounded:
            self.ph.velocity = (0.6, self.ph.velocity[1])

    def draw (self, screen, grounds, enemies, money, exit):



        self.sum += self.clock.getDelta()
        if self.sum > 1.2:
            self.jumping = False


        self.ph.draw(screen, grounds)

        self.right_movement_reward = 0.0
        if self.X < self.ph.pos_x:
            self.right_movement_reward = 0.001
        if self.X > self.ph.pos_x:
            self.right_movement_reward = -0.002
        self.X = self.ph.pos_x

        #if last_X - self.X < 0.0:
        #    self.right_movement_reward = 0.00 #0.00055

        #if last_X - self.X > 0.0:
        #    self.right_movement_reward = -0.01 #-0.00022


        #self.right_movement_reward = max ( 0.0, min ( 0.001, self.max_X - last_max_X))

        #if self.right_movement_reward > 0.0:
        #    print(self.right_movement_reward, '??????')

        money_reward = self.ph.collides_with_money(money)

        self.won = self.won or self.ph.collides_with_door(exit)
        enemies_collide = self.ph.collides_with_enemies(enemies)

        self.killed = self.killed or enemies_collide[0]

        if self.ph.pos_y > self.bottom_edge: self.killed = True

        if abs(self.ph.velocity[1])< 0.05 and abs (self.ph.velocity[0]) < 0.05 :
            money_reward -= 0.2

        money_reward += enemies_collide[1]
        #if abs(self.ph.velocity[0]) < 0.05:
        self.reward += money_reward
        self.reward += self.right_movement_reward

        return (self.killed, self.won, self.reward)