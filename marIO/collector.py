import pygame

class collector(pygame.sprite.Sprite):

    def __init__(self, height, width, color):
        super(collector, self).__init__()

        self.surf = pygame.Surface(( height, width))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.left = -1000.0
        self.rect.top = -1000.0

    def collides(self, obj_lists):
        for L in obj_lists:
            collides = pygame.sprite.spritecollide( self, L, dokill = False)
            for c in collides:
                L.remove(c)

    def draw(self, screen, pos):
        self.rect.top  = 10.0
        self.rect.left = pos[0] - 200.0
        #print(self.rect.top, self.rect.left)

        #screen.blit(self.surf, ( 10.0, 20.0))
        #print(pos)


    def update(self, screen, obj_lists, pos):
        self.draw(screen, pos)
        self.collides(obj_lists)
        pass