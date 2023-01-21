from generator import *
from Ui import *
import random
from queue import PriorityQueue
import time
class Solver:
    def __init__(self, mazeGen:MazeGen):
        self._maze = mazeGen
        self._mazeMap = self._maze.getMazeMap
        self._startPos = self._maze.getStartPos
        self._endPos = self._maze.getEndPos

    def checkIsEnd(self, x:int, y:int) -> str:
        try:
            if self._mazeMap[x,y+1]["Type"] == 4 and self._mazeMap[x,y+1]["N"] == 0: return "End" # The end is north
        except KeyError:pass
        try:
            if self._mazeMap[x-1,y]["Type"] == 4 and self._mazeMap[x-1,y]["E"] == 0: return "End"
        except KeyError:pass
        try:
            if self._mazeMap[x,y-1]["Type"] == 4 and self._mazeMap[x,y-1]["S"] == 0: return "End"
        except KeyError:pass
        try:
            if self._mazeMap[x+1,y]["Type"] == 4 and self._mazeMap[x+1,y]["W"] == 0: return "End"
        except KeyError:pass

    def checkNeighCells(self, x:int, y:int) -> list:
        '''
        This will check the neighbouring cells of the current cell and check if they are blocked by a wall or not returning the valid cell
        '''
        neighCells = []
        try:
            if self._mazeMap[x,y+1]["Type"] == 1 and self._mazeMap[x,y+1]["N"] == 0: neighCells.append((x,y+1)) # North as it wants north of next cell
        except KeyError: pass
            #This means that the cell is on the edge of the maze or has been visited
        try:
            if self._mazeMap[x-1,y]["Type"] == 1 and self._mazeMap[x-1,y]["E"] == 0: neighCells.append((x-1,y))
        except KeyError:pass 
        try:
            if self._mazeMap[x,y-1]["Type"] == 1 and self._mazeMap[x,y-1]["S"] == 0: neighCells.append((x,y-1))
        except KeyError:pass
        try:
            if self._mazeMap[x+1,y]["Type"] == 1 and self._mazeMap[x+1,y]["W"] == 0: neighCells.append((x+1,y))
        except KeyError:pass
        return neighCells   

    def findNextMove(self, x:int, y:int):
        '''
        Takes in the current cell and returns the next cell to move to
        '''
        nextMove = []
        if len(self.checkNeighCells(x, y)) == 0: 
            return "DeadEnd"   
        nextMove.append(random.choice(self.checkNeighCells(x, y)))
        return (nextMove[0][0], nextMove[0][1])

############################################
#                                          #
#     CATEGORY A SKILL: RECURSION          #
#     CATEGORY A SKILL: LIST OPERATION     #
#                                          #
############################################

class DFS(Solver):
    def __init__(self, mazeGen):
        super().__init__(mazeGen)
        self._stackSearched = []
        self._stack = []
        self._tempStack = []
        self._tempStackSearched = []
        self._startTime = 0
        self._endTime = 0

    def run(self):
        self._startTime = time.time()
        self.solve(self._startPos[0], self._startPos[1])

    def deadEnd(self):
        self._stack.pop()
        if len(self._stack) != 0:
            self._stackSearched.append(self._stack[-1])
        if self.findNextMove(self._stack[-1][0], self._stack[-1][1]) == "DeadEnd":
            self.deadEnd()

    def solve(self, x:int, y:int):
        if self.checkIsEnd(x, y) == "End":
            for item in self._stackSearched:
                if item == "DeadEnd":
                    self._stackSearched.remove(item)
            print("Solved")
            self._endTime = time.time()
            self.setSolution()
            self._tempStackSearched = self._stackSearched.copy()
            self._stackSearched = []
            self._tempStack = self._stack.copy()
            self._stack = []
            return self._stackSearched, self._tempStack
        self._stack.append(self.findNextMove(x, y))
        self._stackSearched.append(self._stack[-1])
        if self._stack[-1] == "DeadEnd":
            self.deadEnd()
        try:
            #print(self._stack)
            self._mazeMap[self._stack[-1][0], self._stack[-1][1]]["Type"] = 2
        except:
            #this error occurs when the stack is empty, only happens on the second solve in huntandkill
            print("Dont hit solve twice")
        try:
            #time.sleep(0.5)
            self.solve(self._stack[-1][0], self._stack[-1][1])
        except IndexError:
            pass

    def setSolution(self):
        for cell in self._mazeMap:
            self._mazeMap[cell[0], cell[1]]["Type"] = 0
        for cell in self._stackSearched:
            self._mazeMap[cell[0], cell[1]]["Type"] = 5
        for cell in self._stack:
            self._mazeMap[cell[0], cell[1]]["Type"] = 2
        self._mazeMap[self._startPos[0], self._startPos[1]]["Type"] = 3
        self._mazeMap[self._endPos[0], self._endPos[1]]["Type"] = 4

    @property
    def getSolution(self):
        return self._tempStack

    @property
    def getSearch(self):
        return self._tempStackSearched
    
    @property
    def getTimeTaken(self):
        return round((self._endTime - self._startTime), 4)


