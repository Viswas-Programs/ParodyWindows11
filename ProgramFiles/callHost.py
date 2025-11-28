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
    for usr in ParWFS._instances["root"].RUNNING_APPS.keys():
        while PID in (ParWFS._instances["root"].RUNNING_APPS[usr]).keys():
            PID = random.randint(rangeOfPID[0], rangeOfPID[1])
    return PID
def addToRunningAppsList(PID, type):
    ParWFS._instances["root"].RUNNING_APPS["defaultuser0"][PID] = type
def returnRunningAppsList():
    return [ParWFS._instances["root"].RunAppsFrame,ParWFS._instances["root"].RUNNING_APPS]
def getReqIcon(iconStr, root):
    return W11.giveIcon(iconStr, root)
def appImportNameCheck(appName):
    return W11.GUIButtonCommand.AppImportNameCheck(appName)
def endTaskByName(importName: str, externalPrintMsg=print):
    RUNNING_APPS: dict[int, dict[int, str]] = ParWFS._instances["root"].RUNNING_APPS
    PIDS = []
    USERNAMES = []
    for usr in list(dict(RUNNING_APPS).keys()):
        for prPid in list(dict(RUNNING_APPS)[usr].keys()):
            appName = dict(RUNNING_APPS)[usr][prPid]
            print(W11.GUIButtonCommand.AppImportNameCheck(appName), importName)
            if appImportNameCheck(appName) == importName: 
                PIDS.append(prPid)
                USERNAMES.append(usr)
    for x, PID in enumerate(PIDS):
        print(PID)
        try: W11.TaskManager.endTask(f"{PID}:{USERNAMES[x]}")
        except Exception as EXP:externalPrintMsg(f"\nCould not terminate process {PID} under username {USERNAMES[x]} associated with process {importName}\nError:{EXP}")
        else:externalPrintMsg(f"\nKilled process {PID} under username {USERNAMES[x]} associated with process {importName}")
def endTaskByPID(PID: int, externalPrintMsg=print):
    USERNAME = None
    RUNNING_APPS: dict[int, dict[int, str]] = ParWFS._instances["root"].RUNNING_APPS
    for usr in list(dict(RUNNING_APPS).keys()):
        for appName in list(dict(RUNNING_APPS)[usr].keys()):
            if appName == PID:USERNAME = usr
    try: W11.TaskManager.endTask(f"{PID}:{USERNAME}")
    except Exception as EXP: externalPrintMsg(f"\n Could not terminate process {PID} under username {USERNAME}\nError: {EXP}")
    else: externalPrintMsg(f"\nKilled process {PID} under username {USERNAME}")
def getCurrentUsername():
    print("Here")
    return ParWFS._instances["root"].GLOBAL_VARS.USERNAME
def appLauncherForExternalApps(appName, userName, param):
    USER_CONFIG = None
    import shelve, os

    with shelve.open(os.path.join(getHostDir(), "Users", userName, "USER_CONFIG")) as shelveRead:
        USER_CONFIG=dict(shelveRead)
    W11._AppLauncherForExternalApps(appName, USER_CONFIG, param, userName, W11.notification )