class Node:
    def __init__(self, data = None):
        self.data = data
        self.branch = []

    def hasNext(self):
        return self.branch != []
    
    def getData(self):
        return self.data

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