############################################################
#                                                          #
#     CATEGORY A SKILL: RECURSION                          #
#     CATEGORY A SKILL: LIST OPERATION                     #
#     CATEGORY A SKILL: COMPLEX USER-DEFINED ALGORITHM     #
#                                                          #
############################################################

class AStar(Solver):
    def __init__(self, mazeGen: MazeGen):
        super().__init__(mazeGen)
        #self._qSearch = []
        self._start = tuple(self._startPos)
        self._end = tuple(self._endPos)
        self._searchPath = {}
        self._solvePath = {}
        self._gScore = {cell: float("inf") for cell in self._mazeMap}
        self._fScore = {cell: float("inf") for cell in self._mazeMap}
        self._pQueue = PriorityQueue()
        self._pQueue.put((self.heuristic(self._start, self._end),self.heuristic(self._start, self._end), (self._start)))
        self._gScore[self._start] = 0
        self._fScore[self._start] = self.heuristic(self._start, self._end)
        self._startTime = 0
        self._endTime = 0
    
    def run(self):
        self._startTime = time.time()
        self.algorithm()

    def heuristic(self, cell1, cell2) -> int:
        x1, y1 = cell1
        x2, y2 = cell2
        return abs(x1-x2) + abs(y1-y2)
    
    def algorithm(self):
        currCell=self._pQueue.get()[2]
        if self.checkIsEnd(currCell[0], currCell[1]) == "End":
            self._endTime = time.time()
            self._searchPath[self._end] = currCell
            print("Solved")
            self.setSolution()
            return "Solved"
        for childCell in self.checkNeighCells(currCell[0], currCell[1]):
            tempGScore = self._gScore[currCell] + 1
            tempFScore = tempGScore + self.heuristic(childCell, self._end)
            if tempFScore < self._fScore[childCell]:
                self._searchPath[childCell] = currCell
                self._gScore[childCell] = tempGScore
                self._fScore[childCell] = tempGScore + self.heuristic(childCell, self._end)
                self._pQueue.put((self._fScore[childCell], self.heuristic(childCell, self._end), childCell))
        self.algorithm()

    def setSolution(self):
        cell = self._end
        while cell != self._start:
            self._solvePath[self._searchPath[cell]] = cell
            cell = self._searchPath[cell]
        for cell in self._searchPath:
            self._mazeMap[cell[0], cell[1]]["Type"] = 5
        for cell in self._solvePath:
            self._mazeMap[cell[0], cell[1]]["Type"] = 2
        self._mazeMap[self._startPos[0], self._startPos[1]]["Type"] = 3
        self._mazeMap[self._endPos[0], self._endPos[1]]["Type"] = 4

    @property
    def getSolution(self):
        return self._searchPath, self._solvePath

    @property
    def getTimeTaken(self):
        return round((self._endTime - self._startTime), 4)

