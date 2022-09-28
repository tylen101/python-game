from mimetypes import init
import pygame
from settings import *
from os import path


class SoilLayer:
  def __init__(self, all_sprites):

    # sprite groups
    self.all_sprites = all_sprites
    self.soil_sprites = pygame.sprite.Group()

    # graphics
    soil_path = path('graphics', 'soil', 'o.png')
    self.soil_surf = pygame.image.load(soil_path)

    self.create_soil_grid()

    # requirements
  def create_soil_grid(self):
    # if area is farmable
    ground_path = path('graphics', 'world', 'ground.png')
    ground = pygame.image.load(ground_path)
    h_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE
    # if area has been watered

