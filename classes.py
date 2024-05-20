import pygame
import math
from game_config import *

# Vector class represents a 2D vector with i and j components
class vector:

    def __init__(self, i: float, j: float):
        """
        Initializes a vector with i and j components.
        """
        self.i: float = i
        self.j: float = j

    def __repr__(self) -> str:
        """
        Returns a string representation of the vector.
        """
        return f"i: {self.i}, j: {self.j}"

    def __eq__(self, other: "vector") -> bool:
        """
        Checks if two vectors are equal.
        """
        return self.i == other.i and self.j == other.j
    
    def __lt__(self, other: "vector") -> bool:
        """
        Compares the magnitude of two vectors.
        """
        if isinstance(self, other):
            return abs(self) < abs(other)
        else:
            raise TypeError
    
    def __gt__(self, other: "vector") -> bool:
        """
        Compares the magnitude of two vectors.
        """
        if isinstance(self, other):
            return abs(self) > abs(other)
        else:
            raise TypeError
        
    
    def __abs__(self) -> float :
        """
        Calculates the magnitude of the vector.
        """
        return (self.i**2 + self.j**2)**0.5

    def __add__(self, other: "vector") -> "vector":
        """
        Adds two vectors.
        """
        return vector(self.i + other.i, self.j + other.j)
    
    def __sub__(self, other: "vector") -> "vector":
        """
        Subtracts two vectors.
        """
        return vector(self.i - other.i, self.j - other.j)
    
    def __mul__(self, other: float) -> "vector":
        """
        Multiplies a vector by a scalar.
        """
        return vector(self.i * other, self.j * other)
    
    def __iadd__(self, other: "vector") -> "vector":
        """
        Adds a vector to itself.
        """
        return self + other
    
    def __isub__(self, other: "vector") -> "vector":
        """
        Subtracts a vector from itself.
        """
        return self - other
    
    def __truediv__(self, other: float) -> "vector":
        """
        Divides a vector by a scalar.
        """
        return self * (1/other)
    
    @classmethod
    def zero(cls) -> "vector":
        """
        Returns a zero vector.
        """
        return vector(0, 0)
    
    def is_zero(self) -> bool:
        """
        Checks if the vector is zero.
        """
        return not (self.i or self.j)
    
    def unit(self) -> "vector":
        """
        Returns the unit vector of the current vector.
        """
        if self.is_zero():
            return self.zero()
        else:
            return self/abs(self)

    def pos(self) -> tuple[float, float]:
        """
        Returns the position of the vector as a tuple.
        """
        return (self.i, self.j)
    
    def angle(self, offset: float = 0, scale: float = 1) -> float:
        """
        Calculates the angle of the vector.
        """
        return math.atan2(self.i, self.j) * scale + offset 
    
# Camera class manages the camera view
class camera:

    def __init__(self):
        """
        Initializes the camera with default position, scale, and center.
        """
        self.pos: vector = vector(0, 0)
        self.scale: float = 1
        self.center: vector = vector(*(i/2 for i in Game.SCREEN_SIZE))

    def get_pos(self, pos: tuple[float, float]) -> tuple[float, float]:
        """
        Returns the position relative to the camera as a tuple.
        """
        return (((vector(*pos) - self.pos)* self.scale) + self.center).pos()
    
    def get_vector(self, pos: vector) -> vector:
        """
        Returns the position relative to the camera as a vector.
        """
        return (pos - self.pos + self.center) * self.scale
    
    def follow_player(self, sphere: "influencer"):
        """
        Sets the camera position to follow the player.
        """
        self.pos = sphere.pos
    

