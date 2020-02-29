from Node import *
import pickle
import time

root = Node([0, 0, 0, 0]) # Create a root node
depth = root.getSize() # depth of tree
branchingFactor = pow(2, depth) # branching factor of each node

for i in range(0, branchingFactor):
    root.addBranch(Node([0, 0, 0, i]))

for i in range(0, root.getBranchSize()):
    for j in range(0, branchingFactor):
        root.branch[i].addBranch(Node([0, 0, j, i]))

for i in range(0, root.getBranchSize()):
    for j in range(0, root.branch[i].getBranchSize()):
        for k in range(0, branchingFactor):
            root.branch[i].branch[j].addBranch(Node([0, k, j, i]))
            
for i in range(0, root.getBranchSize()):
    for j in range(0, root.branch[i].getBranchSize()):
        for k in range(0, root.branch[i].branch[j].getBranchSize()):
            for l in range(0, branchingFactor):
                root.branch[i].branch[j].branch[k].addBranch(Node([l, k, j, i]))
       

with open('data-4d.tree', 'wb') as data_file:
    pickle.dump(root, data_file, protocol=-1)

# print('-',root.getData())
# for i in root.getBranch():
#     print('--',i.getData())
#     for j in i.getBranch():
#         print('---', j.getData())
#         for k in j.getBranch():
#             print('----', k.getData())
#         #     for l in k.getBranch():
#         #         print('-----', l.getData())