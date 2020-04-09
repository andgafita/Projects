import pygame

class cronometer:
    def __init__(self):
        self.last_frame = pygame.time.get_ticks()

    def getDelta(self):
        t = pygame.time.get_ticks()
        res = (self.last_frame - t) /1000.0
        self.last_frame = t
        if res < -1.0: res = 0.0
        return res