import os

def getModules():
    root = os.path.dirname(os.path.realpath(__file__))
    return [ f[0:-3] for f in os.listdir(root) \
                 if os.path.isfile(os.path.join(root, f)) \
                 and f[0] != '.' and f[-3:] == '.py' and \
                 f != '__init__.py' and f != "IAPI.py"]
