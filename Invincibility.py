'''
Invincibility powerup
'''

import pygame
import math
from GameObject import GameObject
from Magnet import Magnet
from Coin import Coin

class Invinc(GameObject):
    
    @staticmethod
    def init():
        image = pygame.image.load('images/wings.png')
        image = pygame.transform.scale(image, (60,60))
        Invinc.invincImage = image
    
    def __init__(self, x, y):
        super().__init__(Invinc.invincImage, x, y)
        self.diameter = 60
        self.dilate = 1.02
        
    @staticmethod
    def getDilation(pt1, pt2, d): #pt1 is dilation pt; pt2 is dilated pt; d is dilation factor
        x3 = d*(pt2[0] - pt1[0]) + pt1[0]
        y3 = d*(pt2[1] - pt1[1]) + pt1[1]
        return (x3,y3)

    def dilate(self, apex):
        self.x = Invinc.getDilation((apex), (self.x,self.y), self.dilate)[0] 
        self.y = Invinc.getDilation((apex), (self.x,self.y), self.dilate)[1] 
        self.diameter *= 1.003
        self.image = pygame.transform.scale( Invinc.invincImage, (int(self.diameter), int(self.diameter)) ) 
        
        self.rect = pygame.Rect(self.x - self.diameter/2, self.y - self.diameter/2, self.diameter, self.diameter)