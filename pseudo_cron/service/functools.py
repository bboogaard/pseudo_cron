import multiprocessing

from .exceptions import TimeoutException


def exec_safe(func, timeout):
    p = multiprocessing.Process(target=func)
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        raise TimeoutException('Job timed out')
