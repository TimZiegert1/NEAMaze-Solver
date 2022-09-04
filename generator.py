import random
from tracemalloc import start
from Ui import *

class MazeGen:
    def __init__(self):
        self._mazeMap = {}
        self._Compass = ["N", "E", "S", "W"]
        

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
                self._mazeMap[x,y]={'N':1,'E':1,'S':1,'W':1,'Type':0}
                x += 1  
        edgeList = self.pickEdge(width, height)
        self.startPos(edgeList[0])
        self.endPos(edgeList[1])

    def setMazeMap(self, newMazeMap:dict) -> dict:
        self._mazeMap = newMazeMap

    def getMazeMap(self) -> dict:
        print(self._mazeMap)
        return self._mazeMap

    def pickEdge(self, width:int, height:int) -> list:
        edge = random.randint(1,4)
        print(edge)
        if edge == 1: #North
            #Start Coord
            startCoord = [random.randint(1, width),1]
            self._mazeMap[startCoord[0],startCoord[1]]["N"] = 0
            #End Coord
            endCoord = [random.randint(1, width),height]
            self._mazeMap[endCoord[0],endCoord[1]]["S"] = 0
        elif edge == 2: #East
            #Start Coord
            startCoord = [width,random.randint(1, height)]
            self._mazeMap[startCoord[0],startCoord[1]]["E"] = 0
            #End Coord
            endCoord = [1,random.randint(1, height)]
            self._mazeMap[endCoord[0],endCoord[1]]["W"] = 0
        elif edge == 3: #South
            #Start Coord
            startCoord = [random.randint(1, width),height]
            self._mazeMap[startCoord[0],startCoord[1]]["S"] = 0
            #End Coord
            endCoord = [random.randint(1, width),1]
            self._mazeMap[endCoord[0],endCoord[1]]["N"] = 0
        elif edge == 4: #West
            #Start Coord
            startCoord = [1,random.randint(1, height)]
            self._mazeMap[startCoord[0],startCoord[1]]["W"] = 0
            #End Coord
            endCoord = [width,random.randint(1, height)]
            self._mazeMap[endCoord[0],endCoord[1]]["E"] = 0
        return startCoord, endCoord

    #This will pick the starting point for the maze
    def startPos(self, edgeCoord:list) -> dict:
        print(edgeCoord)
        self._mazeMap[edgeCoord[0],edgeCoord[1]]["Type"] = 2 
        return self._mazeMap
   
    def getStartPos(self):
        return self.startPos()
    
    #This will pick the end point for maze
    def endPos(self, edgeCoord:list) -> dict:
        print(edgeCoord)
        self._mazeMap[edgeCoord[0],edgeCoord[1]]["Type"] = 3 
        return self._mazeMap  
    
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
    def printMaze(self):
        '''
         1:N
        101 W:Type:East
         1:S
        '''
        cell = ([])
        for values in self._mazeMap.values():
            print(values.values())
            

    def delNorth(self,x:int,y:int):
        self._mazeMap[x,y]["N"] = 0
        try:
            if self._mazeMap[x,y-1]["S"] > 0:
                self._mazeMap[x,y-1]["S"] = 0
        except:
            #This mean a Outside wall has been hit
            self.deadEnd()
            pass
    
    def delEast(self,x:int,y:int):
        self._mazeMap[x,y]["E"] = 0
        try:
            if self._mazeMap[x+1,y]["W"] > 0:
                self._mazeMap[x+1,y]["W"] = 0   
        except:
            self.deadEnd()
            pass

    def delSouth(self,x:int,y:int):
        self._mazeMap[x,y]["S"] = 0
        try:
            if self._mazeMap[x,y+1]["N"] > 0:
                self._mazeMap[x,y+1]["N"] = 0
        except:
            self.deadEnd()
            pass

    def delWest(self,x:int,y:int):
        self._mazeMap[x,y]["W"] = 0
        try:
            if self._mazeMap[x-1,y]["E"] > 0:
                self._mazeMap[x-1,y]["E"] = 0
        except:
            self.deadEnd()
            pass

    def getCellType(self,x:int,y:int) -> int:
        '''
        Returns the cellType with the position of x and y coords
        '''
        return self._mazeMap[x,y]["Type"]

    def changeCellType(self, x:int, y:int, newCellType:int):
        '''
        Changes the celltype with the x and y coords to the chosen newCellType
        '''
        self._mazeMap[x,y]["Type"] = newCellType

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

    