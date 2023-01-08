import time
import pygame
from pygame.locals import * # imported KEYDOWN, QUIT
from elements import Snake, Apple
from settings import game_setting


class Game:
    def __init__(self, surface) -> None:

        self.surface = surface
        self.play_background_music()

        # making a Snake
        length = 1
        self.snake = Snake(self.surface, length)
        self.snake.draw()

        # making an apple
        self.apple = Apple(self.surface, self.snake)
        self.apple.draw()

        # If the player presses a special sequence depending on scenerio,
        # the snake can move backword and eat itself, this lock will prevent it.
        self.move_lock = False

        # Maintin Score
        self.score = 0

    def play_background_music(self):
        if game_setting.music:
            pygame.mixer.music.load('resources/bg_music_1.mp3')
            pygame.mixer.music.play()

    def play_sound(self,sound):
        if game_setting.g_sound:
            play = pygame.mixer.Sound(f'resources/{sound}.mp3')
            pygame.mixer.Sound.play(play)

    def display_score(self):
        font = pygame.font.SysFont('arial',20)
        score = font.render(f"Score: {self.score}", True, (200, 200, 200))
        self.surface.blit(score, (900, 20))

    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + game_setting.size:
            if y1 >= y2 and y1 < y2 + game_setting.size:
                return True
        return False

    def crash_collision(self):
        self.play_sound('crash')
        raise Exception("Game Over")

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        self.move_lock=False

        # Snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.score +=1
            if self.score%5==0 and game_setting.speed > 0.06:game_setting.speed-=0.05
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.crash_collision()

        # Snake colliding with wall
        if self.snake.x[0] < 0 or self.snake.y[0] < 0 or self.snake.x[0] >= game_setting.screen_x or self.snake.y[0] >= game_setting.screen_y:
            self.crash_collision()

    def run(self):
        # running window in Infinite loop
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if not pause and not self.move_lock:
                        if event.key == K_UP and not self.snake.direction == "DOWN":
                            self.snake.direction="UP"
                        if event.key == K_DOWN and not self.snake.direction == "UP":
                            self.snake.direction = "DOWN"
                        if event.key == K_LEFT and not self.snake.direction == "RIGHT":
                            self.snake.direction = "LEFT"
                        if event.key == K_RIGHT and not self.snake.direction == "LEFT":
                            self.snake.direction = "RIGHT"
                        self.move_lock=True
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

            time.sleep(game_setting.speed)
        
    def show_game_over(self):
        font = pygame.font.SysFont('arial',40)
        over = font.render(f"Game Over", True, (200, 200, 200))
        self.surface.blit(over, (400, 300))
        score = font.render(f"Score: {self.score}", True, (200, 200, 200))
        self.surface.blit(score, (400, 400))
        replay = font.render(f"Play Again", True, (200, 200, 200))
        self.surface.blit(replay, (300, 500))
        back = font.render(f"Back", True, (200, 200, 200))
        self.surface.blit(back, (500, 500))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        game_setting.speed=0.25

        # resetting Snake
        self.snake = Snake(self.surface,1)
        self.snake.draw()

        # making an apple
        self.apple = Apple(self.surface,self.snake)
        self.apple.draw()

if __name__=="__main__":
    play = Game()
    play.run()