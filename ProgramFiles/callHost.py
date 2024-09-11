import importlib
W11 = importlib.import_module("Windows 11")

def acknowledgeEndTask(PID: int, RunningAppsList):
    W11.GUIButtonCommand.handleExits(PID, RunningAppsList)

def getHostDir():
    return W11.CWD