import pygame
from classes import *


cam = camera()
app = Game(cam)
sphere = influencer()

uteres = map(app, sphere, cam)

app.run(sphere, uteres)