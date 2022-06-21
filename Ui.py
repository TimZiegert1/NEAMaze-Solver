from generator import *

class TerminalUi():
    def __init__(self):
        self.mazeGen = MazeGen()
        self.height = int(input("Please enter the height of the maze: "))
        self.width = int(input("Please enter the width of the maze: "))
    
    def run(self):
        self.mazeGen.genMaze(self.height, self.width)

class GUI():
    def __init__(self):
        ...