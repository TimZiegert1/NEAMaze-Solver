from itertools import count
from pyamaze import maze

arrayTest = [[52,3,4],[32,1]]
#print(arrayTest)
arrayTest.append([23,5,23])
#print(arrayTest)

mazeDict = {}

def grid():
    #Type: Undefined cell 0, Defined path cell 1, Start 2, End 3.
    y=0
    for _ in range(3): # colounm
        x = 1
        y += 1
        for _ in range(4): # rows
            mazeDict[x,y]={'E':1,'W':1,'N':1,'S':1,'Type':0}
            x += 1

mazething = grid()
#print(mazeDict)

#print(mazeDict[1,1]["N"])
mazeDict[1,1]["N"] = 0
#print(mazeDict[1,1]["N"])
#print(mazeDict)

tempDict = {}
#for i in range(3):
    #tempDict[i] = {"N":1, "E":1, "S":1, "W":1, "Type": 0}

#tempDict[(1,1)]["N"] = 0
#tempDict = {int(k):[int(i) for i in v] for k,v in tempDict.items()}
#print(tempDict)

cell = {
    (1,1):{"N":1, "E":1, "S":1, "W":1, "Type": 0},(1,2):{"N":0, "E":0, "S":1, "W":1, "Type": 0},
    (2,1):{"N":1, "E":0, "S":1, "W":1, "Type": 0},(2,2):{"N":1, "E":1, "S":0, "W":1, "Type": 0}
    }

cellValues = []
for values in cell.values():
    cellValues.append(values)

for i in range(1,3):
    for j in range(1,3):
        if j == 1:
            print(cell[i,j],end=" ")
            print(cellValues[i])
        else:
            print(cell[i,j])

row = 2
column = 2
for i in range(1,row+1):
    for j in range(1,column+1):
        if j == 1:
            print(f"{cellValues[i]['W']}{cellValues[i]['Type']}{cellValues[i]['E']}")
        elif j == 0:
            print(f" {cellValues[i]['N']} ")
        elif j == 2:
            print(f" {cellValues[i]['S']} ")

'''
for i in range(3):
    if i == 1:
        print(1,1,1)
    else:
        print(1)
'''