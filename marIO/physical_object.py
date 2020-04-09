import pygame
from cronometer import *
from camera import *

class physical_object:
    def __init__(self, height, width, pos_x, pos_y, color):

        self.height = height
        self.width = width

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color

        self.collider = collider( height, width, color)
        self.acc_gravity = 0.9

        self.velocity = (0.0, 0.0)

        self.time = cronometer()
        self.time2 = cronometer()

        self.grounded = False
        self.left_collision = False
        self.right_collision = False


    def collides(self, grounds):
        L = pygame.sprite.spritecollide( self.collider, grounds, dokill = False)
        self.grounded = False
        self.left_collision = False
        self.right_collision = False

        for l in L:
            if self.collider.rect.right > l.rect.left and self.collider.rect.left < l.rect.right :
                if l.rect.bottom + 2 > self.collider.rect.top > l.rect.bottom - 2 and self.velocity[0] > 0.0:
                    v = -self.velocity[0]
                    grounds.remove(l)
                    self.velocity = (v, self.velocity[1])

                if l.rect.top + 2 > self.collider.rect.bottom > l.rect.top - 2 and self.velocity[0] < 0.0:
                    self.grounded = True
                    v = 0.0
                    self.velocity = (v, self.velocity[1])

                if l.rect.top + 5 > self.collider.rect.bottom > l.rect.top - 5 and self.velocity[0] == 0.0:
                    self.pos_y -= 0.5
                    self.grounded = True

            if self.collider.rect.bottom - 3 > l.rect.top and self.collider.rect.top < l.rect.bottom + 3:
                if l.rect.right + 3 >= self.collider.rect.left >= l.rect.right - 3 and self.velocity[1] > 0.0:
                    self.left_collision = True
                    self.pos_x += 0.5
                    self.velocity = (self.velocity[0], 0.0)

                if l.rect.left + 3 >= self.collider.rect.right >= l.rect.left - 3 and self.velocity[1] < 0.0:
                    self.right_collision = True
                    self.pos_x -= 0.5
                    self.velocity = (self.velocity[0], 0.0)

        if not self.grounded:
            v = self.velocity[0]
            v = v + self.acc_gravity * self.time2.getDelta()
            self.velocity = (v, self.velocity[1])

    def collides_with_enemies(self, enemies):
        L = pygame.sprite.spritecollide(self.collider, enemies, dokill=False)
        reward = 0.0
        res = False
        v = 0.0

        for l in L:
            if self.collider.rect.right > l.rect.left and self.collider.rect.left < l.rect.right:
                if l.rect.top + 2 > self.collider.rect.bottom > l.rect.top - 2 and self.velocity[0] <= 0.0:
                    enemies.remove(l)
                    reward += 0.2
                    v = 0.3
                else:
                    res = True

        if v > 0.0:
            self.velocity = (v, self.velocity[1])

        return res, reward

    def collides_with_money (self, money):
        L = pygame.sprite.spritecollide(self.collider, money, dokill=False)
        reward = 50.0
        s = 0.0
        for l in L:
            money.remove(l)
            s += reward
        return s

    def collides_with_door (self, exit):
        L = pygame.sprite.spritecollide(self.collider, exit, dokill=False)
        res = False
        for l in L:
            exit.remove(l)
            res = True
        return res

    def draw(self, screen, grounds):
        self.collides(grounds)
        self.update_position()

        screen.blit(self.collider.surf, (self.pos_x - camera.pos_x, self.pos_y - camera.pos_y))

    def update_position(self):
        self.pos_x -= self.velocity[1]
        self.pos_y -= self.velocity[0]
        self.collider.rect.left = self.pos_x - self.velocity[1] * self.time.getDelta()
        self.collider.rect.top = self.pos_y - self.velocity[0] * self.time.getDelta()


class collider(pygame.sprite.Sprite):
    def __init__(self, height, width, color):
        super(collider, self).__init__()
        self.surf = pygame.Surface(( height, width))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
