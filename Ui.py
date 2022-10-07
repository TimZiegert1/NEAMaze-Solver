from generator import *
from tkinter import *
from generator import *
from pygame import *
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
        self._main = Tk()

    def run(self):
        self.mainPanel()

    def mainPanel(self):
        self._main.title("Main")
        mazeButton = Button(self._main, text="Maze", command=self.mazePanel)
        quitButton = Button(self._main, text="Quit", command=self._main.destroy)
        mazeButton.place(x=0, y=0)
        self._main.mainloop()

    def mazePanel(self):
        mazeScreen = display.set_mode((1080, 720))
        mazeScreen.fill((255,255,255))
        #quitButton = 
        display.flip()
        running = True
        while running:
            for event in event.get():
                if event.type == QUIT:
                    running = False
                    break
                
    def onEvent():


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
    