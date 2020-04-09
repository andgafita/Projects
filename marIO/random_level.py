import random

class random_level:
    def __init__(self):
        self.default_pos_x = 0.0
        self.default_pos_y = 400.0

        self.last_pos_x = 0.0
        self.last_pos_y = 400.0

        self.step = 30.0

    def init_level(self):
        g = []
        for i in range(15):
            g.append((self.step, self.step, self.last_pos_x, self.last_pos_y))
            self.last_pos_x += self.step
        return g, [], [], []

    def add_game_objects(self):

        g, e, m, d = [], [], [], []

        if random.randrange(1, 100) >= 3:

            if random.randrange(1, 100) >= 73:
                m.append((self.step / 2.5, self.step / 2.5, self.last_pos_x + self.step / 2.5,
                          self.last_pos_y - self.step - random.randrange(0, 75)))

            if random.randrange(1, 500) >= 491:
                d.append((1.5 * self.step, 3.1 * self.step, self.last_pos_x + self.step / 2,
                          self.last_pos_y - self.step - 62.0))


            g.append( (self.step, self.step, self.last_pos_x, self.last_pos_y) )
            self.last_pos_x += self.step

            if random.randrange (1, 100) >= 95:
                g.append((self.step, self.step, self.last_pos_x, self.last_pos_y - self.step - random.randrange(0, 200)))
                if random.randrange(1, 100) >= 95:
                    g.append(
                        (self.step, self.step, self.last_pos_x, self.last_pos_y - self.step - random.randrange(0, 200)))


        else:
            self.last_pos_x += 20
            self.last_pos_x += self.step

        if random.randrange(1, 100) >= 92:
            e.append((self.step, self.step, self.last_pos_x + self.step / 2, self.last_pos_y - self.step - 10.0))

        return g, e, m, d