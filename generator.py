import random
from colorama import init, Fore

class MazeGen:
    def __init__(self):
        init()
        self._maze = [[],[]]# * userChoice

    #Generatos the basic maze with "u" (unvisted) as all its slots
    def genMaze(self, width, height):
        ...
        '''for _ in range(height):
            line = []
            for _ in range(width):
                line.append("u")
            self._maze.append(line)
        self.startPos(height, width)
        self.printMaze(self._maze)'''   

    def startPos(self, height, width):
        startingHeight = random.randint(1,height-1)
        startingWidth = random.randint(1,width-1)
        self.maze[startingHeight][startingWidth] = f" {self.cell}" 
        self.addWall(startingHeight, startingWidth)  

    def addWall(self, startingHeight, startingWidth):
        ... 
            
        

    #Prints out the maze
    def printMaze(self, maze):
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == "u":
                    print(Fore.WHITE, f"{maze[i][j]}", end=" ")
                elif maze[i][j] == "W":
                    print(Fore.RED, f"{maze[i][j]}", end=" ")
                else:
                    print(f"{maze[i][j]}", end=" ")
            print("\n")
 

