import pygame


class Game:

    SCREEN_SIZE = (800, 400)
    FPS = 120
    CLOCK = pygame.time.Clock()


    def __init__(self):

        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

    def get_events(self):

        events = pygame.event.get()
        mouse_press = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        raw_dt = self.CLOCK.get_time()
        dt = raw_dt * self.FPS

    
        return {
            "events": events,
            "mouse press": mouse_press,
            "keys": keys,
            "mouse pos": mouse_pos,
            "raw dt": raw_dt,
            "dt": dt,
        }
    
    def run(self):

        while True:

            events = self.get_events()
            for event in events["events"]:
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.draw.circle(self.screen, "RED", (300, 200),50)
            pygame.display.update()
