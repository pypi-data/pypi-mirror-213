class Random:
    def __init__(self, seed):
        self.current_value = seed
        self.a = 16807
        self.p = 2**31 - 1
        return

    def _random(self):
        while True:
            next_value = self.a * self.current_value % self.p
            self.current_value = next_value
            yield next_value

    def integer(self):
        return next(self._random())

    def real(self):
        return next(self._random()) / self.p
