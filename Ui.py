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
        self._bColour = (225,225,225)
        self._hColour = (0,195,195)
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
        self._font1 = pygame.font.Font(None, 40)
        self._fontDij = pygame.font.Font(None, 37)
        self._font2 = pygame.font.Font(None, 30)
        self._fontTxt = pygame.font.Font(None, 20)
        self._main = tk.Tk()
        self._mazeScreen = pygame.display.set_mode((1375,850), flags=pygame.HIDDEN) #15 rows and 15 col is perfect fit!
        self._xBox = self.getRescaleValue(self._width, self._height)[0]
        self._yBox = self.getRescaleValue(self._width, self._height)[1]
        self._xWall = self.getRescaleValue(self._width, self._height)[2]
        self._yWall = self.getRescaleValue(self._width, self._height)[3]
        self._BTdirection = "NW"

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                if event.type == pygame.QUIT:
                    running = False
                    break
                #Quit button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1280 and mouse[1] > 790 and mouse[1] < 840 and mouse[0] < 1380:
                        running = False
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1290 and mouse[1] > 10 and mouse[1] < 85 and mouse[0] < 1365:
                        print("settings")
                        #run settings
                        self.settingsPanel()
                        break
                #Solve DFS Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 885 and mouse[1] > 145 and mouse[1] < 205 and mouse[0] < 995 and self._isGeneration == True:
                        self._DFS = DFS(self._mazeGen)
                        self._DFS.run()
                        rdfsSearch = self._DFS.getSearch
                        rdfsSolve = self._DFS.getSolution
                        rdfsSolve.reverse()
                        self.labels(self._DFS.getTimeTaken, len(rdfsSearch), len(rdfsSolve))
                        self.drawMazeSolve(self._mazeGen.getMazeMap, rdfsSearch, rdfsSolve, self._searchTime, self._solveTime)
                #Solve BFS Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1045 and mouse[1] > 145 and mouse[1] < 205 and mouse[0] < 1155 and self._isGeneration == True:
                        self._BFS = BFS(self._mazeGen)
                        self._BFS.run()
                        BFSSearch = [x for x in self._BFS.getSolution[0]]
                        BFSSolve = [x for x in self._BFS.getSolution[1]]
                        self.labels(self._BFS.getTimeTaken, len(BFSSearch), len(BFSSolve))
                        #self.drawMaze(self._mazeGen.getMazeMap)
                        self.drawMazeSolve(self._mazeGen.getMazeMap, BFSSearch, BFSSolve, self._searchTime, self._solveTime)
                #Solve AStar Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 885 and mouse[1] > 215 and mouse[1] < 275 and mouse[0] < 995 and self._isGeneration == True:
                        self._AStar = AStar(self._mazeGen)
                        self._AStar.run()
                        AStarSearch = [x for x in self._AStar.getSolution[0]]
                        AStarSolve = [x for x in self._AStar.getSolution[1]]
                        self.labels(self._AStar.getTimeTaken, len(AStarSearch), len(AStarSolve))
                        #self.drawMaze(self._mazeGen.getMazeMap)
                        self.drawMazeSolve(self._mazeGen.getMazeMap, AStarSearch, AStarSolve, self._searchTime, self._solveTime)
                #Dijkstra Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()  
                    if mouse[0] > 1205 and mouse[1] > 145 and mouse[1] < 205 and mouse[0] < 1315 and self._isGeneration == True:
                        self._Dijkstra = Dijkstra(self._mazeGen)
                        self._Dijkstra.run()
                        DijkstraSearch = [x for x in self._Dijkstra.getSolution[0]]
                        DijkstraSolve = [x for x in self._Dijkstra.getSolution[1]]
                        self.labels(self._Dijkstra.getTimeTaken, len(DijkstraSearch), len(DijkstraSolve))
                        #self.drawMaze(self._mazeGen.getMazeMap)
                        self.drawMazeSolve(self._mazeGen.getMazeMap, DijkstraSearch, DijkstraSolve, self._searchTime, self._solveTime)
                #Solve RHW Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1045 and mouse[1] > 215 and mouse[1] < 275 and mouse[0] < 1155 and self._isGeneration == True:
                        self._RHW = RHW(self._mazeGen)
                        self._RHW.run()
                        RHWSearch = self._RHW.getSolution[0]
                        RHWSolve = self._RHW.getSolution[1]
                        RHWSolve.reverse()
                        self.labels(self._RHW.getTimeTaken, len(RHWSearch), len(RHWSolve))
                        self.drawMazeSolve(self._mazeGen.getMazeMap, RHWSearch, RHWSolve, self._searchTime, self._solveTime)
                #Solve LHW Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1205 and mouse[1] > 215 and mouse[1] < 275 and mouse[0] < 1315  and self._isGeneration == True:
                        self._LHW = LHW(self._mazeGen)
                        self._LHW.run()
                        LHWSearch = self._LHW.getSolution[0]
                        LHWSolve = self._LHW.getSolution[1]
                        LHWSolve.reverse()
                        self.labels(self._LHW.getTimeTaken, len(LHWSearch), len(LHWSolve))
                        self.drawMazeSolve(self._mazeGen.getMazeMap, LHWSearch, LHWSolve, self._searchTime, self._solveTime)
                        #self.drawMazeTest(self.getMazeMap)
                #Clear Solve button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1205 and mouse[1] > 375 and mouse[1] < 435 and mouse[0] < 1315 and self._isGeneration == True:
                        self._mazeGen.setMazeMap(copy.deepcopy(self._mazeGen.getTempMaze))
                        self.drawMaze(self._mazeGen.getTempMaze)
                        self._isGeneration = False
                #RDFS GEN button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 885 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 995 and self._isGeneration == False:
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
                    if mouse[0] > 1045 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 1155 and self._isGeneration == False:
                        self._isGeneration = True
                        self._huntAndKill = HuntAndKill(self._mazeGen)
                        self._huntAndKill.run()
                        self.drawMaze(self._mazeGen.getMazeMap)
                #Binary Tree gen button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1205 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 1315 and self._isGeneration == False:
                        self._isGeneration = True
                        self._binaryTree = BinaryTree(self._mazeGen)
                        self._binaryTree.run(self._BTdirection)
                        self.drawMaze(self._mazeGen.getMazeMap)
                #Generate new maze button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1210 and mouse[1] > 680 and mouse[1] < 730 and mouse[0] < 1310:
                        self._mazeGen.setMazeMap = {}
                        self._mazeGen = MazeGen(self._height, self._width)
                        self.drawMaze(self._mazeGen.getMazeMap)
                        self._isGeneration = False
                #Hovers
                if event.type == pygame.MOUSEMOTION:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 885 and mouse[1] > 145 and mouse[1] < 205 and mouse[0] < 995:
                        self.solveRDFSHover()
                        self.solveText("This is a test")
                    else:
                        self.solveRDFSButton(self._mazeScreen, (225,225,225) ,(890, 150,100, 50), "RDFS")
                        pygame.display.update()
                    if mouse[0] > 1045 and mouse[1] > 145 and mouse[1] < 205 and mouse[0] < 1155:
                        self.solveBFSHover()
                    else:
                        self.solveBFSButton(self._mazeScreen, self._bColour ,(1050, 150,100, 50), "BFS")
                        pygame.display.update()
                    if mouse[0] > 1205 and mouse[1] > 145 and mouse[1] < 205 and mouse[0] < 1315:
                        self.solveDijkstraHover()
                    else:
                        self.solveDijkstraButton(self._mazeScreen, self._bColour ,(1210, 150,100, 50), "Dijkstra")
                    if mouse[0] > 885 and mouse[1] > 215 and mouse[1] < 275 and mouse[0] < 995:
                        self.solveAStarHover()
                    else:
                        self.solveAStarButton(self._mazeScreen, self._bColour ,(890, 220,100, 50), "A*")
                        pygame.display.update()
                    if mouse[0] > 1045 and mouse[1] > 215 and mouse[1] < 275 and mouse[0] < 1155:
                        self.solveRHWHover()
                    else:
                        self.solveRHWButton(self._mazeScreen, self._bColour ,(1050, 220,100, 50), "RHW")
                        pygame.display.update()
                    if mouse[0] > 1205 and mouse[1] > 215 and mouse[1] < 275 and mouse[0] < 1315:
                        self.solveLHWHover()
                    else:
                        self.solveLHWButton(self._mazeScreen, self._bColour ,(1210, 220,100, 50), "LHW")
                        pygame.display.update()
                    if mouse[0] > 1205 and mouse[1] > 375 and mouse[1] < 435 and mouse[0] < 1315:
                        self.clearSolveHover()
                    else:
                        self.clearSolveButton(self._mazeScreen, self._bColour ,(1210, 380,100, 50), "Clear")
                        pygame.display.update()
                    if mouse[0] > 885 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 995:
                        self.rdfsGenHover()
                    else:
                        self.rdfsGenButton(self._mazeScreen, self._bColour ,(890, 510,100, 50), "RBT")
                        pygame.display.update()
                    if mouse[0] > 1045 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 1155:
                        self.huntAndKillHover()
                    else:
                        self.huntAndKillButton(self._mazeScreen, self._bColour ,(1050, 510,100, 50), "Hunt&Kill")
                        pygame.display.update()
                    if mouse[0] > 1205 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 1315:
                        self.binaryTreeHover()
                    else:
                        self.binaryTreeButton(self._mazeScreen, self._bColour ,(1210, 510,100, 50), "BST")
                        pygame.display.update()
                    if mouse[0] > 1210 and mouse[1] > 680 and mouse[1] < 730 and mouse[0] < 1310:
                        self.clearHover()
                    else:
                        self.clearButton(self._mazeScreen, self._bColour ,(1210, 680,100, 50), "Clear")
                        pygame.display.update()
                
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
                    pygame.draw.rect(self._mazeScreen, self._blue, ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
                elif mazeMap[x+1,y+1]["Type"] == 4:
                    #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._red, ((x*(self._xBox+self._xWall))+(2*self._xWall),(y*(self._yBox+self._yWall))+(2*self._yWall),self._xBox+self._xWall,self._yBox+self._yWall))
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
                #Pause button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1075 and mouse[1] > 780 and mouse[1] < 830 and mouse[0] < 1125:
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
                #Quit Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1280 and mouse[1] > 790 and mouse[1] < 840 and mouse[0] < 1380:
                        pygame.quit()
                        quit()
                #Settings Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1290 and mouse[1] > 10 and mouse[1] < 85 and mouse[0] < 1365:
                        print("settings")
                        #run settings
                        self.settingsPanel()
                #Step Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1150 and mouse[1] > 780 and mouse[1] < 830 and mouse[0] < 1200:
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
                    if mouse[0] > 1000 and mouse[1] > 780 and mouse[1] < 830 and mouse[0] < 1050:
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
                    if mouse[0] > 1075 and mouse[1] > 780 and mouse[1] < 830 and mouse[0] < 1125:          
                        index = self.pause(index, searchPath)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        index = self.pause(index, searchPath)
                #Step Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1150 and mouse[1] > 780 and mouse[1] < 830 and mouse[0] < 1200:
                        index = self.pause(index, searchPath)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1000 and mouse[1] > 780 and mouse[1] < 830 and mouse[0] < 1050:
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
                if searchTime != 0:
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
                        if solveTime != 0:
                            pygame.display.update()
                        index += 1
                    else:
                        break
                break
        pygame.display.update()    

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
        #Solve Border
        pygame.draw.rect(self._mazeScreen, self._black ,(850,100,500,350))
        pygame.draw.rect(self._mazeScreen, self._white ,(855,105,490,340))
        self._mazeScreen.blit(self._font.render("Solve", True, (0,0,0)), (1050,110))
        #Gen Border
        pygame.draw.rect(self._mazeScreen, self._black ,(850,455,500,300))
        pygame.draw.rect(self._mazeScreen, self._white ,(855,460,490,290))
        self._mazeScreen.blit(self._font.render("Generate", True, (0,0,0)), (1025,465))

        self._mazeScreen.blit(self._font2.render("Time Taken", True, (0,0,0)), (850,10))
        self._mazeScreen.blit(self._font2.render("Searched Cells", True, (0,0,0)), (980,10))
        self._mazeScreen.blit(self._font2.render("Solved Cells", True, (0,0,0)), (1150,10))
        self.labels()   

        self.settingsButton(self._mazeScreen, pygame.image.load("img\settingsIcon.png") ,(1290, 10))
        self.pauseButton(self._mazeScreen, pygame.image.load("img\pause.png") ,(1075, 780))
        self.stepButton(self._mazeScreen, pygame.image.load("img\stepButton.png") ,(1150, 780))
        self.stepBackButton(self._mazeScreen, pygame.image.load("img\stepBackButton.png") ,(1000, 780))
        self.quitButton(self._mazeScreen, self._white ,(1270, 790,100, 50), "Quit")

        self.solveRDFSButton(self._mazeScreen, self._bColour ,(890, 150,100, 50), "RDFS")
        self.solveBFSButton(self._mazeScreen, self._bColour ,(1050, 150,100, 50), "BFS")
        self.solveDijkstraButton(self._mazeScreen, self._bColour ,(1210, 150,100, 50), "Dijkstra")
        self.solveAStarButton(self._mazeScreen, self._bColour ,(890, 220,100, 50), "A*")
        self.solveRHWButton(self._mazeScreen, self._bColour ,(1050, 220,100, 50), "RHW")
        self.solveLHWButton(self._mazeScreen, self._bColour ,(1210, 220,100, 50), "LHW")
        self.clearSolveButton(self._mazeScreen, self._bColour ,(1210, 380,100, 50), "Clear")  
                
        self.clearButton(self._mazeScreen, self._bColour ,(1210, 680, 100, 50), "Clear")
        self.rdfsGenButton(self._mazeScreen, self._bColour ,(890, 510,100, 50), "RBT")
        self.huntAndKillButton(self._mazeScreen, self._bColour ,(1050, 510,100, 50), "Hunt&Kill")
        self.binaryTreeButton(self._mazeScreen, self._bColour ,(1210, 510,100, 50), "BST")


    def quitButton(self, screen, colour, pos, text:str):
        quitButton = pygame.draw.rect(screen, colour, pos)
        quitText = self._font.render(text, True, (255,0,0))
        screen.blit(quitText, quitText.get_rect(center=quitButton.center))

    def solveRDFSButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (885,145,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))
    
    def solveRDFSHover(self):
        #pygame.draw.rect(self._mazeScreen, self._black, (885,145,110,60), border_radius=18)
        solveButton = pygame.draw.rect(self._mazeScreen, self._hColour,(890, 150,100, 50), border_radius=15)
        solveText = self._font1.render("RDFS", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def solveBFSButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (1045,145,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveBFSHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._hColour, (1050, 150,100, 50), border_radius=15)
        solveText = self._font1.render("BFS", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()
    
    def solveDijkstraButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (1205,145,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._fontDij.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))
    
    def solveDijkstraHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._hColour, (1210, 150,100, 50), border_radius=15)
        solveText = self._fontDij.render("Dijkstra", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def solveAStarButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (885,215,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveAStarHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._hColour, (890, 220,100, 50), border_radius=15)
        solveText = self._font1.render("A*", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def solveRHWButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (1045,215,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveRHWHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._hColour, (1050, 220,100, 50), border_radius=15)
        solveText = self._font1.render("RHW", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def solveLHWButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (1205,215,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))
    
    def solveLHWHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._hColour, (1210, 220,100, 50), border_radius=15)
        solveText = self._font1.render("LHW", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def clearSolveButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (1205,375,110,60), border_radius=18)
        clearButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        clearText = self._font1.render(text, True, (0,0,0))
        screen.blit(clearText, clearText.get_rect(center=clearButton.center))
    
    def clearSolveHover(self):
        clearButton = pygame.draw.rect(self._mazeScreen, self._hColour, (1210, 380,100, 50), border_radius=15)
        clearText = self._font1.render("Clear", True, (0,0,0))
        self._mazeScreen.blit(clearText, clearText.get_rect(center=clearButton.center))
        pygame.display.update()

    def rdfsGenButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (885,505,110,60), border_radius=18)
        runButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        runText = self._font1.render(text, True, (0,0,0))
        screen.blit(runText, runText.get_rect(center=runButton.center))

    def rdfsGenHover(self): 
        runButton = pygame.draw.rect(self._mazeScreen, self._hColour, (890, 510,100, 50), border_radius=15)
        runText = self._font1.render("RBT", True, (0,0,0))
        self._mazeScreen.blit(runText, runText.get_rect(center=runButton.center))
        pygame.display.update()

    def huntAndKillButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (1045,505,110,60), border_radius=18)
        runButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        runText = self._font2.render(text, True, (0,0,0))
        screen.blit(runText, runText.get_rect(center=runButton.center))

    def huntAndKillHover(self):
        runButton = pygame.draw.rect(self._mazeScreen, self._hColour, (1050, 510,100, 50), border_radius=15)
        runText = self._font2.render("Hunt&Kill", True, (0,0,0))
        self._mazeScreen.blit(runText, runText.get_rect(center=runButton.center))
        pygame.display.update()

    def binaryTreeButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (1205,505,110,60), border_radius=18)
        runButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        runText = self._font2.render(text, True, (0,0,0))
        screen.blit(runText, runText.get_rect(center=runButton.center))

    def binaryTreeHover(self):
        runButton = pygame.draw.rect(self._mazeScreen, self._hColour, (1210, 510,100, 50), border_radius=15)
        runText = self._font2.render("BST", True, (0,0,0))
        self._mazeScreen.blit(runText, runText.get_rect(center=runButton.center))
        pygame.display.update()

    def clearButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._black, (1205,675,110,60), border_radius=18)
        clearButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        clearText = self._font.render(text, True, (0,0,0))
        screen.blit(clearText, clearText.get_rect(center=clearButton.center))

    def clearHover(self):
        clearButton = pygame.draw.rect(self._mazeScreen, self._hColour, (1210, 680, 100, 50), border_radius=15)
        clearText = self._font.render("Clear", True, (0,0,0))
        self._mazeScreen.blit(clearText, clearText.get_rect(center=clearButton.center))
        pygame.display.update()

    #Compare button will first bring up tkinter window to select two mazes to compare
    #Compare button can bring up a new window with two 10x10, or if resize is done anysize mazes side by side
    #and a button to compare the two
    def compareButton(self, screen, colour, pos, text:str):
        compareButton = pygame.draw.rect(screen, colour, pos)
        compareText = self._font.render(text, True, (255,0,0))
        screen.blit(compareText, compareText.get_rect(center=compareButton.center))

    def stepButton(self, screen, img, pos):
        screen.blit(img, pos)

    def stepBackButton(self, screen, img, pos):
        screen.blit(img, pos)


    def pauseButton(self, screen, img, pos):
        screen.blit(img, pos)

    def drawPauseButton(self):
        if self._isPaused == False:
            pygame.draw.rect(self._mazeScreen, self._white, (1075, 780, 50, 50))
            self.pauseButton(self._mazeScreen, pygame.image.load("img\pause.png") ,(1075, 780))
            pygame.display.update()
        else:
            pygame.draw.rect(self._mazeScreen, self._white, (1075, 780, 50, 50))
            self.pauseButton(self._mazeScreen, pygame.image.load(r"img\unpause.png") ,(1075, 780))
            pygame.display.update()

    def settingsButton(self, screen, img, pos):
        screen.blit(img, pos)

    def labels(self, timeNum=0, searchNum=0, solveNum=0):
        pygame.draw.rect(self._mazeScreen, self._white, (850,45, 425, 40))
        self._mazeScreen.blit(self._font.render((f"{timeNum}"), True, (0,0,0)), (850,45))
        self._mazeScreen.blit(self._font.render((f"{searchNum}"), True, (0,0,0)), (980,45))
        self._mazeScreen.blit(self._font.render((f"{solveNum}"), True, (0,0,0)), (1150,45))

    def solveText(self, text):
        self._mazeScreen.blit(self._font1.render((f"{text}"), True, (0,0,0)), (890,310))

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

    