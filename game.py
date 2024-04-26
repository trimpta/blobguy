import pygame


class game:

    def __init__(self, screen_size: tuple):
        
        pygame.init()
        
        self.screen = pygame.display.set_mode(screen_size)

        
