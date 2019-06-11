'''
Game.py

Actually implements the game
Uses framework from Lukas Peraza, 2015 for 15-112 Pygame Lecture
https://github.com/LBPeraza/Pygame-Asteroids
'''

import pygame
import math
import random
from pathlib import Path
import operator



from Player import Player 
from Road import Road 
from Coin import Coin 
from Hole import Hole
from Magnet import Magnet
from Invincibility import Invinc
from Leaderboard import Leaderboard
from AI import AI
from pygamegame import PygameGame


class Game(PygameGame):
    def init(self):
        pygame.mixer.init()
        self.timer = 0
        self.score = 0
    
        self.splash = pygame.image.load('images/splash.png')
        self.bg2 = pygame.transform.scale(pygame.image.load('images/base2.jpg'), (954,720))
        
        self.helpScreens = [pygame.image.load('images/help/help1.png'), 
                            pygame.image.load('images/help/help2.png')]
                            
        self.rightRail = pygame.image.load('images/rightrail2.png')
        self.leftRail = pygame.image.load('images/leftrail2.png')
        self.topRail = pygame.transform.scale(pygame.image.load('images/toprail.png'), (954, 720))
        self.fog = pygame.transform.scale(pygame.image.load('images/fog3.png').convert_alpha(), (960,200))

        self.mode = "Splash" #see redrawAll for possible modes     

        self.enteredName = ""
        self.leaderboard = Leaderboard() 
        #has path, enterNameBase, leaderboardBase
        
        
        #jumping action
        self.jumpAdd = [-40, -35, -30, -25, -20, -15, -10, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 15, 20, 25, 30, 35, 40]  
        
        #MERGING ACTION
        self.isMerge = False
        self.mergeTime = None
        
        #ROAD
        self.road = Road((self.width, self.height), self.screen)
        self.roadTimer = 0
        
        self.apex = (self.width//2, self.height-self.width * math.tan(math.pi / 6))
        self.middleApex = (self.width//2, self.height-self.width * math.tan(math.pi / 6))

        self.leftApex = (483.25, 180.033160740402)
        self.rightApex = (470.75, 180.033160740402)
        
        #CHARACTER
        Player.init()
        player = Player(self.width//2, 8 * self.height//10)
        self.playerGroup = pygame.sprite.GroupSingle(player)
        self.man = self.playerGroup.sprite
        self.runningManTimer = 0
        
        
        #COINS
        Coin.init()
        self.coins = pygame.sprite.Group()
        self.coinLoc = None
        self.isMakingCoins = True
        
        #GENERAL POWERUPS
        self.powerupTime = random.randint(550, 700)
        self.powerupChoices = ["magnets", "invincs"]
        self.powerupTimer = 0
        
        #MAGNETS
        Magnet.init()
        self.magnets = pygame.sprite.Group()
        self.magnetLoc = None
        self.isMakingMagnets = True
        self.isMagnetic = False
        self.magneticTimer = 0
        self.isMagnetPresent = (len(self.magnets) > 0)
        
        
        #INVINCS
        Invinc.init()
        self.invincs = pygame.sprite.Group()
        self.invincLoc = None
        self.isMakingInvincs = False
        self.isInvinc = False
        self.invincTimer = 0
        self.isInvincPresent = (len(self.invincs) > 0)
        
        #AI
        AI.init()
        self.AIs = pygame.sprite.Group()
        self.AILoc = None
        self.isMakingAIs = False
        self.isAI = False
        self.AITimer = 0
        self.isAIPresent = (len(self.AIs) > 0)
        self.AITime = random.randint(900,1000)
        
        
        #HOLES
        self.holes = []
        self.isHolePresent = False
        self.isMakingHoles = True
        self.holeTime = None
        
        #DEATH
        self.deadScreens = [pygame.image.load('images/dead/burnt.png'), 
                            pygame.image.load('images/dead/crevice.png'),
                            pygame.image.load('images/dead/didntSlide.png'),
                            pygame.image.load('images/dead/ranOff.png')]
                            
        #SOUNDS
        #https://www.youtube.com/watch?v=WzQEbRAZJRE
        pygame.mixer.music.load('sounds/soundtrack.mp3') 
        pygame.mixer.music.set_volume(0.1)
        #https://www.sounds-resource.com/mobile/templerun/sound/6075/
        self.invincSound = pygame.mixer.Sound('sounds/angelWings.wav')
        self.coinSound = pygame.mixer.Sound('sounds/coin.wav')
        self.gruntJumpSound = pygame.mixer.Sound('sounds/gruntJump.wav')
        self.gruntJumpLandSound = pygame.mixer.Sound('sounds/gruntJumpLand.wav')
        self.magnetSound = pygame.mixer.Sound('sounds/magnet.wav')
        self.AISound = pygame.mixer.Sound('sounds/shimmer.wav')
        self.splashSound = pygame.mixer.Sound('sounds/splash.wav')
        self.splatSound = pygame.mixer.Sound('sounds/splat.wav')
        self.turnSound = pygame.mixer.Sound('sounds/footstepsTurn.wav')
        
        self.mouseClick = pygame.mixer.Sound('sounds/mouseClick.wav')
        
        
        
    def resetPlay(self):
        self.isMerge = False #turned left or right
        self.isMakingCoins = True
        self.isMakingHoles = True
        self.isMakingAIs = True
        self.road.k = 5
        
        self.man.x = self.width // 2
        self.man.y = 8 * self.height//10
        self.man.updateRect()
        self.runningManTimer = 0
        
        powerupChoice = random.choice(["magnet", "invinc"])
        Game.pickPowerup(self, powerupChoice)
        
        for coin in self.coins:
            self.coins.remove(coin)
        for magnet in self.magnets:
            self.magnets.remove(magnet)
        for invinc in self.invincs:
            self.invincs.remove(invinc)

        self.mode = "Play"
        pygame.mixer.music.play(-1)  #PLAY MUSIC HERE
        
    def mergeShutDown(self):
        self.isMakingCoins = False
        self.isMakingMagnets = False
        self.isMakingInvincs = False
        self.isMakingHoles = False
        self.isMakingAIs = False

    def mousePressed(self, x, y):
        deadScreens = ["GameOverFell", "GameOverNoJump", "GameOverNoSlide"]
        if self.mode == "Splash" and 330 < x < 695 and 350 < y < 458:
            self.mouseClick.play()
            self.mode = "Play"
            pygame.mixer.music.play(-1)
            
        elif self.mode == "Splash" and 330 < x < 695 and 517 < y < 633:
            self.mode = "Help1"
            self.mouseClick.play()
            
            
        elif self.mode == "Help1" and 582 < x < 845 and 550 < y < 636:
            self.mode = "Help2"
            self.mouseClick.play()
            
        elif self.mode == "Help2" and 582 < x < 845 and 550 < y < 636:
            self.mode = "Play"
            self.mouseClick.play()
            pygame.mixer.music.play(-1)
            
        elif self.mode in deadScreens:
            if 45 < x < 440 and 550 < y < 680:
                self.mouseClick.play()
                self.score = 0
                self.resetPlay()
                self.mode = "Play"
                self.isMagnetic = False
                self.isInvinc = False
                self.isAI = False
            elif 500 < x < 895 and 550 < y < 680:
                self.mode = "EnterName"
                self.mouseClick.play()

        if self.mode == "Leaderboard" and 241 < x < 636 and 551 < y < 683:
            self.mouseClick.play()
            self.score = 0
            self.resetPlay()
            self.mode = "Play"
            self.isMagnetic = False
            self.isInvinc = False
            self.isAI = False
            
    def keyPressed(self, code, mod):
        deadScreens = ["GameOverFell", "GameOverNoJump", "GameOverNoSlide"]
        
        if self.mode == "Play":

            #finish this by limiting k; and push sprite up the page; if sprite doesn't
            #turn by a certain point up the page, flash Game Over
            if self.isMerge:
                if code == pygame.K_a: 
                    self.turnSound.play()
                    self.resetPlay()
                    self.mode = "Play"
            
            if self.isMerge: 
                if code == pygame.K_d:  #turn right
                    self.turnSound.play()
                    self.resetPlay()
                    self.mode = "Play"
                
            if code == pygame.K_UP: #JUMP
                self.man.isJump = True
                self.gruntJumpSound.play()
                self.man.jumpIndex = 0
                self.man.left = False
                self.man.right = False
                
            if code == pygame.K_DOWN: #SLIDE
                self.man.isSlide = True
                
            if code == pygame.K_o:
                self.isAI = not(self.isAI)
                
            #TESTING PURPOSES#
            
            if code == pygame.K_h and not(self.isHolePresent):
                self.isHolePresent = True
                self.holes.append(Hole(412, 250))
                
            if code == pygame.K_m: 
                self.isMerge = True
                self.isMakingCoins = False
                self.isMakingMagnets = False
                self.isMakingInvincs = False
                self.isMakingHoles = False
                
        elif self.mode == "EnterName":
            if 97 <= code <= 122: #is lowercase alpha
                self.enteredName += pygame.key.name(code)
                
            elif code == pygame.K_BACKSPACE:
                while len(self.enteredName) >= 1:
                    self.enteredName = self.enteredName[:-1]
            if code == pygame.K_RETURN:
                Leaderboard.editLeaderboard(self.leaderboard, self.enteredName, self.score)
                self.enteredName = ""
                self.score = 0
                self.mode = "Leaderboard"
                

    def pickPowerup(self, powerupChoice):
        if powerupChoice == "magnet":
            self.isMakingMagnets = True
            self.isMakingInvincs = False
            
        else:
            self.isMakingMagnets = False
            self.isMakingInvincs = True        

            
    
    def timerFired(self, dt):

        if self.mode == "Play":

            self.timer += 1
            
            if self.timer % 4 == 0:
                self.roadTimer += 1
            
            if self.timer % 4 == 0:
                self.runningManTimer += 1
                
            if not(self.isMerge):
                self.powerupTimer += 1
                
            #POWERUP TIMING
            if self.powerupTimer % 700 == 0:
                powerupChoice = random.choice(["magnet", "invinc"])
                self.powerupTime = random.randint(550, 700)
                
                if powerupChoice == "magnet":
                    self.isMakingMagnets = True
                    self.isMakingInvincs = False
                    
                else:
                    self.isMakingMagnets = False
                    self.isMakingInvincs = True
                    
            #AI TIMING
            if self.powerupTimer % 1000 == 0:
                self.AITime = random.randint(900, 1000)
                
                    
                
            #COIN WORK
            if self.timer > 50:
                if self.isMakingCoins and not(self.isMerge): 
                    if len(self.coins) < 1:
                        self.coinLoc = random.choice(["middle", "left", "right"])
                        
                        if self.coinLoc == "middle" and not(self.isMerge):
                            initialX = self.middleApex[0]
                            initialY = self.middleApex[1] + 10
                            dx = 0
                            dy = 2
                            for i in range(5):
                                self.coins.add(Coin(initialX + i*dx, initialY + i*dy))
                            
                        elif self.coinLoc == "left" and not(self.isMerge):
                            initialX = 477
                            initialY = 169.207843193097 + 25
                            dx = -1.1547005
                            dy = 2
                            numCoins = random.randint(5,8)
                            for i in range(numCoins):
                                self.coins.add(Coin(initialX + i*dx, initialY + i*dy))
                            
                        elif self.coinLoc == "right" and not(self.isMerge):
                            initialX = 477
                            initialY = 169.207843193097 + 25
                            dx = 1.1547005
                            dy = 2
                            numCoins = random.randint(5,8)
                            for i in range(numCoins):
                                self.coins.add(Coin(initialX + i*dx, initialY + i*dy))
            
            #dilate the coins
            for coin in self.coins:
                if self.coinLoc == "middle":
                    Coin.dilate(coin, self.middleApex)
                elif self.coinLoc == "left":
                    Coin.dilate(coin, self.leftApex)
                elif self.coinLoc == "right":
                    Coin.dilate(coin, self.rightApex)
                 
                #check if it goes out of bounds
                if coin.y > self.height:
                    if self.isMagnetic:
                        self.score += 1
                    self.coins.remove(coin)
            
            if not self.man.isJump: #can't collect coins while jumping
                coinsHit = pygame.sprite.spritecollide(self.playerGroup.sprite, self.coins, True)
                
                for coin in coinsHit:
                    self.coinSound.play()
                    self.score +=1
            
             
            #MAGNET WORK 
            if self.timer > 170:
                if self.isMakingMagnets and not(self.isMerge):
                    if len(self.magnets) < 1: 
                        
                        if self.timer % 700 == self.powerupTime:
                        
                            self.magnetLoc = random.choice(["left", "right"])
                            
                            if self.magnetLoc == "left" and not(self.isMerge):
                                initialX = 477
                                initialY = 169.207843193097 + 25
                                dx = -1.1547005
                                dy = 2
                                self.magnets.add(Magnet(initialX, initialY))
                            
                            elif self.magnetLoc == "right" and not(self.isMerge):
                                initialX = 477
                                initialY = 169.207843193097 + 25
                                dx = 1.1547005
                                dy = 2
                                self.magnets.add(Magnet(initialX, initialY))
            
            
            #dilate the magnet
            for magnet in self.magnets:
                if self.magnetLoc == "left":
                    Magnet.dilate(magnet, self.leftApex)
                elif self.magnetLoc == "right":
                    Magnet.dilate(magnet, self.rightApex)
                    
                #check if it goes out of bounds
                if magnet.y > self.height:
                    self.magnets.remove(magnet)
                    
            if not self.man.isJump: #can't collect magnets while jumping
                magnetsHit = pygame.sprite.spritecollide(self.playerGroup.sprite, self.magnets, True)
                
                if len(magnetsHit) == 1:
                    self.magnetSound.play()
                    self.isMagnetic = True
                    self.road.color = (0,0,200)
            
            #magnetic timer
            if self.isMagnetic:
                self.magneticTimer += 1
                if self.magneticTimer == 250:
                    self.isMagnetic = False
                    self.magneticTimer = 0
                    self.road.color = (200, 200, 0)
            
                
            #INVINCIBILITY WORK 
            if self.timer > 250:
                if self.isMakingInvincs and not(self.isMerge):
                    if len(self.invincs) < 1: 
                        
                        if self.powerupTimer % 700 == self.powerupTime:
                        
                            self.invincLoc = random.choice(["left", "right"])
                            
                            if self.invincLoc == "left" and not(self.isMerge):
                                initialX = 477
                                initialY = 169.207843193097 + 25
                                self.invincs.add(Invinc(initialX, initialY))
                            
                            elif self.invincLoc == "right" and not(self.isMerge):
                                initialX = 477
                                initialY = 169.207843193097 + 25
                                self.invincs.add(Invinc(initialX, initialY))
            
            
            #dilate the invinc
            for invinc in self.invincs:
                if self.invincLoc == "left":
                    Invinc.dilate(invinc, self.leftApex)
                elif self.invincLoc == "right":
                    Invinc.dilate(invinc, self.rightApex)
                    
                #check if it goes out of bounds
                if invinc.y > self.height:
                    self.invincs.remove(invinc)
                    
            if not self.man.isJump: #can't collect invincs while jumping
                invincsHit = pygame.sprite.spritecollide(self.playerGroup.sprite, self.invincs, True)
                
                if len(invincsHit) == 1:
                    self.invincSound.play()
                    self.isInvinc = True
                    self.road.color = (200,0,0)
            
            #invinc timer
            if self.isInvinc:
                print(self.invincTimer)
                self.invincTimer += 1
                if self.invincTimer == 250:
                    self.isInvinc = False
                    self.invincTimer = 0
                    self.invincTime = None
                    self.road.color = (200, 200, 0)
                    
                    
            #AI WORK 
            if self.timer > 200:
                if self.isMakingAIs:
                    if len(self.AIs) < 1: 
                        
                        if self.powerupTimer % 1000 == self.AITime:
                            
                            self.AILoc = random.choice(["left", "right"])

                            if self.AILoc == "left":
                                initialX = 477
                                initialY = 169.207843193097 + 25
                                self.AIs.add(AI(initialX, initialY))
                            
                            elif self.AILoc == "right":
                                initialX = 477
                                initialY = 169.207843193097 + 25
                                self.AIs.add(AI(initialX, initialY))
            
            #dilate the AI
            for ai in self.AIs:
                if self.AILoc == "left":
                    AI.dilate(ai, self.leftApex)
                elif self.AILoc == "right":
                    AI.dilate(ai, self.rightApex)
                    
                #check if it goes out of bounds
                if ai.y > self.height:
                    self.AIs.remove(ai)
                    
            if not self.man.isJump: #can't collect AIs while jumping
                AIsHit = pygame.sprite.spritecollide(self.playerGroup.sprite, self.AIs, True)
                if len(AIsHit) == 1:
                    self.AISound.play()
                    self.isAI = True
                    self.road.color = (124,252,0)
            
            #AI timer 
            
            if self.isAI:
                self.road.color = (124,252,0)
                self.AITimer += 1
                if self.AITimer == 1000:
                    self.isAI = False
                    self.AITimer = 0
                    self.AITime = None
                    self.road.color = (200, 200, 0)

            #HOLES
            
            #generate a hole
            if self.timer % 500 == 0:
                self.holeTime = random.randint(300, 499)
                
            if self.timer % 500 == self.holeTime and self.isMakingHoles:
                self.isHolePresent = True
                self.holes.append(Hole(412, 250))
            
            
            #dilate the hole
            if self.isHolePresent:
                for hole in self.holes:
                    Hole.dilate(hole, self.middleApex)
                    if hole.centerY - hole.height//2 > self.height:
                        self.isHolePresent = False
                        self.holes = []
                        
            #how to die
            for hole in self.holes:
                bottom = hole.centerY + hole.height//2
                if self.isAI:
                    if hole.centerY >= self.man.y - 35: #MAYBE STILL USE BOTTOM
                        if not(self.man.shouldJump):
                            self.man.shouldJump = True
                            self.man.shouldJumpIndex = 0
                
                if hole.centerY >= self.man.y and not(self.isAI) and not(self.isInvinc) and not(self.man.isJump): #if there's no merge
                    if not(self.isMerge):
                        self.mode = "GameOverNoJump"
                        self.isMagnetic = False
                        self.isInvinc = False
                        self.isAI = False
                        self.holes = []
                        pygame.mixer.music.stop()
                    elif self.isMerge:
                        if hole.centerY - self.man.y < 60:
                            self.mode = "GameOverNoJump"
                            self.isMagnetic = False
                            self.isInvinc = False
                            self.isAI = False
                            self.holes = []
                            pygame.mixer.music.stop()
            
            #MAKE MERGE
            if self.timer % 500 == 0:
                self.mergeTime = random.randint(300, 499)
                
            if self.timer % 500 == self.mergeTime:
                self.isMerge = True
        
            
            
                
            if self.isMerge:
                self.isMakingCoins = False
                self.isMakingMagnets = False
                self.isMakingInvincs = False
                self.isMakingHoles = False
                if self.road.k == self.height // 4:

                    if self.man.y < 140:
                        self.mode = "GameOverFell"
                        pygame.mixer.music.stop()
                        
                        #reset
                        
                        
                        self.isMerge = False 
                        self.isMakingCoins = True
                        self.isMagnetic = False
                        self.isInvinc = False
                        self.isAI = False
                        

                        self.road.k = 5
                        self.man.x = self.width // 2
                        self.man.y = 8 * self.height//10
                        self.man.updateRect()
                        
                        powerupChoice = random.choice(["magnet", "invinc"])
                        Game.pickPowerup(self, powerupChoice)
                        
                        
                    elif self.man.y > self.height // 4 - 50:
                        self.man.y -= 5
                        self.man.updateRect()

                elif self.road.k < self.height // 4:
                    self.road.k += 1
                
                
            
            #MOVE LEFT AND RIGHT
            if self.isKeyPressed(pygame.K_LEFT) and self.man.left:
                self.playerGroup.sprite.moveLeft(self.width) #move left
            if self.isKeyPressed(pygame.K_RIGHT) and self.man.right:
                self.playerGroup.sprite.moveRight(self.width) #move left   
                
            #MAKE JUMP
            if self.man.isJump and not(self.man.left) and not(self.man.right): #GLITCH when you click arrow keys too fast
                
                if self.man.jumpIndex < len(self.jumpAdd): 

                    self.man.y += self.jumpAdd[self.man.jumpIndex]
                    self.man.updateRect()
                    self.man.jumpIndex += 1
                    
                elif self.man.jumpIndex >= len(self.jumpAdd):
                    self.man.isJump = False
                    self.gruntJumpLandSound.play()
                    self.man.jumpIndex = 0
                    self.man.left = True
                    self.man.right = True
                    
                    
            #AI WORK
            if self.isAI:   

                if self.isMerge:
                    
                    if self.man.shouldJump: #DON'T click arrow keys too fast/simultaneously
                        
                        if self.man.shouldJumpIndex < len(self.jumpAdd): 
                            self.man.y += self.jumpAdd[self.man.shouldJumpIndex]
                            self.man.shouldJumpIndex += 1
                            self.man.updateRect()
                            
                            
                        elif self.man.shouldJumpIndex >= len(self.jumpAdd):
                            self.man.shouldJump = False
                            self.man.shouldJumpIndex = 0
                            self.man.left = True
                            self.man.right = True    
                            
                    #get to the middle
                    if 350 < self.man.y < 566:
                        Player.AIgetCoins(self.man, "middle", self.width)
                            
                    elif 140 < self.man.y < 222:
                        self.resetPlay()
                        self.mode = "Play"

                elif not(self.isMerge):   
                
                    if self.man.shouldJump: #DON'T click arrow keys too fast/simultaneously
                    
                        
                        if self.man.shouldJumpIndex < len(self.jumpAdd): 
                            self.man.y += self.jumpAdd[self.man.shouldJumpIndex]
                            self.man.shouldJumpIndex += 1
                            self.man.updateRect()
                            
                            
                        elif self.man.shouldJumpIndex >= len(self.jumpAdd):
                            self.man.shouldJump = False
                            self.man.shouldJumpIndex = 0
                            self.man.left = True
                            self.man.right = True 
                     
                    Player.AIgetCoins(self.man, self.coinLoc, self.width)
                

                
                
                    

                    
      
    def displayScore(self, screen): #https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
        font = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface = font.render("Score: " + str(self.score), False, (0, 0, 0))
        screen.blit(textsurface,(0,0))
        

    def redrawAll(self, screen):
        pygame.font.init()
        
        if self.mode == "Splash":
            screen.blit(self.splash, (0,0))
            
        elif self.mode == "Help1":
            screen.blit(self.helpScreens[0], (0,0))
            
            
        elif self.mode == "Help2":
            screen.blit(self.helpScreens[1], (0,0))
            

        elif self.mode == "Play":
            screen.blit(self.bg2, (0,0))
            
            self.road.draw()
            screen.blit(self.rightRail, (508,175))
            screen.blit(self.leftRail, (-5, 175))
            
            
            if self.isMerge == True:
                self.road.drawMerge()
                screen.blit(self.topRail, (-3,60))
                screen.blit(self.topRail, (-3, 60 + self.road.k))
                screen.blit(self.rightRail, (508,175))
                screen.blit(self.leftRail, (-5, 175))
                if self.road.k >= 60:
                    self.road.drawSkinnyMerge()
                
                self.road.draw()
                
            
            
            if self.isHolePresent:
                for hole in self.holes:
                    hole.draw(screen)

                
            self.magnets.draw(screen)
            self.invincs.draw(screen)
            self.AIs.draw(screen)
                
            self.coins.draw(screen)
            
            i = self.runningManTimer % 10
            self.man.image = self.man.runningImages[i]
            self.playerGroup.draw(screen)
        
            screen.blit(self.fog, (40,60))
            
            self.displayScore(screen)
            
        elif self.mode == "GameOverFell": 
            screen.blit(self.deadScreens[3], (0,0))
            font = pygame.font.SysFont('Comic Sans MS', 50)

            
            
        elif self.mode == "GameOverNoJump":
            screen.blit(self.deadScreens[1], (0,0))
            font = pygame.font.SysFont('Comic Sans MS', 50)

           
        
        elif self.mode == "GameOverNoSlide":
            screen.blit(self.deadScreens[2], (0,0))
            font = pygame.font.SysFont('Comic Sans MS', 50)
            
        
        elif self.mode == "EnterName":
            screen.blit(self.leaderboard.enterNameBase, (0,0))
            
            font = pygame.font.SysFont('Arial', 50)
            textsurfaceName = font.render(self.enteredName, False, (0, 0, 0))
            screen.blit(textsurfaceName,(195,230))
            
            
        elif self.mode == "Leaderboard":
            screen.blit(self.leaderboard.leaderboardBase, (0,0))
            Leaderboard.drawData(self.leaderboard, self.leaderboard.topFive, self.screen)
            
            
        
Game().run()

