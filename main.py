from graphics import *
import time
import numpy as np
from Node import *
from Queue import *
import pickle

def changeColor(rect, wip):
    for i in range(0, len(rect[0])-1):
        for j in range(0, len(rect[0])-1):
            if wip[i][j] == 1:
                rect[i][j].setFill(color_rgb(0, 220, 220))
            else:
                rect[i][j].setFill(color_rgb(0, 100, 255))

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

def probNgoal(n):
  prob = np.random.randint(1, 9, (n,n))
  goalState = np.random.random_integers(1, 2**n-1, n)
  goalPosition = np.asarray([list(map(int, bin(x)[2:].zfill(4))) for x in goalState])

  goalSum = [list(prob[i] * goalPosition[i]) for i in range(4)]
  sumX = np.sum(goalSum, axis=0)
  sumY = np.sum(goalSum, axis=1)
  
  return prob.tolist(), goalState.tolist(), goalPosition, goalSum, sumX.tolist(), sumY.tolist()

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

def doHeuristicSearch(root, goal, problemTable):
    global found
    frontier = Queue()
    frontier.enQueue(root)
    costInFrontier = []
    minIndex = 0

    while frontier.size() > 0 and not found:
        currentNode = frontier.deQueueWithIndex(minIndex)
        if costInFrontier: del costInFrontier[minIndex]

        changeColor(problemTable, convertIntToListBinary(currentNode.getData()))

        if(currentNode.getData() == goal):
            found = True

        for i in range(0, currentNode.getBranchSize()):
            node = currentNode.branch[i]
            frontier.enQueue(node)
            costInFrontier.append(node.getHeuristicValue())

        minIndex = np.argmin(costInFrontier)

def heuristicValue(data, sumY, state):
    selectPos = np.asarray([list(map(int, bin(x)[2:].zfill(4))) for x in state])
    sumSelectInRow = [sum(x) for x in selectPos*data]
    hValue = sum([abs(x-y) for x,y in zip(sumY,sumSelectInRow)])
    return hValue

def createTree(data, sumY):
    start_time = time.time()
    root = Node([0, 0, 0, 0]) # Create a root node
    depth = root.getSize() # depth of tree
    branchingFactor = pow(2, depth) # branching factor of each node

    for i in range(0, branchingFactor):
        state = [0, 0, 0, i]
        root.addBranch(Node(state, heuristicValue(data, sumY, state)))

    for i in range(0, root.getBranchSize()):
        for j in range(0, branchingFactor):
            state = [0, 0, j, i]
            root.branch[i].addBranch(Node(state, heuristicValue(data, sumY, state)))

    for i in range(0, root.getBranchSize()):
        for j in range(0, root.branch[i].getBranchSize()):
            for k in range(0, branchingFactor):
                state = [0, k, j, i]
                root.branch[i].branch[j].addBranch(Node(state, heuristicValue(data, sumY, state)))

    for i in range(0, root.getBranchSize()):
        for j in range(0, root.branch[i].getBranchSize()):
            for k in range(0, root.branch[i].branch[j].getBranchSize()):
                for l in range(0, branchingFactor):
                    state = [l, k, j, i]
                    root.branch[i].branch[j].branch[k].addBranch(Node(state, heuristicValue(data, sumY, state)))

    stop_time = time.time()
    print("Create tree time:",stop_time - start_time)

    with open('data-4d.tree', 'wb') as data_file:
        pickle.dump(root, data_file, protocol=-1)

def loadTree():
    start_time = time.time()
    with open('data-4d.tree', 'rb') as data_file:
        root = pickle.load(data_file)
    stop_time = time.time()
    print("Load tree time:",stop_time - start_time)
    return root

def main():
    global found
    initState = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]

    n = 4

    win = createUI(n)

    win.setBackground(color_rgb(255, 255, 255))
    winWidth = win.getWidth()
    winHeight = win.getHeight()
    
    menu(win,winWidth,winHeight)
    
    data, goal, goalPos, goalSum, sumX, sumY = probNgoal(n)
    problemTable = setDefault(win, n, data, sumX, sumY)
    changeColor(problemTable, initState)
    print("Goal: ",goal)

    createTree(data, sumY)
    root = loadTree()

    while True:
        key = win.getKey()
        
        if key == '0':
            data, goal, selectedPos, goalSum, sumX, sumY = probNgoal(n)
            problemTable = setDefault(win, n, data, sumX, sumY)
            print("Goal: ",goal)

            createTree(data, sumY)
            root = loadTree()
          
        elif key=='1':
            print('BFS Search Algorithm')
            found = False
            start_time = time.time()
            # breadthFirstSearch(root, goal, problemTable)
            
            # Aomsin BFS
            goalState = np.array(goal)
            startState = np.zeros((1,len(goal)), dtype=np.int)
            doBreadthFirstSearch(startState, goalState, problemTable)
            
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

        elif key=='3':
            print('Heuristic Search')
            # print(convertIntToListBinary(goal))
            found = False
            start_time = time.time()
            doHeuristicSearch(root, goal, problemTable)
            stop_time = time.time()
            print("Heuristic Search Time:" , stop_time - start_time, "s")
            
        elif key=='Escape':
            win.close()
    
main()
