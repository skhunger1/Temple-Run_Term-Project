import pygame
import math

class Hole(object):

    def __init__(self, topLeftX, topLeftY): #x,y 
        image = pygame.image.load('images/hole.png').convert_alpha()
        image = pygame.transform.scale(image, (128,44))
        
        self.image = image
        self.dilate = 1.02
        
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        
        self.width = 128
        self.height = 44
        
        self.centerX = self.topLeftX + self.width/2
        self.centerY = self.topLeftY + self.height/2
        
        
    @staticmethod
    def getDilation(pt1, pt2, d): #pt1 is dilation pt; pt2 is dilated pt; d is dilation factor
        x3 = d*(pt2[0] - pt1[0]) + pt1[0]
        y3 = d*(pt2[1] - pt1[1]) + pt1[1]
        return (x3,y3)

    def dilate(self, apex):
        self.image = pygame.transform.scale(self.image, (int(self.width * self.dilate), int(self.height * self.dilate)))
        self.centerX = Hole.getDilation((apex), (self.centerX,self.centerY), self.dilate)[0] 
        self.centerY = Hole.getDilation((apex), (self.centerX,self.centerY), self.dilate)[1] 
        self.updateRect()
        
    def draw(self, screen):
        self.imgRect = self.image.get_rect()
        self.imgRect.center = (self.centerX, self.centerY)
        screen.blit(self.image, self.imgRect)
        
    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.imgRect = pygame.Rect(self.centerX - self.width / 2, self.centerY - self.height / 2, self.width, self.height)

        
        

