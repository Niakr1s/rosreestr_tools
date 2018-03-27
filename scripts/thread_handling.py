from threading import Thread


class Threads:
    def __init__(self, queue, max_threads, bar):
        self.queue = queue
        self.is_active = True
        self.max_threads = max_threads
        self.bar = bar
        self.bar_count = 0
        self.threads = self.get_threads()

    def get_threads(self):
        threads = []
        for i in range(self.max_threads):
            t = Thread(target=self.worker)
            t.start()
            threads.append(t)
        return threads

    def worker(self):
        while True:
            task = self.queue.get()
            if task is None:
                break
            if isinstance(task, tuple):
                task[0](*task[1])
            else:
                task()
            self.queue.task_done()
            if self.bar is not None:
                self.bar_count += 1
                if self.bar_count <= self.bar.max_value:
                    self.bar.update(self.bar_count)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        for i in range(self.max_threads):
            self.queue.put(None)
