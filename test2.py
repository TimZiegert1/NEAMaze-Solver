class MazeGen:
    def __init__(self):
        self._mazeMap = {}

    #This Procedure will generate a maze grid layout of the users chosen size
    def genMaze(self, height:int, width:int) -> dict:
        #Type: Undefined cell 0, Defined path cell 1, Start 2, End 3.
        y = 0
        for _ in range(height): # height
            x = 1
            y += 1
            for _ in range(width): # widths
                self._mazeMap[x,y]={'E':1,'W':1,'N':1,'S':1,'Type':0}
                x += 1  
        return self._mazeMap

mazeThing =MazeGen()
print(mazeThing.genMaze(2,3))