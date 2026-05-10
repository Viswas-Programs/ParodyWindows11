import importlib, ParWFS
import shelve, os
#W11 = importlib.import_module("Windows 11")
MSGBOX = "MSGBOX_IDS"
PRID = "PROCESS_IDS"
PRG_ID = "PROGRESSBAR_IDS"
FILEASK = "FILEASK_IDS"
DIALOGUE_BOXES = "DIALOGUE_IDS"
LOADED_APPS = None

REPLY_RECEIVED = False
MSG_DATA = None

def sendCallToAnotherApp(YourPID, appName, messageContent: dict):
    RUNNING_APPS = returnRunningAppsList()[1]
    importName= appImportNameCheck(appName)
    for usr in list(dict(RUNNING_APPS).keys()):
        for PID in list(dict(RUNNING_APPS)[usr].keys()):
            appName = dict(RUNNING_APPS)[usr][PID]
            if appImportNameCheck(appName) == importName: _sendCallToPID(YourPID, PID, messageContent)
                
def _sendCallToPID(YourPID, PID, msg):
    from ProgramFiles import dwm
    message = {
        "SenderPID": YourPID,
        "ReceiverPID": PID,
        "messageContent": msg
    }
    dwm.receiveMessage(PID, message)
def setLoadedApps(loadedAppInst):
    global LOADED_APPS
    LOADED_APPS = loadedAppInst
def acknowledgeEndTask(PID: int):
    _sendCallToPID(2, 0, {"method": "EXEC_ACTION", "ACK_ENDTASK": PID})
    #W11.GUIButtonCommand.handleExits(PID, returnRunningAppsList())
def getHostDir():
    _sendCallToPID(2, 0, {"method": "GET", "GETATTR": "CWD"})
    return waitForFurtherReply()[1]["GETATTR"]
def getRangeToGenPID(type:str):
    _sendCallToPID(2, 0, {"method": "GET", "GEN_PID": type})
    return waitForFurtherReply()[1]["GEN_PID"]
    #rangeOfPID = PIDsToGen[type]
    #PID = random.randint(rangeOfPID[0], rangeOfPID[1])
    #for usr in ParWFS._instances["root"].RUNNING_APPS.keys():
    #    while PID in (ParWFS._instances["root"].RUNNING_APPS[usr]).keys():
    #        PID = random.randint(rangeOfPID[0], rangeOfPID[1])
    #return PID
def addToRunningAppsList(PID, type):
    #ParWFS._instances["root"].RUNNING_APPS[getCurrentUsername()][PID] = type
    _sendCallToPID(2, 0, {"method": "EXEC_ACTION", "ADD_RUNNING_APP": {"PID": PID, "appname": type}})
def returnRunningAppsList():
    _sendCallToPID(2, 0, {"method": "GET", "GETATTR": "RUNAPPSLIST"})
    data = waitForFurtherReply()[1]["GETATTR"]
    return data
    #return [ParWFS._instances["root"].RunAppsFrame,ParWFS._instances["root"].RUNNING_APPS]
def getReqIcon(iconStr, root, subsample=None):
    _sendCallToPID(2, 0, {"method": "GET", "GET_ICON":{"appname": iconStr, "root": root, "subsample": subsample}})
    IMAGE = root.TEMPORARY_REFERENCE = waitForFurtherReply()[1]["GET_ICON"]
    #if isinstance(IMAGE, Image.Image): IMAGE = root.TEMPORARY_REFERENCE = ImageTk.PhotoImage(IMAGE, master=root)
    return IMAGE
    #return W11.giveIcon(iconStr, root)
def appImportNameCheck(appName):
    #try:
    _sendCallToPID(2, 0, {"method": "GET", "GET_APP_IMPORT_NAME": appName})
    return waitForFurtherReply()[1]["GET_APP_IMPORT_NAME"]
    #return W11.GUIButtonCommand.AppImportNameCheck(appName)
