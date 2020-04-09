import pygame
from camera import *

class ground(pygame.sprite.Sprite):

    def __init__(self, width, height, pos_x, pos_y):

        super(ground, self).__init__()

        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((100, 55, 20))
        self.rect = self.surf.get_rect()
        self.rect.left = self.pos_x
        self.rect.top = self.pos_y

    def draw(self, screen):
        screen.blit(self.surf, (self.pos_x - camera.pos_x, self.pos_y - camera.pos_y))