import pygame
from settings import *
from os import path
from pytmx.util_pygame import load_pygame


class SoilLayer:
  def __init__(self, all_sprites):

    # sprite groups
    self.all_sprites = all_sprites
    self.soil_sprites = pygame.sprite.Group()

    # graphics
    soil_path = path.join('graphics', 'soil', 'o.png')
    self.soil_surf = pygame.image.load(soil_path)

    self.create_soil_grid()

    # requirements
  def create_soil_grid(self):

    # if area is farmable
    ground_path = path.join('graphics', 'world', 'ground.png')
    ground = pygame.image.load(ground_path)
    h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

    self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
    tmx_path = path.join('data', 'map.tmx')
    for x, y, _ in load_pygame(tmx_path).get_layer_by_name('Farmable').tiles():
      self.grid[y][x].append('F')
