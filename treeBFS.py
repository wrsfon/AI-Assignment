from Node import *
from Queue import *
import pickle,time

goal = Node([0, 0, 1, 15]) # Goal node
found = False

start_time = time.time()
with open('data-4d.tree', 'rb') as data_file:
    root = pickle.load(data_file)
stop_time = time.time()
print("Load time",stop_time - start_time)


def breadthFirstSearch(root, goal):
    global found
    q = Queue()
    q.enQueue(root)
    
    while q.size() > 0 and not found:
        node = q.deQueue()
        # print(node.getData())
        
        if(node.getData() == goal.getData()):
            found = True
        # add all the children to the back of the queue
        for i in range(0,node.getBranchSize()):
            q.enQueue(node.branch[i])

start_time = time.time()
breadthFirstSearch(root, goal)
stop_time = time.time()
print(stop_time - start_time)