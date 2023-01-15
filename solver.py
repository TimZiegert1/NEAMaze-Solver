from generator import *
from Ui import *
import random
from queue import PriorityQueue
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

class DFS(Solver):
    def __init__(self, mazeGen):
        super().__init__(mazeGen)
        self._stackSearched = []
        self._stack = []
        self._tempStack = []
        self._tempStackSearched = []

    def run(self):
        self.solve(self._startPos[0], self._startPos[1])

    def deadEnd(self):
        self._stack.pop()
        if self.findNextMove(self._stack[-1][0], self._stack[-1][1]) == "DeadEnd":
            self.deadEnd()

    def solve(self, x:int, y:int):
        if self.checkIsEnd(x, y) == "End":
            print("Solved")
            self.setSolution()
            self._tempStackSearched = self._stackSearched.copy()
            self._stackSearched = []
            self._tempStack = self._stack.copy()
            self._stack = []
            return self._stackSearched, self._tempStack
        self._stack.append(self.findNextMove(x, y))
        if self._stack[-1] != "DeadEnd":
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
    
    def run(self):
        self.algorithm()

    def heuristic(self, cell1, cell2) -> int:
        x1, y1 = cell1
        x2, y2 = cell2
        return abs(x1-x2) + abs(y1-y2)
    
    def algorithm(self):
        currCell=self._pQueue.get()[2]
        if self.checkIsEnd(currCell[0], currCell[1]) == "End":
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


class BFS(Solver):
    def __init__(self, mazeGen:MazeGen):
        super().__init__(mazeGen)
        self._start = tuple(self._startPos)
        self._end = tuple(self._endPos)
        self._front = [self._start]
        self._searched = {}
        self._solvePath = {}
    
    def run(self):
        self.solve()

    def solve(self):
        try:
            currCell = self._front.pop(0)
            if self.checkIsEnd(currCell[0], currCell[1]) == "End":
                self._searched[self._end] = currCell
                print("Solved")
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

class Dijkstra(Solver):
    def __init__(self, mazeGen:MazeGen) -> None:
        super().__init__(mazeGen)
        self._unVisited = {cell: float("inf") for cell in self._mazeMap}
        self._unVisited[self._maze.getStartPos[0], self._maze.getStartPos[1]] = 0
        self._searched = {}
        self._revPath = {}
        self._solvedPath = {}
        self._solved = False

    def run(self):
        self._mazeMap[self._endPos[0], self._endPos[1]]["Type"] = 4
        self.solve()

    #The end cell is not being added to the searched list
    #It sometimes solves it but prints out the wrong path
    #The search might be a little off
    def solve(self):
        currCell = min(self._unVisited, key=self._unVisited.get)
        if self.checkIsEnd(currCell[0], currCell[1]) == "End" and self._solved == False:
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

class RHW(Solver):
    def __init__(self, mazeGen:MazeGen):
        super().__init__(mazeGen)
        self._direction = {"up": "N", "left": "W", "down": "S", "right": "E"}
        self._stack = []

    def run(self):
        self.solve(self._startPos[0], self._startPos[1])

    def rotateCW(self):
        values = list(self._direction.values())
        self._direction = dict(zip(self._direction.keys(), [values[-1]]+values[:-1]))

    def rotateCCW(self):
        values = list(self._direction.values())
        self._direction = dict(zip(self._direction.keys(), values[1:]+[values[0]]))

    def moveForward(self, x:int, y:int):
        if self._direction["up"] == "N":
            return (x, y+1)
        elif self._direction["up"] == "E":
            return (x+1, y)
        elif self._direction["up"] == "S":
            return (x, y-1)
        elif self._direction["up"] == "W":
            return (x-1, y)

    def deadEnd(self):
        self._stack.pop()
        self.solve(self._stack[-1][0], self._stack[-1][1])
    
    def solve(self,x:int, y:int):
        self._stack.append((x, y))
        print(self._stack)
        if self.checkIsEnd(x, y) == "End":
            print("Solved")
            self.setSolution()
            return "Solved"
        if self._mazeMap[x, y]["E"] == 1:
            if self._mazeMap[x, y]["N"] == 1:
                self.rotateCW()
            else:
                self.solve(self.moveForward(x, y)[0], self.moveForward(x, y)[1])
        else:
            self.rotateCCW()
            self.solve(self.moveForward(x, y)[0], self.moveForward(x, y)[1])


    def setSolution(self):
        for cell in self._stack:
            self._mazeMap[cell[0], cell[1]]["Type"] = 5
        self._mazeMap[self._startPos[0], self._startPos[1]]["Type"] = 3
        self._mazeMap[self._endPos[0], self._endPos[1]]["Type"] = 4



