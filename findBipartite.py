import math
import json

def main(matrix):

    if not matrix:
        print("Enter a Valid Filepath")
        return 

    if not checkSquareMatrix(matrix):
        print("Not A Square Matrix")
        return

    if not checkBitValueEntries(matrix):
        print("Not All Entries are Bits")
        return
        
    if not checkSelfLoops(matrix):
        print("Self Loop Detected")
        return

    if not checkSymmetric(matrix):
        print("Not Symmetric")
        return

    return findBipartite(matrix)

def checkSquareMatrix(matrix):

    length = len(matrix)

    for i in range(length):
        if len(matrix[i]) != length:
            return False
    return True

def checkBitValueEntries(matrix):

    length = len(matrix)

    for i in range(length):
        for j in range(length):
            if ((matrix[i][j] != 1) and (matrix[i][j] != 0)):
                return False
    return True

def checkSelfLoops(matrix):

    length = len(matrix)

    for i in range(length):
        if matrix[i][i] != 0:
            return False
    return True
    
def checkSymmetric(matrix):

    length = len(matrix)
    counter = 0

    for i in range(length):
        for j in range(length):
            counter += matrix[i][j]
    return not counter%2

def getMatrix(filepath):

    try:
        f = open(filepath, "r")
        lines = f.readlines()
    except:
        return False

    matrix = []
    for line in lines:
        row = []
        for bit in line.strip('\n'):
            try:
                row.append(int(bit))
            except ValueError:
                row.append(bit)
        matrix.append(row)
    return(matrix)

def findBipartite(matrix):
    length = len(matrix)
    girth = math.inf
    graph = {}
    shortestCycle = "None"
    red = []
    blue = []
    isBipartite = True
    
    for v in range(length):
        graph[v] = {}
        graph[v]["id"] = v
        graph[v]["color"] = "WHITE"
        graph[v]["bcolor"] = ""
        graph[v]["d"] = 0
        graph[v]["ancestors"] = []
        graph[v]["parent"] = None
        
    graph[0]["color"] = "GRAY"
    graph[0]["bcolor"] = "RED"
    Q = [graph[0]]
    q = len(Q)
    red.append(graph[0]["id"])
    onBlue = True
    while q != 0:
        u = Q.pop(0)
        q = len(Q)
        for j in range(length):
            edge = matrix[u["id"]][j]
            if edge:
                if graph[j]["bcolor"] == u["bcolor"] and u['parent']['id'] != graph[j]['id']:
                    isBipartite = False
                if graph[j]["color"] == "WHITE":
                    if onBlue:
                        graph[j]["bcolor"] = "BLUE"
                        blue.append(graph[j]["id"])
                    if not onBlue:
                        graph[j]["bcolor"] = "RED"
                        red.append(graph[j]["id"])
                    graph[j]["color"] = "GRAY"
                    graph[j]["d"] = u["d"] + 1
                    graph[j]["parent"] = u
                    graph[j]["ancestors"] += u["ancestors"]
                    graph[j]["ancestors"].append(u["id"])
                    Q.append(graph[j])
                    q = len(Q)
                elif graph[j]["color"] == "GRAY" and u['parent']['id'] != graph[j]['id']:
                    for vert in reversed(graph[j]['ancestors']):
                        if vert in u['ancestors']:
                            parentDistance = graph[vert]["d"]
                            cycleLength = (u["d"] + graph[j]["d"] - parentDistance*2) + 1
                            break
                        else:
                            cycleLength = u["d"] + graph[j]["d"] + 1
                    if cycleLength < girth :
                        girth = cycleLength
                        shortestCycle = f"{u['id']} --> {graph[j]['id']} --> "
                        for ancestor in reversed(graph[j]['ancestors']):
                            shortestCycle += f"{ancestor} --> "
                            if ancestor in u['ancestors']:
                                break
                        for grancestor in reversed(u['ancestors']):
                            if grancestor not in graph[j]['ancestors']:
                                shortestCycle += f"{grancestor} --> "   
                        shortestCycle += f"{u['id']}"
                                          
        onBlue = not onBlue
    if isBipartite:
        print("This graph is Bipartite")
        print(f"V1: {red}")
        print(f"V2: {blue}")
    else:
        print("This graph is not Bipartite")
        print(f"Cycle: {shortestCycle}")

    return(girth)

while True:
    filepath = input("Please Enter Filepath: ")
    main(getMatrix(filepath))