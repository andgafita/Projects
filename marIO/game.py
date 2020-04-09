from level import *
import pygame
from physical_object import *
from ground import *
from player import *
from input import *
from camera import *
import numpy as np
from PIL import Image

from RL.rn import *

class game:

    def __init__(self, my_model = None):
        pygame.init()

        self.inputs_count = 0
        self.frame_rate = 30
        self.frame_count = 0

        self.screen = pygame.display.set_mode([512, 512])
        self.level = level(self.screen)
        self.my_model = my_model
        self.action = [0, 0, 0]

        camera.screen = self.screen
        camera.player = self.level.player
        camera.length = 512
        camera.width = 512

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #self.my_model.network.save_weights("front_model.h5")
                    running = False

            pygame.display.flip()
            self.get_input()
            camera.update(self.level.get_recyclables())

        pygame.quit()

    def restart_level(self):
        new_level = level(self.screen)
        camera.player = new_level.player

        #if self.my_model != None:
        #    self.my_model.update( end_of_level = True)

        return new_level

    def get_input(self):
        self.frame_count = (self.frame_count + 1) % self.frame_rate
        if self.frame_count != 0:
            state_res = self.level.update(self.action)
            return None

        if self.my_model == None:
            self.action = input.get_input()
            #print(self.action, 'oooooo')
            state_res = self.level.update(np.array(self.action))
        else:
            self.action = self.my_model.get_input()
            #print(self.action, 'oooooo')
            #print(self.action, "wtfff")
            state_res = self.level.update(np.array(self.action))
            self.level.player.reward = 0.0
            #print(self.action)

        self.set_model_state(self.get_state(), state_res, self.action)

        self.inputs_count += 1

        if self.inputs_count > 256:
            self.inputs_count = 0
            self.level = self.restart_level()

        if state_res[0] == True or state_res[1] == True:
            self.inputs_count = 0
            self.level = self.restart_level()


    def set_model_state(self, state, result, action):
        if result[1] == True:
            reward = 1.0
        elif result[0] == True:
            reward = -1.0
        else:
            reward = min(0.1, result[2] / 100.0)

        #if reward == 0.0:
        #    reward = -0.0001

        if self.my_model != None:
            self.my_model.set_state(state, reward, action)

    def get_state(self):
        np_a = pygame.image.tostring(self.screen, "RGB")
        np_a = Image.frombytes("RGB", self.screen.get_size(), np_a)
        np_a = np_a.resize((64, 64), Image.ANTIALIAS)
        pix = np.array(np_a.getdata()).reshape(64, 64, 3) / 255
        return pix