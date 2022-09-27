from pygame.math import Vector2

# screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# tile size
TILE_SIZE = 64

# overlay positions
OVERLAY_POSITIONS = {
  'tool' : (40, SCREEN_HEIGHT - 15),
  'seed' : (99, SCREEN_HEIGHT - 5)
}



Layers = {
  'water' : 0,
  'ground' : 1,
  'soil' : 2,
  'soil water' : 3,
  'rain floor' : 4,
  'house bottom' : 5,
  'ground plant' : 6,
  'main' : 7,
  'house top' : 8,
  'fruit' : 9,
  'rain drops' : 10,
}
