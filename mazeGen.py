import random
import copy
class MazeGen():
    def __init__(self, height:int=15, width:int=15):
        self._height = height
        self._width = width
        self.mazeMapReturn = self.genMaze()  
        self.mazeMap = self.mazeMapReturn[0]
        self.grid = self.mazeMapReturn[1]
        #self.tempMaze = {}
        self.__pickEdge = self.pickEdge()
        self.startPos = self.__pickEdge[0]
        self.endPos = self.__pickEdge[1]
        self.setStartPos(self.startPos)
        self.setEndPos(self.endPos)

################################################
#                                              #
#     CATEGORY A SKILL: COMPLEX DATA MODEL     #
#     CATEGORY B SKILL: DICTIONARIES           #
#                                              #
################################################

    #Generates the blank maze

    def genMaze(self) -> dict: 
        '''
        Generates the raw maze dict base with its Walls and type
        Type: Undefined cell 0, Defined path cell 1, Solved path cell 2, Start 3, End 4.
        '''
        self.mazeMap = {}
        self.grid = []
        y = 0
        for _ in range(self._height): # height
            x = 1
            y += 1
            for _ in range(self._width): # widths
                self.grid.append((x,y))
                self.mazeMap[x,y]={'N':1,'E':1,'S':1,'W':1,'Type':0}
                x += 1
        return self.mazeMap, self.grid

    def setMazeMap(self, newMazeMap:dict) -> dict:
        self.mazeMap = newMazeMap

    @property
    def getMazeMap(self) -> dict:
        return self.mazeMap

    @property
    def getGrid(self) -> list:
        return self.grid

    def setTempMaze(self, newTempMaze:dict) -> dict:
        self.tempMaze = newTempMaze

    @property
    def getTempMaze(self) -> dict:
        return self.tempMaze

    #Sets the start and end positions

    def pickEdge(self) -> list:
        '''
        This will pick the starting and ending COORDs for the maze
        '''
        edge = random.randint(1,4)
        if edge == 1: #North
            #Start Coord
            startCoord = [random.randint(1, self._width),1]
            self.mazeMap[startCoord[0],startCoord[1]]["N"] = 0
            #End Coord
            endCoord = [random.randint(1, self._width),self._height]
            self.mazeMap[endCoord[0],endCoord[1]]["S"] = 0
        elif edge == 2: #East
            #Start Coord
            startCoord = [self._width,random.randint(1, self._height)]
            self.mazeMap[startCoord[0],startCoord[1]]["E"] = 0
            #End Coord
            endCoord = [1,random.randint(1, self._height)]
            self.mazeMap[endCoord[0],endCoord[1]]["W"] = 0
        elif edge == 3: #South
            #Start Coord
            startCoord = [random.randint(1, self._width),self._height]
            self.mazeMap[startCoord[0],startCoord[1]]["S"] = 0
            #End Coord
            endCoord = [random.randint(1, self._width),1]
            self.mazeMap[endCoord[0],endCoord[1]]["N"] = 0
        elif edge == 4: #West
            #Start Coord
            startCoord = [1,random.randint(1, self._height)]
            self.mazeMap[startCoord[0],startCoord[1]]["W"] = 0
            #End Coord
            endCoord = [self._width,random.randint(1, self._height)]
            self.mazeMap[endCoord[0],endCoord[1]]["E"] = 0
        return startCoord, endCoord

    def setStartPos(self, edgeCoord:list) -> dict:
        '''
        This sets the start point type
        '''
        self.startPos = [edgeCoord[0], edgeCoord[1]]
        #print(f"Start Point: {edgeCoord}")
        self.mazeMap[edgeCoord[0], edgeCoord[1]]["Type"] = 3
        return self.startPos

    def setEndPos(self, edgeCoord:list) -> dict:
        '''
        This sets the end point type
        '''
        self.endPos = [edgeCoord[0], edgeCoord[1]]
        #print(f"End Point: {edgeCoord}")
        self.mazeMap[edgeCoord[0], edgeCoord[1]]["Type"] = 4 #if removed then maze can be fully generated
        return self.endPos

    @property 
    def getStartPos(self) -> list:
        return self.startPos

    @property
    def getEndPos(self) -> list:
        return self.endPos

    def setWidth(self, newWidth:int) -> int:
        self._width = newWidth

    @property
    def getWidth(self) -> int:
        return self._width
    
    def setHeight(self, newHeight:int) -> int:
        self._height = newHeight

    @property
    def getHeight(self) -> int:
        return self._height