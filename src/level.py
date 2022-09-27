import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from os import path
from pytmx.util_pygame import load_pygame
from support import *


class Level:
  def __init__(self):
    # get display surface
    self.display_surface = pygame.display.get_surface()

    # sprite goups
    self.all_sprites = CameraGroup()
    self.collision_sprites = pygame.sprite.Group()

    self.setup()
    self.overlay = Overlay(self.player)

  def setup(self):
    # load map
    map_path = path.join('data','map')
    tmx_data = load_pygame(map_path + '.tmx')

####################clean up later#####################
    # house
    for layer in ['HouseFloor', 'HouseFurnitureBottom']:
      for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
        Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, Layers['house bottom'])

    for layer in ['HouseWalls', 'HouseFurnitureTop']:
      for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
        Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, Layers['main'])

    # fence
    for layer in ['Fence']:
      for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
        Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

    # water
    water_path = path.join('graphics', 'water')
    water_frames = import_folder(water_path)
    for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
      Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

    # wildflowers
    for obj in tmx_data.get_layer_by_name('Decoration'):
      WildFlower((obj.x, obj.y), obj.image,  [self.all_sprites, self.collision_sprites])

    # trees
    for obj in tmx_data.get_layer_by_name('Trees'):
      Tree((obj.x, obj.y), obj.image,  [self.all_sprites, self.collision_sprites], obj.name)

    # collision tiles
    for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
      Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)


    # player
    for obj in tmx_data.get_layer_by_name('Player'):
      if obj.name == 'Start':
        self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites)

    world_path = path.join('graphics', 'world', 'ground')
    Generic(
      pos = (0, 0),
      surf = pygame.image.load(world_path + '.png').convert_alpha(),
      groups = self.all_sprites,
      z = Layers['ground']
    )



  def run(self,dt):
    self.display_surface.fill('black')
    self.all_sprites.custom_draw(self.player)
    self.all_sprites.update(dt)


    self.overlay.display()

class CameraGroup(pygame.sprite.Group):
  def __init__(self):
    super().__init__()

    self.display_surface = pygame.display.get_surface()
    self.offset = pygame.math.Vector2()

  def custom_draw(self, player):
    self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
    self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

    for layer in Layers.values():
      for sprite in sorted(self.sprites(), key = lambda sprite : sprite.rect.centery):
        if sprite.z == layer:
          offset_rect = sprite.rect.copy()
          offset_rect.center -= self.offset
          self.display_surface.blit(sprite.image, offset_rect)
