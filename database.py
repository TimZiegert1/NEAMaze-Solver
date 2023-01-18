import sqlite3
from Ui import *
from mazeGen import *

ui = Ui()
maze = MazeGen(ui._height, ui._width)

conn = sqlite3.connect('database.db')

c = conn.cursor()

# Create table

#c.execute("""CREATE TABLE Users (
#    primaryKey integer PRIMARY KEY,
#    username text,
#    password text
#        )""")

#c.execute("""CREATE TABLE MazeSave(
#    primaryKey integer PRIMARY KEY,
#    UserKey integer,
#    MazeName text,
#    MazeData blob
#)""")

print(maze.getMazeMap)

# Insert a row of data
#c.execute("INSERT INTO Users VALUES (1, 'admin', 'admin')")
c.execute("INSERT INTO MazeSave VALUES (1, 1, 'test', :mazeData)", {'mazeData': maze.getMazeMap})
c.execute("SELECT * FROM Users WHERE username = 'admin' AND password = 'admin'") 
print(c.fetchone())

conn.commit()

conn.close()