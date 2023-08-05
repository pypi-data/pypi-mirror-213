import time


class TimeChecker:
    def __init__(self, is_init=True):
        self.st_time = None
        if is_init:
            self.st_pinning()

    def st_pinning(
        self,
    ):
        if self.st_time is not None:
            print("Override the starting time")
        self.st_time = time.time()

    def print_elapsed_time(self, txt="Elapsed time: "):
        self.print_lap_time(txt)
        self.clear()

    def print_conditional_elapsed_time(
        self, min_limit=-1.0, max_limit=1e10, txt="Elapsed time: "
    ):
        if (
            min_limit < time.time() - self.st_time
            and time.time() - self.st_time < max_limit
        ):
            self.print_lap_time(txt)
        self.clear()

    def print_lap_time(self, txt="Elapsed time: "):
        print(txt, time.time() - self.st_time)

    def clear(
        self,
    ):
        self.st_time = None
