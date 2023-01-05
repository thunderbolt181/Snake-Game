import time
import pygame
from random import randint
from pygame.locals import * # imported KEYDOWN, QUIT

SIZE = 25
SCREEN_X = 1000
SCREEN_Y = 800
BACKGROUND_COLOR = (66, 66, 97)


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

class Game:
    def __init__(self) -> None:
        # initlizing pygame
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()

        # making surface
        self.surface = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
        self.surface.fill(BACKGROUND_COLOR)

        # making a Snake
        length = 3
        self.snake = Snake(self.surface,length)
        self.snake.draw()

        # making an apple
        self.apple = Apple(self.surface)
        self.apple.draw()

        # Maintin Score
        self.score = 0

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def play_sound(self,sound):
        play = pygame.mixer.Sound(f'resources/{sound}.mp3')
        pygame.mixer.Sound.play(play)

    def display_score(self):
        font = pygame.font.SysFont('arial',20)
        score = font.render(f"Score: {self.score}", True, (200, 200, 200))
        self.surface.blit(score, (900, 20))

    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def crash_collision(self):
        self.play_sound('crash')
        raise "Game Over"

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.score +=1
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.crash_collision()

        # Snake colliding with wall
        if self.snake.x[0] < 0 or self.snake.y[0] < 0 or self.snake.x[0] >= SCREEN_X or self.snake.y[0] >= SCREEN_Y:
            self.crash_collision()

    def run(self):
        # running window in Infinite loop
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        self.score=0
                        pause=False
                    if not pause:
                        if event.key == K_UP and not self.snake.direction == "DOWN":
                            self.snake.direction="UP"
                        if event.key == K_DOWN and not self.snake.direction == "UP":
                            self.snake.direction = "DOWN"
                        if event.key == K_LEFT and not self.snake.direction == "RIGHT":
                            self.snake.direction = "LEFT"
                        if event.key == K_RIGHT and not self.snake.direction == "LEFT":
                            self.snake.direction = "RIGHT"
                    self.snake.draw()
                elif event.type == QUIT:
                    running=False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                pause = True
                self.show_game_over()
                self.reset()

            time.sleep(0.1)
        
    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial',40)
        over = font.render(f"Game Over", True, (200, 200, 200))
        self.surface.blit(over, (300, 300))
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (300, 400))
        replay = font.render(f"Press Enter to Play the Game Again", True, (200, 200, 200))
        self.surface.blit(replay, (300, 500))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        # resetting Snake
        self.snake = Snake(self.surface,1)
        self.snake.draw()

        # making an apple
        self.apple = Apple(self.surface)
        self.apple.draw()


if __name__ == "__main__":
    game = Game()
    game.run()

    