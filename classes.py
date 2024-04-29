import pygame

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
        return (self.i, self.j)

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
    maxvel = 5
    vel_factor = 0.1

    xaddn_factor = vector(0.2, 0)
    yaddn_factor = vector(0, 0.2)



    color = "aqua"

    def __init__(self):
        
        self.size = 10

        self.pos = vector(400, 200)
        self.vel = vector(0, 0)
        self.accn = vector(0, 0)

    def update_pos(self, game):

        keys = game.get_events()["keys"]

        targetvel = self.xaddn_factor * keys[pygame.K_d] - self.xaddn_factor * keys[pygame.K_a]  - self.yaddn_factor * keys[pygame.K_w] + self.yaddn_factor * keys[pygame.K_s]

        speed_diff = targetvel - self.vel*0.1

        self.pos += speed_diff
        


    def draw(self, game):
        pygame.draw.circle(game.screen , self.color,self.pos.pos() , self.size)

        
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