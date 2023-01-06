from generator import *
from solver import *
from mazeGen import *
import tkinter as tk
import pygame
class Ui:
    def __init__(self):
        self._height = 15
        self._width = 15
        self._mazeGen = MazeGen(self._height, self._width)
        self._gen = Generator(self._mazeGen.getMazeMap, self._mazeGen.getStartPos, self._mazeGen.getEndPos, self._mazeGen)
        self._RDFS = RDFS(self._mazeGen.getMazeMap, self._mazeGen.getStartPos, self._mazeGen.getEndPos, self._mazeGen)
        self._solver = Solver(self._mazeGen.getMazeMap, self._mazeGen.getStartPos, self._mazeGen.getEndPos, self._mazeGen)
        self._DFS = DFS(self._mazeGen.getMazeMap, self._mazeGen.getStartPos, self._mazeGen.getEndPos, self._mazeGen)
        #self._height = int(input("Please enter the height of the maze: "))
        #self._width = int(input("Please enter the width of the maze: "))
        #self._gen.genMaze(self._height, self._width)
        self._black= (0, 0, 0)
        self._white = (255, 255, 255)
        self._green = (0, 255, 0)
        self._red = ( 255, 0, 0)
        self._blue = (0,0,255)

    def changeWidth(self, newWidth):
        self._width = newWidth
    
    def getWidth(self):
        return self._height

    def changeHeight(self, newHeight):
        self._height = newHeight

    def getHeight(self):
        return self._height


class Terminal(Ui):
    def __init__(self):
        super().__init__()  

    def run(self):
        print(self._mazeGen.getMazeMap)
