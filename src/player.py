import pygame
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, group):
    super().__init__(group)

    self.import_assets()

    # general setup
    self.image = pygame.Surface((32, 64))
    self.image.fill('green')
    self.rect = self.image.get_rect(center = pos)
    self.speed = 200

    # movement
    self.direction = pygame.math.Vector2()
    self.pos = pygame.math.Vector2(self.rect.center)

  def import_assets(self):
    self.animations = {'up': [], 'down' : [], 'right' : [], 'left' : [],
    'right_idle': [], 'left_idle' : [], 'up_idle' : [], 'down_idle' : [],
    'right_hoe': [], 'left_hoe' : [], 'up_hoe' : [], 'down_hoe' : [],
    'right_axe': [], 'left_axe' : [], 'up_axe' : [], 'down_axe' : [],
    'right_water': [], 'left_water' : [], 'up_water' : [], 'down_water' : []}

    for animation in self.animations.keys():
      full_path = '../graphics/character' + animation
      self.animations[animation] = import_folder(full_path)

  def input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
      self.direction.y = -1
    elif keys[pygame.K_s]:
      self.direction.y = 1
    else:
      self.direction.y = 0


    if keys[pygame.K_a]:
      self.direction.x = -1
    elif keys[pygame.K_d]:
      self.direction.x = 1
    else:
      self.direction.x = 0

  def move(self, dt):
    # normalize the vector
    if self.direction.magnitude() > 0:
      self.direction = self.direction.normalize()

    # horizontal movement
    self.pos.x += self.direction.x * self.speed * dt
    self.rect.centerx = self.pos.x
    # vertical movement
    self.pos.y += self.direction.y * self.speed * dt
    self.rect.centery = self.pos.y


  def update(self, dt):
      self.input()
      self.move(dt)