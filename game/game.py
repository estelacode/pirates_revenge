from importlib import resources
import pygame
from game.config import Config
from game.support import import_csv_layout, import_cut_graphics
from game.tiles import Tile, StaticTile,Stone_move, Liquid, Coin , Treasure, Gem, Decoration,Goal
from game.enemy import Enemy 
from game.player import Player
from game.bars import Bars
from game.button import Button

class Game:

    def __init__(self):
      
        pygame.init() 
        
        # screen setup     
        self.__screen_width = Config.instance().data["screen_width"]
        vertical_tile_number =  Config.instance().data["vertical_tile_number"]
        self.__tile_size   = Config.instance().data["tile_size"]
        self.__screen_height = vertical_tile_number * self.__tile_size   
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        self.__screen_title = Config.instance().data["game_tile"]
        pygame.display.set_caption(self.__screen_title) 
    
        self.__running = False
        
        #game attributes setup
        self.attributes_setup()
        # level elements setup 
        self.level_setup()
        # initial menu setup 
        self.menu_setup()
        # music setup 
        self.music_setup()
        
        
        
    def run(self):

        self.__running = True
        while self.__running:
            delta_time = self.__fps_clock.tick(Config.instance().data["fps"])
            self.__process_events() 
            self.__update(delta_time) 
            self.__render() 
        self.__quit() 

    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.__running = False

    def __update(self,delta_time):
      
        self.terrain_sprites.update(self.world_shift)
        self.gem_sprites.update(self.world_shift)
        self.stone_move_sprites.update(self.world_shift)
        self.coin_sprites.update(self.world_shift)
        self.liquid_sprites.update(self.world_shift)
        self.treasure_sprites.update(self.world_shift)
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.goal_sprites.update(self.world_shift)
        self.player.update()
           
     
        self.check_reward_collision(self.treasure_sprites)
        self.check_reward_collision(self.coin_sprites)
        self.check_reward_collision(self.gem_sprites)
        self.check_enemy_collision()
        self.enemy_collision_reverse()
        self.check_liquid_collision()
        self.check_play_health()   
        self.horizontal_mov_collision()
        self.vertical_mov_collision()
        self.check_decoration_collision()
        self.check_goal_collision()
        self.scroll_x()       
        
        
    
    def __render(self):

        self.__screen.fill(Config.instance().data["background_color"])
        self.__screen.blit( self.__bg,(0,0))  
            
        if self.main_menu == True:
            self.menu_music.play(loops=-1)
            if self.exit_button.draw(self.__screen) :
                self.__running = False
            if self.start_button.draw(self.__screen) :
                self.main_menu = False    
                self.menu_music.stop()   
                self.game_music.play(loops=-1)
        else: 
         
            # draw bars
            self.__bars.draw_health(self.__cur_health,self.__max_health)
            self.__bars.draw_score(self.__score)
            # draw tiles 
            self.terrain_sprites.draw(self.__screen)
            self.liquid_sprites.draw(self.__screen)
            self.gem_sprites.draw(self.__screen)
            self.stone_move_sprites.draw(self.__screen)
            #draw rewards
            self.coin_sprites.draw(self.__screen)
            self.goal_sprites.draw(self.__screen)
            self.treasure_sprites.draw(self.__screen)
            # draw enemies
            self.enemy_sprites.draw(self.__screen)
            #draw player
            self.player.draw(self.__screen)
            #draw decoration
            self.decoration.draw(self.__screen, self.world_shift)
            
            # if player has died, reseat nivel, puntos, salud y flag de game a over a 0
            if self.game_over == -1:
                if self.restart_button.draw(self.__screen):
                    self.attributes_setup()
                    self.level_setup()  
                    self.game_music.play(loops=-1)       
            
            if self.game_over == 2:    
               self.main_menu = True
                
        pygame.display.update()
  
    def __quit(self): 
        pygame.quit() 
  
 
        
    def create_tiles(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * self.__tile_size  
                    y = row_index * self.__tile_size  

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('game/assets/images/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(self.__tile_size   , x, y, tile_surface)
                    
                    if type == 'liquids':
                       if value == '0': sprite = Liquid(self.__tile_size   ,x,y, 'game/assets/images/liquid/water')
                       if value == '1': sprite = Liquid(self.__tile_size   ,x,y, 'game/assets/images/liquid/lava')    
                        
                    if type == 'gems':
                        if value == '0': sprite = Gem(self.__tile_size   ,x,y, 'game/assets/images/gem/white',100)
                        if value == '1': sprite = Gem(self.__tile_size   ,x,y, 'game/assets/images/gem/red',50)
                        if value == '2': sprite = Gem(self.__tile_size   ,x,y, 'game/assets/images/gem/blue',20)
                       
                    if type == 'stone_move':
                        sprite = Stone_move(self.__tile_size   ,x,y)

                    if type == 'coins':
                        if value == '0': sprite = Coin(self.__tile_size   ,x,y, 'game/assets/images/coins/gold',5)
                        if value == '1': sprite = Coin(self.__tile_size   ,x,y, 'game/assets/images/coins/silver',1)

                    if type == 'treasure':
                        sprite = Treasure(self.__tile_size   ,x,y, 'game/assets/images/treasure',500)
                        
                    if type == 'enemies':
                        sprite = Enemy(self.__tile_size   ,x,y)

                    if type == 'constraint':
                        sprite = Tile(self.__tile_size   ,x,y)
                    
                    if type == 'goal':
                        sprite = Goal(self.__tile_size   ,x,y,'game/assets/images/goal')
                        
                    
                    sprite_group.add(sprite)

        return sprite_group

    def create_player(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                x = col_index * self.__tile_size 
                y = row_index * self.__tile_size 
                if value == '0':
                    sprite = Player((x,y), self.__screen, self.__cur_health)
                    self.player.add(sprite)
        
    def level_setup(self):
        
        level_data = Config.instance().data["level_0"]
        
        # player setup
        self.player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.create_player( self.player_layout)
        # terrains setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tiles(terrain_layout,'terrain')    
        #liquid setup
        liquid_layout = import_csv_layout(level_data['liquids'])
        self.liquid_sprites = self.create_tiles(liquid_layout,'liquids') 
        # gems setup
        gem_layout = import_csv_layout(level_data['gems'])
        self.gem_sprites = self.create_tiles(gem_layout,'gems')
        # stone move setup
        stone_move_layout = import_csv_layout(level_data['stone_move'])
        self.stone_move_sprites = self.create_tiles(stone_move_layout,'stone_move')
        # coins setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tiles(coin_layout,'coins')
        # treasure setup
        treasure_layout = import_csv_layout(level_data['treasure'])
        self.treasure_sprites = self.create_tiles(treasure_layout,'treasure')
        # enemies setup
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tiles(enemy_layout,'enemies')
        # enemis constraints setup
        constraint_layout = import_csv_layout(level_data['constraint'])
        self.constraint_sprites = self.create_tiles(constraint_layout,'constraint')
        # decoration water
        level_width = len(terrain_layout[0] * self.__tile_size  )
        self.decoration = Decoration(self.__screen_height - 40, level_width,self.__screen_width)
        # next level
        goal_layout = import_csv_layout(level_data['goal'])
        self.goal_sprites = self.create_tiles(goal_layout,'goal')
        
        with resources.path(Config.instance().data["background"]["bg_path"],Config.instance().data["background"]["filename"]) as bg_path:
             self.__bg = pygame.image.load(bg_path).convert()
                 
    def menu_setup(self):
        self.main_menu = True
        restart_img = pygame.image.load('game/assets/images/restart_btn.png')
        start_img = pygame.transform.scale(pygame.image.load('game/assets/images/start_btn.png'), (self.__tile_size *4, self.__tile_size *2))
        exit_img = pygame.transform.scale(pygame.image.load('game/assets/images/exit_btn.png'), (self.__tile_size *4, self.__tile_size *2))
        self.restart_button = Button( self.__screen_width //2 - 50,   self.__screen_height // 2 +100, restart_img)
        self.start_button = Button( self.__screen_width //2 - 250,   self.__screen_height // 2, start_img)
        self.exit_button = Button( self.__screen_width //2 + 100,   self.__screen_height // 2, exit_img)          
        
    def music_setup(self):
        self.menu_music = pygame.mixer.Sound('game/assets/audio/overworld_music.wav')
        self.game_music = pygame.mixer.Sound('game/assets/audio/level_music.wav')
        self.coin_sound = pygame.mixer.Sound('game/assets/audio/effects/coin.wav')
        self.stomp_sound = pygame.mixer.Sound('game/assets/audio/effects/stomp.wav')
        self.hit_sound = pygame.mixer.Sound('game/assets/audio/effects/hit.wav')
 
    def attributes_setup(self):
        self.__fps_clock = pygame.time.Clock()
        self.__score = 0
        self.__max_health = 100
        self.__cur_health = 100
        self.__bars = Bars(self.__screen)
        self.world_shift = 0
        self.current_x = None
        self.game_over = 0

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()
             

                
    def horizontal_mov_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.stone_move_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left  and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right  and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_mov_collision(self):
        player = self.player.sprite
        if self.game_over == 0:
            player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.stone_move_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling =  False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < self.__screen_width /4 and direction_x < 0:      
            self.world_shift = 8
            player.speed = 0
        elif player_x > self.__screen_width - (self.__screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0 
            player.speed = 8
            
    def change_score(self,amount):
        self.__score += amount
        
    def check_reward_collision(self, element_sprites):
        collided_element = pygame.sprite.spritecollide(self.player.sprite,element_sprites,True)
        if collided_element:
            self.coin_sound.play()
            for element in collided_element:
                self.change_score(element.price) 
    
    def check_goal_collision(self):
        goal_collisions= pygame.sprite.spritecollide(self.player.sprite,self.goal_sprites,False)
        if goal_collisions :
            self.game_over = 2
           
    def check_enemy_collision(self):
        enemies_collisions= pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
        if enemies_collisions :
            for enemy in enemies_collisions:
                
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
               
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    # El jugador mata al enemigo
                    self.player.sprite.direction.y = -15
                    enemy.kill()
                    self.stomp_sound.play()
                else:
                  # El enemigo daña al jugador
                    self.player.sprite.get_damage() # el jugador se daña
                    self.__cur_health = self.player.sprite.get_health() 
                    self.hit_sound.play()
    
    def check_liquid_collision(self):
        liquids_collisions= pygame.sprite.spritecollide(self.player.sprite,self.liquid_sprites,False)
        if liquids_collisions: 
            # Si colisionas con lava o agua, se muere 
            self.game_over = -1
            self.__cur_health = 0
            self.player.sprite.get_killed()
            self.game_music.stop()

    def check_decoration_collision(self):
        decoration_collision= pygame.sprite.spritecollide(self.player.sprite, self.decoration.get_sprite(),False)
        if decoration_collision: 
            # Si colisionas con lava o agua, se muere 
            self.game_over = -1
            self.__cur_health = 0
            self.player.sprite.get_killed()
            self.game_music.stop()
            
    def check_play_health(self):
        if self.__cur_health <= 0 :
            # Si el jugador se queda sin salud, se muere
            self.game_over = -1
            self.__cur_health = 0
            self.player.sprite.get_killed()
            self.game_music.stop()
            
