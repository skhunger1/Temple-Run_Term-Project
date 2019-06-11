'''
GameObject.py

implements base for objects in the game
Uses framework from Lukas Peraza, 2015 for 15-112 Pygame Lecture
https://github.com/LBPeraza/Pygame-Asteroids
'''


import pygame

class GameObject(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y): #screenDim is a tuple
        #Game object: x, y, image, w, h, screenWidth, screenHeight
        super(GameObject, self).__init__() #why is this line necessary?

        self.x = x
        self.y = y

        
        self.image = image
        self.w, self.h = self.image.get_size() 

        self.rect = pygame.Rect(self.x - self.w/2, self.y - self.h/2, self.w, self.h)

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - self.w / 2, self.y - self.h / 2, self.w, self.h)

        
    
        
        
        