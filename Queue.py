class Queue:
    def __init__(self, items=None):
        if items is None:
            self.items = []
        else:
            self.items = items

    def size(self):
        return len(self.items)

    def empty(self):
        return self.items == []

    def front(self):
        return self.items[0]

    def enQueue(self, element):
        self.items +=[element]

    def deQueue(self):
        return self.items.pop(0) 