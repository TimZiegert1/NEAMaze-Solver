import random


class MazeGen:
    def __init__(self):
        self._mazeMap = {}
        self._compass = ["N", "E", "S", "W"]
        self._dimentions = []


    def genMaze(self, height:int=10, width:int=10) -> dict: 
        '''
        Generates the raw maze dict base with its Walls and type
        Type: Undefined cell 0, Defined path cell 1, Start 2, End 3.
        '''
        self._grid = []
        self._dimentions = [height, width]
        y = 0
        for _ in range(height): # height
            x = 1
            y += 1
            for _ in range(width): # widths
                self._grid.append((x,y))
                self._mazeMap[x,y]={'N':1,'E':1,'S':1,'W':1,'Type':0}
                x += 1  
        edgeList = self.pickEdge(width, height)
        self.setStartPos(edgeList[0])
        self.setEndPos(edgeList[1])

    def setMazeMap(self, newMazeMap:dict) -> dict:
        self._mazeMap = newMazeMap

    @property
    def getMazeMap(self) -> dict:
        return self._mazeMap
    
    def getMazeMapCoord(self):
        return

    def pickEdge(self, width:int, height:int) -> list:
        '''
        This will pick the starting and ending COORDs for the maze
        '''
        edge = random.randint(1,4)
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

    def setStartPos(self, edgeCoord:list) -> dict:
        '''
        This sets the start point type
        '''
        self.startPoint = edgeCoord
        #print(edgeCoord)
        self.changeCellType(edgeCoord[0], edgeCoord[1], 2)
        return self._mazeMap

    def setEndPos(self, edgeCoord:list) -> dict:
        '''
        This sets the end point type
        '''
        self.endPoint = edgeCoord
        #print(edgeCoord)
        self.changeCellType(edgeCoord[0], edgeCoord[1], 3)
        return self._mazeMap  

    def getStartPos(self) -> list:
        return self.pickEdge[0]
    
    def getEndPos(self) -> list:
        return self.pickEdge[1]

    #Algorithm to generate a random path
    def randomPathGen(self):
        direction = random.choice(self._compass)
        return direction 

    def outsideWall(self, x, y):
        '''
        This means and outside wall has been selected as a random path and the path needs to be selected again
        '''
        self.findNextMove(x, y)

    #Prints out the maze
    def printMaze(self):
        '''
         1:N
        101 W:Type:East
         1:S
        '''
        #cell = ([])
        #for values in self._mazeMap.values():
            #print(values.values())
        ...

    def delNorth(self,x:int,y:int):
        '''
        Checks for a wall on the coords inputed and with change that wall type into a 0 denoting that the wall is removed
        '''
        self._mazeMap[x,y]["N"] = 0
        try:
            if self._mazeMap[x,y-1]["S"] > 0:
                self._mazeMap[x,y-1]["S"] = 0
        except:
            #This mean a Outside wall has been hit
            self.outsideWall(x, y)
            pass
    
    def delEast(self,x:int,y:int):
        self._mazeMap[x,y]["E"] = 0
        try:
            if self._mazeMap[x+1,y]["W"] > 0:
                self._mazeMap[x+1,y]["W"] = 0   
        except:
            self.outsideWall(x, y)
            pass

    def delSouth(self,x:int,y:int):
        self._mazeMap[x,y]["S"] = 0
        try:
            if self._mazeMap[x,y+1]["N"] > 0:
                self._mazeMap[x,y+1]["N"] = 0
        except:
            self.outsideWall(x, y)
            pass

    def delWest(self,x:int,y:int):
        self._mazeMap[x,y]["W"] = 0
        try:
            if self._mazeMap[x-1,y]["E"] > 0:
                self._mazeMap[x-1,y]["E"] = 0
        except:
            self.outsideWall(x, y)
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

    def checkNeighCells(self, x:int, y:int) -> list:
        '''
        This will check the neighbouring cells of the current cell and return a list of the cells that are not visited
        '''
        neighCells = []
        try:
            if self._mazeMap[x,y+1]["Type"] == 0: neighCells.append((x,y+1))
        except KeyError: pass
            #This means that the cell is on the edge of the maze or has been visited
        try:
            if self._mazeMap[x+1,y]["Type"] == 0: neighCells.append((x+1,y))
        except KeyError:pass
        try:
            if self._mazeMap[x,y-1]["Type"] == 0: neighCells.append((x,y-1))
        except KeyError:pass
        try:
            if self._mazeMap[x-1,y]["Type"] == 0: neighCells.append((x-1,y))
        except KeyError:pass 
        print(neighCells)
        return neighCells
        
    def findNextMove(self, x:int, y:int):
        '''
        This will find the next move for the maze
        '''
        
        if len(self.checkNeighCells(x, y)) == 0:
            #self.deadEnd()
            return "Dead End"
        else:
            nextMove = random.choice(self.checkNeighCells(x,y))
            print(nextMove)
            if nextMove[1] < y: 
                print(x,y-1)
                return ("N", x, y-1)
            if nextMove[0] > x: 
                print(x+1,y)
                return ("W", x+1, y)
            if nextMove[1] > y: 
                print(x,y+1)
                return ("S",x, y+1)
            if nextMove[0] < x: 
                print(x-1,y)
                return ("E",x-1, y)
            #As there are no possible moves the maze generator will need to backtrack
            


class RDFS(MazeGen):
    def __init__(self):
        super().__init__()
        self._stack = []

    def run(self):
        self.solve()
    
    def solve(self, mazeGen, x:int, y:int):
        self._mazeMap = mazeGen
        self._stack.append(self.findNextMove(x,y))
        if self._stack[0] == "S":
            self.delSouth(self._stack[1],self._stack[2])
        elif self._stack[0] == "W":
            self.delWest(self._stack[1],self._stack[2])
        elif self._stack[0] == "E":
            self.delEast(self._stack[1],self._stack[2])
        elif self._stack[0] == "N":
            self.delNorth(self._stack[1],self._stack[2])
        print(self._stack)
        



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