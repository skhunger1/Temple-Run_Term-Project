'''
Player.py

creates player
Uses framework from Lukas Peraza, 2015 for 15-112 Pygame Lecture
https://github.com/LBPeraza/Pygame-Asteroids
'''


import pygame
from GameObject import GameObject

class Player(GameObject):
    
    @staticmethod
    def init():
        Player.playerImage = pygame.image.load('images/man/croprun/run5.png').convert_alpha()
        #46 36
        #102 88
        
    def __init__(self,x,y):
        super().__init__(Player.playerImage, x, y)
            #Game object: takes in self, image, screenDim, screen
            #image needed: 'images/runningManSmall.jpg'
            #defines x, y, image, w, h, screenWidth, screenHeight, velocity
        self.vel = 0
        self.isJump = False
        self.shouldJump = False
        self.shouldJumpIndex = 0
        self.jumpAdd = [-40, -35, -30, -25, -20, -15, -10, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 15, 20, 25, 30, 35, 40]  
        self.isSlide = False
        self.jumpIndex = 0
        self.right = True
        self.left = True
        self.runningImages = [pygame.transform.scale(pygame.image.load('images/man/croprun/run6.png'), (86,180)),
                                pygame.transform.scale(pygame.image.load('images/man/croprun/run7.png'), (86,180)),
                                pygame.transform.scale(pygame.image.load('images/man/croprun/run9.png'), (86,180)),
                                pygame.transform.scale(pygame.image.load('images/man/croprun/run10.png'), (86,180)),
                                pygame.transform.scale(pygame.image.load('images/man/croprun/run11.png'), (86,180)),
                                pygame.transform.scale(pygame.image.load('images/man/croprun/run12.png'), (86,180)),
                                pygame.transform.scale(pygame.image.load('images/man/croprun/run13.png'), (86,180)),
                                pygame.transform.scale(pygame.image.load('images/man/croprun/run14.png'), (86,180)),
                                pygame.transform.scale(pygame.image.load('images/man/croprun/run15.png'), (86,180)),
                                pygame.transform.scale(pygame.image.load('images/man/croprun/run16.png'), (86,180))  ]
                                
        self.slidingImages = []

        
        
    def moveRight(self, width):
        if self.x < width - 10:
            self.x += 5
            self.updateRect()
            
    def moveLeft(self, width):
        if self.x > 10:
            self.x -= 5
            self.updateRect()
            
            
            
    #### AI FUNCTIONS ####
    
    
    def AIgetCoins(self, coinLoc, width):
          
        if coinLoc == "middle":
            if self.x > width//2:
                    Player.moveLeft(self, width)
                    
            elif self.x < width//2:
                    Player.moveRight(self, width)
                    
        #right at 717
        if coinLoc == "right":
            if self.x > 717:
                    Player.moveLeft(self, width)
                    
            elif self.x < 717:
                    Player.moveRight(self, width)
        
        #left at 237
        if coinLoc == "left":
            if self.x > 237:
                    Player.moveLeft(self, width)
                    
            elif self.x < 237:
                    Player.moveRight(self, width)
                    
    def AIdetectHoles(self, holes):
        if len(holes) > 0:
            for hole in holes:
                bottom = hole.centerY + hole.height//2
                if bottom > self.y - 20:
                    self.isJump = True
                    self.jumpIndex = 0
                    
                    
    def AIexecuteJump(self):
        if self.isJump:
            if self.jumpIndex < len(self.jumpAdd): 
    
                self.y += self.jumpAdd[self.jumpIndex]
                self.updateRect()
                self.jumpIndex += 1
                
            elif self.jumpIndex >= len(self.jumpAdd):
                self.isJump = False
                self.jumpIndex = 0
                self.left = True
                self.right = True
                
    def jump(self, d):
        self.y += d
            
