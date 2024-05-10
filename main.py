import pygame
from classes import *


cam = camera()
app = Game(cam)
sphere = influencer()

app.run(sphere);