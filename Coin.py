'''
Coin.py

Implements Coin CLass
Uses framework from Lukas Peraza, 2015 for 15-112 Pygame Lecture
https://github.com/LBPeraza/Pygame-Asteroids
'''

import pygame
import math
from GameObject import GameObject

class Coin(GameObject):
    
    @staticmethod
    def init():
        image = pygame.image.load('images/newCoin.png')
        image = pygame.transform.scale(image, (40,40))
        Coin.coinImage = image
    
    def __init__(self, x, y):
        super().__init__(Coin.coinImage, x, y)
        self.diameter = 40
        self.dilate = 1.02
        
    @staticmethod
    def getDilation(pt1, pt2, d): #pt1 is dilation pt; pt2 is dilated pt; d is dilation factor
        x3 = d*(pt2[0] - pt1[0]) + pt1[0]
        y3 = d*(pt2[1] - pt1[1]) + pt1[1]
        return (x3,y3)

    def dilate(self, apex):
        self.x = Coin.getDilation((apex), (self.x,self.y), self.dilate)[0] 
        self.y = Coin.getDilation((apex), (self.x,self.y), self.dilate)[1] 
        self.diameter *= 1.003
        self.image = pygame.transform.scale( Coin.coinImage, (int(self.diameter), int(self.diameter)) ) 
        
        self.rect = pygame.Rect(self.x - self.diameter/2, self.y - self.diameter/2, self.diameter, self.diameter)
        

        
        
    