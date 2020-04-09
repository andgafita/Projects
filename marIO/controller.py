import numpy as np

class controller:

    def __init__(self, player):
        self.player = player

    def update(self, actions):

        #print(actions, '!!!!')
        if len(actions) > 3:
            actions = self.get_input (actions)
            #print(actions)

        if actions[0] == 1.0:
            self.player.jump()

        if actions[1] == 1.0:
            if self.player.ph.left_collision == False:
                self.player.ph.velocity = (self.player.ph.velocity[0], 0.4)
        elif actions[2] == 1.0:
            if self.player.ph.right_collision == False:
                self.player.ph.velocity = (self.player.ph.velocity[0], -0.4)
        else:
            self.player.ph.velocity = (self.player.ph.velocity[0], 0.0)

    def get_input(self, actions):
        a_max = np.argmax(actions)
        res = np.zeros(3)

        if a_max == 1:
            res[2] = 1.0
        elif a_max == 2:
            res[1] = 1.0
        elif a_max == 3:
            res[0] = 1.0
            res[2] = 1.0
        elif a_max == 4:
            res[0] = 1.0
            res[1] = 1.0
        elif a_max == 5:
            res[0] = 1.0
        return res


