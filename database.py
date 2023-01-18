import sqlite3
from hashlib import sha256

conn = sqlite3.connect('database.db')

c = conn.cursor()

# Create table

c.execute("""CREATE TABLE IF NOT EXISTS Users (
    username text PRIMARY KEY,
    password text
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS MazeSave(
    UserKey integer,
    MazeName text PRIMARY KEY,
    MazeData blob
)""")

#print(maze.getMazeMap)

def login(username:str, password:str) -> bool:
    #hash the password
    hashPassword = sha256(password.encode()).hexdigest()
    c.execute(
    "SELECT password FROM Users WHERE username = :name", {"name": f"{username}"}
    )
    print(hashPassword)
    userPassword = c.fetchone()
    print(userPassword)
    if userPassword[0] == hashPassword:
        return True
    else:
        return False

def register(username:str, password:str):
    hashPassword = sha256(password.encode()).hexdigest()
    try:
        c.execute("""
            INSERT INTO Users (username, password)
            VALUES (:name, :pwd)
        """, {"name": f"{username}", "pwd":f"{hashPassword}"})
    except sqlite3.IntegrityError:
        print("This username is already in use")

#register("admin2", "admin")
print(login("admin2", "admin"))

# Insert a row of data
#c.execute("INSERT INTO Users VALUES ('admin', 'admin')")
#c.execute("INSERT INTO MazeSave VALUES (1, 'test', :mazeData)", {'mazeData': f"{maze.getMazeMap}"})
#c.execute("SELECT * FROM Users WHERE username = 'admin' AND password = 'admin'") 
#print(c.fetchone())

conn.commit()

conn.close()