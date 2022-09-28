import pygame
from settings import *

class Transition:
  def __init__(self, reset, player) :
    self.display_surface = pygame.display.get_surface() # gives access to the map surfaces
    self.reset = reset
    self.player = player

    # overlay
    self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.color = 255
    self.speed = -1

  def play(self):
    self.color += self.speed
    if self.color <= 0:
      self.speed *= -1
      self.color = 0
      self.reset()
      # some transition screen here?
    if self.color > 255:
      self.color = 255
      self.player.sleep = False
      self.speed = -1

    self.image.fill((self.color, self.color, self.color))
    self.display_surface.blit(self.image, (0, 0), special_flags = pygame.BLEND_RGB_MULT)
