from Node import *
import time
import pickle


goal = Node([0, 0, 1, 15]) # Goal node
found = False

start_time = time.time()
with open('data-4d.tree', 'rb') as data_file:
    root = pickle.load(data_file)
stop_time = time.time()
print("Load time",stop_time - start_time)

def iterativeDeepeningDepthFirstSearch(root,goal):
    # Repeatedly depth-first search up-to a maximum depth of 6.
    for maxDepth in range(0,goal.getSize()+1):
        depthFirstSearch(root, goal, maxDepth)

def depthFirstSearch(root, goal, maxDepth):
    global found
    if not found:
        # print(root.getData())
        if(root.getData() == goal.getData()):
            found = True
            
        # If reached the maximum depth, stop recursing.
        if maxDepth <= 0:
            return 
        # Recurse for all children of node.
        for i in range(0,root.getBranchSize()):
            depthFirstSearch(root.branch[i], goal, maxDepth-1)

start_time = time.time()
iterativeDeepeningDepthFirstSearch(root,goal)
stop_time = time.time()
print(stop_time - start_time)