from generator import *
import tkinter as tk
import pygame
class Ui:
    def __init__(self):
        self._gen = MazeGen()
        self._height = int(input("Please enter the height of the maze: "))
        self._width = int(input("Please enter the width of the maze: "))

class Terminal(Ui):
    def __init__(self):
        super().__init__()  

    def run(self):
        self._gen.genMaze(self._height, self._width)
        self._gen.getMazeMap()
        #self._gen.printMaze()
        self._gen.printMaze()
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
        self._mazeMap = self._gen.getMazeMap()
        #self._font = pygame.font.Font(None, 50)
        self._main = tk.Tk()
        

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
        mazeScreen = pygame.display.set_mode((1080, 720))
        mazeScreen.fill((255,255,255))
        quitButton = pygame.draw.rect(mazeScreen, (0,0,0), (0,0,100,50))
        font = pygame.font.Font(None, 50)
        text = font.render("Quit", True, (0,0,255))
        mazeScreen.blit(text, text.get_rect(center=quitButton.center))
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] < 100 and mouse[1] < 50:
                        running = False
                        break
        pygame.quit()

    def createMaze(self):
        print(self._mazeMap)

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
    