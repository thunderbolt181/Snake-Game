import time
import pygame
from random import randint
from pygame.locals import * # imported KEYDOWN, QUIT
from settings import game_setting


class Apple:
    def __init__(self,parent_screen,snake) -> None:
        self.img = self.block = pygame.image.load('resources/apple.png').convert()
        self.img = pygame.transform.scale(self.img,(game_setting.size,game_setting.size))
        self.parent_screen = parent_screen
        self.x = 1
        self.y = 1
        self.snake = snake
        self.move()

    def draw(self):
        self.parent_screen.blit(self.img,(self.x,self.y))

    def move(self):
        while True:
            self.x = randint(0,(game_setting.screen_x//25)-1)*game_setting.size
            self.y = randint(0,(game_setting.screen_y//25)-1)*game_setting.size
            if self.x not in self.snake.x and self.y not in self.snake.y:
                self.draw()
                break

class Snake:
    def __init__(self,parent_screen, length) -> None:
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/snake.png').convert()
        self.block = pygame.transform.scale(self.block,(game_setting.size,game_setting.size))
        self.y = [game_setting.size]*length
        self.x = [game_setting.size]*length
        self.direction = "DOWN"
        self.length = length

    def draw(self):
        game_setting.render_background(self.parent_screen)
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "DOWN":
            self.y[0] += game_setting.size
        elif self.direction == "UP":
            self.y[0] -= game_setting.size
        elif self.direction == "RIGHT":
            self.x[0] += game_setting.size
        elif self.direction == "LEFT":
            self.x[0] -= game_setting.size
        
        self.draw()

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
