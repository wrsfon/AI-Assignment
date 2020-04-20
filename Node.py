class Node:
    def __init__(self, data = None, heuristicValue = 0):
        self.data = data
        self.branch = []
        self.heuristicValue = heuristicValue

    def hasNext(self):
        return self.branch != []
    
    def getData(self):
        return self.data

    def getHeuristicValue(self):
        return self.heuristicValue

    def getSize(self):
        return len(self.data)

    def addBranch(self, node):
        self.branch.append(node)

    def getBranch(self):
        return self.branch

    def getBranchSize(self):
        return len(self.branch)
    
    def PostorderTraversal(self, root):
        res = []
        if root:
            res = self.PostorderTraversal(root.left)
            res = res + self.PostorderTraversal(root.right)
            res.append(root.data)
        return res
