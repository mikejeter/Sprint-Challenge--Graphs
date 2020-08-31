class Queue():
    def __init__(self):
        self.queue = []

    def dequeue(self):
        
        if self.size() > 0:
            return self.queue.pop(0)
        
    def enqueue(self, value):
            self.queue.append(value)

    def size(self):
            return len(self.queue)