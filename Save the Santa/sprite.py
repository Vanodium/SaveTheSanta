import pygame
import sys
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos_x, self.pos_y = pos_x, pos_y
        #super().__init__(player_group, all_sprites)
        #self.image = player_image
        
    def update(self, direction):
        if direction == 'down':
            self.pos_y -= 1
