from generator import *
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

    def runRDFS(self):
        DFS().run()

class DFS(Solver):
    def __init__(self, mazeGen):
        super().__init__(mazeGen)
        self._stackSearched = []
        self._stack = []
    
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
            self._stack = []
            return "Solved"
        self._stack.append(self.findNextMove(x, y))
        if self._stack[-1] != "DeadEnd":
            self._stackSearched.append(self._stack[-1])
        try:
            if self._stack[-1] == "DeadEnd":
                self.deadEnd()
        except:
            pass
        try:
            self._mazeMap[self._stack[-1][0], self._stack[-1][1]]["Type"] = 2
        except:
            print("Dont hit solve twice")
        try:
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

class RHW(Solver):
    def __init__(self):
        super().__init__()
        self._stack = []

    def run(self):
        self.solve()

    def deadEnd(self):
        self._stack.pop()
        if self.findNextMove(self._stack[-1][0], self._stack[-1][1]) == "DeadEnd":
            self.deadEnd()
    
    def solve(self, mazeMap, x:int, y:int):
        #Follows the right hand side of the wall
        ...

