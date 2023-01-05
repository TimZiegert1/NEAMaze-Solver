from generator import *
import random
from queue import PriorityQueue
class Solver():
    def __init__(self):
        #self._mazeMap = mazeMap
        #self._x = x
        #self._y = y
        ...

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
        self._mazeMap = mazeMap
        if self.checkIsEnd(x, y) == "End":
            print(self._stack)
            print("Solved")
            self.setSolution()
            self._stack = []
            return "Solved"
        self._stack.append(self.findNextMove(x, y))
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
            self.solve(self._mazeMap, self._stack[-1][0], self._stack[-1][1])
        except IndexError:
            pass

    def setSolution(self):
        for cell in self._mazeMap:
            self._mazeMap[cell[0], cell[1]]["Type"] = 1
        for cell in self._stack:
            self._mazeMap[cell[0], cell[1]]["Type"] = 2


class AStar(Solver):
    def __init__(self):
        super().__init__()
        self._start = self._mazeGen.getStartPos
        self._gScore= {cell: float("inf") for cell in self._mazeMap}
        self._gScore[self._start] = 0
        self._fScore= {cell: float("inf") for cell in self._mazeMap}
    
    def heuristic(self, x:int, y:int) -> int:
        x1, y1 = x
        x2, y2 = y
        return abs(x1-x2) + abs(y1-y2)

    def run(self):
        open= PriorityQueue()
        open.put(self.heuristic(self._start,(1,1), self.heuristic(self._start, (1,1), self._start)))
        closed = []
        while not open.empty():
            current = open.get()[2]
            if current == self._mazeGen.getEndPos:
                return "Solved"
            closed.append(current)
            for neighbour in self.checkNeighCells(current[0], current[1]):
                if neighbour in closed:
                    continue
                tentative_gScore = self._gScore[current] + 1
                if tentative_gScore >= self._gScore[neighbour]:
                    continue
                self._cameFrom[neighbour] = current
                self._gScore[neighbour] = tentative_gScore
                self._fScore[neighbour] = self._gScore[neighbour] + self.heuristic(neighbour, self._mazeGen.getEndPos)
                if neighbour not in [i[2] for i in open.queue]:
                    open.put((self._fScore[neighbour], neighbour))
        return "No Solution"


    def algorithm():
        ...

class BFS(Solver):
    def __init__(self):
        super().__init__()
        self._queue = []
    
    def run(self):
        self.solve()
        #self._mazeGen._mazeMap = mazeMap
    
    def solve(self, mazeMap, x:int, y:int):
        #Breadth first search algorithm
        self._mazeMap = mazeMap
        self._queue.append(self.findNextMove(x, y))
        if self._queue[-1] == "DeadEnd":
            self.deadEnd()
        self._mazeMap[self._queue[-1][0], self._queue[-1][1]]["Type"] = 2
        if self.findNextMove(self._queue[-1][0], self._queue[-1][1]) == "End":
            print(self._queue)
            print("Solved")
            return "Solved"
        try:
            self.solve(self._mazeMap, self._queue[-1][0], self._queue[-1][1])
        except IndexError:
            print(self._queue)
            print("ERROR")
            pass
        #self._mazeGen.changeCellType(self._stack[-1][0], self._stack[-1][1], 2)

class RHW(Solver):
    def __init__(self):
        super().__init__()
        self._stack = []

    def run(self):
        self.solve()
        #self._mazeGen._mazeMap = mazeMap

    def deadEnd(self):
        self._stack.pop()
        if self.findNextMove(self._stack[-1][0], self._stack[-1][1]) == "DeadEnd":
            self.deadEnd()
    
    def solve(self, mazeMap, x:int, y:int):
        #Follows the right hand side of the wall
        self._mazeMap = mazeMap
        self._stack.append(self.findNextMove(x, y))
        if self._stack[-1] == "DeadEnd":
            self.deadEnd()
        self._mazeMap[self._stack[-1][0], self._stack[-1][1]]["Type"] = 2
        ...

      
