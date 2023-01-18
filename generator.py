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
        #if y-1 > 0:
        try:
            if self._mazeMap[x,y-1]["S"] > 0:
                self._mazeMap[x,y-1]["S"] = 0
        except KeyError:
        #elif y-1 ==0:
            #This mean a Outside wall has been hit
            pass
    
    def delEast(self,x:int,y:int):
        self._mazeMap[x,y]["E"] = 0
        try:
        #if x+1 < self._maze.getDimentions[0]:
            if self._mazeMap[x+1,y]["W"] > 0:
                self._mazeMap[x+1,y]["W"] = 0   
        except KeyError:
        #elif x+1 == self._maze.getDimentions[0]:
            pass

    def delSouth(self,x:int,y:int):
        self._mazeMap[x,y]["S"] = 0
        try:
        #if y+1 < self._maze.getDimentions[1]:
            if self._mazeMap[x,y+1]["N"] > 0:
                self._mazeMap[x,y+1]["N"] = 0
        except KeyError:
        #elif y+1 == self._maze.getDimentions[1]:
            pass

    def delWest(self,x:int,y:int):
        self._mazeMap[x,y]["W"] = 0
        try:
        #if x-1 > 0:
            if self._mazeMap[x-1,y]["E"] > 0:
                self._mazeMap[x-1,y]["E"] = 0
        except KeyError:
        #elif x-1 == 0:
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
        if y+1 > self._maze.getHeight: pass
        else:
            if self._mazeMap[x,y+1]["Type"] == type: neighCells.append((x,y+1))
            #This means that the cell is on the edge of the maze or has been visited
        if x-1 <= 0: pass
        else:
            if self._mazeMap[x-1,y]["Type"] == type: neighCells.append((x-1,y))
        if y-1 <= 0: pass
        else:
            if self._mazeMap[x,y-1]["Type"] == type: neighCells.append((x,y-1))
        if x+1 > self._maze.getWidth: pass
        else:
            if self._mazeMap[x+1,y]["Type"] == type: neighCells.append((x+1,y))
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
        self._stackGen.append(self.findNextMove(x,y))
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
        return self._stackGen

class HuntAndKill(Generator):
    def __init__(self, mazeGen):
        super().__init__(mazeGen)
        self._stack = []
        self._lastSolvedLine = 1

    def run(self):
        self.changeCellType(self._maze.getStartPos[0], self._maze.getStartPos[1], 0)
        self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 0)
        self.algorithm(self._maze.getStartPos[0], self._maze.getStartPos[1])

    def findHunt(self, x, y):
        neighCells = []
        try:
            if self._mazeMap[x,y+1]["Type"] == 1: 
                #self.delSouth(x,y)
                neighCells.append((x,y+1)) 
                return "S"
        except KeyError: pass
            #This means that the cell is on the edge of the maze or has been visited
        try:
            if self._mazeMap[x-1,y]["Type"] == 1: 
                #self.delWest(x,y)
                neighCells.append((x-1,y))
                return "W"
        except KeyError:pass 
        try:
            if self._mazeMap[x,y-1]["Type"] == 1: 
                #self.delNorth(x,y)
                neighCells.append((x,y-1))
                return "N"
        except KeyError:pass
        try:
            if self._mazeMap[x+1,y]["Type"] == 1: 
                #self.delEast(x,y)
                neighCells.append((x+1,y))
                return "E"
        except KeyError:pass
        if len(neighCells) == 0: return "Dead End"
        return random.choice(neighCells)    

    def checkSolved(self):
        for cell in self._mazeMap:
            if self._mazeMap[cell]["Type"] == 0:
                return False
        return True

    def checkLineSolved(self):
        count = 0
        for x in range(self._maze.getWidth):
            if self.findHunt(x+1, self._lastSolvedLine) == "Dead End" and self._mazeMap[x+1, self._lastSolvedLine]["Type"] == 1:
                count += 1
            if count == self._maze.getWidth:
                self._lastSolvedLine += 1

    def deadEnd(self):
        self.checkLineSolved()
        y = -1+self._lastSolvedLine
        for _ in range(self._maze.getHeight):
            x = 1
            y += 1
            if y <= self._maze.getHeight:
                for _ in range(self._maze.getWidth):
                    if self._mazeMap[x, y]["Type"] == 0 and self.findHunt(x, y) != "Dead End":
                        self._stack.append((x, y))
                        self._mazeMap[x, y]["Type"] = 1
                        delWall = self.findHunt(x,y)
                        if delWall == "S":
                            self.delSouth(x,y)
                        elif delWall == "W":
                            self.delWest(x,y)
                        elif delWall == "E":
                            self.delEast(x,y)
                        elif delWall == "N":
                            self.delNorth(x,y)
                        self.algorithm(x, y)
                    x+=1
            else:
                pass


    def algorithm(self, x, y):
        self._stack.append(self.findNextMove(x,y))
        if self.checkSolved() == True:
            self._stack.pop()
            self.changeCellType(self._maze.getStartPos[0], self._maze.getStartPos[1], 3)
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
            pass
        try:
            self.algorithm(self._stack[-1][1], self._stack[-1][2]) 
        except:
            pass      

