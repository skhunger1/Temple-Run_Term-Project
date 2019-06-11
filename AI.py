'''
AI Powerup
'''

import pygame
import math
from GameObject import GameObject
from Coin import Coin

class AI(GameObject):
    
    @staticmethod
    def init():
        image = pygame.image.load('images/AI.png')
        image = pygame.transform.scale(image, (60,60))
        AI.AIImage = image
    
    def __init__(self, x, y):
        super().__init__(AI.AIImage, x, y)
        self.diameter = 60
        self.dilate = 1.02
        
    @staticmethod
    def getDilation(pt1, pt2, d): #pt1 is dilation pt; pt2 is dilated pt; d is dilation factor
        x3 = d*(pt2[0] - pt1[0]) + pt1[0]
        y3 = d*(pt2[1] - pt1[1]) + pt1[1]
        return (x3,y3)

    def dilate(self, apex):
        self.x = AI.getDilation((apex), (self.x,self.y), self.dilate)[0] 
        self.y = AI.getDilation((apex), (self.x,self.y), self.dilate)[1] 
        self.diameter *= 1.003
        self.image = pygame.transform.scale( AI.AIImage, (int(self.diameter), int(self.diameter)) ) 
        
        self.rect = pygame.Rect(self.x - self.diameter/2, self.y - self.diameter/2, self.diameter, self.diameter)