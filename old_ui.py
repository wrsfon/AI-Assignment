from graphics import *
import time
import numpy as np
from Node import *
import pickle
from Queue import *
import os
import psutil


def probNgoal(n):
  prob = np.random.randint(1, 9, (n,n))
  goalState = np.random.random_integers(1, 2**n-1, n)
#   goalState = np.array([0, 3, 5, 7])
  goalPosition = np.asarray([list(map(int, bin(x)[2:].zfill(4))) for x in goalState])

  goalSum = [list(prob[i] * goalPosition[i]) for i in range(4)]
  sumX = np.sum(goalSum, axis=0)
  sumY = np.sum(goalSum, axis=1)
  
  return prob, goalState, goalPosition, goalSum, sumX, sumY

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

    for x in range(0, n + 1):
        for y in range(0, n + 1):
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

def buttons():
    random = Rectangle(Point(20, 620), Point(136, 660))
    bfs = Rectangle(Point(156, 620), Point(272, 660))
    idfs = Rectangle(Point(292, 620), Point(408, 660))
    save = Rectangle(Point(428, 620), Point(544, 660))
    quit = Rectangle(Point(564, 620), Point(680, 660))

    random.draw(win)
    bfs.draw(win)
    idfs.draw(win)
    save.draw(win)
    quit.draw(win)
    return random, bfs, idfs, save, quit

def text():
    text_random = Text(Point(78, 640), "Random")
    text_bfs = Text(Point(214, 640), "BFS")
    text_idfs = Text(Point(350, 640), "IDFS")
    text_save = Text(Point(486, 640), "Save")
    text_quit = Text(Point(622, 640), "Quit")
    
    text_head = Text(Point(350, 50), "Pluszle 4 x 4")
    text_head.setSize(30)
    text_head.setStyle('bold')

    text_random.draw(win)
    text_bfs.draw(win)
    text_idfs.draw(win)
    text_save.draw(win)
    text_quit.draw(win)
    text_head.draw(win)
    
def textGoal(goal):
    text_goal = Text(Point(350, 700), "Goal : " + str(goal))
    text_goal.setSize(20)
    text_goal.setStyle('bold')
    text_goal.draw(win)
    return text_goal

def setGoal(goal):
    text_goal.setText("Goal : " + str(goal))
    return text_goal

def inside(point, rectangle):
    """ Is point inside rectangle? """
    ll = rectangle.getP1()  # assume p1 is ll (lower left)
    ur = rectangle.getP2()  # assume p2 is ur (upper right)
    return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()

def setRandomProblem():
    global random, bfs, idfs, save, quit
    win.delete('all')

    prob, goalState, goalPosition, goalSum, sumX, sumY = probNgoal(n)
    data = prob.tolist() # Convert array to list
    sumX = sumX.tolist()
    sumY = sumY.tolist()
    goalState = goalState.tolist()
    goal = goalState
    selectedPos = goalPosition.tolist()
    # print("Random Problem: ",data)
    # print("Sum X: ", sumX)
    # print("Sum Y: ", sumY)
    # print("Goal State: ", goalState)
    # print("Goal Position: ", selectedPos)
    # print("goal sum: ", goalSum)
    
    problemTable = setDefault(win, n, data, sumX, sumY)
    changeColor(problemTable, selectedPos)
    
    random, bfs, idfs, save, quit = buttons()
    text()
    textGoal(goalState)
    
    return goal,problemTable



def convertIntToListBinary(goal):
    searchGoal = []
    for i in goal:
        searchGoal.append([int(x) for x in list('{0:04b}'.format(i))])
    return searchGoal 

data = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
sumX = [0, 0, 0, 0]
sumY = [0, 0, 0, 0]

selectedPos = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]

goal = [0,0,0,0]
n = 4
width = 100*(n+3)
height = width + 40
win = GraphWin("Pluszle", width, height )
win.setBackground(color_rgb(255, 255, 255))
random, bfs, idfs, save, quit = buttons()
text()
text_goal = textGoal(goal)
# setRandomProblem()
problemTable = setDefault(win, n, data, sumX, sumY)

start_time = time.time()
with open('data-4d.tree', 'rb') as data_file:
    root_init = pickle.load(data_file)
stop_time = time.time()
print("Load time",stop_time - start_time)

found = False
# time.sleep(1)
# resetColor(problemTable)
# time.sleep(1)
# changeColor(problemTable, selectedPos)

def iterativeDeepeningDepthFirstSearch(root,goal):
    # Repeatedly depth-first search up-to a maximum depth of 6.
    for maxDepth in range(0,len(goal)+1):
        depthFirstSearch(root, goal, maxDepth)

def depthFirstSearch(root, goal, maxDepth):
    global found
    global problemTable
    if not found:
        #print(root.getData(), convertIntToListBinary(root.getData()))
        changeColor(problemTable, convertIntToListBinary(root.getData()))
        
        if(root.getData() == goal):
            found = True
            
        # If reached the maximum depth, stop recursing.
        if maxDepth <= 0:
            return 
        # Recurse for all children of node.
        for i in range(0,root.getBranchSize()):
            depthFirstSearch(root.branch[i], goal, maxDepth-1)

def breadthFirstSearch(root, goal):
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
                                
while True:
    clickPoint = win.getMouse()
    if clickPoint is None:  # so we can substitute checkMouse() for getMouse()
        print("None")
    elif inside(clickPoint, random):
        goal, problemTable = setRandomProblem()
        found = False
    elif inside(clickPoint, bfs):
        print("BFS")
        found = False
        root = root_init
        print(goal)
        print(convertIntToListBinary(goal))
        start_time = time.time()
        breadthFirstSearch(root, goal)
        stop_time = time.time()
        print("BFS Time :" , stop_time - start_time)
        process = psutil.Process(os.getpid())
        print("Process Space :", process.memory_info().rss, "Bytes")
        print("Process Space (%)", str(process.memory_percent() * 100))
    elif inside(clickPoint, idfs):
        print("IDFS")
        found = False
        root = root_init
        print(goal)
        print(convertIntToListBinary(goal))
        start_time = time.time()
        iterativeDeepeningDepthFirstSearch(root,goal)
        stop_time = time.time()
        print("IDFS Time :" , stop_time - start_time)
        process = psutil.Process(os.getpid())
        print("Process Space :", process.memory_info().rss, "Bytes")
        print("Process Space (%)", str(process.memory_percent() * 100))
    elif inside(clickPoint, save):
        print("Save")
    elif inside(clickPoint, quit):
        break
    else:
        print(clickPoint)

win.close()