def endTaskByName(importName: str, externalPrintMsg=print):
    RUNNING_APPS: dict[int, dict[int, str]] = ParWFS._instances["root"].RUNNING_APPS
    PIDS = []
    USERNAMES = []
    for usr in list(dict(RUNNING_APPS).keys()):
        for prPid in list(dict(RUNNING_APPS)[usr].keys()):
            appName = dict(RUNNING_APPS)[usr][prPid]
            if appImportNameCheck(appName) == importName: 
                PIDS.append(prPid)
                USERNAMES.append(usr)
    for x, PID in enumerate(PIDS):
        try:
            _sendCallToPID(2, 0, {"method": "EXEC_ACTION", "END_TASK": f"{PID}:{USERNAMES[x]}"})
            data = waitForFurtherReply()[1]
            if data["END_TASK"] != True: raise Exception(data["END_TASK"]) 
            #W11.TaskManager.endTask(f"{PID}:{USERNAMES[x]}")
        except Exception as EXP:externalPrintMsg(f"\nCould not terminate process {PID} under username {USERNAMES[x]} associated with process {importName}\nError:{EXP}")
        else:externalPrintMsg(f"\nKilled process {PID} under username {USERNAMES[x]} associated with process {importName}")
def endTaskByPID(PID: int, externalPrintMsg=print):
    USERNAME = None
    RUNNING_APPS: dict[int, dict[int, str]] = ParWFS._instances["root"].RUNNING_APPS
    for usr in list(dict(RUNNING_APPS).keys()):
        for appName in list(dict(RUNNING_APPS)[usr].keys()):
            if appName == PID:USERNAME = usr
    try:
        _sendCallToPID(2, 0, {"method": "EXEC_ACTION", "END_TASK": f"{PID}:{USERNAME}"})
        data = waitForFurtherReply()[1]
        if data["END_TASK"] != True: raise Exception(data["END_TASK"])
        #W11.TaskManager.endTask(f"{PID}:{USERNAME}")
    except Exception as EXP: externalPrintMsg(f"\n Could not terminate process {PID} under username {USERNAME}\nError: {EXP}")
    else: externalPrintMsg(f"\nKilled process {PID} under username {USERNAME}")
def getCurrentUsername():
    _sendCallToPID(2, 0, {"method": "GET", "GETATTR": "USERNAME"})
    return waitForFurtherReply()[1]["GETATTR"]
def appLauncherForExternalApps(appName, userName, param, USER_CONFIG=None):
    if not USER_CONFIG: 
        with shelve.open(os.path.join(getHostDir(), "Users", userName, "USER_CONFIG")) as shelveRead: USER_CONFIG=dict(shelveRead)
    _sendCallToPID(2, 0, {"method": "EXEC_ACTION", "LAUNCH_APP_EXTAPPLNCHR": {"APP_NAME": appName, "USERNAME": userName, "USER_CONFIG": USER_CONFIG, "PARAMS": param}})
    #W11._AppLauncherForExternalApps(appName, USER_CONFIG, param, userName)
def getTheme():
    _sendCallToPID(2, 0, {"method": "GET", "GETATTR": "THEME_WINDOW_BG"})
    LS = ["Black", "White", "Black"]
    BG = waitForFurtherReply()[1]["GETATTR"]
    if not isinstance(BG, Exception): LS[0] = BG
    _sendCallToPID(2,0, {"method": "GET", "GETATTR": "THEME_FOREGROUND"})
    FG = waitForFurtherReply()[1]["GETATTR"]
    if not isinstance(FG, Exception): LS[1] = FG
    _sendCallToPID(2,0, {"method": "GET", "GETATTR": "THEME_WN_CLR"})
    WC = waitForFurtherReply()[1]["GETATTR"]
    if not isinstance(WC, Exception): LS[2] = WC
    return LS

def messageReceiver(messageConts: dict):
    global REPLY_RECEIVED, MSG_DATA
    REPLY_RECEIVED = True
    replyToPID = messageConts["SenderPID"]
    msgConts = messageConts["messageContent"]
    MSG_DATA = (replyToPID, msgConts)
    return replyToPID, msgConts

def waitForFurtherReply():
    global REPLY_RECEIVED
    while not REPLY_RECEIVED: pass
    REPLY_RECEIVED = False
    return MSG_DATA

class INTERNALS__messageHandler():
    def __init__(self):
        self.MESSAGES = {}
        self.MESSAGES_CALLBACK = messageReceiver
        self.MESSAGES_AUTODELETE = True
messageHandler = INTERNALS__messageHandler()
def INIT_DWM():
    from ProgramFiles import dwm
    dwm.MANAGED_DWM_INSTANCES[2] = [None, None, messageHandler, None, None, None]
    