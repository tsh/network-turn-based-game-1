import pygame, sys
from pygame import Rect
from pygame.locals import *

import requests

from map import Map

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 500
HEIGHT = 400
HALF_WIDTH = int(WIDTH / 2)
HALF_HEIGHT = int(HEIGHT / 2)
TILE_WIDTH = 25
TILE_HEIGHT = 25


class Game(object):
    def __init__(self):
        pygame.init()
        #Set up the window
        self.windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('Hello World')
        #Set up fonts
        basicFont = pygame.font.SysFont(None, 48)
        self.text = basicFont.render('HELLO WORLD', True, WHITE)
        self.textRect = self.text.get_rect()
        self.textRect.centerx = self.windowSurface.get_rect().centerx
        self.textRect.centery = self.windowSurface.get_rect().centery

        rsp = requests.post('http://127.0.0.1:8001')
        rsp.raise_for_status()
        id_ = rsp.json()['id']
        rsp = requests.get('http://127.0.0.1:8001/'+str(id_))
        mp = rsp.json()['map']
        self.map = Map()
        self.map.initialize(mp)


    def game_loop(self):
        clock = pygame.time.Clock()
        #Run the game loop
        while True:
            clock.tick(60)
            self.map.render(self.windowSurface)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(pos)

game = Game()
game.game_loop()
sys.exit()
