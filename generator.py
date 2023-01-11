import random
from mazeGen import *
import sys
import copy

#sys.setrecursionlimit(100)
class Generator:
    def __init__(self, mazeGen:MazeGen):
        self._maze = mazeGen
        self._mazeMap = self._maze.getMazeMap
        self._startPos = self._maze.getStartPos
        self._endPos = self._maze.getEndPos
        self._compass = ["N", "E", "S", "W"]

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

    def changeCellType(self, x:int, y:int, newCellType:int):
        '''
        Changes the celltype with the x and y coords to the chosen newCellType
        '''
        self._mazeMap[x,y]["Type"] = newCellType

    @property
    def getCellType(self,x:int,y:int) -> int:
        '''
        Returns the cellType with the position of x and y coords
        '''
        return self._mazeMap[x,y]["Type"]

    def checkNeighCells(self, x:int, y:int, type:int) -> list:
        '''
        This will check the neighbouring cells of the current cell and return a list of the cells that are not visited
        '''
        neighCells = []
        try:
            if self._mazeMap[x,y+1]["Type"] == type: neighCells.append((x,y+1))
        except KeyError: pass
            #This means that the cell is on the edge of the maze or has been visited
        try:
            if self._mazeMap[x-1,y]["Type"] == type: neighCells.append((x-1,y))
        except KeyError:pass 
        try:
            if self._mazeMap[x,y-1]["Type"] == type: neighCells.append((x,y-1))
        except KeyError:pass
        try:
            if self._mazeMap[x+1,y]["Type"] == type: neighCells.append((x+1,y))
        except KeyError:pass
        return neighCells
        
    def findNextMove(self, x:int, y:int):
        '''
        This will find the next move for the maze
        '''
        if len(self.checkNeighCells(x, y, 0)) == 0: return "Dead End"
        else:
            nextMove = random.choice(self.checkNeighCells(x,y,0))
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

class RDFS(Generator):
    def __init__(self, mazeGen):
        super().__init__(mazeGen)
        self._stack = []
        self._stackGen = []

    def run(self):
        self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 0)
        self.generate(self._maze.getStartPos[0], self._maze.getStartPos[1])

    #Change to -1 as it is a stack
    def deadEnd(self):
        self._stack.pop()
        try:
            if self.findNextMove(self._stack[-1][1], self._stack[-1][2]) == "Dead End":
                self.deadEnd()
        except:
            pass
            #print("Dont hit run twice")

    def generate(self, x, y):
        #self._stack.append(self.getStartPos)
        self._stack.append(self.findNextMove(x,y))
        if self._stack[-1] != "Dead End":
            self._stackGen.append(self._stack[-1][1:])
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
            self.generate(self._stack[-1][1], self._stack[-1][2])       
        except IndexError:
            self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 4)
            tempMaze = copy.deepcopy(self._mazeMap)
            self._maze.setTempMaze(tempMaze)
            print("Generated Maze")

    @property
    def getGen(self):
        print(self._stackGen)
        return self._stackGen

class HuntAndKill(Generator):
    def __init__(self, mazeGen):
        super().__init__(mazeGen)
        self._stack = []
        self._lastSolvedLine = 1

    def run(self):
        self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 0)
        self.algorithm(self._maze.getStartPos[0], self._maze.getStartPos[1])

    def findHunt(self, x, y):
        neighCells = []
        try:
            if self._mazeMap[x,y+1]["Type"] == 1: neighCells.append((x,y+1))
        except KeyError: pass
            #This means that the cell is on the edge of the maze or has been visited
        try:
            if self._mazeMap[x-1,y]["Type"] == 1: neighCells.append((x-1,y))
        except KeyError:pass 
        try:
            if self._mazeMap[x,y-1]["Type"] == 1: neighCells.append((x,y-1))
        except KeyError:pass
        try:
            if self._mazeMap[x+1,y]["Type"] == 1: neighCells.append((x+1,y))
        except KeyError:pass
        if len(neighCells) == 0: return "Dead End"
        return random.choice(neighCells)    

    def deadEnd(self):
        if self._lastSolvedLine <= self._maze.getDimentions[0]:
            for x in range(self._maze.getDimentions[1]):
                if self._mazeMap[x+1, self._lastSolvedLine]["Type"] == 0 and self.findHunt(x, self._lastSolvedLine) != "Dead End":
                    self.algorithm(x+1, self._lastSolvedLine)
                elif self._mazeMap[x+1, self._lastSolvedLine]["Type"] == 1 and x+1 == self._maze.getDimentions[1]:
                    self._lastSolvedLine += 1
                    self.deadEnd()
        else:
            print("ERROR THING")


    def algorithm(self, x, y):
        self._stack.append(self.findNextMove(x,y))
        if self._stack[-1] == self._maze.getEndPos:
            self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 4)
            tempMaze = copy.deepcopy(self._mazeMap)
            self._maze.setTempMaze(tempMaze)
            print("Generated Maze")
            return
        if self._stack[-1][0] == "S":
            self.delSouth(self._stack[-1][1],self._stack[-1][2])
        elif self._stack[-1][0] == "W":
            self.delWest(self._stack[-1][1],self._stack[-1][2])
        elif self._stack[-1][0] == "E":
            self.delEast(self._stack[-1][1],self._stack[-1][2])
        elif self._stack[-1][0] == "N":
            self.delNorth(self._stack[-1][1],self._stack[-1][2])
        elif self._stack[-1] == "Dead End":
            self._stack.pop()
            self.deadEnd() 
        try:
            self.changeCellType(self._stack[-1][1],self._stack[-1][2],1)
        except:
            #print("Dont hit run twice")
            pass
        try:
            self.algorithm(self._stack[-1][1], self._stack[-1][2])       
        except IndexError:
            pass
        '''
            self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 4)
            tempMaze = copy.deepcopy(self._mazeMap)
            self._maze.setTempMaze(tempMaze)
            print("Generated Maze")
        '''

class BFS(Generator):
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