class BFS(Solver):
    def __init__(self, mazeGen:MazeGen):
        super().__init__(mazeGen)
        self._start = tuple(self._startPos)
        self._end = tuple(self._endPos)
        self._front = [self._start]
        self._searched = {}
        self._solvePath = {}
        self._startTime = 0
        self._endTime = 0
    
    def run(self):
        self._startTime = time.time()
        self.solve()

    def solve(self):
        try:
            currCell = self._front.pop(0)
            if self.checkIsEnd(currCell[0], currCell[1]) == "End":
                self._searched[self._end] = currCell
                print("Solved")
                self._endTime = time.time()
                self.setSolution()
                return "Solved"
            for childCell in self.checkNeighCells(currCell[0], currCell[1]):
                self._mazeMap[childCell[0], childCell[1]]["Type"] = 5
                self._front.append(childCell)
                self._searched[childCell] = currCell
            self.solve()
        except:
            pass


    def setSolution(self):
        cell = self._end
        while cell != self._start:
            self._solvePath[self._searched[cell]] = cell
            cell = self._searched[cell]
        for cell in self._searched:
            self._mazeMap[cell[0], cell[1]]["Type"] = 5
        for cell in self._solvePath:
            self._mazeMap[cell[0], cell[1]]["Type"] = 2
        self._mazeMap[self._startPos[0], self._startPos[1]]["Type"] = 3
        self._mazeMap[self._endPos[0], self._endPos[1]]["Type"] = 4

    @property
    def getSolution(self):
        return self._searched, self._solvePath

    @property
    def getTimeTaken(self):
        return round((self._endTime - self._startTime), 4)

class Dijkstra(Solver):
    def __init__(self, mazeGen:MazeGen) -> None:
        super().__init__(mazeGen)
        self._unVisited = {cell: float("inf") for cell in self._mazeMap}
        self._unVisited[self._maze.getStartPos[0], self._maze.getStartPos[1]] = 0
        self._searched = {}
        self._revPath = {}
        self._solvedPath = {}
        self._solved = False
        self._startTime = 0
        self._endTime = 0

    def run(self):
        self._startTime = time.time()
        self._mazeMap[self._endPos[0], self._endPos[1]]["Type"] = 4
        self.solve()

    #The end cell is not being added to the searched list
    #It sometimes solves it but prints out the wrong path
    #The search might be a little off
    def solve(self):
        currCell = min(self._unVisited, key=self._unVisited.get)
        if self.checkIsEnd(currCell[0], currCell[1]) == "End" and self._solved == False:
            self._endTime = time.time()
            self._revPath[tuple(self._endPos)] = currCell
            self.setSolution()
        else:
            self._searched[currCell] = self._unVisited[currCell]
            for childCell in self.checkNeighCells(currCell[0], currCell[1]):
                if childCell in self._searched:
                    continue
                tempDist = self._unVisited[currCell] + 1
                if tempDist < self._unVisited[childCell]:
                    self._unVisited[childCell] = tempDist
                    self._revPath[childCell] = currCell
            #if currCell == (self._endPos[0], self._endPos[1]):
            self._unVisited.pop(currCell)
            self.solve()

    def setSolution(self):
        cell = tuple(self._maze.getEndPos)
        #currently getting stuck
        while cell != tuple(self._maze.getStartPos):
            self._solvedPath[self._revPath[cell]] = cell
            cell = self._revPath[cell]
        for cell in self._revPath:
            self._mazeMap[cell[0], cell[1]]["Type"] = 5
        for cell in self._solvedPath:
            self._mazeMap[cell[0], cell[1]]["Type"] = 2
        self._mazeMap[self._startPos[0], self._startPos[1]]["Type"] = 3
        self._mazeMap[self._endPos[0], self._endPos[1]]["Type"] = 4

    @property
    def getSolution(self):
        return self._revPath, self._solvedPath

    @property
    def getTimeTaken(self):
        return round((self._endTime - self._startTime), 4)

