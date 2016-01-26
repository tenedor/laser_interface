#!/usr/bin/python
import pygame, sys
from pygame.locals import *
import pygame.camera

pygame.init()
pygame.camera.init()
dimensions = (640, 480)
cam = pygame.camera.Camera("/dev/video0", dimensions)
cam.start()
window = pygame.display.set_mode(dimensions)
image = pygame.Surface(dimensions)

while True:
  cam.get_image(image)
  window.blit(image, (0, 0))
  pygame.display.update()
