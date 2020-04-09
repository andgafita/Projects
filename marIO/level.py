from ground import *
from player import *
from controller import *
from input import *
from enemy import *
from money import *
from door import *

from random_level import *

class level():

    def __init__(self, screen):
        self.rand_level = random_level()
        self.screen = screen
        p = ( 25, 40, 100, 250)
        d = ( 40, 65, 730, 335)

        self.player = player( p[0], p[1], p[2], p[3])
        self.controller = controller(self.player)

        self.exit = pygame.sprite.Group()
        self.grounds = pygame.sprite.Group()
        self.enemy_sprites, self.enemies = pygame.sprite.Group(), []
        self.money = pygame.sprite.Group()
        self.set_game_objects()



    def add_grounds(self, g):
        res = self.grounds
        for p in g:
            res.add( ground (p[0], p[1], p[2], p[3]) )
        return res

    def add_money(self, g):
        res = self.money
        for p in g:
            res.add( money (p[0], p[1], p[2], p[3]) )
        return res

    def add_door(self, d):
        res = self.exit
        for p in d:
            res.add( door (p[0], p[1], p[2], p[3]) )
        return res

    def add_enemies(self, e):
        res1 = self.enemy_sprites
        res2 = self.enemies
        for p in e:
            s = enemy(p[0], p[1], p[2], p[3])
            res1.add( s.ph.collider)
            res2.append(s)
        return res1, res2

    def update(self, player_input):
        self.add_game_objects()
        self.screen.fill((100, 180, 250))

        self.controller.update( player_input)

        res = self.player.draw(self.screen, self.grounds, self.enemy_sprites, self.money, self.exit)
        for d in self.exit:
            d.draw(self.screen)

        for m in self.money:
            m.draw(self.screen)
        for g in self.grounds:
            g.draw(self.screen)
        for e in self.enemies:
            if e.ph.collider not in self.enemy_sprites:
                self.enemies.remove(e)
            else:
                e.draw(self.screen, self.grounds)
            if e.ph.collider.rect.top > self.player.bottom_edge:
                self.enemies.remove(e)
                self.enemy_sprites.remove(e.ph.collider)

        return res


    def set_game_objects(self):

        g, e, m, d = self.rand_level.init_level()
        self.grounds = self.add_grounds(g)
        self.enemy_sprites, self.enemies = self.add_enemies(e)
        self.money = self.add_money(m)
        self.exit = self.add_door(d)

    def add_game_objects(self):
        if self.grounds.__len__() < 30:
            g, e, m, d = self.rand_level.add_game_objects()
            self.grounds = self.add_grounds(g)
            self.enemy_sprites, self.enemies = self.add_enemies(e)
            self.money = self.add_money(m)
            self.exit = self.add_door(d)

    def get_recyclables (self):
        return (self.grounds, self.enemy_sprites, self.money)