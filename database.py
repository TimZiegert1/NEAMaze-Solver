import sqlite3
from hashlib import sha256

conn = sqlite3.connect('database.db')

c = conn.cursor()

###########################################################
#                                                         #
#     CATEGORY B SKILL: SIMPLE DATA MODEL IN DATABASE     #
#                                                         #
###########################################################

# Create table

c.execute("""CREATE TABLE IF NOT EXISTS Users (
    username text PRIMARY KEY,
    password text
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS MazeSave(
    User text,
    MazeName text PRIMARY KEY,
    MazeData blob
)""")

#print(maze.getMazeMap)

def loginDataBase(username:str, password:str) -> bool:
    
    #hash the password
    hashPassword = sha256(password.encode()).hexdigest()
    c.execute(
    "SELECT password FROM Users WHERE username = :name", {"name": f"{username}"}
    )
    userPassword = c.fetchone()
    if userPassword and userPassword[0] == hashPassword:
        return True
    else:
        return False

#####################################
#                                   #
#     CATEGORY A SKILL: HASHING     #
#                                   #
#####################################

def registerDataBase(username:str, password:str):
    hashPassword = sha256(password.encode()).hexdigest()
    try:
        c.execute("""
            INSERT INTO Users (username, password)
            VALUES (:name, :pwd)
        """, {"name": f"{username}", "pwd":f"{hashPassword}"})
        conn.commit()
    except sqlite3.IntegrityError:
        #This means that the username is already taken
        return "Taken"

def saveMazeDataBase(username:str, mazeName:str, mazeData:dict):
    try:
        c.execute("""
            INSERT INTO MazeSave (User, MazeName, MazeData)
            VALUES (:name, :mazeName, :mazeData)
        """, {"name": f"{username}", "mazeName": f"{mazeName}", "mazeData": f"{mazeData}"})
        conn.commit()
    except sqlite3.IntegrityError:
        #This means that the name is already taken
        return "Taken"

def loadMazeDataBase(username:str, mazeName:str):
    c.execute(
    "SELECT MazeData FROM MazeSave WHERE User = :name AND MazeName = :mazeName", {"name": f"{username}", "mazeName": f"{mazeName}"}
    )
    mazeData = c.fetchone()
    if mazeData:
        return mazeData[0]
    else:
        return False
