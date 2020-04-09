from keras import models, layers
from keras.datasets import mnist
from keras import optimizers
from keras.utils import to_categorical
from keras.layers import Conv2D, MaxPooling2D, AvgPool2D, Dropout
import keras
import numpy as np
import random
from keras.models import load_model, save_model

from keras.regularizers import l2

class rn:

    def __init__(self):
        self.network = self.create_model()
        self.data = []

        self.last_state_2 = -1
        self.last_state_1 = -1

        self.current_state = -1

        self.epsilon = 0.0 #0.7387 #0.2323
        self.epsilon_desc_rate = 0.995

        try:
            self.network.load_weights("my_model.h5")
        except:
            pass
        pass

    def create_model(self):
        #model = models.Sequential()

        input1 = layers.Input( shape= (64, 64, 3))
        input2 = layers.Input(shape=(64, 64, 3))

        # kernel_regularizer= l2(0.01),
        x1_0 = Conv2D(64, (8, 8), activation='relu')(input1)
        x2_0 = Conv2D(16, (8, 8), activation='relu')(input2)
        #model.add(Dropout(0.25))
        #model.add(Conv2D(32, (3, 3), activation='relu'))

        #x1_1 = Conv2D(16, (8, 8), activation='relu')(x1_0)
        #x2_1 = Conv2D(16, (8, 8), activation='relu')(x2_0)

        #model.add(Dropout(0.2))
        #model.add(Conv2D(16, (3, 3), activation='relu' ))

        x1_2 = Conv2D(16, (8, 8), activation='relu')(x1_0)
        x2_2 = Conv2D(8, (8, 8), activation='relu')(x2_0)
        #model.add(Dropout(0.22))
        #model.add(Conv2D(16, (3, 3), activation='relu'))
        x1_3 = Conv2D(16, (3, 3), activation='relu')(x1_2)
        x2_3 = Conv2D(16, (3, 3), activation='relu')(x2_2)
        #model.add( Dropout(0.2))

        #model.add(layers.Flatten())

        x1_4 = layers.Flatten()(x1_3)
        x2_4 = layers.Flatten()(x2_3)
        x_5 = keras.layers.Add()([x1_4, x2_4])

        x_6 = layers.Dense(128, activation='relu')(x_5)
        #model.add(layers.Dense(512, activation='relu'))
        #model.add(Dropout(0.2))
        #model.add(layers.Dense(256, activation='relu'))

        x_7 = layers.Dense(64, activation='relu')(x_6)
        x_8 = layers.Dense(32, activation='relu')(x_7)
        x_9 = layers.Dense(16, activation='relu')(x_8)
        x_10 = layers.Dense(6, activation='linear')(x_9)
        #model.add(Dropout(0.2))

        #model.add(layers.Dense(128, activation='relu'))


        #model.add(layers.Dense(64, activation='relu'))
        #model.add(layers.Dense(32, activation='relu'))
        #model.add(layers.Dense(6, activation='linear'))

        model = keras.models.Model (inputs=[input1, input2], outputs = x_10)

        model.compile(optimizer=optimizers.SGD(learning_rate=0.0008, nesterov = True), #0.012
                        loss='mean_squared_error', metrics=['accuracy'])

        return model


    def set_state(self, state, reward, action):

        print(action, reward)

        self.current_state = state
        self.last_action = action

        if type(self.last_state_1) != int and type(self.last_state_2) != int:
            self.data.append( (np.array(self.last_state_1), np.array(self.last_state_2), np.array(self.current_state), np.array(self.last_action), reward) )


    def get_input(self):
        #print(self.current_state.type)
        if type (self.current_state) == int or type(self.last_state_1) == int:
            self.last_state_2 = self.last_state_1
            self.last_state_1 = self.current_state
            return [0, 0, 0]

        #try:
        i = [self.current_state]
        j = [self.last_state_1]

        i = np.reshape(i, (1, 64, 64, 3))
        j = np.reshape(j, (1, 64, 64, 3))
        res = self.network.predict([j, i])[0]
        #except:
        '''
            print("asta-i???")
            c = random.randrange(0, 5)
            res = np.zeros(6)
            res[c] = 1
        '''
        #print(res, '?????')
        self.last_state_2 = self.last_state_1
        self.last_state_1 = self.current_state

        if self.data.__len__() > 2000:
            self.update()

        if random.random() > self.epsilon:
            return res

        if self.epsilon > 0.05:
            self.epsilon *= self.epsilon_desc_rate

        c = random.randrange(0, 5)
        res = np.zeros(6)
        res[c] = 1
        return res


    def update(self, end_of_level = False):
        len = self.data.__len__()
        if len > 2000:
            random.shuffle(self.data)
            self.data = self.data[:-1024]

        '''
        if end_of_level == True:
            try:
                self.network.load_weights("my_model.h5")
            except:
                pass
        '''

        x_train1, x_train2, y_train = self.add_targets()

        self.network.fit([x_train1, x_train2], [y_train],
                  epochs = 1, shuffle=True)
        #if end_of_level == True:
        self.network.save("my_model.h5")

        self.data = []

        #print( self.epsilon)

    def add_targets(self):
        res_x1 = []
        res_x2 = []

        res_y = []
        for d in self.data:
            #if d[3] == 0.0 or (d[3] not in (-1.0, 1.0) and d[3] < 0.0):
                #import random
                #if random.randint(1, 100) > 95:
                #    continue
            i = [d[2]]
            j = [d[1]]
            i = np.reshape(i, (1, 64, 64, 3))
            j = np.reshape(j, (1, 64, 64, 3))

            new_action = self.network.predict([j, i])[0]

            #print(d[3])
            #print(d[2], new_action)

            i = d[1]
            i = np.reshape(i, (64, 64, 3))
            res_x1.append(np.array(i))

            i = d[2]
            i = np.reshape(i, (64, 64, 3))
            res_x2.append(np.array(i))

            max_a = np.argmax(new_action)
            res_y.append(np.array(d[3]))

            if d[4] not in [-1.0, 1.0]:
                res_y[-1][max_a] = d[4] + 0.75 * new_action[max_a]
            else:
                res_y[-1][max_a] = d[4]

            #res_y[-1] -= np.amin(res_y[-1])
            #res_y[-1] /= np.sum(res_y[-1])


        return np.array(res_x1), np.array(res_x2), np.array(res_y)
