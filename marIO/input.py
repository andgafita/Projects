import pygame
import numpy as np

from pygame.locals import (
    K_UP,
    K_LEFT,
    K_RIGHT,
)

class input:

    def get_input():
        res = np.zeros(3)

        pygame.key.get_focused()
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            res[0] = 1.0
        if pressed_keys[K_LEFT]:
            res[1] = 1.0
        elif pressed_keys[K_RIGHT]:
            res[2] = 1.0

        return res