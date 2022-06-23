import random

class MazeGen:
    def __init__(self):
        self._mazeMap = {}

    #This Procedure will generate a maze grid layout of the users chosen size
    def genMaze(self, height:int=10, width:int=10) -> dict:
        '''
        Generatos the raw maze dictonary base with its Walls and type
        Type: Undefined cell 0, Defined path cell 1, Start 2, End 3.
        '''

        y = 0
        for _ in range(height): # height
            x = 1
            y += 1
            for _ in range(width): # widths
                self._mazeMap[x,y]={'E':1,'W':1,'N':1,'S':1,'Type':0}
                x += 1  

    def setMazeMap(self, newMazeMap:dict) -> dict:
        self._mazeMap = newMazeMap

    def getMazeMap(self) -> dict:
        print(self._mazeMap)
        return self._mazeMap

    #This will pick the starting point for the maze
    def startPos(self):
        ...
   
    def getStartPos(self):
        return self.startPos()
    
    #This will pick the end point for maze
    def endPos():
        ...   
    
    #Algorithm to generate a random path
    def randomPathGen():
        ...

    #Finds the next move of the random maze generator
    def findNextMove():
        ...

    #If a deadEnd is hit run this function
    def deadEnd():
        ...

    #Prints out the maze
    def printMaze(self, maze):
        for x,y in range():
            ...

    def delNorth(self,x:int,y:int):
        self._mazeMap[x,y]["N"] = 0
        if y-1 > 0:
            self._mazeMap[x,y-1]["N"] = 0
    
    def delEast(self,x:int,y:int):
        self._mazeMap[x,y]["E"] = 0
        if y-1 > 0:
            self._mazeMap[x,y-1]["E"] = 0   

    def delSouth(self,x:int,y:int):
        self._mazeMap[x,y]["S"] = 0
        if y-1 > 0:
            self._mazeMap[x,y-1]["S"] = 0

    def delWest(self,x:int,y:int):
        self._mazeMap[x,y]["W"] = 0
        if y-1 > 0:
            self._mazeMap[x,y-1]["W"] = 0

    def getCell(self):
        ...

    def changeCell(self):
        ...
class HuntAndKill(MazeGen):
    def __init__(self):
        super().__init__()
        self._lastSolvedLine = 0

    def algorithm():
        ...

    def SearchBlankCell():
        ...

class RDFS(MazeGen):
    def __init__(self):
        super().__init__()

    