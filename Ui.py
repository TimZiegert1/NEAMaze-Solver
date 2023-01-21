from generator import *
from solver import *
from mazeGen import *
from database import *

import tkinter as tk
from tkinter import messagebox as tkMessageBox
import pygame
import copy
import time
class Ui:
    def __init__(self):
        self._height = 15
        self._width = 15
        self._mazeGen = MazeGen(self._height, self._width)
        self._colours = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "green": (0, 255, 0),
            "red": ( 255, 0, 0),
            "blue": (0,0,255),
            "search": (50,50,50),
            "solve": (255,0,50),
            "button": (225,225,225),
            "hover": (0,195,195)
        }
        self._searchTime = 0.15
        self._solveTime = 0.05
        self._isPaused = False
        self._isGeneration = False

class Terminal(Ui):
    def __init__(self):
        super().__init__()  
        self.__solution = []
        self.__searched = []
        self.__generateOptions = {
            1: "RBT",
            2: "HuntAndKill",
            3: "BinarySearchTree",
        }
        self.__solveOptions = {
            1: "RDFS",
            2: "BFS",
            3: "Dijkstra",
            4: "A*",
            5: "RightHW",
            6: "LeftHW"
        }

    def run(self):
        heightChoice = int(input("Enter height of maze: "))
        widthChoice = int(input("Enter width of maze: "))
        self._mazeGen.setHeight(heightChoice)
        self._mazeGen.setWidth(widthChoice)
        self._mazeGen.genMaze()
        self._mazeGen.setEndPos(self._mazeGen.pickEdge()[1])
        self._mazeGen.setStartPos(self._mazeGen.pickEdge()[0])
        choice = int(input("Enter 1 to generate maze, 2 to solve maze, -1 to quit: "))
        if choice == 1:
            self.generate()
        elif choice == 2:
            self.solve()
        elif choice == -1:
            print("Goodbye!")

    def generate(self):
        print("Choose a generation algorithm:")
        for key, value in self.__generateOptions.items():
            print(f"{key}: {value}")
        choice = int(input("Enter choice: "))
        if choice == 1:
            RBT(self._mazeGen).run()
        elif choice == 2:
            HuntAndKill(self._mazeGen).run()
        elif choice == 3:
            BinaryTree(self._mazeGen).run()
        print("Maze generated!")
        print(f"MAZE MAP GENERATED: {self._mazeGen.getMazeMap}")
        solve = int(input("Enter 1 to solve maze, or -1 to quit: "))
        if solve == 1:
            self.solve()
        elif solve == -1:
            print("Goodbye!")

    def solve(self):
        for key, value in self.__solveOptions.items():
            print(f"{key}: {value}")
        choice = int(input("Enter choice: "))
        if choice == 1:
            DFS(self._mazeGen).run()
        elif choice == 2:
            BFS(self._mazeGen).run()
        elif choice == 3:
            Dijkstra(self._mazeGen).run()
        elif choice == 4:
            AStar(self._mazeGen).run()
        elif choice == 5:
            RHW(self._mazeGen).run()
        elif choice == 6:
            LHW(self._mazeGen).run()
        print("Maze solved!")
        for cell in self._mazeGen.getMazeMap:
            if self._mazeGen.getMazeMap[cell[0], cell[1]]["Type"] == 2:
                self.__searched.append(cell)
                self.__solution.append(cell)
        for cell in self._mazeGen.getMazeMap:
            if self._mazeGen.getMazeMap[cell[0], cell[1]]["Type"] == 5:
                self.__searched.append(cell)
        print(f"MAZE MAP SOLVED: {self._mazeGen.getMazeMap}")
        print(f"SEARCHED: {self.__searched}")
        print(f"SOLUTION: {self.__solution}")
                
        



