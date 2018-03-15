from threading import Thread


class ListOfMethodsThread(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        func = self.queue.get()
        if type(func) == 'tuple':
            func[0](func[1])
        else:
            func()
        self.queue.task_done()
        print('class queue', self.queue.qsize())
