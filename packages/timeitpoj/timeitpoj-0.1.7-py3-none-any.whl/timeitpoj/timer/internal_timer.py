import time


class InternalTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

        self.internal_time = 0

    def __enter__(self):
        if self.start_time is not None:
            return self

        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is None:
            return
        self.internal_time += time.time() - self.start_time
        self.start_time = None
