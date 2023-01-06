import pygame
from game import Game
from pygame.locals import * # imported KEYDOWN, QUIT
from init import SIZE, SCREEN_X, SCREEN_Y, BACKGROUND_COLOR

class Menu:
    def __init__(self) -> None:
        # initlizing pygame
        pygame.init()

        # Play Background Music
        pygame.mixer.init()
        self.play_background_music()

        # making surface
        self.surface = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
        self.surface.fill(BACKGROUND_COLOR)


    def display_menu(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial',30)
        over = font.render(f"Start Game", True, (200, 200, 200))
        self.surface.blit(over, (300, 400))
        score = font.render(f"Settings", True, (200, 200, 200))
        self.surface.blit(score, (600, 400))
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
                                print("Settings")
                    elif event.type == QUIT:
                        running=False
                self.display_menu()
        except Exception as e:
            if e == "QUIT":
                pygame.quit()
        
    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def play(self):
        self.game = Game(self.surface)
        self.game.run()

if __name__ == "__main__":
    game = Menu()
    game.run()