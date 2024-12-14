import importlib, ParWFS, random
W11 = importlib.import_module("Windows 11")
MSGBOX = "MSGBOX_IDS"
PRID = "PROCESS_IDS"
PRG_ID = "PROGRESSBAR_IDS"
FILEASK = "FILEASK_IDS"
PIDsToGen = {
    "PROCESS_IDS": W11.PROCESS_IDS,
    "MSGBOX_IDS": W11.MESSAGEBOX_IDS, 
    "PROGRESSBAR_IDS": W11.PROGRESSBAR_IDS,
    "FILEASK_IDS": W11.FILEASK_WINDOWS
}
def acknowledgeEndTask(PID: int):
    W11.GUIButtonCommand.handleExits(PID, returnRunningAppsList())
def getHostDir():
    return W11.CWD
def getRangeToGenPID(type:str):
    rangeOfPID = PIDsToGen[type]
    PID = random.randint(rangeOfPID[0], rangeOfPID[1])
    while PID in ParWFS._instances["root"].RUNNING_APPS.keys():
        PID = random.randint(rangeOfPID[0], rangeOfPID[1])
    return PID
def addToRunningAppsList(PID, type):
    ParWFS._instances["root"].RUNNING_APPS[PID] = type
def returnRunningAppsList():
    return [ParWFS._instances["root"].RunAppsFrame,ParWFS._instances["root"].RUNNING_APPS]
def getReqIcon(iconStr, root):
    return W11.giveIcon(iconStr, root)