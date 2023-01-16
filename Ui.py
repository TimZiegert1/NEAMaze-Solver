from generator import *
from solver import *
from mazeGen import *
import tkinter as tk
import pygame
import copy
import time
import mysql.connector
class Ui:
    def __init__(self):
        #self._clock = pygame.time.Clock()
        self._height = 15
        self._width = 15
        self._mazeGen = MazeGen(self._height, self._width)
        self._black= (0, 0, 0)
        self._white = (255, 255, 255)
        self._green = (0, 255, 0)
        self._red = ( 255, 0, 0)
        self._blue = (0,0,255)
        self._searchTime = 0.15
        self._solveTime = 0.05
        self._isPaused = False
        self._isGeneration = False
        '''
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="Test",
            password="Test",
            database="Maze"
        )
        '''

class Terminal(Ui):
    def __init__(self):
        super().__init__()  

    def run(self):
        print(self._mazeGen.getMazeMap)
class GUI(Ui):
    def __init__(self):
        super().__init__()
        pygame.init()
        #Use either 15x15 or 25x25, these work best with the screen size
        self._font = pygame.font.Font(None, 50)
        self._main = tk.Tk()
        self._mazeScreen = pygame.display.set_mode((1375,850), flags=pygame.HIDDEN) #15 rows and 15 col is perfect fit!
        self._xBox = self.getRescaleValue(self._width, self._height)[0]
        self._yBox = self.getRescaleValue(self._width, self._height)[1]
        self._xWall = self.getRescaleValue(self._width, self._height)[2]
        self._yWall = self.getRescaleValue(self._width, self._height)[3]

    def run(self):
        self.startPanel()

    def startPanel(self):
        self._main.title("Main")
        mazeButton = tk.Button(self._main, text="Maze",width=20,height=3, command=lambda: [self._main.destroy(), self.mazePanel()] )
        helpButton = tk.Button(self._main, text="Help",width=20, height=3)#, command=self.helpPanel)
        quitButton = tk.Button(self._main, text="Quit",width=20,height=3, command=self._main.destroy)
        mazeButton.grid(row=0, column=0)
        helpButton.grid(row=1,column=0)
        quitButton.grid(row=2, column=0)
        self._main.mainloop()

    #def dataBase(self):
        '''
        self._database = tk.Tk()
        self._database.deiconify()
        self._database.title("Database")
        self._database.mainloop()
        '''
        #print(self.mydb)

    def settingsPanel(self):
        self._settings = tk.Tk()
        self._settings.deiconify()
        self._settings.title("Settings")
        widthLabel = tk.Label(self._settings, text="Width")
        heightLabel = tk.Label(self._settings, text="Height")
        #self._wSlider = tk.Scale(self._settings, from_=4, to=200, orient=tk.HORIZONTAL, command=self.slide())#, command=self.changeWidth)
        #self._hSlider = tk.Scale(self._settings, from_=4, to=200, orient=tk.HORIZONTAL)#, command=self.changeHeight)
        #self._wSlider.set(self._width)
        #self._hSlider.set(self._height)
        speedSearch = tk.Label(self._settings, text="Speed of Search")
        speedSolve = tk.Label(self._settings, text="Speed of Solve")
        startPos = tk.Label(self._settings, text="Start Position")
        endPos = tk.Label(self._settings, text="End Position")
        widthLabel.grid(row=0, column=0)
        heightLabel.grid(row=1, column=0)
        speedSearch.grid(row=2, column=0)
        speedSolve.grid(row=3, column=0)
        startPos.grid(row=4, column=0)
        endPos.grid(row=5, column=0) 
        wBox = tk.Entry(self._settings, width=5)
        hBox = tk.Entry(self._settings, width=5)
        speedSliderSearch = tk.Scale(self._settings, from_=0.0, to=1.0, resolution=0.01 ,orient=tk.HORIZONTAL)
        speedSliderSolve = tk.Scale(self._settings, from_=0.0, to=1.0, resolution=0.01 ,orient=tk.HORIZONTAL)
        speedSliderSearch.set(self._searchTime)
        speedSliderSolve.set(self._solveTime)
        startPosbox = tk.Entry(self._settings, width=5)
        endPosbox = tk.Entry(self._settings, width=5)
        #self._wSlider.grid(row=0, column=1)
        #self._hSlider.grid(row=1, column=1)
        wBox.grid(row=0, column=1)
        hBox.grid(row=1, column=1)
        speedSliderSearch.grid(row=2, column=1)
        speedSliderSolve.grid(row=3, column=1)
        startPosbox.grid(row=4, column=1)
        endPosbox.grid(row=5, column=1)
        applyButton = tk.Button(self._settings, text="Apply", command=lambda: [self.applyButton(hBox, wBox, speedSliderSearch, speedSliderSolve, startPosbox, endPosbox), self._settings.destroy(), self.mazePanel()])
        applyButton.grid(row=6, column=0)
        self._settings.mainloop()

    def applyButton(self, hBox, wBox, speedSliderSearch, speedSliderSolve, startPosbox, endPosbox):
        if hBox.get() == "" or wBox.get() == "" or hBox.get().isdigit() == False or wBox.get().isdigit() == False or int(hBox.get()) < 4 or int(wBox.get()) < 4 or int(hBox.get()) > 200 or int(wBox.get()) > 200:
            pass
        else:
            self._width = int(wBox.get())
            self._height = int(hBox.get())
        if startPosbox.get() == "" or endPosbox.get() == "" or endPosbox.get().isdigit() == False or endPosbox.get().isdigit() == False or int(startPosbox.get()) <= 0 or int(endPosbox.get()) <= 0 or int(startPosbox.get()) > self._mazeGen.getWidth or int(endPosbox.get()) > self._mazeGen.getWidth:
            pass
        else:
            self._mazeGen.getMazeMap[self._mazeGen.getStartPos]["Type"] = 0
            self._mazeGen.getMazeMap[self._mazeGen.getEndPos]["Type"] = 0
            self._mazeGen.getMazeMap[int(startPosbox.get())].setStartPos()
            self._mazeGen.getMazeMap[int(endPosbox.get())].setEndPos()
        self._searchTime = speedSliderSearch.get()
        self._solveTime = speedSliderSolve.get()
        self._mazeGen = MazeGen(self._height, self._width)
        #self._mazeGen.genMaze()
        self._xBox = self.getRescaleValue(self._width, self._height)[0]
        self._yBox = self.getRescaleValue(self._width, self._height)[1]
        self._xWall = self.getRescaleValue(self._width, self._height)[2]
        self._yWall = self.getRescaleValue(self._width, self._height)[3]
        self.drawMaze(self._mazeGen.getMazeMap)
        self._settings.destroy()
        #self._settings.withdraw()
        self.mazePanel()

    def helpButton(self):
        ...

    def mazePanel(self):
        self._mazeScreen = pygame.display.set_mode((1375,850), flags=pygame.SHOWN)
        self._mazeScreen.fill((255,255,255))
        self.drawMaze(self._mazeGen.getMazeMap)
        self.drawButtons()
        #self.drawMazeTest(self._mazeMap)
        #C:\Users\Tim Ziegert\AppData\Local\Programs\Python\Python310
        #self.dataBase()
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                #Quit button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 670 and mouse[1] < 720 and mouse[0] < 1080:
                        running = False
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1290 and mouse[1] > 10 and mouse[1] < 85 and mouse[0] < 1365:
                        print("settings")
                        #run settings
                        self.settingsPanel()
                        break
                #RDFS GEN button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 570 and mouse[1] < 620 and mouse[0] < 1080:
                        #self._gen.findNextMove(self._gen.startPoint[0], self._gen.startPoint[1])
                        self._isGeneration = True
                        self._RDFS = RDFS(self._mazeGen)
                        #print(self._RDFS.getGen)
                        self._RDFS.run()
                        genStack = self._RDFS.getGen
                        #genStack = [("N",14,14)]
                        #print(genStack)
                        self.drawMaze(self._mazeGen.getMazeMap)
                        #self.drawMazeGen(genStack)
                #HuntAndKill gen button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 270 and mouse[1] < 320 and mouse[0] < 1080:
                        self._isGeneration = True
                        self._huntAndKill = HuntAndKill(self._mazeGen)
                        self._huntAndKill.run()
                        self.drawMaze(self._mazeGen.getMazeMap)
                #Solve DFS Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 520 and mouse[1] < 570 and mouse[0] < 1080:
                        self._isGeneration = False
                        self._DFS = DFS(self._mazeGen)
                        self._DFS.run()
                        #self.drawMaze(self._mazeGen.getMazeMap) # THIS TO PRINT INSTANTLY
                        rdfsSearch = self._DFS.getSearch
                        rdfsSolve = self._DFS.getSolution
                        rdfsSolve.reverse()
                        '''
                        if stepButton == True:
                            self.drawMazeSolveStep(self._mazeGen.getMazeMap, rdfsSearch, rdfsSolve, self._searchTime, self._solveTime)
                            rdfsSolve.pop()[0]
                        '''
                        self.drawMazeSolve(self._mazeGen.getMazeMap, rdfsSearch, rdfsSolve, self._searchTime, self._solveTime)
                #Solve AStar Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 470 and mouse[1] < 520 and mouse[0] < 1080:
                        self._isGeneration = False
                        self._AStar = AStar(self._mazeGen)
                        self._AStar.run()
                        #AStarSearch = self._AStar.getSolution[0]
                        AStarSearch = [x for x in self._AStar.getSolution[0]]
                        #AStarSolve = self._AStar.getSolution[1]
                        AStarSolve = [x for x in self._AStar.getSolution[1]]
                        #self.drawMaze(self._mazeGen.getMazeMap)
                        self.drawMazeSolve(self._mazeGen.getMazeMap, AStarSearch, AStarSolve, self._searchTime, self._solveTime)
                #Solve BFS Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 420 and mouse[1] < 470 and mouse[0] < 1080:
                        self._isGeneration = False
                        self._BFS = BFS(self._mazeGen)
                        self._BFS.run()
                        #BFSSearch = self._BFS.getSolution[0]
                        BFSSearch = [x for x in self._BFS.getSolution[0]]
                        #BFSSolve = self._BFS.getSolution[1]
                        BFSSolve = [x for x in self._BFS.getSolution[1]]
                        #self.drawMaze(self._mazeGen.getMazeMap)
                        self.drawMazeSolve(self._mazeGen.getMazeMap, BFSSearch, BFSSolve, self._searchTime, self._solveTime)
                #Solve RHW Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 370 and mouse[1] < 420 and mouse[0] < 1080:
                        self._isGeneration = False
                        self._RHW = RHW(self._mazeGen)
                        self._RHW.run()
                        self.drawMaze(self._mazeGen.getMazeMap)
                #Dijkstra Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()  
                    if mouse[0] > 980 and mouse[1] > 220 and mouse[1] < 270 and mouse[0] < 1080:
                        self._isGeneration = False
                        self._Dijkstra = Dijkstra(self._mazeGen)
                        self._Dijkstra.run()
                        #DijkstraSearch = self._Dijkstra.getSolution[0]
                        DijkstraSearch = [x for x in self._Dijkstra.getSolution[0]]
                        #DijkstraSolve = self._Dijkstra.getSolution[1]
                        DijkstraSolve = [x for x in self._Dijkstra.getSolution[1]]
                        #self.drawMaze(self._mazeGen.getMazeMap)
                        self.drawMazeSolve(self._mazeGen.getMazeMap, DijkstraSearch, DijkstraSolve, self._searchTime, self._solveTime)
                #Generate new maze button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 620 and mouse[1] < 670 and mouse[0] < 1080:
                        self._mazeGen.setMazeMap = {}
                        self._mazeGen = MazeGen(self._height, self._width)
                        self.drawMaze(self._mazeGen.getMazeMap)
                        #self.drawMazeTest(self.getMazeMap)
                #Clear Solve button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 320 and mouse[1] < 370 and mouse[0] < 1080:
                        self._mazeGen.setMazeMap(copy.deepcopy(self._mazeGen.getTempMaze))
                        self.drawMaze(self._mazeGen.getTempMaze)
                #Pause button
                #if event.type == pygame.MOUSEBUTTONDOWN:
                    #mouse = pygame.mouse.get_pos()
                    #if mouse[0] > 980 and mouse[1] > 170 and mouse[1] < 220 and mouse[0] < 1080:
        pygame.quit()
        #This line allows to close and reopen the window
        #self._mazeScreen = pygame.display.set_mode((1080, 720), flags=pygame.HIDDEN)

    def drawWalls(self,mazeMap):
        y=-1
        for _ in range(self._height): # height
            x = 0
            y += 1
            for _ in range(self._width): # widths
                if mazeMap[x+1,y+1]["N"] == 1:
                    #pygame.draw.rect(self._mazeScreen, self._black, ((x*55)+5,((y*50)+(y-1)*5)+10,60,5))
                    pygame.draw.rect(self._mazeScreen, self._black, ((x*(self._xBox+self._xWall))+self._xWall,((y*self._yBox)+(y-1)*self._yWall)+(2*self._yWall),(self._xBox+(2*self._xWall)),self._xWall))
                if mazeMap[x+1,y+1]["S"] == 1:
                    #pygame.draw.rect(self._mazeScreen, self._black, ((x*55)+5,((y*50)+(y-1)*5)+65,60,5))
                    pygame.draw.rect(self._mazeScreen, self._black, ((x*(self._xBox+self._xWall))+self._xWall,((y*self._yBox)+(y-1)*self._yWall)+(self._yBox+(3*self._yWall)),(self._xBox+(2*self._xWall)),self._xWall))
                if mazeMap[x+1,y+1]["E"] == 1:
                    #pygame.draw.rect(self._mazeScreen, self._black, (((x*50)+(x-1)*5)+65,(y*55)+5,5,60))
                    pygame.draw.rect(self._mazeScreen, self._black, (((x*self._xBox)+(x-1)*self._xWall)+(self._xBox+(3*self._xWall)),(y*(self._yBox+self._yWall))+self._yWall,self._yWall,self._yBox+(2*self._yWall)))
                if mazeMap[x+1,y+1]["W"] == 1:
                    #pygame.draw.rect(self._mazeScreen, self._black, (((x*50)+(x-1)*5)+10,(y*55)+5,5,60))
                    pygame.draw.rect(self._mazeScreen, self._black, (((x*self._xBox)+(x-1)*self._xWall)+(2*self._xWall),(y*(self._yBox+self._yWall))+self._yWall,self._yWall,self._yBox+(2*self._yWall)))
                x += 1

    def drawMaze(self, mazeMap):
        y=-1
        for _ in range(self._height): # height
            x = 0
            y += 1
            for _ in range(self._width): # widths
                if mazeMap[x+1,y+1]["Type"] == 3:
                    #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._white, ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                elif mazeMap[x+1,y+1]["Type"] == 4:
                    #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._white, ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                elif mazeMap[x+1,y+1]["Type"] == 0:
                    #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._white, ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                elif mazeMap[x+1,y+1]["Type"] == 1:
                    #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._white, ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                elif mazeMap[x+1,y+1]["Type"] == 5:
                    #pygame.draw.rect(self._mazeScreen, (50,50,50), ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, (50,50,50), ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                elif mazeMap[x+1,y+1]["Type"] == 2:
                    #pygame.draw.rect(self._mazeScreen, (255,0,50), ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, (255,0,50), ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                self.drawWalls(mazeMap)
                if self._isGeneration == True:
                    if mazeMap[x+1,y+1]["Type"] == 3:
                        #pygame.draw.rect(self._mazeScreen, self._blue, ((x*55)+10,(y*55)+10,55,55))
                        pygame.draw.rect(self._mazeScreen, self._blue, ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                    elif mazeMap[x+1,y+1]["Type"] == 4:
                        #pygame.draw.rect(self._mazeScreen, self._red, ((x*55)+10,(y*55)+10,55,55))
                        pygame.draw.rect(self._mazeScreen, self._red, ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                    if mazeMap[x+1,y+1]["N"] == 0:
                        #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,((y*50)+(y-1)*5)+10,50,5))
                        pygame.draw.rect(self._mazeScreen, self._white, ((x*(self._xBox+self._xWall))+(2*self._xWall),((y*self._yBox)+(y-1)*self._yWall)+(2*self._yWall),self._xBox,self._yWall))
                    if mazeMap[x+1,y+1]["S"] == 0:
                        #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,((y*50)+(y-1)*5)+65,50,5))
                        pygame.draw.rect(self._mazeScreen, self._white, ((x*(self._xBox+self._xWall))+(2*self._xWall),((y*self._yBox)+(y-1)*self._yWall)+self._yBox+(3*self._yWall),self._xBox,self._yWall))
                    if mazeMap[x+1,y+1]["E"] == 0:
                        #pygame.draw.rect(self._mazeScreen, self._white, (((x*50)+(x-1)*5)+65,(y*55)+10,5,50))
                        pygame.draw.rect(self._mazeScreen, self._white, (((x*self._xBox)+(x-1)*self._xWall)+self._xBox+(3*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xWall,self._yBox))
                    if mazeMap[x+1,y+1]["W"] == 0:
                        #pygame.draw.rect(self._mazeScreen, self._white, (((x*50)+(x-1)*5)+10,(y*55)+10,5,50)) 
                        pygame.draw.rect(self._mazeScreen, self._white, (((x*self._xBox)+(x-1)*self._xWall)+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xWall,self._yBox)) 
                    #pygame.display.update()
                x += 1
        pygame.display.update() #USE THIS IF YOU WANT IT TO BE INSTANT

    def drawMazeGen(self, path):
        xBox = self.getRescaleValue(self._width, self._height)[0]
        yBox = self.getRescaleValue(self._width, self._height)[1]
        xWall = self.getRescaleValue(self._width, self._height)[2]
        yWall = self.getRescaleValue(self._width, self._height)[3]
        for cell in path:
            if cell[0] == "S":
                #pygame.draw.rect(self._mazeScreen, self._white, ((cell[1]*55)-45,((cell[2]*50)+(cell[2]-1)*5)+10,50,5))
                pygame.draw.rect(self._mazeScreen, self._white, ((cell[1]*55)-45,((cell[2]*50)+(cell[2]-1)*5)+10,50,5))
                time.sleep(0.05)
                pygame.display.update()
            elif cell[0] == "W":
                #pygame.draw.rect(self._mazeScreen, self._white, (((cell[1]*50)+(cell[1]-1)*5)-45,(cell[2]*55)-45,5,50)) 
                pygame.draw.rect(self._mazeScreen, self._white, (((cell[1]*50)+(cell[1]-1)*5)-45,(cell[2]*55)-45,5,50)) 
                time.sleep(0.05)
                pygame.display.update()
            elif cell[0] == "E":
                #pygame.draw.rect(self._mazeScreen, self._white, (((cell[1]*50)+(cell[1]-1)*5)+10,(cell[2]*55)-45,5,50))
                pygame.draw.rect(self._mazeScreen, self._white, (((cell[1]*50)+(cell[1]-1)*5)+10,(cell[2]*55)-45,5,50))
                time.sleep(0.05)
                pygame.display.update()
            elif cell[0] == "N":
                #pygame.draw.rect(self._mazeScreen, self._white, ((cell[1]*55)-45,((cell[2]*50)+(cell[2]-1)*5)-45,50,5))
                pygame.draw.rect(self._mazeScreen, self._white, ((cell[1]*55)-45,((cell[2]*50)+(cell[2]-1)*5)-45,50,5))
                time.sleep(0.05)
                pygame.display.update()
            elif cell == "Dead End":
                pass

    def pause(self, index, searchPath):
        self._isPaused = True
        self.drawPauseButton()
        while self._isPaused:
            for event in pygame.event.get():
                # can either run the step button from here or from below
                #if run from here then the game is paused then step works but have to explain that
                #if run from below then can call paused and then step, this will probably work better
                #you have to make it so that step can also be called from the very start
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 170 and mouse[1] < 220 and mouse[0] < 1080:
                        self._isPaused = False
                        self.drawPauseButton()
                        #pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                        pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[index-1][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index-1][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                        return index
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._isPaused = False
                        self.drawPauseButton()
                        #pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                        pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[index-1][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index-1][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                        return index
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 670 and mouse[1] < 720 and mouse[0] < 1080:
                        pygame.quit()
                        quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1290 and mouse[1] > 10 and mouse[1] < 85 and mouse[0] < 1365:
                        print("settings")
                        #run settings
                        self.settingsPanel()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 120 and mouse[1] < 170 and mouse[0] < 1080:
                        if index < len(searchPath):
                            #pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                            #pygame.draw.rect(self._mazeScreen, (255,0,50), ((searchPath[index][0]*55)-45,(searchPath[index][1]*55)-45,55,55))
                            pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[index-1][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index-1][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                            pygame.draw.rect(self._mazeScreen, (255,255,255), ((searchPath[index][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                            self.drawWalls(self._mazeGen.getMazeMap)
                            pygame.display.update()
                            index += 1
                        else:
                            self._isPaused = False
                            self.drawPauseButton()
                            return index
                    if mouse[0] > 980 and mouse[1] > 70 and mouse[1] < 120 and mouse[0] < 1080:
                        if index > 1:
                            #pygame.draw.rect(self._mazeScreen, (255,255,255), ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                            #pygame.draw.rect(self._mazeScreen, (255,0,50), ((searchPath[index-2][0]*55)-45,(searchPath[index-2][1]*55)-45,55,55))
                            pygame.draw.rect(self._mazeScreen, (255,255,255), ((searchPath[index-1][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index-1][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                            pygame.draw.rect(self._mazeScreen, (255,0,50), ((searchPath[index-2][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index-2][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                            self.drawWalls(self._mazeGen.getMazeMap)
                            pygame.display.update()
                            index -= 1
                        else:
                            self._isPaused = False
                            self.drawPauseButton()
                            return index
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if index < len(searchPath):
                            #pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                            #pygame.draw.rect(self._mazeScreen, (255,0,50), ((searchPath[index][0]*55)-45,(searchPath[index][1]*55)-45,55,55))
                            pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[index-1][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index-1][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                            pygame.draw.rect(self._mazeScreen, (255,0,50), ((searchPath[index][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                            self.drawWalls(self._mazeGen.getMazeMap)
                            pygame.display.update()
                            index += 1
                        else:
                            self._isPaused = False
                            self.drawPauseButton()
                            return index
                    if event.key == pygame.K_LEFT:
                        if index > 1:
                            #pygame.draw.rect(self._mazeScreen, (255,255,255), ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                            #pygame.draw.rect(self._mazeScreen, (255,0,50), ((searchPath[index-2][0]*55)-45,(searchPath[index-2][1]*55)-45,55,55))
                            pygame.draw.rect(self._mazeScreen, (255,255,255), ((searchPath[index-1][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index-1][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                            pygame.draw.rect(self._mazeScreen, (255,0,50), ((searchPath[index-2][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index-2][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                            self.drawWalls(self._mazeGen.getMazeMap)
                            pygame.display.update()
                            index -= 1
                        else:
                            self._isPaused = False
                            self.drawPauseButton()
                            return index
            #THIS MAKES SO CAN USE BUTTONS IN PAUSE
                '''
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 620 and mouse[1] < 670 and mouse[0] < 1080:
                        self._mazeGen.setMazeMap = {}
                        self._mazeGen = MazeGen(self._height, self._width)
                        self.drawMaze(self._mazeGen.getMazeMap)
                        pause = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if mouse[0] > 980 and mouse[1] > 320 and mouse[1] < 370 and mouse[0] < 1080:
                            self._mazeGen.setMazeMap(copy.deepcopy(self._mazeGen.getTempMaze))
                            self.drawMaze(self._mazeGen.getTempMaze)
                            pause = False
                '''

    def drawMazeSolve(self, mazeMap, searchPath, solvePath, searchTime = 0.15, solveTime = 0.05, index = 0):
        head = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 170 and mouse[1] < 220 and mouse[0] < 1080:          
                        index = self.pause(index, searchPath)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        index = self.pause(index, searchPath)
                #Step Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 120 and mouse[1] < 170 and mouse[0] < 1080:
                        index = self.pause(index, searchPath)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 980 and mouse[1] > 70 and mouse[1] < 120 and mouse[0] < 1080:
                        index = self.pause(index, searchPath)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        index = self.pause(index, searchPath)
                    if event.key == pygame.K_LEFT:
                        index = self.pause(index, searchPath)
                #COULD ADD A STEP BACK BUTTON

                #CAN ADD OTHER BUTTONS WANTING TO BE USED WHILE BEING SOLVED HERE
            if index < len(searchPath):
                if head != 0:
                    #pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[tempIndex][0]*55)-45,(searchPath[tempIndex][1]*55)-45,55,55))
                    pygame.draw.rect(self._mazeScreen, (50,50,50), ((searchPath[tempIndex][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[tempIndex][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                #pygame.draw.rect(self._mazeScreen, (255,0,50), ((searchPath[index][0]*55)-45,(searchPath[index][1]*55)-45,55,55))
                pygame.draw.rect(self._mazeScreen, (255,0,50), ((searchPath[index][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(searchPath[index][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                tempIndex = index
                self.drawWalls(mazeMap)
                #time.sleep(searchTime)
                pygame.time.wait(int(searchTime*100))
                pygame.display.update()
                head = 1
                index += 1
            else:
                index = 0
                while True:
                    if index < len(solvePath):
                        #pygame.draw.rect(self._mazeScreen, (255,0,50), ((solvePath[index][0]*55)-45,(solvePath[index][1]*55)-45,55,55))
                        pygame.draw.rect(self._mazeScreen, (255,0,50), ((solvePath[index][0]*(self._xBox+self._xWall))-(self._xBox-self._xWall),(solvePath[index][1]*(self._yBox+self._yWall))-(self._yBox-self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                        self.drawWalls(mazeMap)
                        #time.sleep(solveTime)
                        pygame.time.wait(int(solveTime*100))
                        pygame.display.update()
                        index += 1
                    else:
                        break
                break

    #Paste rescale code here to test

    def getRescaleValue(self, width, height):
        rescaleValue = 900
        rescaleHeight = rescaleValue/height
        rescaleWidth = rescaleValue/width
        x = (5*rescaleHeight)/6
        y = (5*rescaleWidth)/6
        xWalls = x/10
        yWalls = y/10
        return x, y, xWalls, yWalls


    def drawButtons(self):
        self.settingsButton(self._mazeScreen, pygame.image.load("settingsIcon.png"),(1290, 10))
        self.quitButton(self._mazeScreen, self._black ,(980, 670,100, 50), "Quit")
        self.clearButton(self._mazeScreen, self._black ,(980, 620,100, 50), "Clear")
        self.rdfsGenButton(self._mazeScreen, self._black ,(980, 570,100, 50), "RDFS Gen")
        self.huntAndKillButton(self._mazeScreen, self._black ,(980, 270,100, 50), "Hunt and Kill")
        self.solveRDFSButton(self._mazeScreen, self._black ,(980, 520,100, 50), "Solve")
        self.solveAStarButton(self._mazeScreen, self._black ,(980, 470,100, 50), "A*")
        self.solveBFSButton(self._mazeScreen, self._black ,(980, 420,100, 50), "BFS")
        self.solveRHWButton(self._mazeScreen, self._black ,(980, 370,100, 50), "RHW")
        self.solveDijkstraButton(self._mazeScreen, self._black ,(980, 220,100, 50), "Dijkstra")
        self.clearSolveButton(self._mazeScreen, self._black ,(980, 320,100, 50), "Clear Solve")
        self.pauseButton(self._mazeScreen, self._black ,(980, 170,100, 50), "Pause")
        self.stepButton(self._mazeScreen, self._black ,(980, 120,100, 50), "Step")
        self.stepBackwardButton(self._mazeScreen, self._black ,(980, 70,100, 50), "Step Back")


    def quitButton(self, screen, colour, pos, text:str):
        quitButton = pygame.draw.rect(screen, colour, pos)
        quitText = self._font.render(text, True, (0,0,255))
        screen.blit(quitText, quitText.get_rect(center=quitButton.center))

    def rdfsGenButton(self, screen, colour, pos, text:str):
        runButton = pygame.draw.rect(screen, colour, pos)
        runText = self._font.render(text, True, (255,0,0))
        screen.blit(runText, runText.get_rect(center=runButton.center))

    def huntAndKillButton(self, screen, colour, pos, text:str):
        runButton = pygame.draw.rect(screen, colour, pos)
        runText = self._font.render(text, True, (255,0,0))
        screen.blit(runText, runText.get_rect(center=runButton.center))
    
    def solveRDFSButton(self, screen, colour, pos, text:str):
        solveButton = pygame.draw.rect(screen, colour, pos)
        solveText = self._font.render(text, True, (255,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveAStarButton(self, screen, colour, pos, text:str):
        solveButton = pygame.draw.rect(screen, colour, pos)
        solveText = self._font.render(text, True, (255,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveBFSButton(self, screen, colour, pos, text:str):
        solveButton = pygame.draw.rect(screen, colour, pos)
        solveText = self._font.render(text, True, (255,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveRHWButton(self, screen, colour, pos, text:str):
        solveButton = pygame.draw.rect(screen, colour, pos)
        solveText = self._font.render(text, True, (255,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveDijkstraButton(self, screen, colour, pos, text:str):
        solveButton = pygame.draw.rect(screen, colour, pos)
        solveText = self._font.render(text, True, (255,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def clearButton(self, screen, colour, pos, text:str):
        clearButton = pygame.draw.rect(screen, colour, pos)
        clearText = self._font.render(text, True, (255,0,0))
        screen.blit(clearText, clearText.get_rect(center=clearButton.center))

    def clearSolveButton(self, screen, colour, pos, text:str):
        clearButton = pygame.draw.rect(screen, colour, pos)
        clearText = self._font.render(text, True, (255,0,0))
        screen.blit(clearText, clearText.get_rect(center=clearButton.center))

    def pauseButton(self, screen, colour, pos, text:str):
        pauseButton = pygame.draw.rect(screen, colour, pos)
        pauseText = self._font.render(text, True, (255,0,0))
        screen.blit(pauseText, pauseText.get_rect(center=pauseButton.center))

    #Compare button will first bring up tkinter window to select two mazes to compare
    #Compare button can bring up a new window with two 10x10, or if resize is done anysize mazes side by side
    #and a button to compare the two
    def compareButton(self, screen, colour, pos, text:str):
        compareButton = pygame.draw.rect(screen, colour, pos)
        compareText = self._font.render(text, True, (255,0,0))
        screen.blit(compareText, compareText.get_rect(center=compareButton.center))

    def drawPauseButton(self):
        if self._isPaused == False:
            self.pauseButton(self._mazeScreen, self._black ,(980, 170,100, 50), "Pause")
            pygame.display.update()
        else:
            self.pauseButton(self._mazeScreen, self._black ,(980, 170,100, 50), "unpause")
            pygame.display.update()

    #def unPauseButton(self):
        #pauseButton = pygame.draw.rect(self._mazeScreen, self._white, (900, 170,100, 50))
        #pauseText = self._font.render("unpause", True, (255,0,0))
        #self._mazeScreen.blit(pauseText, pauseText.get_rect(center=pauseButton.center))

    def stepButton(self, screen, colour, pos, text:str):
        stepButton = pygame.draw.rect(screen, colour, pos)
        stepText = self._font.render(text, True, (255,0,0))
        screen.blit(stepText, stepText.get_rect(center=stepButton.center))

    def stepBackwardButton(self, screen, colour, pos, text:str):
        stepButton = pygame.draw.rect(screen, colour, pos)
        stepText = self._font.render(text, True, (255,0,0))
        screen.blit(stepText, stepText.get_rect(center=stepButton.center))

    def settingsButton(self, screen, img, pos):
        screen.blit(img, pos)

    def labels(self):
        ... #Labels for the maze

    def pickGen(self):
        ... #Drop down of all maze Generation algorithms

    def pickSolve(self):
        ... #Drop down of all maze solving algorithms

    def editMaze(self):
        ...

    def customise(self):
        ... #Customise, colours, etc

    def userChangeStart(self):
        ...

    def userChangeEnd(self):
        ...

    def login(self):
        ...

    def logout(self):
        ...

    def createAccount(self):
        ...

    def importMaze(self):
        ...

    def saveMaze(self):
        ...

    