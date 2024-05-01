import pygame
import math

class vector:


    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __repr__(self):
        return f"i: {self.i}, j: {self.j}"

    def __eq__(self, other) -> bool:
        return self.i == other.i and self.j == other.j
    
    def __lt__(self, other) -> bool:
        if isinstance(self, other):
            return abs(self) < abs(other)
        else:
            raise TypeError
    
    def __gt__(self, other) -> bool:
        if isinstance(self, other):
            return abs(self) > abs(other)
        else:
            raise TypeError
        
    
    def __abs__(self) -> float :
        return (self.i**2 + self.j**2)**0.5

    def __add__(self, other):
        return vector(self.i + other.i, self.j + other.j)
    
    def __sub__(self, other):
        return vector(self.i - other.i, self.j - other.j)
    
    def __mul__(self, other):
        if isinstance(other, vector):
            raise NotImplementedError
        
        elif isinstance(other, bool):
            if other:
                return self
            else:
                return vector(0, 0)
            
        elif isinstance(other, float) or isinstance(other, int):
            return vector(self.i * other, self.j * other)
        
        else:
            raise NotImplementedError
    
    def __iadd__(self, other):
        return self + other
    
    def __isub__(self, other):
        return self - other

    def pos(self) -> tuple:
        '''Returns position as a tuple in the form (i, j)'''
        return (self.i, self.j)
    
class camera:

    def __init__(self):
        '''init'''

        self.pos = vector(0, 0)
        self.scale = 1/100

    def get_pos(self, pos: tuple) -> tuple:
        '''returns pos relative to camera as tuple'''
        return ((vector(*pos) - self.pos)* self.scale ).pos()
    
    def get_vector(self, pos:vector) -> vector:
        '''returns pos relative to camera as vector'''
        return (pos - self.pos) * self.scale
    


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
    maxax = 5
    maxvel = 100
    vel_factor = 0.1

    xaddn_factor = vector(1, 0)
    yaddn_factor = vector(0, 1)



    color = "aqua"

    def __init__(self):
        
        self.size = 5

        self.pos = vector(4000, 2000)
        self.vel = vector(0, 0)
        self.accn = vector(0, 0)
        self.space_counter = 0
        self.history = []

    def dash(self, mgame):
        self.history.append(self.pos.pos())

        if len(self.history) > 100 :
            del self.history[0]

        for ind, i in enumerate(self.history):
            size = math.ceil((ind)/len(self.history)*self.size)
            pygame.draw.circle(mgame.screen , "BLUE",i, size)
            mgame.cam.pos = vector(*i)
        



    def update_pos(self, game):

        keys = game.get_events()["keys"]

        targetvel = self.xaddn_factor * keys[pygame.K_d] \
                  - self.xaddn_factor * keys[pygame.K_a] \
                  - self.yaddn_factor * keys[pygame.K_w] \
                  + self.yaddn_factor * keys[pygame.K_s]

        if keys[pygame.K_SPACE]:
            if self.space_counter<10000:
                if keys[pygame.K_LSHIFT]:
                    self.vel -= self.vel * 0.4
                else:
                    if abs(self.vel)> 40:
                        self.vel -= self.vel * 0.6

                        
                self.accn = vector(0,0)
                self.pos += self.vel
        
        if self.space_counter > 0:
            self.space_counter = 0

        self.accn += targetvel
        # speed_diff = targetvel - self.vel
        # if abs(self.vel) <= self.maxvel:
        self.vel += self.accn
        
        self.pos += self.vel

        self.vel -= self.vel * 0.01
        # self.accn = vector(0,0)
        self.accn -= self.accn * 0.9

        

    
    def reset(self, game):
        keys = game.get_events()["keys"]
        
        if keys[pygame.K_e]:
            self.pos = vector(100,100)


    def draw(self, game):

        
        pygame.draw.circle(game.screen , self.color,game.cam.get_pos(self.pos.pos()), self.size)

        
class Game:

    SCREEN_SIZE = (1000, 800)
    FPS = 1000
    CLOCK = pygame.time.Clock()
    pygame.font.init()

    temp_font = pygame.font.SysFont('chalkduster.ttf', 40)
    # temp_bg = pygame.image.load('oil.jpeg').convert()



    def __init__(self, cam):

        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.cam = cam
        self.temp_bg = pygame.image.load('oil.jpeg').convert()


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
    
    def circle(self, color, center, radius, width = 0):
        '''draw circle'''

        pygame.draw.circle(self.screen, color, center, radius, width)
        
    
    def run(self, sphere):

        while True:

            events = self.get_events()
            for event in events["events"]:
                if event.type == pygame.QUIT:
                    pygame.quit()

            # self.screen.fill((0,0,0))
            self.screen.blit(self.temp_bg, self.cam.get_pos((0, 0)))

            sphere.update_pos(self)
            sphere.dash(self)
            sphere.draw(self)
            sphere.reset(self)

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

            pygame.display.set_caption(str(round(self.CLOCK.get_fps())))