class BinaryTree(Generator):
    def __init__(self, mazeGen: MazeGen):
        super().__init__(mazeGen)

    def run(self, direction:str):
        self.changeCellType(self._maze.getStartPos[0], self._maze.getStartPos[1], 0)
        self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 0)
        self.algorithm(direction)

    def algorithm(self, direction):
        for cell in self._mazeMap:
            if direction == "NW":
                self._mazeMap[cell]["Type"] = 1
                randNum = random.randint(0,1)
                if cell[1] == 1 and cell[0] != 1:
                    self.delWest(cell[0], cell[1])              
                if cell[0] == 1 and cell[1] != 1:
                    self.delNorth(cell[0], cell[1])
                if cell[1] != 1:
                    if randNum == 0:
                        self.delNorth(cell[0], cell[1])
                if cell[0] != 1:
                    if randNum == 1:
                        self.delWest(cell[0], cell[1])
            elif direction == "NE":
                self._mazeMap[cell]["Type"] = 1
                randNum = random.randint(0,1)
                if cell[1] == 1 and cell[0] != self._maze.getWidth:
                    self.delEast(cell[0], cell[1])              
                if cell[0] == self._maze.getWidth and cell[1] != 1:
                    self.delNorth(cell[0], cell[1])
                if cell[1] != 1:
                    if randNum == 0:
                        self.delNorth(cell[0], cell[1])
                if cell[0] != self._maze.getWidth:
                    if randNum == 1:
                        self.delEast(cell[0], cell[1])
            elif direction == "SW":
                self._mazeMap[cell]["Type"] = 1
                randNum = random.randint(0,1)
                if cell[1] == self._maze.getHeight and cell[0] != 1:
                    self.delWest(cell[0], cell[1])              
                if cell[0] == 1 and cell[1] != self._maze.getHeight:
                    self.delSouth(cell[0], cell[1])
                if cell[1] != self._maze.getHeight:
                    if randNum == 0:
                        self.delSouth(cell[0], cell[1])
                if cell[0] != 1:
                    if randNum == 1:
                        self.delWest(cell[0], cell[1])
            elif direction == "SE":
                self._mazeMap[cell]["Type"] = 1
                randNum = random.randint(0,1)
                if cell[1] == self._maze.getHeight and cell[0] != self._maze.getWidth:
                    self.delEast(cell[0], cell[1])              
                if cell[0] == self._maze.getWidth and cell[1] != self._maze.getHeight:
                    self.delSouth(cell[0], cell[1])
                if cell[1] != self._maze.getHeight:
                    if randNum == 0:
                        self.delSouth(cell[0], cell[1])
                if cell[0] != self._maze.getWidth:
                    if randNum == 1:
                        self.delEast(cell[0], cell[1])
            if cell == (self._maze.getWidth, self._maze.getHeight):
                self.changeCellType(self._maze.getStartPos[0], self._maze.getStartPos[1], 3)
                self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 4)
                tempMaze = copy.deepcopy(self._mazeMap)
                self._maze.setTempMaze(tempMaze)
                print("Generated Maze")
                return
