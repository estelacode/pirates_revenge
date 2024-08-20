import pygame
from game.support import import_folder

class Tile(pygame.sprite.Sprite):

    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def update(self, shift):
        self.rect.x += shift # shift (desplazamiento)

class StaticTile(Tile):
    def __init__(self,size, x, y, surface):
        super().__init__( size, x, y)
        self.image = surface


  
class Stone_move(StaticTile):
    def __init__(self, size,x,y):
        super().__init__(size,x,y,pygame.image.load('game/assets/images/terrain/stone_m.png').convert_alpha())


class AnimatedTile(Tile):
    
    def __init__(self, size,x,y, path):
         super().__init__( size, x, y)
         self.frames = import_folder(path)
         self.frames_index = 0
         self.image = self.frames[self.frames_index]

    def animate(self):
        self.frames_index += 0.15
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift

class Coin(AnimatedTile):
    def __init__(self, size,x,y, path, price):
        super().__init__(size,x,y,path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
        self.price = price
        
      

class Gem(AnimatedTile):
    def __init__(self, size,x,y, path,price):
        super().__init__(size,x,y,path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
        self.price = price


class Goal(AnimatedTile):
    def __init__(self, size,x,y, path):
        super().__init__(size,x,y,path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
  

class Treasure(AnimatedTile):
    def __init__(self, size,x,y, path,price):
        super().__init__(size,x,y,path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
        self.price = price
    
    def animate(self):
        self.frames_index += 0.02
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]
        
class Liquid(AnimatedTile):
    def __init__(self, size,x,y, path):
        super().__init__(size,x,y,path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))

class Decoration:
    def __init__(self, top, level_width,screen_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + 2*screen_width) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x =  tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192,x,y, 'game/assets/images/decoration')
            self.water_sprites.add(sprite)

    def get_sprite(self):
        return self.water_sprites
    
    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)