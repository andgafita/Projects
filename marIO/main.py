import pygame
from physical_object import *
from ground import *
from player import *
from input import *
from camera import *
from game import *
from RL.rn import *

if __name__ == '__main__':

    game = game(my_model = rn())