# Influencer class represents the player character
class influencer:

    maxax: float = 5
    maxvel: float = 1500
    vel_factor: float = 0.1

    xaddn_factor: vector = vector(1, 0)
    yaddn_factor: vector = vector(0, 1)

    color: str = "BLACK"

    def __init__(self):
        """
        Initializes the player with default size, position, velocity, acceleration, history, and sperm image.
        """
        self.size: float = 10
        self.pos: vector = vector(0, 0)
        self.vel: vector = vector(0, 0)
        self.accn: vector = vector(0, 0)
        self.space_counter: int = 0
        self.history: list[tuple[float, float]] = []

        self.sperm: pygame.Surface = pygame.image.load("c_head.png").convert_alpha()
        self.sperm_rect: pygame.Rect = self.sperm.get_rect()
        # self.sperm_mask = pygame.mask.from_surface()

    def dash(self, mgame: "Game"):
        """
        Handles the dash mechanic, drawing the player's history and updating the position.
        """
        self.history.append(self.pos.pos())
        

        if len(self.history) > 100:
            del self.history[0]

        for ind, i in enumerate(self.history):
            size = math.ceil((ind)/len(self.history)*self.size)
            pygame.draw.circle(mgame.screen , "WHITE",mgame.cam.get_pos(i), size)
        
    def update_pos(self, game: "Game"):
        """
        Updates the player's position based on user input and braking functionality.
        """
        keys: dict[int, bool] = game.get_events()["keys"]
        targetvel: vector = self.xaddn_factor * keys[pygame.K_d] \
                  - self.xaddn_factor * keys[pygame.K_a] \
                  - self.yaddn_factor * keys[pygame.K_w] \
                  + self.yaddn_factor * keys[pygame.K_s]
        #Brake functionality
        if keys[pygame.K_SPACE] and abs(self.vel)> 4:
            if keys[pygame.K_LSHIFT]:
                self.vel -= self.vel * 0.1
            else:
                self.vel -= self.vel * 0.4
     
            self.accn = vector(0,0)
            targetvel *= 0.1
            self.pos += self.vel

        self.accn += targetvel.unit() * 2 * game.get_events()["raw_dt"] / 1000


        if abs(self.vel) < self.maxvel:
            self.vel += self.accn * game.get_events()["raw_dt"]
        else:
            self.vel = self.vel.unit() * self.maxvel
        
        self.pos += self.vel * game.get_events()["raw_dt"]

        self.vel *= 0.99
        self.accn *= 0.1

    def reset(self, game: "Game"):
        """
        Resets the player's position and velocity based on user input.
        """
        keys: dict[int, bool] = game.get_events()["keys"]
        
        if keys[pygame.K_e]:
            self.pos = game.cam.center
            self.vel *= 0
            self.accn *= 0

    def draw(self, game: "Game"):
        """
        Draws the player's sperm image rotated based on velocity.
        """
        rotated: pygame.Surface = pygame.transform.rotate(self.sperm, self.vel.angle(offset= 180 , scale= 180/math.pi))
        rotated_rect: pygame.Rect = rotated.get_rect(center=self.sperm_rect.center)

        blit_pos: tuple[int, int] = (500 - rotated_rect.width / 2, 400 - rotated_rect.height / 2)
        game.screen.blit(rotated, blit_pos)

    def render(self, game: "Game"):
        """
        Calls the dash and draw methods.
        """
        self.dash(game)
        self.draw(game)

    def update(self, game: "Game"):
        """
        Calls the update_pos and reset methods.
        """
        self.update_pos(game)
        self.reset(game)


# Map class represents the game map
class map:
    
    size: tuple[int, int] = (1200, 1200)
    sizev: vector = vector(*size)

    def __init__(self, game: "Game", inf: "influencer", cam: "camera"):
        """
        Initializes the map with the background image, game instance, player instance, and camera instance.
        """
        self.bg: pygame.Surface = pygame.transform.scale(pygame.image.load('uteres.png').convert(), self.size)
        self.game: "Game" = game
        self.inf: "influencer" = inf
        self.cam: "camera" = cam

    def update(self):
        """
        Updates the map by drawing the background image.
        """
        self.draw_bg(self.cam.get_pos((0,0)))



    def draw_bg(self, pos: tuple[float, float]):
        """
        Draws the background image centered at the given position.
        """
        cx, cy = pos
        
        self.game.screen.blit(self.bg, (cx, cy))
        

# Game class manages the game loop and functionality
class Game:

    SCREEN_SIZE: tuple[int, int] = (1000, 800)
    FPS: int = 600
    CLOCK: pygame.time.Clock = pygame.time.Clock()
    pygame.font.init()

    temp_font: pygame.font.Font = pygame.font.SysFont('chalkduster.ttf', 40)
    # temp_bg = pygame.image.load('oil.jpeg').convert()



    def __init__(self, cam: "camera"):
        """
        Initializes the game with the screen, camera, and temporary background image.
        """
        self.screen: pygame.Surface = pygame.display.set_mode(self.SCREEN_SIZE)
        self.cam: "camera" = cam
        self.temp_bg: pygame.Surface = pygame.image.load('uteres.png').convert()
        self.temp_bg = pygame.transform.scale(self.temp_bg, (4740/2,3550/2))


    def get_events(self) -> dict:
        """
        Gets all events, mouse presses, key presses, mouse position, raw delta time, and delta time.
        """
        events: list[pygame.event.Event] = pygame.event.get()
        mouse_press: tuple[bool, bool, bool] = pygame.mouse.get_pressed()
        keys: dict[int, bool] = pygame.key.get_pressed()
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        raw_dt: int = self.CLOCK.get_time()
        dt: float = raw_dt * self.FPS

    
        return {
            "events": events,
            "mouse press": mouse_press,
            "keys": keys,
            "mouse pos": mouse_pos,
            "raw_dt": raw_dt,
            "dt": dt,
        }
    
    
    def circle(self, color: str, center: tuple[float, float], radius: float, width: int = 0):
        """
        Draws a circle on the screen.
        """
        pygame.draw.circle(self.screen, color, center, radius, width)

    def debug(self, items: dict):
        """
        Prints the player's position for debugging purposes.
        """
        keys: dict[int, bool] = self.get_events()["keys"]
        if keys[pygame.K_q]:
            print(items["influencer"].pos)
        
    
    def run(self, sphere: "influencer", map: "map"):
        """
        Runs the main game loop.
        """
        while True:

            events: list[pygame.event.Event] = self.get_events()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

            self.screen.fill((0,0,0))
            # self.screen.blit(self.temp_bg, self.cam.get_pos((0, 0)))

            self.debug({"influencer" : sphere})
            
            map.update()

            

            sphere.render(self)
            sphere.update(self)

            self.cam.follow_player(sphere)

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

            pygame.display.set_caption("WOW SREM GAME!!")

