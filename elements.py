import time
import pygame
from random import randint
from pygame.locals import * # imported KEYDOWN, QUIT
from init import SIZE, SCREEN_X, SCREEN_Y, BACKGROUND_COLOR

class Apple:
    def __init__(self,parent_screen) -> None:
        self.img = self.block = pygame.image.load('resources/apple.png').convert()
        self.img = pygame.transform.scale(self.img,(SIZE,SIZE))
        self.parent_screen = parent_screen
        self.x = 1
        self.y = 1
        self.move()

    def draw(self):
        self.parent_screen.blit(self.img,(self.x,self.y))

    def move(self):
        self.x = randint(0,(SCREEN_X//25)-1)*SIZE
        self.y = randint(0,(SCREEN_Y//25)-1)*SIZE
        self.draw()

class Snake:
    def __init__(self,parent_screen, length) -> None:
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/snake.png').convert()
        self.block = pygame.transform.scale(self.block,(SIZE,SIZE))
        self.y = [SIZE]*length
        self.x = [SIZE]*length
        self.direction = "DOWN"
        self.length = length

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "DOWN":
            self.y[0] += SIZE
        elif self.direction == "UP":
            self.y[0] -= SIZE
        elif self.direction == "RIGHT":
            self.x[0] += SIZE
        elif self.direction == "LEFT":
            self.x[0] -= SIZE
        
        self.draw()

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
