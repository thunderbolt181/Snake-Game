import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from game import Game
from pygame.locals import * # imported KEYDOWN, QUIT
from settings import game_setting

class Menu:
    def __init__(self) -> None:
        # initlizing pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        # Play Background Music
        pygame.mixer.init()

        # making screen
        self.screen = pygame.display.set_mode((game_setting.screen_x,game_setting.screen_y))
        game_setting.render_background(self.screen)

    def display_menu(self):
        game_setting.render_background(self.screen)
        font = pygame.font.SysFont('arial',30)
        over = font.render(f"Start Game", True, (200, 200, 200))
        self.screen.blit(over, (300, 400))
        score = font.render(f"Settings", True, (200, 200, 200))
        self.screen.blit(score, (600, 400))
        pygame.display.flip()

    def run(self):
        running = True
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if 300 <= pos[0] <= 450 and 400 <= pos[1] <= 435:
                                self.play()
                            if 595 <= pos[0] <= 690 and 400 <= pos[1] <= 435:
                                self.setting()
                    elif event.type == QUIT:
                        running=False
                self.display_menu()
        except Exception as e:
            print(e)
            if e == "QUIT":
                pygame.quit()

    def play(self):
        self.game = Game(self.screen)
        self.game.run()

    def setting(self):
        game_setting.run(self.screen)

if __name__ == "__main__":
    game = Menu()
    game.run()