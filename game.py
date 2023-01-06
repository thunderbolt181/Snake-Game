import time
import pygame
from pygame.locals import * # imported KEYDOWN, QUIT
from init import SIZE, SCREEN_X, SCREEN_Y, BACKGROUND_COLOR
from elements import Snake, Apple

class Game:
    def __init__(self, surface) -> None:
        self.surface = surface

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
                if event.type == MOUSEBUTTONDOWN and pause:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if 300 <= pos[0] <= 455 and 500 <= pos[1] <= 545:
                            pygame.mixer.music.unpause()
                            self.score=0
                            pause=False
                        if 495 <= pos[0] <= 575 and 500 <= pos[1] <= 545:
                            running = False
                elif event.type == QUIT:
                    raise Exception("QUIT")
            try:
                if not pause:
                    self.play()
            except Exception as e:
                pause = True
                self.show_game_over()
                self.reset()

            time.sleep(0.1)
        
    def show_game_over(self):
        # self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial',40)
        over = font.render(f"Game Over", True, (200, 200, 200))
        self.surface.blit(over, (400, 300))
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (400, 400))
        replay = font.render(f"Play Again", True, (200, 200, 200))
        self.surface.blit(replay, (300, 500))
        back = font.render(f"Back", True, (200, 200, 200))
        self.surface.blit(back, (500, 500))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        # resetting Snake
        self.snake = Snake(self.surface,1)
        self.snake.draw()

        # making an apple
        self.apple = Apple(self.surface)
        self.apple.draw()

if __name__=="__main__":
    play = Game()
    play.run()