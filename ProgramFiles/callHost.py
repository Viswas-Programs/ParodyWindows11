import importlib, ParWFS, random
W11 = importlib.import_module("Windows 11")
MSGBOX = "MSGBOX_IDS"
PRID = "PROCESS_IDS"
PRG_ID = "PROGRESSBAR_IDS"
FILEASK = "FILEASK_IDS"
DIALOGUE_BOXES = "DIALOGUE_IDS"
PIDsToGen = {
    "PROCESS_IDS": W11.PROCESS_IDS,
    "MSGBOX_IDS": W11.MESSAGEBOX_IDS, 
    "PROGRESSBAR_IDS": W11.PROGRESSBAR_IDS,
    "FILEASK_IDS": W11.FILEASK_WINDOWS,
    "DIALOGUE_IDS": W11.DIALOGUE_BOXES
}
LOADED_APPS = None
def setLoadedApps(loadedAppInst):
    global LOADED_APPS
    LOADED_APPS = loadedAppInst
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
def appImportNameCheck(appName):
    return W11.GUIButtonCommand.AppImportNameCheck(appName)
def endTaskByName(importName: str, externalPrintMsg=print):
    RUNNING_APPS: dict[int, str] = ParWFS._instances["root"].RUNNING_APPS
    PIDS = []
    for i, appName in enumerate(list(dict(RUNNING_APPS).values())):
        print(W11.GUIButtonCommand.AppImportNameCheck(appName), importName)
        if appImportNameCheck(appName) == importName: PIDS.append(list(dict(RUNNING_APPS).keys())[i])
    for PID in PIDS:
        W11.TaskManager.endTask(PID)
        externalPrintMsg(f"\nKilled process {PID} associated with process {importName}")
def endTaskByPID(PID: int):
    W11.TaskManager.endTask(PID)
def getCurrentUsername():
    return W11.GLOBAL_VARS.USERNAME