class GUI(Ui):
    def __init__(self):
        super().__init__()
        pygame.init()
        #Use either 15x15 or 25x25, these work best with the screen size
        self._login = False
        self._logout = False
        self._user = ""
        self._font = pygame.font.Font(None, 50)
        self._font1 = pygame.font.Font(None, 40)
        self._fontDij = pygame.font.Font(None, 37)
        self._font2 = pygame.font.Font(None, 30)
        self._fontTxt = pygame.font.Font(None, 20)
        self._main = tk.Tk()
        self._mazeScreen = pygame.display.set_mode((1375,850), flags=pygame.HIDDEN) #15 rows and 15 col is perfect fit!
        self.__xBox = self.getRescaleValue(self._width, self._height)[0]
        self.__yBox = self.getRescaleValue(self._width, self._height)[1]
        self.__xWall = self.getRescaleValue(self._width, self._height)[2]
        self.__yWall = self.getRescaleValue(self._width, self._height)[3]
        self.__BTdirection = "NW"


    def run(self):
        self.startPanel()

    def startPanel(self):
        self._main.title("Main")
        mazeButton = tk.Button(self._main, text="Maze",width=20,height=3, command=lambda: [self._main.quit(), self.checkLogin()] )
        loginButton = tk.Button(self._main, text="Login",width=20,height=3, command=lambda: [self.loginPanel()])
        #registerButton = tk.Button(self._main, text="Register",width=20,height=3, command=lambda: [self.registerPanel()])
        helpButton = tk.Button(self._main, text="Help",width=20, height=3, command=self.helpPanel)
        quitButton = tk.Button(self._main, text="Quit",width=20,height=3, command=self._main.destroy)
        mazeButton.grid(row=0, column=0)
        loginButton.grid(row=1, column=0)
        #registerButton.grid(row=2, column=0)
        helpButton.grid(row=2,column=0)
        quitButton.grid(row=3, column=0)
        self._main.mainloop()

    def checkLogin(self):
        if self._login == True:
            self._main.destroy()
            self.mazePanel()
        else:
            tkMessageBox.showwarning("Error", "Please login to continue, Note: You can register if you do not have an account.", icon="warning")
            self.loginPanel()

    def loginPanel(self):
        if self._login == True:
            tkMessageBox.showinfo("Error", "You are already logged in!", icon="exaclamation")
        else:
            loginScreen = tk.Tk()
            loginScreen.title("Login")
            loginScreen.attributes("-topmost", True)
            usernameLabel = tk.Label(loginScreen, text="Username")
            passwordLabel = tk.Label(loginScreen, text="Password")
            usernameEntry = tk.Entry(loginScreen)
            passwordEntry = tk.Entry(loginScreen, show="*")
            loginButton = tk.Button(loginScreen, text="Login", command=lambda: [self.login(usernameEntry.get(), passwordEntry.get(), loginScreen)])
            registerButton = tk.Button(loginScreen, text="Register", command=lambda: [loginScreen.destroy(), self.registerPanel()])
            closeButton = tk.Button(loginScreen, text="Close", command=lambda: [loginScreen.destroy()])
            usernameLabel.grid(row=0, column=0)
            passwordLabel.grid(row=1, column=0)
            usernameEntry.grid(row=0, column=1)
            passwordEntry.grid(row=1, column=1)
            loginButton.grid(row=2, column=0)
            registerButton.grid(row=2, column=1)
            closeButton.grid(row=2, column=3)
            loginScreen.mainloop()

    def registerPanel(self):
        registerScreen = tk.Tk()
        registerScreen.title("Register")
        registerScreen.attributes("-topmost", True)
        usernameLabel = tk.Label(registerScreen, text="Username")
        passwordLabel = tk.Label(registerScreen, text="Password")
        passwordLabel2 = tk.Label(registerScreen, text="Confirm Password")
        #showPassword = tk.Button(registerScreen, text="Show", command=lambda: [passwordEntry.config(show=""), passwordEntry2.config(show="")])
        close = tk.Button(registerScreen, text="Close", command=lambda: [registerScreen.destroy(), self._main.deiconify()])
        usernameEntry = tk.Entry(registerScreen)
        passwordEntry = tk.Entry(registerScreen, show="*")
        passwordEntry2 = tk.Entry(registerScreen, show="*")
        registerButton = tk.Button(registerScreen, text="Register", command=lambda: [self.checkPasswordMatch(usernameEntry.get(), passwordEntry.get(), passwordEntry2.get(), registerScreen)])
        usernameLabel.grid(row=0, column=0)
        passwordLabel.grid(row=1, column=0)
        passwordLabel2.grid(row=2, column=0)
        usernameEntry.grid(row=0, column=1)
        passwordEntry.grid(row=1, column=1)
        passwordEntry2.grid(row=2, column=1)
        registerButton.grid(row=3, column=0)
        #showPassword.grid(row=3, column=2)
        close.grid(row=3, column=1)
        registerScreen.mainloop()

    def checkPasswordMatch(self, username, password, password2, screen):
        if username == "":
            tkMessageBox.showwarning("Error", "Please enter a username!", icon="warning")
        elif password == "":
            tkMessageBox.showwarning("Error", "Please enter a password!", icon="warning")
        elif password2 == "":
            tkMessageBox.showwarning("Error", "Please confirm your password!", icon="warning")
        if password == password2 and password != "" and password2 != "":
            self.register(username, password, screen)
        elif password != password2 and password != "" and password2 != "":
            tkMessageBox.showwarning("Error", "Passwords do not match!", icon="warning")

    def helpPanel(self):
        helpWindow = tk.Tk()
        helpWindow.title("Help")
        helpWindow.attributes("-topmost", True)
        helpText = tk.Label(helpWindow, text="Welcome to the help page, here you can find information about the program and how to use it.")
        helpText2 = tk.Label(helpWindow, text="To use the program, you must first login or register")
        helpText3 = tk.Label(helpWindow, text="To log in or register, click the login button on the main menu, then if you need to register there is a button to do so in the login panel")
        helpText4 = tk.Label(helpWindow, text="Once you have logged in, you will have a variaty of options")
        helpText5 = tk.Label(helpWindow, text="You can generate a maze, solve a maze, change the settings, or logout")
        helpText6 = tk.Label(helpWindow, text="In the settings panel you are able to change the width and height of the maze, and the speed of the maze generation")
        helpText7 = tk.Label(helpWindow, text="You can also select the start and end position and change the direction of the Binary Search Tree algorithm")
        helpText8 = tk.Label(helpWindow, text="I hope you enjoy using this program!")
        closeButton = tk.Button(helpWindow, text="Close", command=lambda: [helpWindow.destroy()])
        helpText.grid(row=0, column=0)
        helpText2.grid(row=1, column=0)
        helpText3.grid(row=2, column=0)
        helpText4.grid(row=3, column=0)
        helpText5.grid(row=4, column=0)
        helpText6.grid(row=5, column=0)
        helpText7.grid(row=6, column=0)
        helpText8.grid(row=7, column=0)
        closeButton.grid(row=8, column=0)
        helpWindow.mainloop()


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
        BTdropDownLabel = tk.Label(self._settings, text="Binary Tree Direction")
        widthLabel.grid(row=0, column=0)
        heightLabel.grid(row=1, column=0)
        speedSearch.grid(row=2, column=0)
        speedSolve.grid(row=3, column=0)
        startPos.grid(row=4, column=0)
        endPos.grid(row=5, column=0) 
        BTdropDownLabel.grid(row=6, column=0)
        wBox = tk.Entry(self._settings, width=5)
        hBox = tk.Entry(self._settings, width=5)
        speedSliderSearch = tk.Scale(self._settings, from_=0.0, to=1.0, resolution=0.01 ,orient=tk.HORIZONTAL)
        speedSliderSolve = tk.Scale(self._settings, from_=0.0, to=1.0, resolution=0.01 ,orient=tk.HORIZONTAL)
        speedSliderSearch.set(self._searchTime)
        speedSliderSolve.set(self._solveTime)
        startPosbox = tk.Entry(self._settings, width=5)
        endPosbox = tk.Entry(self._settings, width=5)
        BTDropDownclick = tk.StringVar(self._settings)
        BTDropDownclick.set("NW")
        BTdropDown = tk.OptionMenu(self._settings, BTDropDownclick, "NW", "NE", "SW", "SE")
        #self._wSlider.grid(row=0, column=1)
        #self._hSlider.grid(row=1, column=1)
        wBox.grid(row=0, column=1)
        hBox.grid(row=1, column=1)
        speedSliderSearch.grid(row=2, column=1)
        speedSliderSolve.grid(row=3, column=1)
        startPosbox.grid(row=4, column=1)
        endPosbox.grid(row=5, column=1)
        BTdropDown.grid(row=6, column=1)
        logoutButton = tk.Button(self._settings, text="Logout", command=lambda: [self._settings.destroy(), self.logout()])
        applyButton = tk.Button(self._settings, text="Apply", command=lambda: [self.applyButton(hBox, wBox, speedSliderSearch, speedSliderSolve, startPosbox, endPosbox, BTDropDownclick), self._settings.destroy(), self.mazePanel()])
        applyButton.grid(row=7, column=0)
        logoutButton.grid(row=8, column=0)
        self._settings.mainloop()

    def applyButton(self, hBox, wBox, speedSliderSearch, speedSliderSolve, startPosbox, endPosbox, BTDropDownClick):
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
        self.__BTdirection = BTDropDownClick.get()
        self.__xBox = self.getRescaleValue(self._width, self._height)[0]
        self.__yBox = self.getRescaleValue(self._width, self._height)[1]
        self.__xWall = self.getRescaleValue(self._width, self._height)[2]
        self.__yWall = self.getRescaleValue(self._width, self._height)[3]
        self.drawMaze(self._mazeGen.getMazeMap)
        self._isGeneration = False
        self._settings.destroy()
        #self._settings.withdraw()
        self.mazePanel()

    def mazePanel(self):
        self._mazeScreen = pygame.display.set_mode((1375,850), flags=pygame.SHOWN)
        self._mazeScreen.fill((255,255,255))
        self.drawMaze(self._mazeGen.getMazeMap)
        self.drawButtons()
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
                    if mouse[0] > 1255 and mouse[1] > 775 and mouse[1] < 835 and mouse[0] < 1365:
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
                        self._isGeneration = True
                #RDFS GEN button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 885 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 995 and self._isGeneration == False:
                        #self._gen.findNextMove(self._gen.startPoint[0], self._gen.startPoint[1])
                        self._isGeneration = True
                        self._RDFS = RBT(self._mazeGen)
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
                        self._binaryTree.run(self.__BTdirection)
                        self.drawMaze(self._mazeGen.getMazeMap)
                #Generate new maze button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1210 and mouse[1] > 575 and mouse[1] < 635 and mouse[0] < 1310:
                        self._mazeGen.setMazeMap = {}
                        self._mazeGen = MazeGen(self._height, self._width)
                        self.drawMaze(self._mazeGen.getMazeMap)
                        self._isGeneration = False
                #Save Maze
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 885 and mouse[1] > 695 and mouse[1] < 755 and mouse[0] < 995:
                        self.saveMaze()
                #Load Maze
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1045 and mouse[1] > 695 and mouse[1] < 755 and mouse[0] < 1155:
                        self.loadMaze()
                #Hovers
                if event.type == pygame.MOUSEMOTION:
                    mouse = pygame.mouse.get_pos()
                    #quit hover
                    if mouse[0] > 1255 and mouse[1] > 775 and mouse[1] < 835 and mouse[0] < 1365:
                        self.quitHover()
                    else:
                        self.quitButton(self._mazeScreen, self._colours["button"] ,(1260,780,100, 50), "Quit")
                        pygame.display.update()
                    if mouse[0] > 885 and mouse[1] > 145 and mouse[1] < 205 and mouse[0] < 995:
                        self.solveRDFSHover()
                        #self.solveText("This is a test")
                    else:
                        self.solveRDFSButton(self._mazeScreen, (225,225,225) ,(890, 150,100, 50), "RDFS")
                        pygame.display.update()
                    if mouse[0] > 1045 and mouse[1] > 145 and mouse[1] < 205 and mouse[0] < 1155:
                        self.solveBFSHover()
                    else:
                        self.solveBFSButton(self._mazeScreen, self._colours["button"] ,(1050, 150,100, 50), "BFS")
                        pygame.display.update()
                    if mouse[0] > 1205 and mouse[1] > 145 and mouse[1] < 205 and mouse[0] < 1315:
                        self.solveDijkstraHover()
                    else:
                        self.solveDijkstraButton(self._mazeScreen, self._colours["button"] ,(1210, 150,100, 50), "Dijkstra")
                    if mouse[0] > 885 and mouse[1] > 215 and mouse[1] < 275 and mouse[0] < 995:
                        self.solveAStarHover()
                    else:
                        self.solveAStarButton(self._mazeScreen, self._colours["button"] ,(890, 220,100, 50), "A*")
                        pygame.display.update()
                    if mouse[0] > 1045 and mouse[1] > 215 and mouse[1] < 275 and mouse[0] < 1155:
                        self.solveRHWHover()
                    else:
                        self.solveRHWButton(self._mazeScreen, self._colours["button"] ,(1050, 220,100, 50), "RHW")
                        pygame.display.update()
                    if mouse[0] > 1205 and mouse[1] > 215 and mouse[1] < 275 and mouse[0] < 1315:
                        self.solveLHWHover()
                    else:
                        self.solveLHWButton(self._mazeScreen, self._colours["button"] ,(1210, 220,100, 50), "LHW")
                        pygame.display.update()
                    if mouse[0] > 1205 and mouse[1] > 375 and mouse[1] < 435 and mouse[0] < 1315:
                        self.clearSolveHover()
                    else:
                        self.clearSolveButton(self._mazeScreen, self._colours["button"] ,(1210, 380,100, 50), "Clear")
                        pygame.display.update()
                    if mouse[0] > 885 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 995:
                        self.rdfsGenHover()
                    else:
                        self.rdfsGenButton(self._mazeScreen, self._colours["button"] ,(890, 510,100, 50), "RBT")
                        pygame.display.update()
                    if mouse[0] > 1045 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 1155:
                        self.huntAndKillHover()
                    else:
                        self.huntAndKillButton(self._mazeScreen, self._colours["button"] ,(1050, 510,100, 50), "Hunt&Kill")
                        pygame.display.update()
                    if mouse[0] > 1205 and mouse[1] > 505 and mouse[1] < 565 and mouse[0] < 1315:
                        self.binaryTreeHover()
                    else:
                        self.binaryTreeButton(self._mazeScreen, self._colours["button"] ,(1210, 510,100, 50), "BST")
                        pygame.display.update()
                    if mouse[0] > 1210 and mouse[1] > 575 and mouse[1] < 635 and mouse[0] < 1310:
                        self.clearHover()
                    else:
                        self.clearButton(self._mazeScreen, self._colours["button"] ,(1210, 580,100, 50), "Clear")
                        pygame.display.update()
                    if mouse[0] > 885 and mouse[1] > 695 and mouse[1] < 755 and mouse[0] < 995:
                        self.saveHover()
                    else:
                        self.saveButton(self._mazeScreen, self._colours["button"] ,(890, 700,100, 50), "Save")
                        pygame.display.update()
                    if mouse[0] > 1045 and mouse[1] > 695 and mouse[1] < 755 and mouse[0] < 1155:
                        self.loadHover()
                    else:
                        self.loadButton(self._mazeScreen, self._colours["button"] ,(1050, 700,100, 50), "Load")
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
                    pygame.draw.rect(self._mazeScreen, self._colours["black"], ((x*(self.__xBox+self.__xWall))+self.__xWall,((y*self.__yBox)+(y-1)*self.__yWall)+(2*self.__yWall),(self.__xBox+(2*self.__xWall)),self.__xWall))
                if mazeMap[x+1,y+1]["S"] == 1:
                    #pygame.draw.rect(self._mazeScreen, self._black, ((x*55)+5,((y*50)+(y-1)*5)+65,60,5))
                    pygame.draw.rect(self._mazeScreen, self._colours["black"], ((x*(self.__xBox+self.__xWall))+self.__xWall,((y*self.__yBox)+(y-1)*self.__yWall)+(self.__yBox+(3*self.__yWall)),(self.__xBox+(2*self.__xWall)),self.__xWall))
                if mazeMap[x+1,y+1]["E"] == 1:
                    #pygame.draw.rect(self._mazeScreen, self._black, (((x*50)+(x-1)*5)+65,(y*55)+5,5,60))
                    pygame.draw.rect(self._mazeScreen, self._colours["black"], (((x*self.__xBox)+(x-1)*self.__xWall)+(self.__xBox+(3*self.__xWall)),(y*(self.__yBox+self.__yWall))+self.__yWall,self.__yWall,self.__yBox+(2*self.__yWall)))
                if mazeMap[x+1,y+1]["W"] == 1:
                    #pygame.draw.rect(self._mazeScreen, self._black, (((x*50)+(x-1)*5)+10,(y*55)+5,5,60))
                    pygame.draw.rect(self._mazeScreen, self._colours["black"], (((x*self.__xBox)+(x-1)*self.__xWall)+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+self.__yWall,self.__yWall,self.__yBox+(2*self.__yWall)))
                x += 1

    def drawMaze(self, mazeMap):
        y=-1
        for _ in range(self._height): # height
            x = 0
            y += 1
            for _ in range(self._width): # widths
                if mazeMap[x+1,y+1]["Type"] == 3:
                    #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._colours["blue"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                elif mazeMap[x+1,y+1]["Type"] == 4:
                    #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._colours["red"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                elif mazeMap[x+1,y+1]["Type"] == 0:
                    #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._colours["white"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                elif mazeMap[x+1,y+1]["Type"] == 1:
                    #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._colours["white"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                elif mazeMap[x+1,y+1]["Type"] == 5:
                    #pygame.draw.rect(self._mazeScreen, self._colours["search"], ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._colours["search"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                elif mazeMap[x+1,y+1]["Type"] == 2:
                    #pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((x*55)+10,(y*55)+10,55,55))
                    pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                self.drawWalls(mazeMap)
                if self._isGeneration == True:
                    if mazeMap[x+1,y+1]["Type"] == 3:
                        #pygame.draw.rect(self._mazeScreen, self._colours["blue"], ((x*55)+10,(y*55)+10,55,55))
                        pygame.draw.rect(self._mazeScreen, self._colours["blue"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                    elif mazeMap[x+1,y+1]["Type"] == 4:
                        #pygame.draw.rect(self._mazeScreen, self._colours["red"], ((x*55)+10,(y*55)+10,55,55))
                        pygame.draw.rect(self._mazeScreen, self._colours["red"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                    if mazeMap[x+1,y+1]["N"] == 0:
                        #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,((y*50)+(y-1)*5)+10,50,5))
                        pygame.draw.rect(self._mazeScreen, self._colours["white"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),((y*self.__yBox)+(y-1)*self.__yWall)+(2*self.__yWall),self.__xBox,self.__yWall))
                    if mazeMap[x+1,y+1]["S"] == 0:
                        #pygame.draw.rect(self._mazeScreen, self._white, ((x*55)+10,((y*50)+(y-1)*5)+65,50,5))
                        pygame.draw.rect(self._mazeScreen, self._colours["white"], ((x*(self.__xBox+self.__xWall))+(2*self.__xWall),((y*self.__yBox)+(y-1)*self.__yWall)+self.__yBox+(3*self.__yWall),self.__xBox,self.__yWall))
                    if mazeMap[x+1,y+1]["E"] == 0:
                        #pygame.draw.rect(self._mazeScreen, self._white, (((x*50)+(x-1)*5)+65,(y*55)+10,5,50))
                        pygame.draw.rect(self._mazeScreen, self._colours["white"], (((x*self.__xBox)+(x-1)*self.__xWall)+self.__xBox+(3*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xWall,self.__yBox))
                    if mazeMap[x+1,y+1]["W"] == 0:
                        #pygame.draw.rect(self._mazeScreen, self._white, (((x*50)+(x-1)*5)+10,(y*55)+10,5,50)) 
                        pygame.draw.rect(self._mazeScreen, self._colours["white"], (((x*self.__xBox)+(x-1)*self.__xWall)+(2*self.__xWall),(y*(self.__yBox+self.__yWall))+(2*self.__yWall),self.__xWall,self.__yBox)) 
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
                pygame.draw.rect(self._mazeScreen, self._colours["white"], ((cell[1]*55)-45,((cell[2]*50)+(cell[2]-1)*5)+10,50,5))
                time.sleep(0.05)
                pygame.display.update()
            elif cell[0] == "W":
                #pygame.draw.rect(self._mazeScreen, self._white, (((cell[1]*50)+(cell[1]-1)*5)-45,(cell[2]*55)-45,5,50)) 
                pygame.draw.rect(self._mazeScreen, self._colours["white"], (((cell[1]*50)+(cell[1]-1)*5)-45,(cell[2]*55)-45,5,50)) 
                time.sleep(0.05)
                pygame.display.update()
            elif cell[0] == "E":
                #pygame.draw.rect(self._mazeScreen, self._white, (((cell[1]*50)+(cell[1]-1)*5)+10,(cell[2]*55)-45,5,50))
                pygame.draw.rect(self._mazeScreen, self._colours["white"], (((cell[1]*50)+(cell[1]-1)*5)+10,(cell[2]*55)-45,5,50))
                time.sleep(0.05)
                pygame.display.update()
            elif cell[0] == "N":
                #pygame.draw.rect(self._mazeScreen, self._white, ((cell[1]*55)-45,((cell[2]*50)+(cell[2]-1)*5)-45,50,5))
                pygame.draw.rect(self._mazeScreen, self._colours["white"], ((cell[1]*55)-45,((cell[2]*50)+(cell[2]-1)*5)-45,50,5))
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
                        #pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                        pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[index-1][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index-1][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                        return index
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._isPaused = False
                        self.drawPauseButton()
                        #pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                        pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[index-1][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index-1][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                        return index
                #Quit Button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] > 1255 and mouse[1] > 775 and mouse[1] < 835 and mouse[0] < 1365:
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
                            #pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                            #pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index][0]*55)-45,(searchPath[index][1]*55)-45,55,55))
                            pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[index-1][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index-1][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                            pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
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
                            #pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index-2][0]*55)-45,(searchPath[index-2][1]*55)-45,55,55))
                            pygame.draw.rect(self._mazeScreen, (255,255,255), ((searchPath[index-1][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index-1][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                            pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index-2][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index-2][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
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
                            #pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[index-1][0]*55)-45,(searchPath[index-1][1]*55)-45,55,55))
                            #pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index][0]*55)-45,(searchPath[index][1]*55)-45,55,55))
                            pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[index-1][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index-1][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                            pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
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
                            #pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index-2][0]*55)-45,(searchPath[index-2][1]*55)-45,55,55))
                            pygame.draw.rect(self._mazeScreen, (255,255,255), ((searchPath[index-1][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index-1][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                            pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index-2][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index-2][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
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
                    #pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[tempIndex][0]*55)-45,(searchPath[tempIndex][1]*55)-45,55,55))
                    pygame.draw.rect(self._mazeScreen, self._colours["search"], ((searchPath[tempIndex][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[tempIndex][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
                #pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index][0]*55)-45,(searchPath[index][1]*55)-45,55,55))
                pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((searchPath[index][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(searchPath[index][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
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
                        #pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((solvePath[index][0]*55)-45,(solvePath[index][1]*55)-45,55,55))
                        pygame.draw.rect(self._mazeScreen, self._colours["solve"], ((solvePath[index][0]*(self.__xBox+self.__xWall))-(self.__xBox-self.__xWall),(solvePath[index][1]*(self.__yBox+self.__yWall))-(self.__yBox-self.__yWall),self.__xBox+self.__xWall,self.__yBox+self.__yWall))
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
        pygame.draw.rect(self._mazeScreen, self._colours["black"] ,(850,100,500,350))
        pygame.draw.rect(self._mazeScreen, self._colours["white"] ,(855,105,490,340))
        self._mazeScreen.blit(self._font.render("Solve", True, (0,0,0)), (1050,110))
        #Gen Border
        pygame.draw.rect(self._mazeScreen, self._colours["black"] ,(850,455,500,200))
        pygame.draw.rect(self._mazeScreen, self._colours["white"] ,(855,460,490,190))
        self._mazeScreen.blit(self._font.render("Generate", True, (0,0,0)), (1025,465))

        self._mazeScreen.blit(self._font2.render("Time Taken", True, (0,0,0)), (850,10))
        self._mazeScreen.blit(self._font2.render("Searched Cells", True, (0,0,0)), (980,10))
        self._mazeScreen.blit(self._font2.render("Solved Cells", True, (0,0,0)), (1150,10))
        self.labels()   

        self.settingsButton(self._mazeScreen, pygame.image.load("img\settingsIcon.png") ,(1290, 10))
        self.pauseButton(self._mazeScreen, pygame.image.load("img\pause.png") ,(1075, 780))
        self.stepButton(self._mazeScreen, pygame.image.load("img\stepButton.png") ,(1150, 780))
        self.stepBackButton(self._mazeScreen, pygame.image.load("img\stepBackButton.png") ,(1000, 780))
        self.quitButton(self._mazeScreen, self._colours["button"] ,(1260, 780,100, 50), "Quit")

        self.solveRDFSButton(self._mazeScreen, self._colours["button"] ,(890, 150,100, 50), "RDFS")
        self.solveBFSButton(self._mazeScreen, self._colours["button"] ,(1050, 150,100, 50), "BFS")
        self.solveDijkstraButton(self._mazeScreen, self._colours["button"] ,(1210, 150,100, 50), "Dijkstra")
        self.solveAStarButton(self._mazeScreen, self._colours["button"] ,(890, 220,100, 50), "A*")
        self.solveRHWButton(self._mazeScreen, self._colours["button"] ,(1050, 220,100, 50), "RHW")
        self.solveLHWButton(self._mazeScreen, self._colours["button"] ,(1210, 220,100, 50), "LHW")
        self.clearSolveButton(self._mazeScreen, self._colours["button"] ,(1210, 380,100, 50), "Clear")  
                
        self.rdfsGenButton(self._mazeScreen, self._colours["button"] ,(890, 510,100, 50), "RBT")
        self.huntAndKillButton(self._mazeScreen, self._colours["button"] ,(1050, 510,100, 50), "Hunt&Kill")
        self.binaryTreeButton(self._mazeScreen, self._colours["button"] ,(1210, 510,100, 50), "BST")
        self.clearButton(self._mazeScreen, self._colours["button"] ,(1210, 580, 100, 50), "Clear")

        self.saveButton(self._mazeScreen, self._colours["button"] ,(890, 700, 100, 50), "Save")
        self.loadButton(self._mazeScreen, self._colours["button"] ,(1050, 700, 100, 50), "Load")

    def quitButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1255,775,110,60), border_radius=18)
        quitButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        quitText = self._font.render(text, True, (0,0,0))
        screen.blit(quitText, quitText.get_rect(center=quitButton.center))

    def quitHover(self):
        quitButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"],(1260, 780,100, 50), border_radius=15)
        quitText = self._font.render("Quit", True, (255,0,0))
        self._mazeScreen.blit(quitText, quitText.get_rect(center=quitButton.center))

    def solveRDFSButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (885,145,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))
    
    def solveRDFSHover(self):
        #pygame.draw.rect(self._mazeScreen, self._black, (885,145,110,60), border_radius=18)
        solveButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"],(890, 150,100, 50), border_radius=15)
        solveText = self._font1.render("RDFS", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def solveBFSButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1045,145,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveBFSHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (1050, 150,100, 50), border_radius=15)
        solveText = self._font1.render("BFS", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()
    
    def solveDijkstraButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1205,145,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._fontDij.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))
    
    def solveDijkstraHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (1210, 150,100, 50), border_radius=15)
        solveText = self._fontDij.render("Dijkstra", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def solveAStarButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (885,215,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveAStarHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (890, 220,100, 50), border_radius=15)
        solveText = self._font1.render("A*", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def solveRHWButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1045,215,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))

    def solveRHWHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (1050, 220,100, 50), border_radius=15)
        solveText = self._font1.render("RHW", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def solveLHWButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1205,215,110,60), border_radius=18)
        solveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        solveText = self._font1.render(text, True, (0,0,0))
        screen.blit(solveText, solveText.get_rect(center=solveButton.center))
    
    def solveLHWHover(self):
        solveButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (1210, 220,100, 50), border_radius=15)
        solveText = self._font1.render("LHW", True, (0,0,0))
        self._mazeScreen.blit(solveText, solveText.get_rect(center=solveButton.center))
        pygame.display.update()

    def clearSolveButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1205,375,110,60), border_radius=18)
        clearButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        clearText = self._font1.render(text, True, (0,0,0))
        screen.blit(clearText, clearText.get_rect(center=clearButton.center))
    
    def clearSolveHover(self):
        clearButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (1210, 380,100, 50), border_radius=15)
        clearText = self._font1.render("Clear", True, (0,0,0))
        self._mazeScreen.blit(clearText, clearText.get_rect(center=clearButton.center))
        pygame.display.update()

    def rdfsGenButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (885,505,110,60), border_radius=18)
        runButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        runText = self._font1.render(text, True, (0,0,0))
        screen.blit(runText, runText.get_rect(center=runButton.center))

    def rdfsGenHover(self): 
        runButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (890, 510,100, 50), border_radius=15)
        runText = self._font1.render("RBT", True, (0,0,0))
        self._mazeScreen.blit(runText, runText.get_rect(center=runButton.center))
        pygame.display.update()

    def huntAndKillButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1045,505,110,60), border_radius=18)
        runButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        runText = self._font2.render(text, True, (0,0,0))
        screen.blit(runText, runText.get_rect(center=runButton.center))

    def huntAndKillHover(self):
        runButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (1050, 510,100, 50), border_radius=15)
        runText = self._font2.render("Hunt&Kill", True, (0,0,0))
        self._mazeScreen.blit(runText, runText.get_rect(center=runButton.center))
        pygame.display.update()

    def binaryTreeButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1205,505,110,60), border_radius=18)
        runButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        runText = self._font1.render(text, True, (0,0,0))
        screen.blit(runText, runText.get_rect(center=runButton.center))

    def binaryTreeHover(self):
        runButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (1210, 510,100, 50), border_radius=15)
        runText = self._font1.render("BST", True, (0,0,0))
        self._mazeScreen.blit(runText, runText.get_rect(center=runButton.center))
        pygame.display.update()

    def clearButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1205,575,110,60), border_radius=18)
        clearButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        clearText = self._font.render(text, True, (0,0,0))
        screen.blit(clearText, clearText.get_rect(center=clearButton.center))

    def clearHover(self):
        clearButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (1210, 580, 100, 50), border_radius=15)
        clearText = self._font.render("Clear", True, (0,0,0))
        self._mazeScreen.blit(clearText, clearText.get_rect(center=clearButton.center))
        pygame.display.update()

    def stepButton(self, screen, img, pos):
        screen.blit(img, pos)

    def stepBackButton(self, screen, img, pos):
        screen.blit(img, pos)

    def pauseButton(self, screen, img, pos):
        screen.blit(img, pos)

    def drawPauseButton(self):
        if self._isPaused == False:
            pygame.draw.rect(self._mazeScreen, self._colours["white"], (1075, 780, 50, 50))
            self.pauseButton(self._mazeScreen, pygame.image.load("img\pause.png") ,(1075, 780))
            pygame.display.update()
        else:
            pygame.draw.rect(self._mazeScreen, self._colours["white"], (1075, 780, 50, 50))
            self.pauseButton(self._mazeScreen, pygame.image.load(r"img\unpause.png") ,(1075, 780))
            pygame.display.update()

    def settingsButton(self, screen, img, pos):
        screen.blit(img, pos)

    def labels(self, timeNum=0, searchNum=0, solveNum=0):
        pygame.draw.rect(self._mazeScreen, self._colours["white"], (850,45, 425, 40))
        self._mazeScreen.blit(self._font.render((f"{timeNum}"), True, (0,0,0)), (850,45))
        self._mazeScreen.blit(self._font.render((f"{searchNum}"), True, (0,0,0)), (980,45))
        self._mazeScreen.blit(self._font.render((f"{solveNum}"), True, (0,0,0)), (1150,45))

    def solveText(self, text):
        self._mazeScreen.blit(self._font1.render((f"{text}"), True, (0,0,0)), (890,310))

    def saveButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (885,695,110,60), border_radius=18)
        saveButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        saveText = self._font.render(text, True, (0,0,0))
        screen.blit(saveText, saveText.get_rect(center=saveButton.center))

    def saveHover(self):
        saveButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (890, 700, 100, 50), border_radius=15)
        saveText = self._font.render("Save", True, (0,0,0))
        self._mazeScreen.blit(saveText, saveText.get_rect(center=saveButton.center))
        pygame.display.update()

    def loadButton(self, screen, colour, pos, text:str):
        pygame.draw.rect(screen, self._colours["black"], (1045,695,110,60), border_radius=18)
        loadButton = pygame.draw.rect(screen, colour, pos, border_radius=15)
        loadText = self._font.render(text, True, (0,0,0))
        screen.blit(loadText, loadText.get_rect(center=loadButton.center))

    def loadHover(self):
        loadButton = pygame.draw.rect(self._mazeScreen, self._colours["hover"], (1050, 700, 100, 50), border_radius=15)
        loadText = self._font.render("Load", True, (0,0,0))
        self._mazeScreen.blit(loadText, loadText.get_rect(center=loadButton.center))
        pygame.display.update()

    def customise(self):
        ... #Customise, colours, etc

    def login(self, username, password, screen):
        if loginDataBase(username, password) == True:
            self._user = username
            self._logout = False
            self._main.withdraw()
            screen.destroy()
            self.mazePanel()
        else:
            tkMessageBox.showerror("Error", "Your username or password is incorrect")

    def register(self, username, password, screen):
        if registerDataBase(username, password) == "Taken":
            tkMessageBox.showerror("Error", "This username has already been taken")
        else:
            tkMessageBox.showinfo("Success", "You have successfully created a new account!")
            screen.destroy()

    def logout(self):
        pygame.quit()
        self._user = ""
        self._login = False
        self._logout = True
        tempGui = GUI()
        tempGui.run()

    def saveMaze(self):
        saveMazeWindow = tk.Tk()
        saveMazeWindow.title("Save Maze")
        mazeName = tk.Label(saveMazeWindow, text="Maze Name")
        mazeName.grid(row=0, column=0)
        mazeNameEntry = tk.Entry(saveMazeWindow)
        mazeNameEntry.grid(row=0, column=1)
        saveButton = tk.Button(saveMazeWindow, text="Save", command=lambda: [self.saveMazeCheck(mazeNameEntry.get(), saveMazeWindow)])
        saveButton.grid(row=1, column=0)
        closeButton = tk.Button(saveMazeWindow, text="Close", command=lambda: [saveMazeWindow.withdraw(), self.mazePanel()])
        closeButton.grid(row=1, column=1)
        saveMazeWindow.mainloop()

    def saveMazeCheck(self, name, screen):
        if saveMazeDataBase(self._user, name, self._mazeGen.getMazeMap) == "Taken":
            tkMessageBox.showerror("Error", "This name has already been taken")
        else:
            tkMessageBox.showinfo("Success", "You have successfully saved your maze!")
            screen.destroy()
            self.mazePanel()

    def loadMaze(self):
        loadMazeWindow = tk.Tk()
        loadMazeWindow.title("Load Maze")
        mazeName = tk.Label(loadMazeWindow, text="Maze Name")
        mazeName.grid(row=0, column=0)
        mazeNameEntry = tk.Entry(loadMazeWindow)
        mazeNameEntry.grid(row=0, column=1)
        loadButton = tk.Button(loadMazeWindow, text="Load", command=lambda: [self.loadMazeCheck(mazeNameEntry.get(), loadMazeWindow)])
        loadButton.grid(row=1, column=0)
        closeButton = tk.Button(loadMazeWindow, text="Close", command=lambda: [loadMazeWindow.withdraw(), self.mazePanel()])
        closeButton.grid(row=1, column=1)
        loadMazeWindow.mainloop()

    def loadMazeCheck(self, name, screen):
        #loadedMaze RETURNS A STRING NOT A DICT
        if name == "":
            tkMessageBox.showerror("Error", "Please enter a name")
        else:
            loadedMaze = loadMazeDataBase(self._user, name)
            if loadedMaze == False:
                tkMessageBox.showerror("Error", "This maze does not exist")
            else:
                tkMessageBox.showinfo("Success", "You have successfully loaded your maze!")
                screen.destroy()
                self._isGeneration = True
                self._mazeGen.setMazeMap(eval(loadedMaze))
                '''
                for cell in self._mazeGen.getMazeMap:
                    if self._mazeGen.getMazeMap[cell[0], cell[1]] == 3:
                        self._mazeGen.setStartPos(cell)
                    if self._mazeGen.getMazeMap[cell[0], cell[1]] == 4:
                        self._mazeGen.setEndPos(cell)
                '''
                #Set width and height to the last cell corresponding width and height
                self.mazePanel()


    