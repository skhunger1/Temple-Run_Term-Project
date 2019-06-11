'''
Road.py

creates road
Uses framework from Lukas Peraza, 2015 for 15-112 Pygame Lecture
https://github.com/LBPeraza/Pygame-Asteroids
'''


import pygame
import math

class Road(object):
    def __init__(self, screenDim, screen):
        self.angle = math.pi / 6
        self.color = (200,200,0)
        self.screenWidth, self.screenHeight = screenDim
        self.screen = screen
        self.types = [pygame.image.load('images/roads/roadstrips_1.png'), 
                            pygame.image.load('images/roads/roadstrips_2.png'),
                            pygame.image.load('images/roads/roadstrips_3.png'),
                            pygame.image.load('images/roads/roadstrips_4.png')]
        
        self.k = 5 #width of merge                    
        
        
    def draw(self):
        pygame.draw.polygon(self.screen, self.color, [(0,self.screenHeight),
                                              (self.screenWidth,self.screenHeight),
                                              (self.screenWidth//2, self.screenHeight - self.screenWidth * math.tan(self.angle))], 0)
    
    def drawMerge(self):
        pygame.draw.rect(self.screen, self.color, [0,169,954,self.k], 0)
        
    def drawSkinnyMerge(self):
        pygame.draw.rect(self.screen, self.color, [0,169,954,self.k-45], 0)

        
    def drawTopTriangle(self):
        pygame.draw.polygon(self.screen, self.color, [(0,self.screenHeight),
                                              (self.screenWidth,self.screenHeight),
                                              (self.screenWidth//2, self.screenHeight - self.screenWidth * math.tan(self.angle))], 0)
                                              
    def drawBlockMerge(self):
        pygame.draw.rect(self.screen, self.color, [100+self.k,169,954,self.k], 0)
        
        
        