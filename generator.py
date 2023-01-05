import random
import sys

#sys.setrecursionlimit(100)
class MazeGen:
    def __init__(self, height:int=10, width:int=10):
        self.mazeMap = {}
        self._height = height
        self._width = width
        self._compass = ["N", "E", "S", "W"]
        self._dimentions = []
        self._startPos = []
        self._endPos = []

################################################
#                                              #
#     CATEGORY A SKILL: COMPLEX DATA MODEL     #
#                                              #
################################################


    def genMaze(self, height:int=10, width:int=10) -> dict: 
        '''
        Generates the raw maze dict base with its Walls and type
        Type: Undefined cell 0, Defined path cell 1, Solved path cell 2, Start 3, End 4.
        '''
        self._grid = []
        self._dimentions = [height, width]
        y = 0
        for _ in range(height): # height
            x = 1
            y += 1
            for _ in range(width): # widths
                self._grid.append((x,y))
                self.mazeMap[x,y]={'N':1,'E':1,'S':1,'W':1,'Type':0}
                x += 1  
        edgeList = self.pickEdge(width, height)
        self.setStartPos(edgeList[0])
        self.setEndPos(edgeList[1])

    def setMazeMap(self, newMazeMap:dict) -> dict:
        self.mazeMap = newMazeMap

    @property
    def getMazeMap(self) -> dict:
        return self.mazeMap

    @property
    def getGrid(self) -> list:
        return self._grid

    def pickEdge(self, width:int, height:int) -> list:
        '''
        This will pick the starting and ending COORDs for the maze
        '''
        edge = random.randint(1,4)
        if edge == 1: #North
            #Start Coord
            startCoord = [random.randint(1, width),1]
            self.mazeMap[startCoord[0],startCoord[1]]["N"] = 0
            #End Coord
            endCoord = [random.randint(1, width),height]
            self.mazeMap[endCoord[0],endCoord[1]]["S"] = 0
        elif edge == 2: #East
            #Start Coord
            startCoord = [width,random.randint(1, height)]
            self.mazeMap[startCoord[0],startCoord[1]]["E"] = 0
            #End Coord
            endCoord = [1,random.randint(1, height)]
            self.mazeMap[endCoord[0],endCoord[1]]["W"] = 0
        elif edge == 3: #South
            #Start Coord
            startCoord = [random.randint(1, width),height]
            self.mazeMap[startCoord[0],startCoord[1]]["S"] = 0
            #End Coord
            endCoord = [random.randint(1, width),1]
            self.mazeMap[endCoord[0],endCoord[1]]["N"] = 0
        elif edge == 4: #West
            #Start Coord
            startCoord = [1,random.randint(1, height)]
            self.mazeMap[startCoord[0],startCoord[1]]["W"] = 0
            #End Coord
            endCoord = [width,random.randint(1, height)]
            self.mazeMap[endCoord[0],endCoord[1]]["E"] = 0
        return startCoord, endCoord

    def setStartPos(self, edgeCoord:list) -> dict:
        '''
        This sets the start point type
        '''
        self._startPos = [edgeCoord[0], edgeCoord[1]]
        #print(f"Start Point: {edgeCoord}")
        self.changeCellType(edgeCoord[0], edgeCoord[1], 3)
        return self.mazeMap

    def setEndPos(self, edgeCoord:list) -> dict:
        '''
        This sets the end point type
        '''
        self._endPos = [edgeCoord[0], edgeCoord[1]]
        #print(f"End Point: {edgeCoord}")
        #self.changeCellType(edgeCoord[0], edgeCoord[1], 4) #if removed then maze can be fully generated
        return self.mazeMap  

    @property 
    def getStartPos(self) -> list:
        print(self._startPos)
        return self._startPos

    @property
    def getEndPos(self) -> list:
        #print(self._endPos)
        return self._endPos

    #Algorithm to generate a random path
    def randomPathGen(self):
        direction = random.choice(self._compass)
        return direction 

    def outsideWall(self, x, y):
        '''
        This means and outside wall has been selected as a random path and the path needs to be selected again
        '''
        self.findNextMove(x, y)

    def delNorth(self,x:int,y:int):
        '''
        Checks for a wall on the coords inputed and with change that wall type into a 0 denoting that the wall is removed
        '''
        self.mazeMap[x,y]["N"] = 0
        try:
            if self.mazeMap[x,y-1]["S"] > 0:
                self.mazeMap[x,y-1]["S"] = 0
        except:
            #This mean a Outside wall has been hit
            self.outsideWall(x, y)
            pass
    
    def delEast(self,x:int,y:int):
        self.mazeMap[x,y]["E"] = 0
        try:
            if self.mazeMap[x+1,y]["W"] > 0:
                self.mazeMap[x+1,y]["W"] = 0   
        except:
            self.outsideWall(x, y)
            pass

    def delSouth(self,x:int,y:int):
        self.mazeMap[x,y]["S"] = 0
        try:
            if self.mazeMap[x,y+1]["N"] > 0:
                self.mazeMap[x,y+1]["N"] = 0
        except:
            self.outsideWall(x, y)
            pass

    def delWest(self,x:int,y:int):
        self.mazeMap[x,y]["W"] = 0
        try:
            if self.mazeMap[x-1,y]["E"] > 0:
                self.mazeMap[x-1,y]["E"] = 0
        except:
            self.outsideWall(x, y)
            pass

    def getCellType(self,x:int,y:int) -> int:
        '''
        Returns the cellType with the position of x and y coords
        '''
        return self.mazeMap[x,y]["Type"]

    def changeCellType(self, x:int, y:int, newCellType:int):
        '''
        Changes the celltype with the x and y coords to the chosen newCellType
        '''
        self.mazeMap[x,y]["Type"] = newCellType

    def checkNeighCells(self, x:int, y:int) -> list:
        '''
        This will check the neighbouring cells of the current cell and return a list of the cells that are not visited
        '''
        neighCells = []
        try:
            if self.mazeMap[x,y+1]["Type"] == 0: neighCells.append((x,y+1))
        except KeyError: pass
            #This means that the cell is on the edge of the maze or has been visited
        try:
            if self.mazeMap[x-1,y]["Type"] == 0: neighCells.append((x-1,y))
        except KeyError:pass 
        try:
            if self.mazeMap[x,y-1]["Type"] == 0: neighCells.append((x,y-1))
        except KeyError:pass
        try:
            if self.mazeMap[x+1,y]["Type"] == 0: neighCells.append((x+1,y))
        except KeyError:pass

        return neighCells
        
    def findNextMove(self, x:int, y:int):
        '''
        This will find the next move for the maze
        '''
        if len(self.checkNeighCells(x, y)) == 0: return "Dead End"
        else:
            nextMove = random.choice(self.checkNeighCells(x,y))
            if nextMove[1] < y: 
                return ("S", x, y-1)
            if nextMove[0] > x: 
                return ("W", x+1, y)
            if nextMove[1] > y: 
                return ("N",x, y+1)
            if nextMove[0] < x: 
                return ("E",x-1, y)
            #As there are no possible moves the maze generator will need to backtrack
            

