import pygame
from pygame.locals import *

class Settings:
    def __init__(self) -> None:

        self.size = 25
        self.screen_x = 1000
        self.screen_y = 800
        self.background_color = (66, 66, 97)
        self.music = True
        self.g_sound = True
        self.speed = 0.25
    
    def render_background(self,surface):
        bg = pygame.image.load('resources/background.jpg').convert()
        surface.blit(bg, (0,0))
        
    def draw(self):
        font = pygame.font.SysFont('arial',25)

        if self.music: m_color = (174, 240, 151)
        else: m_color = (227, 62, 105)
        over = font.render(f"BACKGROUND MUSIC", True, m_color)
        self.surface.blit(over, (500, 200))

        if self.g_sound: g_color = (174, 240, 151)
        else: g_color = (227, 62, 105)
        score = font.render(f"CRASH SOUND", True, g_color)
        self.surface.blit(score, (500, 300))

        replay = font.render(f"BACK", True, (200, 200, 200))
        self.surface.blit(replay, (500, 400))
        pygame.display.flip()

    def run(self, surface):

        self.surface = surface
        self.render_background(self.surface)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if 500 <= pos[0] <= 720 and 200 <= pos[1] <= 225:
                            self.music = False if self.music else True
                        if 500 <= pos[0] <= 655 and 300 <= pos[1] <= 325:
                            self.g_sound = False if self.g_sound else True
                        if 500 <= pos[0] <= 655 and 400 <= pos[1] <= 425:
                            running = False
                elif event.type == QUIT:
                    raise Exception("QUIT")
            self.draw()
        
game_setting = Settings()