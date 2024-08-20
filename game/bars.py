
import pygame

class Bars:
    def __init__(self, screen):
        # setup
        self.display_surface = screen

        # health
        self.health_bar = pygame.image.load('game/assets/images/graphic/health_bar.png').convert_alpha()
        self.health_bar_top_left = (54,39)
        self.bar_max_witdh = 152
        self.bar_height = 4

        # score 
        self.coin = pygame.image.load('game/assets/images/graphic/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft =(50,61))
        self.font = pygame.font.Font('game/assets/images/graphic/ARCADEPI.TTF',30)

    def draw_health(self, current, full):
        self.display_surface.blit(self.health_bar,(20,10))
        current_health_ratio = current /full
        current_bar_width = self.bar_max_witdh * current_health_ratio
        health_bar_rect = pygame.Rect(( self.health_bar_top_left),(current_bar_width,self.bar_height ))
        pygame.draw.rect(self.display_surface,'#dc4949',health_bar_rect)
        
        
    def draw_score(self, score):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surf = self.font.render(str(score), False, '#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = ( self.coin_rect.right+4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)
        