from generator import *
import tkinter as tk
import pygame
class Ui:
    def __init__(self):
        self._gen = MazeGen()
        self._RDFS = RDFS()
        self._height = int(input("Please enter the height of the maze: "))
        self._width = int(input("Please enter the width of the maze: "))
        self._gen.genMaze(self._height, self._width)

class Terminal(Ui):
    def __init__(self):
        super().__init__()  

    def run(self):
        self._gen.getMazeMap()

    def changeHeight(self, newWidth):
        self._width = newWidth
    
    def getWidth(self):
        return self._height

    def changeHeight(self, newHeight):
        self._height = newHeight

    def getHeight(self):
        return self._height

class GUI(Ui):
    def __init__(self):
        super().__init__()
        pygame.init()
        self._mazeMap = self._gen.getMazeMap
        self._font = pygame.font.Font(None, 50)
        self._main = tk.Tk()
        self._mazeScreen = pygame.display.set_mode((1080, 720), flags=pygame.HIDDEN)
        

    def run(self):
        self.mainPanel()

    @property
    def getMazeMap(self):
        self._mazeMap = self._gen.getMazeMap
        return self._mazeMap

    def mainPanel(self):
        self._main.title("Main")
        mazeButton = tk.Button(self._main, text="Maze", command=self.mazePanel)
        helpButton = tk.Button(self._main, text="Help")#, command=self.helpPanel)
        quitButton = tk.Button(self._main, text="Quit", command=self._main.destroy)
        mazeButton.place(x=0, y=0)
        quitButton.pack()
        self._main.mainloop()

    def mazePanel(self):
        self._mazeScreen = pygame.display.set_mode((1080, 720), flags=pygame.SHOWN)
        self._mazeScreen.fill((255,255,255))
        quitButton = pygame.draw.rect(self._mazeScreen, (0,0,0), (980,670,100,50))
        runButton = pygame.draw.rect(self._mazeScreen, (0,0,0), (980,570,100,50))
        quitText = self._font.render("Quit", True, (0,0,255))
        self._mazeScreen.blit(quitText, quitText.get_rect(center=quitButton.center))
        runText = self._font.render("Run", True, (255,0,0))
        self._mazeScreen.blit(runText, runText.get_rect(center=runButton.center))
        #self._gen.findNextMove(self._gen.startPoint[0], self._gen.startPoint[1])
        self.createMaze(self._mazeMap)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 670:
                        running = False
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 570 and mouse[1] < 620 and mouse[0] < 1080:
                        #self._gen.findNextMove(self._gen.startPoint[0], self._gen.startPoint[1])
                        self._RDFS.solve(self._gen.getMazeMap, self._gen.startPoint[0], self._gen.startPoint[1])
                        self.createMaze(self.getMazeMap)
        pygame.quit()
        #This line allows to close and reopen the window
        #self._mazeScreen = pygame.display.set_mode((1080, 720), flags=pygame.HIDDEN)

    def createMaze(self, mazeMap):
        y=-1
        for _ in range(self._height): # height
            x = 0
            y += 1
            for _ in range(self._width): # widths
                pygame.draw.rect(self._mazeScreen, (255,255,255), ((x*55)+10,(y*55)+10,50,50))
                if mazeMap[x+1,y+1]["Type"] == 2:
                    pygame.draw.rect(self._mazeScreen, (255,0,0), ((x*55)+10,(y*55)+10,50,50))
                elif mazeMap[x+1,y+1]["Type"] == 3:
                    pygame.draw.rect(self._mazeScreen, (0,0,255), ((x*55)+10,(y*55)+10,50,50))
                #elif mazeMap[x+1,y+1]["Type"] == 1:
                    #pygame.draw.rect(self._mazeScreen, (50,50,50), ((x*55)+10,(y*55)+10,50,50))
                if mazeMap[x+1,y+1]["N"] == 1:
                    pygame.draw.rect(self._mazeScreen, (0,0,0), ((x*55)+5,((y*50)+(y-1)*5)+10,60,5))
                if mazeMap[x+1,y+1]["S"] == 1:
                    pygame.draw.rect(self._mazeScreen, (0,0,0), ((x*55)+10,((y*50)+(y-1)*5)+65,55,5))
                if mazeMap[x+1,y+1]["E"] == 1:
                    pygame.draw.rect(self._mazeScreen, (0,0,0), (((x*50)+(x-1)*5)+65,(y*55)+10,5,55))
                if mazeMap[x+1,y+1]["W"] == 1:
                    pygame.draw.rect(self._mazeScreen, (0,0,0), (((x*50)+(x-1)*5)+10,(y*55)+10,5,55))
                if mazeMap[x+1,y+1]["N"] == 0:
                    pygame.draw.rect(self._mazeScreen, (255,255,255), ((x*55)+5,((y*50)+(y-1)*5)+10,60,5))
                if mazeMap[x+1,y+1]["S"] == 0:
                    pygame.draw.rect(self._mazeScreen, (255,255,255), ((x*55)+10,((y*50)+(y-1)*5)+65,55,5))
                if mazeMap[x+1,y+1]["E"] == 0:
                    pygame.draw.rect(self._mazeScreen, (255,255,255), (((x*50)+(x-1)*5)+65,(y*55)+10,5,55))
                if mazeMap[x+1,y+1]["W"] == 0:
                    pygame.draw.rect(self._mazeScreen, (255,255,255), (((x*50)+(x-1)*5)+10,(y*55)+10,5,55))

                pygame.display.update()
                x += 1  
    


    def changeStart(self):
        ...

    def changeEnd(self):
        ...

    def login(self):
        ...

    def logout(self):
        ...
    
    def startButton(self):
        ...

    def settingsButton(self):
        ...
    
    def importMaze(self):
        ...

    def saveMaze(self):
        ...

    def stepButtonForward(self):
        ...
    
    def stepButtonBackward(self):
        ...

    def pauseButton(self):
        ...

    def widthChanger(self):
        ... #Both slider and textbox
    
    def heightChaner(self):
        ... #Both slider and textbox

    def pickGen(self):
        ... #Drop down of all maze Generation algorithms

    def pickSolve(self):
        ... #Drop down of all maze solving algorithms

    def resetButton(self):
        ...

    def speedSlider(self):
        ... #Text box or slider
    