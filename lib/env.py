import os

def env(name, value = None):
    if (value is None):
        return os.environ.get(name)
    else:
        return os.environ.get(name, value)