#READ THIS, TURN THIS INTO HUNT AND KILL ALGORITHM LATER

#######################################################
#                                                     #
#     CATEGORY A SKILL: ADVANCED STACK OPERATIONS     #
#     CATEGORY A SKILL: RECURSIVE ALGORITHM           #
#                                                     #
#######################################################

##############################################################
#                                                            #
#     CATEGORY A SKILL: COMPLEX USE OF OOP (INHERITENCE)     #        
#                                                            #
##############################################################

class RDFS(MazeGen):
    def __init__(self):
        super().__init__()
        self._stack = []
        #self._mazeMap = mazeMap

        

    def run(self):
        #print(self._mazeMap)
        self.generate() 

    #Change to -1 as it is a stack
    def deadEnd(self):
        self._stack.pop()
        try:
            if self.findNextMove(self._stack[-1][1], self._stack[-1][2]) == "Dead End":
                #print(self._stack)
                self.deadEnd()
        except:
            pass
            #print("Dont hit run twice")

    def generate(self, mazeGen, x:int, y:int, endX:int, endY:int):
        #self._stack.append(self.getStartPos)
        self.mazeMap = mazeGen
        self._stack.append(self.findNextMove(x,y))
        if self._stack[-1][0] == "S":
            self.delSouth(self._stack[-1][1],self._stack[-1][2])
        elif self._stack[-1][0] == "W":
            self.delWest(self._stack[-1][1],self._stack[-1][2])
        elif self._stack[-1][0] == "E":
            self.delEast(self._stack[-1][1],self._stack[-1][2])
        elif self._stack[-1][0] == "N":
            self.delNorth(self._stack[-1][1],self._stack[-1][2])
        elif self._stack[-1] == "Dead End":
            self.deadEnd()     
        try:
            self.changeCellType(self._stack[-1][1],self._stack[-1][2],1)
        except:
            #print("Dont hit run twice")
            pass
        try:
            self.generate(self.mazeMap, self._stack[-1][1], self._stack[-1][2], endX, endY)       
        except IndexError:
            #print(self.getEndPos[0], self.getEndPos[1])
            self.changeCellType(endX, endY, 4)
            print("Generated Maze")
            #print(self.getGrid)

class BFS(MazeGen):
    def __init__(self):
        super().__init__()
        self._stack = [MazeGen.getStartPos]
        self._visited = []

    def run(self):
        self.getStack()

    def nextCell(self):
        ...

    @property
    def getStack(self):
        return self._stack

class HuntAndKill(MazeGen):
    def __init__(self):
        super().__init__()
        self._lastSolvedLine = 0

    def algorithm():
        ...

    def SearchBlankCell():
        ...
