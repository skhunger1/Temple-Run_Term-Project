'''
Fire.py

Implements Coin CLass
Uses framework from Lukas Peraza, 2015 for 15-112 Pygame Lecture
https://github.com/LBPeraza/Pygame-Asteroids
'''

import pygame
import math
from GameObject import GameObject

class Fire(GameObject):
    image = pygame.image.load('images/fireArch10.png')
    image = pygame.transform.scale(image, (158,158))
    fireImage = image
    
        
        
    
    def __init__(self, x, y):
        super().__init__(Fire.fireImage, x, y)
        
        self.diameter = 128
        self.dilate = 1.02
        
        self.centerX  = self.x + self.diameter//2
        self.centerY = self.y + self.diameter//2
        
        
        
    @staticmethod
    def getDilation(pt1, pt2, d): #pt1 is dilation pt; pt2 is dilated pt; d is dilation factor
        x3 = d*(pt2[0] - pt1[0]) + pt1[0]
        y3 = d*(pt2[1] - pt1[1]) + pt1[1]
        return (x3,y3)

    def dilate(self, apex):
        self.x = Fire.getDilation((apex), (self.x,self.y), self.dilate)[0] 
        self.y = Fire.getDilation((apex), (self.x,self.y), self.dilate)[1]
        self.diameter *= 1.003
        self.width = self.diameter
        self.height = self.diameter
        self.image = pygame.transform.scale( Fire.fireImage, (int(self.diameter), int(self.diameter)) ) 
        
        self.rect = pygame.Rect(self.x - self.diameter/2, self.y - self.diameter/2, self.diameter, self.diameter)
        
        
    def draw(self, screen):
        self.imgRect = self.image.get_rect()
        self.imgRect.center = (self.centerX, self.centerY)
        screen.blit(self.image, self.imgRect)
        
        
        
    