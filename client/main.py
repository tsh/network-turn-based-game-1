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


class GameServer:
    def __init__(self, address='127.0.0.1', port=8001):
        self.url = f'http://{address}:{port}'
        # create game
        rsp = requests.post(self.url)
        rsp.raise_for_status()
        self.id = rsp.json()['id']

    def game_map(self):
        rsp = requests.get('{url}/{path}'.format(url=self.url, path=self.id))
        return rsp.json()['map']

    def check_server(self):
        path = '{id}/check'.format(id=self.id)
        rsp = requests.get('{url}/{path}'.format(url=self.url, path=path))
        rsp.raise_for_status()
        print(rsp.json())



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

        self.game_server = GameServer()
        self.map = Map()
        self.map.initialize(self.game_server.game_map())

        pygame.time.set_timer(pygame.USEREVENT, 1000)


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
                if event.type == pygame.USEREVENT:
                    self.game_server.check_server()

game = Game()
game.game_loop()
sys.exit()
