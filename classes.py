import pygame


class blob:

    head = None
    bloblist = []

    size = 20
    colour = "aqua"

    def __init__(self, head):

        self.head = head
        self.state = {
            "pos_x":None,
            "pos_y":None,
            "vel_x":None,
            "vel_y":None
        }

    def draw(self):
        pass

class influencer:

    maxvel_x, maxvel_y = 5,5
    vel_factor = 0.1

    color = "aqua"

    def __init__(self, size = 50):
        
        self.size = size
        self.pos_x = 400
        self.pos_y = 200
        self.vel_x = 0
        self.vel_y = 0

    def update_pos(self, game):

        keys = game.get_events()["keys"]

        print(abs(self.vel_x))
        
        if keys[pygame.K_a]:
            if abs(self.vel_x) < self.maxvel_x:
                self.vel_x -= 2

        if keys[pygame.K_d]:
            if abs(self.vel_x) < self.maxvel_x:
                self.vel_x += 2

        

        

        if keys[pygame.K_w]:
            if abs(self.vel_y) < self.maxvel_y:
                self.vel_y -= 2

        if keys[pygame.K_s]:
            if abs(self.vel_y) < self.maxvel_y:
                self.vel_y += 2
        
        

        self.pos_x += self.vel_x * self.vel_factor
        self.pos_y += self.vel_y * self.vel_factor

        self.vel_x = 0
        self.vel_y = 0



    def draw(self, game):
        pygame.draw.circle(game.screen , self.color,(self.pos_x, self.pos_y) , self.size)

        
class Game:

    SCREEN_SIZE = (800, 400)
    FPS = 60
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
    
    def run(self, sphere):

        while True:

            events = self.get_events()
            for event in events["events"]:
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.screen.fill((0,0,0))

            sphere.update_pos(self)
            sphere.draw(self)

            pygame.display.update()
