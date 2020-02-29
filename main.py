from graphics import *
import time
import numpy as np
from Node import *
from Queue import *
import pickle

def resetColor(rect):
    for i in range(0, len(rect[0])-1):
        for j in range(0, len(rect[0])-1):
                rect[i][j].setFill(color_rgb(0, 100, 255))

def changeColor(rect, wip):
    resetColor(rect)
    for i in range(0, len(rect[0])-1):
        for j in range(0, len(rect[0])-1):
            if wip[i][j] == 1:
                rect[i][j].setFill(color_rgb(0, 220, 220))

def setDefault(win, n, data, sumX, sumY):
    rect = [[0 for x in range(n + 1)] for y in range(n + 1)]

    for x in range(n + 1):
        for y in range(n + 1):
            if x == n and y == n:
                break
            rect[x][y] = Rectangle(Point((y + 1) * 100, (x + 1) * 100), Point((y + 1) * 100 + 100, (x + 1) * 100 + 100))
            if x == n or y == n:
                rect[x][y].setFill(color_rgb(220, 220, 220))

            else:
                rect[x][y].setFill(color_rgb(0, 100, 255))
            rect[x][y].draw(win)

            if x == n:
                txt = Text(Point((y + 1) * 100 + 50, (x + 1) * 100 + 50), sumX[y])
                txt.setTextColor(color_rgb(128, 128, 128))
            elif y == n:
                txt = Text(Point((y + 1) * 100 + 50, (x + 1) * 100 + 50), sumY[x])
                txt.setTextColor(color_rgb(128, 128, 128))
            else:
                txt = Text(Point((y + 1) * 100 + 50, (x + 1) * 100 + 50), data[x][y])
                txt.setTextColor(color_rgb(255, 255, 255))
            txt.setSize(30)
            txt.setStyle('bold')
            txt.draw(win)
    return rect

def createUI(n):
    width = 100*(n+3)
    win = GraphWin("Pluszle", width, width)
    return win

def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def probNgoal(n):
  prob = np.random.randint(1, 9, (n,n))
  goalState = np.random.random_integers(1, 2**n-1, n)
  # goalState = np.array([0, 0, 1, 7])
  goalPosition = np.asarray([list(map(int, bin(x)[2:].zfill(4))) for x in goalState])

  goalSum = [list(prob[i] * goalPosition[i]) for i in range(4)]
  sumX = np.sum(goalSum, axis=0)
  sumY = np.sum(goalSum, axis=1)
  
  return prob, goalState, goalPosition, goalSum, sumX, sumY

def menu(win,winWidth,winHeight):
    logo = Image(Point(winWidth / 4, winHeight / 16 + 2), "images/logo_small.gif")
    logo.draw(win)
    random = Image(Point(winWidth / 2 + 200, winHeight / 16 + 2), "images/random.gif")
    random.draw(win)
    
    imgMethod = Image(Point(winWidth / 4, winHeight - 50), "images/method.gif")
    imgMet1 = Image(Point(winWidth / 2 + 120, winHeight - 65), "images/met1.gif")
    imgMet2 = Image(Point(winWidth / 2 + 120, winHeight - 30), "images/met2.gif")

    imgMethod.draw(win)
    imgMet1.draw(win)
    imgMet2.draw(win)

def convertIntToListBinary(goal):
    searchGoal = []
    for i in goal:
        searchGoal.append([int(x) for x in list('{0:04b}'.format(i))])
    return searchGoal 

found = False # Search Flag

def iterativeDeepeningDepthFirstSearch(root, goal, problemTable):
    # Repeatedly depth-first search up-to a maximum depth of 6.
    for maxDepth in range(0,len(goal)+1):
        depthFirstSearch(root, maxDepth, goal, problemTable)

def depthFirstSearch(root, maxDepth, goal, problemTable):
    global found
    if not found:
        # print(root.getData(), convertIntToListBinary(root.getData()))
        changeColor(problemTable, convertIntToListBinary(root.getData()))
        
        if(root.getData() == goal):
            found = True
            
        # If reached the maximum depth, stop recursing.
        if maxDepth <= 0:
            return 
        # Recurse for all children of node.
        for i in range(0,root.getBranchSize()):
            depthFirstSearch(root.branch[i], maxDepth-1, goal, problemTable)

