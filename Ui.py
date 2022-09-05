from generator import *
from tkinter import *

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
        self._win=Tk()
        self._win.state('zoomed')
        self._win.title('Maze')
        self._canvas = Canvas()

    def run(self):
        self._canvas.create_line(1)
        self._win.mainloop()

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
    