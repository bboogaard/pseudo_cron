class MockProcess:

    _is_alive: bool = False

    def __init__(self, target):
        self.func = target

    def start(self):
        self.func()

    def join(self, timeout):
        ...

    def is_alive(self):
        return self._is_alive

    def terminate(self):
        ...
