'''
Base class for Powerups
Foundation for Magnets and Invincs
'''

impot pygame

class Powerup(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y): #screenDim is a tuple
        super(Powerup, self).__init__() #why is this line necessary?
        self.powerupLoc = None
        self.isMakingPowerups = True
        self.isPowerup = False
        self.powerupTimer = 0
        self.isPowerupPresent = False
        self.powerupTime = None
        
    @staticmethod
    def getDilation(pt1, pt2, d): #pt1 is dilation pt; pt2 is dilated pt; d is dilation factor
        x3 = d*(pt2[0] - pt1[0]) + pt1[0]
        y3 = d*(pt2[1] - pt1[1]) + pt1[1]
        return (x3,y3)

    def dilate(self, apex):
        self.image = pygame.transform.scale(self.image, (int(self.w * self.dilate), int(self.h * self.dilate)))
        self.x = Powerup.getDilation((apex), (self.x,self.y), self.dilate)[0] 
        self.y = Powerup.getDilation((apex ), (self.x,self.y), self.dilate)[1] 
        self.updateRect()
        
    def addPowerup(self):
        if self.isMakingPowerups:
            pass