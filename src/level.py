import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Interaction, Water, WildFlower, Tree
from os import path
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer

class Level:
  def __init__(self):
    # get display surface
    self.display_surface = pygame.display.get_surface()

    # sprite goups
    self.all_sprites = CameraGroup()
    self.collision_sprites = pygame.sprite.Group()
    self.tree_sprites = pygame.sprite.Group()
    self.interaction_sprites = pygame.sprite.Group()

    self.setup()
    self.overlay = Overlay(self.player)
    self.transition = Transition(self.reset, self.player)
    soil_layer = SoilLayer(self.all_sprites)

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
      Tree(
        pos = (obj.x, obj.y),
        surf = obj.image,
        groups = [self.all_sprites, self.collision_sprites, self.tree_sprites],
        name = obj.name,
        player_add = self.player_add)

    # collision tiles
    for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
      Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)


    # player
    for obj in tmx_data.get_layer_by_name('Player'):
      if obj.name == 'Start':
        self.player = Player(
          pos = (obj.x,obj.y),
          group = self.all_sprites,
          collision_sprites= self.collision_sprites,
          tree_sprites = self.tree_sprites,
          interaction = self.interaction_sprites
          )
      # if obj.name == 'Bed':
      #   Interaction(
      #     pos = (obj.x, obj.y),
      #     size = (obj.width, obj.height),
      #     groups = self.interaction_sprites,
      #     name = obj.name
      #   )
      if obj.name == 'Bed':
        Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

    world_path = path.join('graphics', 'world', 'ground')
    Generic(
      pos = (0, 0),
      surf = pygame.image.load(world_path + '.png').convert_alpha(),
      groups = self.all_sprites,
      z = Layers['ground']
    )

  def player_add(self, item):
    self.player.item_inventory[item] += 1

  def reset(self):

    # re-spawn apples
    for tree in self.tree_sprites.sprites():
      for apple in tree.apple_sprites.sprites():
        apple.kill()
      tree.create_fruit()


  def run(self,dt):
    self.display_surface.fill('black')
    self.all_sprites.custom_draw(self.player)
    self.all_sprites.update(dt)

    self.overlay.display()

    if self.player.sleep:
      self.transition.play()

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

          # # anaytics
          # if sprite == player:
          #   pygame.draw.rect(self.display_surface,'red',offset_rect,5)
          #   hitbox_rect = player.hitbox.copy()
          #   hitbox_rect.center = offset_rect.center
          #   pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)
          #   target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
          #   pygame.draw.circle(self.display_surface,'blue',target_pos,5)
