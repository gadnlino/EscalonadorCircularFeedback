class Node(object):

    def __init__(self, data=None):
        self.data = data
        self.next = None
        
    def getData(self):
        return self.data

class LinkedList(object):
    def __init__(self, head=None):
        self.num = 0
        self.head = head
        self.tail = None


    def enqueueEnd(self, data):
        new_node = Node(data)
        if(self.num == 0):
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.num+=1

    def dequeueBegin(self):
        if(self.num > 0):
            self.head = self.head.next
            self.num -= 1
            if(self.num == 0):
                self.tail = None

    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next
