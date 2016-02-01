#!/usr/bin/python
import pygame, sys
from pygame.locals import *
from pygame.surfarray import *
import pygame.camera

pygame.init()
pygame.camera.init()
dimensions = (640, 480)
cam = pygame.camera.Camera("/dev/video0", dimensions)
cam.start()
window = pygame.display.set_mode(dimensions)
image = pygame.Surface(dimensions, depth=32)

while True:
  cam.get_image(image)

  #pixels = pixels3d(image)
  """
  i = 0
  for x in range(dimensions[0]):
    for y in range(dimensions[1]):
      #i = i + 1
      if pixels[x][y][0] > 200:
        pixels[x][y][0] = 0
        pixels[x][y][1] = 0
        pixels[x][y][2] = 255
  """
  #print pixels
  #del pixels

  window.blit(image, (0, 0))
  pygame.display.update()