def breadthFirstSearch(root, goal, problemTable):
    global found
    q = Queue()
    q.enQueue(root)
    
    while q.size() > 0 and not found:
        node = q.deQueue()
        #print(node.getData(), convertIntToListBinary(node.getData()))
        changeColor(problemTable, convertIntToListBinary(node.getData()))
        
        if(node.getData() == goal):
            found = True
        # add all the children to the back of the queue
        for i in range(0,node.getBranchSize()):
            q.enQueue(node.branch[i])
            
# Aomsin BFS Algorithm
def isSameState(state1: np, state2: np):
    return (state1 == state2).all()

def formatState(state: np):
    arraySize = state.shape[1] * (-1)
    indexChecker = -1
    formatState = state
    while(indexChecker > arraySize): 
        if formatState[0, indexChecker] == 16:
            formatState[0, indexChecker] = 0
            formatState[0, indexChecker-1] += 1
        indexChecker -= 1
    return formatState

def doBreadthFirstSearch(startState: np, goalState: np, problemTable):
    if startState.shape[1] != goalState.shape[0]:
        print("! Error input: StartState size mismatch with GoalState!")
        return
    arraySize = goalState.shape[0]
    currentState = startState
    while not isSameState(currentState, goalState):
        currentState[0, -1] += 1
        currentState = formatState(currentState)
        #print(currentState)
        changeColor(problemTable, convertIntToListBinary(currentState.tolist()[0]))
        
    return currentState
                            
def main():
    global found
    data = [[1, 0, 0, 1],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [1, 0, 0, 1]]
    
    sumX = [0, 0, 0, 0]
    sumY = [0, 0, 0, 0]

    selectedPos = [[1, 0, 0, 1],
                   [0, 1, 1, 0],
                   [0, 1, 1, 0],
                   [1, 0, 0, 1]]

    goal = [0,0,0,0]
    
    n = 4

    win = createUI(n)

    win.setBackground(color_rgb(255, 255, 255))
    winWidth = win.getWidth()
    winHeight = win.getHeight()
    
    menu(win,winWidth,winHeight)
    
    data, goal, selectedPos, goalSum, sumX, sumY = probNgoal(n)
    data = data.tolist() # Convert array to list
    sumX = sumX.tolist()
    sumY = sumY.tolist()
    goal = goal.tolist()
    selectedPos = selectedPos.tolist()
            
    problemTable = setDefault(win, n, data, sumX, sumY)
    changeColor(problemTable, selectedPos)
    print("Goal: ",goal)
    
    start_time = time.time()
    with open('data-4d.tree', 'rb') as data_file:
        root = pickle.load(data_file)
    stop_time = time.time()
    print("Load tree time:",stop_time - start_time)
    
    

    while True:
        key = win.getKey()
        
        if key == '0':
            win.delete('all')
            #clear(win)
            data, goal, selectedPos, goalSum, sumX, sumY = probNgoal(n)
            data = data.tolist() # Convert array to list
            sumX = sumX.tolist()
            sumY = sumY.tolist()
            goal = goal.tolist()
            selectedPos = selectedPos.tolist()

            menu(win,winWidth,winHeight)    
            problemTable = setDefault(win, n, data, sumX, sumY)
            changeColor(problemTable, selectedPos)
            print("Goal: ",goal)
            # print("ID",id(problemTable))
          
        elif key=='1':
            print('BFS Search Algorithm')
            found = False
            start_time = time.time()
            # breadthFirstSearch(root, goal, problemTable)
            
            # Aomsin BFS
            goalState = np.array(goal)
            startState = np.zeros((1,len(goal)), dtype=np.int)
            print(doBreadthFirstSearch(startState, goalState, problemTable))
            
            stop_time = time.time()
            print("BFS  Search Time:" , stop_time - start_time, "s")
            
        elif key=='2':
            print('IDFS Search Algorithm')
            # print(convertIntToListBinary(goal))
            found = False
            start_time = time.time()
            iterativeDeepeningDepthFirstSearch(root, goal, problemTable)
            stop_time = time.time()
            print("IDFS Search Time:" , stop_time - start_time, "s")
            
        elif key=='Escape':
            win.close()
    
main()