class GUI(Ui):
    def __init__(self):
        super().__init__()
        pygame.init()
        self._font = pygame.font.Font(None, 50)
        self._main = tk.Tk()
        self._mazeScreen = pygame.display.set_mode((1375,850), flags=pygame.HIDDEN) #15 rows and 15 col is perfect fit!

    def run(self):
        self.mainPanel()

    def mainPanel(self):
        self._main.title("Main")
        mazeButton = tk.Button(self._main, text="Maze", command=self.mazePanel)
        helpButton = tk.Button(self._main, text="Help")#, command=self.helpPanel)
        quitButton = tk.Button(self._main, text="Quit", command=self._main.destroy)
        mazeButton.place(x=0, y=0)
        quitButton.pack()
        self._main.mainloop()

    def mazePanel(self):
        self._mazeScreen = pygame.display.set_mode((1375,850), flags=pygame.SHOWN)
        self._mazeScreen.fill((255,255,255))
        self.drawButtons()
        self.drawMaze(self._mazeGen.getMazeMap)
        #self.drawMazeTest(self._mazeMap)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                #Quit button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 670 and mouse[1] < 720 and mouse[0] < 1080:
                        running = False
                        break
                #DFS GEN button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 570 and mouse[1] < 620 and mouse[0] < 1080:
                        #self._gen.findNextMove(self._gen.startPoint[0], self._gen.startPoint[1])
                        self._RDFS = RDFS(self._mazeGen.getMazeMap, self._mazeGen.getStartPos, self._mazeGen.getEndPos, self._mazeGen)
                        self._RDFS.run()
                        self.drawMaze(self._mazeGen.getMazeMap)
                        #self.drawMazeTest(self.getMazeMap)
                #Solve DFS Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 520 and mouse[1] < 570 and mouse[0] < 1080:
                        #self._gen.findNextMove(self._gen.startPoint[0], self._gen.startPoint[1])
                        #self._solver.runRDFS()
                        self._DFS = DFS(self._mazeGen.getMazeMap, self._mazeGen.getStartPos, self._mazeGen.getEndPos, self._mazeGen)
                        self._DFS.run()
                        self.drawMaze(self._mazeGen.getMazeMap)
                        #self.drawMazeTest(self.getMazeMap)
                #Generate new maze button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 620 and mouse[1] < 670 and mouse[0] < 1080:
                        #pygame.draw.rect(self._mazeScreen, (255,255,255), (0,0,500,500))
                        self._mazeGen.setMazeMap = {}
                        self._mazeGen = MazeGen(self._height, self._width)
                        self.drawMaze(self._mazeGen.getMazeMap)
                        #self.drawMazeTest(self.getMazeMap)
        pygame.quit()
        #This line allows to close and reopen the window
        #self._mazeScreen = pygame.display.set_mode((1080, 720), flags=pygame.HIDDEN)

    def drawMaze(self, mazeMap):
        y=-1
        for _ in range(self._height): # height
            x = 0
            y += 1
            for _ in range(self._width): # widths
                if mazeMap[x+1,y+1]["Type"] == 3:
                    pygame.draw.rect(self._mazeScreen, self._red, ((x*55)+10,(y*55)+10,50,50))
                elif mazeMap[x+1,y+1]["Type"] == 4:
                    pygame.draw.rect(self._mazeScreen, self._blue, ((x*55)+10,(y*55)+10,50,50))
                elif mazeMap[x+1,y+1]["Type"] == 0:
                    pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,50,50))
                elif mazeMap[x+1,y+1]["Type"] == 2:
                    pygame.draw.rect(self._mazeScreen, self._red, ((x*55)+10,(y*55)+10,50,50))
                #elif mazeMap[x+1,y+1]["Type"] == 1:
                    #pygame.draw.rect(self._mazeScreen, (50,50,50), ((x*55)+10,(y*55)+10,50,50))
                if mazeMap[x+1,y+1]["N"] == 1:
                    pygame.draw.rect(self._mazeScreen, self._black, ((x*55)+5,((y*50)+(y-1)*5)+10,60,5))
                if mazeMap[x+1,y+1]["S"] == 1:
                    pygame.draw.rect(self._mazeScreen, self._black, ((x*55)+5,((y*50)+(y-1)*5)+65,60,5))
                if mazeMap[x+1,y+1]["E"] == 1:
                    pygame.draw.rect(self._mazeScreen, self._black, (((x*50)+(x-1)*5)+65,(y*55)+5,5,60))
                if mazeMap[x+1,y+1]["W"] == 1:
                    pygame.draw.rect(self._mazeScreen, self._black, (((x*50)+(x-1)*5)+10,(y*55)+5,5,60))
                if mazeMap[x+1,y+1]["N"] == 0:
                    pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,((y*50)+(y-1)*5)+10,50,5))
                if mazeMap[x+1,y+1]["S"] == 0:
                    pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,((y*50)+(y-1)*5)+65,50,5))
                if mazeMap[x+1,y+1]["E"] == 0:
                    pygame.draw.rect(self._mazeScreen, self._white, (((x*50)+(x-1)*5)+65,(y*55)+10,5,50))
                if mazeMap[x+1,y+1]["W"] == 0:
                    pygame.draw.rect(self._mazeScreen, self._white, (((x*50)+(x-1)*5)+10,(y*55)+10,5,50)) 
                pygame.display.update()
                x += 1
        #pygame.display.update() USE THIS IF YOU WANT IT TO BE INSTANT

    #Paste rescale code here to test

    def getRescaleValue(self, width, height):
        rescaleValue = 800
        rescaleHeight = 800/height
        rescaleWidth = 800/width
        x = (5*rescaleHeight)/6
        y = (5*rescaleWidth)/6
        xWalls = x/10
        yWalls = y/10


    def drawButtons(self):
        self.quitButton(self._mazeScreen, self._black ,(980, 670,100, 50), "Quit")
        self.clearButton(self._mazeScreen, self._black ,(980, 620,100, 50), "Clear")
        self.runButton(self._mazeScreen, self._black ,(980, 570,100, 50), "Run")
        self.solveButton(self._mazeScreen, self._black ,(980, 520,100, 50), "Solve")
    
    def quitButton(self, screen, colour, pos, text:str):
        quitButton = pygame.draw.rect(screen, colour, pos)
        quitText = self._font.render(text, True, (0,0,255))
        self._mazeScreen.blit(quitText, quitText.get_rect(center=quitButton.center))

    def runButton(self, screen, colour, pos, text:str):
        runButton = pygame.draw.rect(screen, colour, pos)
        runText = self._font.render(text, True, (255,0,0))
        self._mazeScreen.blit(runText, runText.get_rect(center=runButton.center))
    
    def solveButton(self, screen, colour, pos, text:str):
        solveButton = pygame.draw.rect(screen, colour, pos)
        solveText = self._font.render(text, True, (255,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def clearButton(self, screen, colour, pos, text:str):
        clearButton = pygame.draw.rect(screen, colour, pos)
        clearText = self._font.render(text, True, (255,0,0))
        self._mazeScreen.blit(clearText, clearText.get_rect(center=clearButton.center))


    def pickGen(self):
        ... #Drop down of all maze Generation algorithms

    def pickSolve(self):
        ... #Drop down of all maze solving algorithms

    def editMaze(self):
        ...

    def customise(self):
        ... #Customise maze size, colours, etc

    def changeStart(self):
        ...

    def changeEnd(self):
        ...

    def login(self):
        ...

    def logout(self):
        ...

    def createAccount(self):
        ...
    
    def startButton(self):
        ...

    def settingsButton(self):
        ...

    
    def stepForwardButton(self):
        ...
    
    def stepBackwardButton(self):
        ...

    def pauseButton(self):
        ...
    
    def importMaze(self):
        ...

    def saveMaze(self):
        ...

    def widthUpdate(self):
        ... #Both slider and textbox
    
    def heightUpdate(self):
        ... #Both slider and textbox


    def speedSlider(self):
        ... #Text box or slider
    