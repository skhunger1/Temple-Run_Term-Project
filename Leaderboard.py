'''
Leaderboard Values
'''

from pathlib import Path
import operator
import pygame

class Leaderboard(object):
    def __init__(self):
        self.path = 'leaderboard.txt'
        self.enterNameBase = pygame.image.load('images/enterName.png')
        self.leaderboardBase = pygame.image.load('images/leaderboardBase.png')
        
        self.sortedScores = self.getLeaderDict()
        self.topFive = self.getTopFive()
        
    #made name entering feature in keyPressed in main
    
    def editLeaderboard(self, name, score): 
        #name = input("Please enter your name: ")
        contentsToAdd = "\n" + str(name) + ":" + str(score)
        
        f = open("leaderboard.txt", "a+")
        f.write(contentsToAdd)
        f.close()
        
    def getLeaderDict(self): #https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        scoreText = Path(self.path).read_text()
        scoreList = scoreText.split("\n")
        scoreDict = dict()
        for val in scoreList:
            name = val.split(":")[0]
            score = int(val.split(":")[1])
            scoreDict[score] = name

        sortedScores = []
        for key in sorted(scoreDict.keys(), reverse=True):
            sortedScores.append((key, scoreDict[key]))

        return sortedScores
    
    #returns list of tuples, each of form (score, name)
    def getTopFive(self):
        sortedScores = self.getLeaderDict()
        topFive = sortedScores[0:5]
        return topFive
        
    def drawData(self, tuples, screen):
        #tuples is a list of (score, name), where name is in quotation marks
        #this function should put data into the right cells based on the image
        font = pygame.font.SysFont('Arial', 50)
        nameX = 220
        scoreX = 710

        Y = 100
        dY = 84
        
        for tuple in tuples:
            
            #name
            textsurfaceName = font.render(str(tuple[1]), False, (0,0,0))
            screen.blit(textsurfaceName, (nameX, Y))
            
            #score
            textsurfaceScore = font.render(str(tuple[0]), False, (0,0,0))
            screen.blit(textsurfaceScore, (scoreX, Y))
            
            Y += dY
            
            
            
            

            