class RHW(Solver):
    def __init__(self, mazeGen:MazeGen):
        super().__init__(mazeGen)
        self._direction = {"up": "N", "left": "W", "down": "S", "right": "E"}
        self._stack = []
        self._start = tuple(self._maze.getStartPos)
        self._path = ""
        self._solvedPath = [self.findNextMove(self._maze.getStartPos[0], self._maze.getStartPos[1])]
        self._endCell = tuple(self._maze.getEndPos)
        self._startTime = 0
        self._endTime = 0

    def run(self):
        self._startTime = time.time()
        if self._start[0] == 1:
            self._mazeMap[self._maze.getStartPos[0], self._maze.getStartPos[1]]["W"] = 1
        if self._start[0] == self._maze.getWidth:
            self._mazeMap[self._maze.getStartPos[0], self._maze.getStartPos[1]]["E"] = 1
        if self._start[1] == 1:
            self._mazeMap[self._maze.getStartPos[0], self._maze.getStartPos[1]]["N"] = 1
        if self._start[1] == self._maze.getHeight:
            self._mazeMap[self._maze.getStartPos[0], self._maze.getStartPos[1]]["S"] = 1
        self.solve()

    def rotateCW(self):
        values = list(self._direction.values())
        tempDict = dict(zip(self._direction.keys(), [values[-1]]+values[:-1]))
        self._direction = tempDict

    def rotateCCW(self):
        values = list(self._direction.values())
        tempDict = dict(zip(self._direction.keys(), values[1:]+[values[0]]))
        self._direction = tempDict

    def moveForward(self, x:int, y:int):
    #if y-1 > 0:
        if self._direction["up"] == "N":
            return (x, y-1),"N"
    #if x+1 < self._maze.getWidth:
        if self._direction["up"] == "E":
            return (x+1, y),"E"
    #if y+1 < self._maze.getHeight:
        if self._direction["up"] == "S":
            return (x, y+1),"S"
    #if x-1 >= 0:
        if self._direction["up"] == "W":
            return (x-1, y),"W"
            

    def deadEnd(self):
        self._stack.pop()
        self.solve(self._stack[-1][0], self._stack[-1][1])
    
    def solve(self):
        currCell = self.findNextMove(self._maze.getStartPos[0], self._maze.getStartPos[1])
        while True:
            self._stack.append(currCell)
            if self.checkIsEnd(currCell[0], currCell[1]) == "End":
                self._endTime = time.time()
                print("Solved")
                self.setSolution()
                return "Solved"
            if self._mazeMap[currCell][self._direction["right"]] == 1:
                if self._mazeMap[currCell][self._direction["up"]] == 1:
                    self.rotateCCW()
                else:
                    currCell,d=self.moveForward(currCell[0], currCell[1])
                    self._path += d
            else:
                self.rotateCW()
                currCell,d=self.moveForward(currCell[0], currCell[1])
                self._path += d


    def setSolution(self):
        currCell = self._stack[0]
        while "EW" in self._path or "WE" in self._path or "NS" in self._path or "SN" in self._path:
            self._path = self._path.replace("EW", "")
            self._path = self._path.replace("WE", "")
            self._path = self._path.replace("NS", "")
            self._path = self._path.replace("SN", "")
        for d in self._path:
            if d == "N":
                currCell = (currCell[0], currCell[1]-1)
                self._solvedPath.append(currCell)
            if d == "E":
                currCell = (currCell[0]+1, currCell[1])
                self._solvedPath.append(currCell)
            if d == "S":
                currCell = (currCell[0], currCell[1]+1)
                self._solvedPath.append(currCell)
            if d == "W":
                currCell = (currCell[0]-1, currCell[1])
                self._solvedPath.append(currCell)
        for cell in self._stack:
            self._mazeMap[cell[0], cell[1]]["Type"] = 5
        self._solvedPath.append(self._endCell)
        for cell in self._solvedPath:
            self._mazeMap[cell[0], cell[1]]["Type"] = 2
        self._mazeMap[self._startPos[0], self._startPos[1]]["Type"] = 3
        self._mazeMap[self._endPos[0], self._endPos[1]]["Type"] = 4

    @property
    def getSolution(self):
        return self._stack, self._solvedPath

    @property
    def getTimeTaken(self):
        return round((self._endTime - self._startTime), 4)


class LHW(Solver):
    def __init__(self, mazeGen:MazeGen):
        super().__init__(mazeGen)
        self._direction = {"up": "N", "left": "W", "down": "S", "right": "E"}
        self._stack = []
        self._start = tuple(self._maze.getStartPos)
        self._path = ""
        self._solvedPath = [self.findNextMove(self._maze.getStartPos[0], self._maze.getStartPos[1])]
        self._endCell = tuple(self._maze.getEndPos)
        self._startTime = 0
        self._endTime = 0

    def run(self):
        self._startTime = time.time()
        if self._start[0] == 1:
            self._mazeMap[self._maze.getStartPos[0], self._maze.getStartPos[1]]["W"] = 1
        if self._start[0] == self._maze.getWidth:
            self._mazeMap[self._maze.getStartPos[0], self._maze.getStartPos[1]]["E"] = 1
        if self._start[1] == 1:
            self._mazeMap[self._maze.getStartPos[0], self._maze.getStartPos[1]]["N"] = 1
        if self._start[1] == self._maze.getHeight:
            self._mazeMap[self._maze.getStartPos[0], self._maze.getStartPos[1]]["S"] = 1
        self.solve()

    def rotateCW(self):
        values = list(self._direction.values())
        tempDict = dict(zip(self._direction.keys(), [values[-1]]+values[:-1]))
        self._direction = tempDict

    def rotateCCW(self):
        values = list(self._direction.values())
        tempDict = dict(zip(self._direction.keys(), values[1:]+[values[0]]))
        self._direction = tempDict

    def moveForward(self, x:int, y:int):
        if self._direction["up"] == "N":
            return (x, y-1),"N"
        if self._direction["up"] == "E":
            return (x+1, y),"E"
        if self._direction["up"] == "S":
            return (x, y+1),"S"
        if self._direction["up"] == "W":
            return (x-1, y),"W"
    
    def solve(self):
        currCell = self.findNextMove(self._maze.getStartPos[0], self._maze.getStartPos[1])
        while True:
            self._stack.append(currCell)
            if self.checkIsEnd(currCell[0], currCell[1]) == "End":
                self._endTime = time.time()
                print("Solved")
                self.setSolution()
                return "Solved"
            if self._mazeMap[currCell][self._direction["left"]] == 1:
                if self._mazeMap[currCell][self._direction["up"]] == 1:
                    self.rotateCW()
                else:
                    currCell,d=self.moveForward(currCell[0], currCell[1])
                    self._path += d
            else:
                self.rotateCCW()
                currCell,d=self.moveForward(currCell[0], currCell[1])
                self._path += d


    def setSolution(self):
        currCell = self._stack[0]
        while "EW" in self._path or "WE" in self._path or "NS" in self._path or "SN" in self._path:
            self._path = self._path.replace("EW", "")
            self._path = self._path.replace("WE", "")
            self._path = self._path.replace("NS", "")
            self._path = self._path.replace("SN", "")
        for d in self._path:
            if d == "N":
                currCell = (currCell[0], currCell[1]-1)
                self._solvedPath.append(currCell)
            if d == "E":
                currCell = (currCell[0]+1, currCell[1])
                self._solvedPath.append(currCell)
            if d == "S":
                currCell = (currCell[0], currCell[1]+1)
                self._solvedPath.append(currCell)
            if d == "W":
                currCell = (currCell[0]-1, currCell[1])
                self._solvedPath.append(currCell)
        for cell in self._stack:
            self._mazeMap[cell[0], cell[1]]["Type"] = 5
        self._solvedPath.append(self._endCell)
        for cell in self._solvedPath:
            self._mazeMap[cell[0], cell[1]]["Type"] = 2
        self._mazeMap[self._startPos[0], self._startPos[1]]["Type"] = 3
        self._mazeMap[self._endPos[0], self._endPos[1]]["Type"] = 4

    @property
    def getSolution(self):
        return self._stack, self._solvedPath

    @property
    def getTimeTaken(self):
        return round((self._endTime - self._startTime), 4)