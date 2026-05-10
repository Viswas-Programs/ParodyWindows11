from pathlib import Path
import tkinter
import importlib
from datetime import datetime

class ErrorRouter:
    def __init__(self):
        self.LOGS = {str(datetime.now()): "SESSION STARTUP"}
    
    def addTextLog(self, text):
        self.LOGS[str(datetime.now())] = text
    
    def updateFileLogs(self):
        TEXT = ""
        for T, Log in self.LOGS.items():
            TEXT += f"{T}: {Log}\n"
        with open(os.path.join(CWD, "ProgramFiles", "LOG.txt"), "a") as writer:
            writer.write(TEXT)
        with shelve.open(os.path.join(CWD, "ProgramFiles", "LOG"), writeback=True) as shelveWrite:
            shelveWrite.update(self.LOGS)
        self.LOGS.clear()

    def addRawLog(self, exception: Exception, objectsInvolved=[], additionalText="", ):
        typeofExp = exception.__class__.__name__
        extendedText = ""
        if len(objectsInvolved)>0: extendedText += " on the objects"
        for i in objectsInvolved: extendedText += f" {i} of type {type(i)} "
        self.LOGS[str(datetime.now())] = f"{typeofExp} occured with reasoning {additionalText} {exception} {extendedText}"
    def sync(self, errorInstance):
        """ merges given instance of ErrorRouter with current"""
        self.LOGS.update(errorInstance.LOGS)
    def __del__(self):
        try:
            self.LOGS = {str(datetime.now()): "ERROR ROUTER DEL"}
            self.updateFileLogs()
        except: pass


LOGGER = ErrorRouter()

def bsod(obj, supportCode) -> None:
    text = f"""A problem has occured on ParodyWin11 and has been shutdown to prevent further damage\n
If this is the first time you're seeing this stop screen, please make sure you have proper configuration files 
in the right place.\n\nIf the problem still exists, please contact your administrator or have a 
look at this informative page on stop codes! (support link)\n\nSupport: \nhttps://github.com/Viswas-Programs/ParodyWindows11/wiki/STOP_CODES\n\n
Technical information: {obj} Failed to load properly (Improperly loaded!)\nSupport Code: {supportCode}\n
Restarting in a moment..."""
    try:
        def restart():
            LOGGER.updateFileLogs()
            bsodWind.destroy()
            time.sleep(5)
            os.system(f""" python "Windows 11.py" """)
            exit()
        try:
            SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", CBSRESTART + 1)
            with open("ProgramFiles/CRASHLOGS", "a") as UPDATE_CRASH_LOGS: UPDATE_CRASH_LOGS.write(f"\n{supportCode} occured on {datetime.now()} on {obj}")
        except Exception as EXP: exp = EXP; LOGGER.addRawLog(EXP, [SYS_CONFIG["CBSRESTARTATTEMPT"]], "Within BSOD: Unable to either add crashlog or cbs-restart-attempt") 
        finally:
            LOGGER.addTextLog(f"BSOD Occured: {supportCode} on object {obj}")
            LOGGER.updateFileLogs()
            bsodWind = tkinter.Tk()
            bsodWind.configure(background="blue")
            bsodWind.attributes("-fullscreen", True)
            tkinter.Label(bsodWind, background="Blue", foreground="White", text=text, font=("Arial Rounded MT Bold", 18)).pack(anchor=tkinter.W)
            try: 
                if exp: tkinter.Label(bsodWind, background="Blue", foreground="White", text=f"During above error, another error occured: {exp}", font=("Arial Rounded MT Bold", 18)).pack(anchor=tkinter.W)
            except Exception: pass
            bsodWind.after(10000, restart)
            bsodWind.mainloop()
    except Exception as EXP: print(text, EXP); LOGGER.addRawLog(EXP, [supportCode], "Unable to start BSOD. ")
try:
    from ProgramFiles import dwm
    import ParWFS
    from datetime import datetime
    import sys
    import os
    import shelve
    import tkinter
    import tkinter.ttk as ttk
    import time
    import random
    import ProgramFiles.tooltips as tooltips
    from PIL import Image, ImageTk, ImageGrab
    import psutil
    from ProgramFiles.buttons import IconButton, SidebarButtons
    import platform
    from ProgramFiles import entryWidget
    from ProgramFiles.errorHandler import messagebox
    from ProgramFiles import callHost
except Exception as E:
    bsod(__name__, str(E) + "\nMODULE_NOT_FOUND_ERROR")
CWD = os.getcwd()
FILE_SYSTEM = ParWFS.ParWFS()
FILE_SYSTEM.loadConfig("ProgramFiles/SYS_CONFIG", "SYS_CONFIG")
SYS_CONFIG = FILE_SYSTEM.getConfig("SYS_CONFIG")
try:
    PYTHON_COMMAND_ARG = SYS_CONFIG["PYTHON_LAUNCH_COMMAND"]
except Exception as EXP:
    LOGGER.addRawLog(EXP, [SYS_CONFIG], "PYTHON_LAUNCH_COMMAND doesn't exist on SYS_CONFIG")
    FILE_SYSTEM.editConfig("SYS_CONFIG", "PYTHON_LAUNCH_COMMAND", "python3")
    PYTHON_COMMAND_ARG = SYS_CONFIG["PYTHON_LAUNCH_COMMAND"]
USER_FOLDERS_LIST = ["My Documents", "My Pictures", "My Videos", "My Downloads"]
print("Starting OS...")

class LoadedApps():
    def __init__(self):
        self.IMPORTED_APPS = dict()
        self.ROOT = None
    def getAppCache(self, appName, showerror=True):
        try:
            realAppName = appName
            if realAppName not in self.IMPORTED_APPS.keys(): self.reloadAppCache(realAppName, showerror)
            return self.IMPORTED_APPS[appName]
        except Exception as EXP:
            LOGGER.addRawLog(EXP, [realAppName, self.IMPORTED_APPS], f"Unable to import {realAppName}")
            if showerror: messagebox.showerror("Unable to use/import app!", f"Error trying to use/import an app!\n{EXP}", self.ROOT)
    def reloadAppCache(self, appName, showerror=True):
        realAppName = appName
        try:
            self.IMPORTED_APPS[realAppName] = importlib.import_module(realAppName)
        except Exception as EXP:
            LOGGER.addRawLog(EXP, [self.IMPORTED_APPS, realAppName], f"Unable to reload app cache for {realAppName}")
            if showerror: messagebox.showerror("Can't reload app code!", f"Error trying to reload the app code!\n{EXP}")


class PW11GlobalVars():
    """
    Contains all the variables in use for the shell's functions. These act as replacement to global variables.
    """
    def __init__(self):
        self.SPECIAL_PIDS = [0, 1]
        self.ROW_COUNT_NOTIFICATION_WINDOW = 0
        self.ROW_COUNT_DESKTOP_ICONS = 0
        self.COLUMN_COUNT_DESKTOP_ICONS = 0
        self.MAX_ROW_DESKTOP = 10
        self.MAX_COLUMN_DESKTOP = 15
        self.START_MENU_ACTIVE: StartMenu = False
        self.DESKTOP_FRAME: tkinter.Frame = None
        self.WALLPAPER: tkinter.Label = None
        self.APPS_FRAME: tkinter.Frame = None
        self.RUNNING_APPS_FRAME: tkinter.Frame = None
        self.NOTIFICATION_BUTTON: tkinter.Button = None
        self.ROOT_WINDOW: tkinter.Tk = None
        self.DESKTOP_CONTEXT_MENU: tkinter.Menu = None
        self.TASKBAR_CONTEXT_MENU: tkinter.Menu = None
        self.CLOCK_LABEL: tkinter.Label = None
        self.CLOCK_LOOP_ID = None
        self.RUNNING_APPS: dict[str, dict[int, str]] = {}
        self.ICONS: dict[str, Image.Image] = {}
        self.THEME_WINDOW_BG: str = None
        self.THEME_FOREGROUND: str = None
        self.USERNAME: str = "defaultuser0"
        self.APPS_LIST: list[str] = []
        self.COMMAND_APPS_LIST: list[str] = []
        self.USER_CONFIG: shelve.Shelf = None
        self.PINNED_APPS_DESKTOP = []
        self.PINNED_APPS = []
        self.APP_INSTANCE = LoadedApps()
        self.THEME_WN_CLR = None
        self.TASKBAR_FRAME: tkinter.Frame = None
        self.MESSAGES = {}
        self.MESSAGES_CALLBACK = None
        self.MESSAGES_AUTODELETE = False
        self.NOTIFICATIONS = None
        self.DESKTOP_APPS_CONTEXT_MENUS: dict[str, tkinter.Menu] = {}
        self.TASKBAR_APPS_CONTEXT_MENUS: dict[str, tkinter.Menu] = {}
        self.CWD = CWD
        self.RUNAPPSLIST = [self.RUNNING_APPS_FRAME, self.RUNNING_APPS]


UNSAFE_METHODS = ["TASKBAR_FRAME", "MESSAGES", "MESSAGES_CALLBACK", "MESSAGES_AUTODELETE", "APP_INSTANCE", "TASKBAR_FRAME", "CLOCK_LABEL", "CLOCK_LOOP_ID", "DESKTOP_CONTEXT_MENU", "TASKBAR_CONTEXT_MENU", "RUNNING_APPS_FRAME", "NOTIFICATION_BUTTON", "ROOT_WINDOW", "START_MENU_ACTIVE"]

ParWFS._instances["root"].GLOBAL_VARS = PW11GlobalVars()
GLOBAL_VARS = ParWFS._instances["root"].GLOBAL_VARS
GLOBAL_VARS.RUNAPPSLIST = [GLOBAL_VARS.RUNNING_APPS_FRAME, GLOBAL_VARS.RUNNING_APPS]

""" 
SAMPLE REQUEST:
{
    "SenderPID": <PID>,
    "messageContent": {
        =-=-=-=-= FOR GET METHOD CODE =-=-=-=-=
        "method": "GET" 
        "overRideSafety": False,
        "GETATTR": <Attr from GLOBAL_VARS>,
    }
        =-=-=-=-= GET METHOD CODE END =-=-=-=-=
        =-=-=-=-= EXEC_ACTION  METHOD =-=-=-=-=
    "messageContent": {
        "method": "EXEC_ACTION",
        "LAUNCH_APP": {
            "APP_NAME": <AppName>,
            "PARAMS": <Params to launch the app with>
        },
        "CHANGE_BASE_THEME": {
            "WN_CLR": <Desired Title Bar colour>,
            "FG": <Desired Foreground>,
            "BG": <Desired Background>,
            "WRITE_CHANGES": <To whether write changes to the user config>
        },
        "CHANGE_THEME_TO_PRESET": <Desired theme preset name to change to (Filename of the preset in /<CWD>/Themes/),
        "CREATE_DESKTOP_ICON": {
            "appname": <Desired app name>,
            "command": <Desired command - string of filename of app>,
            "writeTo": <Bool - To write to FS or not>,
            "param": <Launch parameters>
        }
    }
        =-=-=-=-= ENDING EXEC_ACTIONS =-=-=-=-=
}



"""
def messageHandler(messageContent: dict):
    global GLOBAL_VARS
    replyToPID = messageContent["SenderPID"]
    messageConts = messageContent["messageContent"]
    reply = {"SenderPID": 0, "STATE": 200, "messageContent": {}}
    formReply = reply["messageContent"]
    if messageConts["method"] == "GET":
        
        if "GETATTR" in messageConts.keys():
            if "overRideSafety" in messageConts.keys():
                if messageConts["overRideSafety"]:
                    try: formReply["GETATTR"] = getattr(GLOBAL_VARS, messageConts["GETATTR"])
                    except Exception as EXP: formReply["GETATTR"] = EXP
            else:
                if messageConts["GETATTR"] in UNSAFE_METHODS: formReply["GETATTR"] = False
                else:
                    try: formReply["GETATTR"] = getattr(GLOBAL_VARS, messageConts["GETATTR"])
                    except Exception as EXP: formReply["GETATTR"] = EXP
        if "GEN_PID" in messageConts.keys():
            try: formReply["GEN_PID"] = generatePID(PIDsToGen[messageConts["GEN_PID"]])
            except Exception as EXP: formReply["GEN_PID"] = EXP
        if "GET_APP_IMPORT_NAME" in messageConts.keys():
            try: formReply["GET_APP_IMPORT_NAME"] = GUIButtonCommand.AppImportNameCheck(messageConts["GET_APP_IMPORT_NAME"])
            except Exception as EXP: formReply["GET_APP_IMPORT_NAME"] = EXP
        if "GET_ICON" in messageConts.keys():
            ROOT = GLOBAL_VARS.ROOT_WINDOW
            subsample= False
            if "root" in messageConts["GET_ICON"].keys(): ROOT = messageConts["GET_ICON"]["root"]
            if "subsample" in messageConts["GET_ICON"].keys(): subsample = messageConts["GET_ICON"]["subsample"]
            try: formReply["GET_ICON"] = ROOT.TEMP_REF = giveIcon(messageConts["GET_ICON"]["appname"], ROOT, subsample,)
            except Exception as EXP: formReply["GET_ICON"] = EXP
    # TODO POST ATTR METHOD
    if messageConts["method"] == "EXEC_ACTION":
        if "LAUNCH_APP" in messageConts.keys(): 
            try: GUIButtonCommand.launchItem(messageConts["LAUNCH_APP"]["APP_NAME"], messageConts["LAUNCH_APP"]["PARAMS"])
            except BaseException as EXP: formReply["LAUNCH_APP"] = EXP
            else: formReply["LAUNCH_APP"] = True
        if "LAUNCH_APP_EXTAPPLNCHR" in messageConts.keys():
            try: _AppLauncherForExternalApps(messageConts["LAUNCH_APP_EXTAPPLNCHR"]["APP_NAME"], messageConts["LAUNCH_APP_EXTAPPLNCHR"]["USER_CONFIG"], messageConts["LAUNCH_APP_EXTAPPLNCHR"]["PARAMS"], messageConts["LAUNCH_APP_EXTAPPLNCHR"]["USERNAME"])
            except BaseException as EXP: formReply["LAUNCH_APP_EXTAPPLNCHR"] = EXP
            else: formReply["LAUNCH_APP_EXTAPPLNCHR"] = True
        if "CHANGE_BASE_THEME" in messageConts.keys(): 
            try: setTheme(messageConts["CHANGE_BASE_THEME"]["WN_CLR"], messageConts["CHANGE_BASE_THEME"]["FG"], messageConts["CHANGE_BASE_THEME"]["BG"], messageConts["CHANGE_BASE_THEME"]["WRITE_CHANGES"])
            except BaseException as EXP: formReply["CHANGE_BASE_THEME"] = EXP
            else: formReply["CHANGE_BASE_THEME"] = True
        if "CHANGE_THEME_TO_PRESET" in messageConts.keys(): 
            try: setPresetTheme(messageConts["CHANGE_THEME_TO_PRESET"])
            except BaseException as EXP: formReply["CHANGE_THEME_TO_PRESET"] = EXP
            else: formReply["CHANGE_THEME_TO_PRESET"] = True
        if "CREATE_DESKTOP_ICON" in messageConts.keys():
            try: AppIconManager.createDesktopAppIcon(messageConts["CREATE_DESKTOP_ICON"]["appname"], messageConts["CREATE_DESKTOP_ICON"]["command"], messageConts["CREATE_DESKTOP_ICON"]["writeTo"], messageConts["CREATE_DESKTOP_ICON"]["param"])
            except BaseException as EXP: formReply["CREATE_DESKTOP_ICON"] = EXP
            else: formReply["CREATE_DESKTOP_ICON"] = True
        if "ADD_RUNNING_APP" in messageConts.keys():
            try: GLOBAL_VARS.RUNNING_APPS[GLOBAL_VARS.USERNAME][messageConts["ADD_RUNNING_APP"]["PID"]] = messageConts["ADD_RUNNING_APP"]["appname"]
            except BaseException as EXP: formReply["ADD_RUNNING_APP"] = EXP
            else: formReply["ADD_RUNNING_APP"] = True
        if "ACK_ENDTASK" in messageConts.keys():
            try: GUIButtonCommand.handleExits(messageConts["ACK_ENDTASK"], [GLOBAL_VARS.RUNNING_APPS_FRAME, GLOBAL_VARS.RUNNING_APPS])
            except BaseException as EXP: formReply["ACK_ENDTASK"] = EXP
            else: formReply = True
        if "END_TASK" in messageConts.keys():
            try: TaskManager.endTask(messageConts["END_TASK"])
            except BaseException as EXP: formReply["END_TASK"] = EXP
            else: formReply["END_TASK"] = True

    if (not (replyToPID in GLOBAL_VARS.SPECIAL_PIDS)): callHost._sendCallToPID(0, replyToPID, formReply)    
GLOBAL_VARS.MESSAGES_CALLBACK = messageHandler
def getUsername(): return GLOBAL_VARS.USERNAME
def createUserAccount(username: str, password: str, userNumber: int, overwriteConfigs=True, THEME=["Black", "White", "Black"]):
    LOGGER.addTextLog(f"User creation process called for: {username} with usernumber {userNumber}")
    try: 
        try: 
            os.mkdir(f"Users")
            os.mkdir(f"Users/{username}")
        except: 
            try: os.mkdir(f"Users/{username}")
            except: pass
        for i in USER_FOLDERS_LIST: os.mkdir(f"Users/{username}/{i}")
    except Exception: print("User folders already exist, skipping...")
    try:
        with open(f"Users/accConfiguration{userNumber}.conf", "wb") as WRITE:
            Rusername= base64.urlsafe_b64encode(username.encode("utf-8"))
            Rpassword = base64.urlsafe_b64encode(password.encode("utf-8"))
            WRITE.writelines([Rusername, "\n".encode("utf-8"),  Rpassword])
        #os.mkdir(f"ProgramFiles/{username}")
    except Exception: print("User already exists, skipping user creation tasks...")
    finally: 
        FILE_SYSTEM.loadConfig(f"Users/{username}/USER_CONFIG", "NEW_USER_CONFIG")
    if not overwriteConfigs: return True
    FILE_SYSTEM.editConfig("NEW_USER_CONFIG", "APPS", [["Command Prompt", "Load External Apps", "Notepad", "Web Browser", "Update Manager", "IP Chat", "File Manager", "Software Store", "File Share", "Black Jack", "Alarms and Timer", "Photo Viewer", "Control Panel", "Task Manager", "Shelve Editor"], ["ProgramFiles.alarmsandtimer", "ProgramFiles.blackjack", "ProgramFiles.commandprompt", "ProgramFiles.loadexternalapps", "ProgramFiles.ipchat", "ProgramFiles.notepad", "ProgramFiles.webbrowser", "ProgramFiles.updatemanager", "ProgramFiles.fileshare", "ProgramFiles.filemanager", "ProgramFiles.softwarestore", "ProgramFiles.photoviewer", "ProgramFiles.controlPanel", "ProgramFiles.taskManager", "ProgramFiles.shelveeditor"]])
    FILE_SYSTEM.editConfig("NEW_USER_CONFIG", "PINNED", [["File Manager"], [["Notepad", None], ["File Manager", None]]])
    FILE_SYSTEM.editConfig("NEW_USER_CONFIG", "THEME", THEME)
    FILE_SYSTEM.editConfig("NEW_USER_CONFIG", "THEME_WN_BORDERS", {"START_MENU_HG_CLR": "Black", "START_MENU_HGBG": "Black", "DWM_HG_CLR": "Black", "DWM_HGBG": "Black"})
    FILE_SYSTEM.editConfig("NEW_USER_CONFIG", "CLOCK-WIDGET", 0)
    FILE_SYSTEM.editConfig("NEW_USER_CONFIG", "DEFAULTAPPASSOCIATION", {"txt": "Notepad", "jpg": "Photo Viewer", "png": "Photo Viewer", "dat": "Shelve Editor"})
    FILE_SYSTEM.editConfig("NEW_USER_CONFIG", "WALLPAPER", None)
    FILE_SYSTEM.editConfig("NEW_USER_CONFIG", "STARTUP_APPS", [])
    FILE_SYSTEM.editConfig("NEW_USER_CONFIG", "PFP", os.path.join(CWD, "ProgramFiles/Icons/defaultpfp.png"))
    FILE_SYSTEM.editConfig("SYS_CONFIG", "UPDATE_BRANCH", "main")
    FILE_SYSTEM.editConfig("SYS_CONFIG", "THEME", ["Black", "White"]) 
    FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)
    FILE_SYSTEM.editConfig("SYS_CONFIG", "SETUP_IN_PROGRESS", 0)
    FILE_SYSTEM.editConfig("SYS_CONFIG", "FS_STOP_PREMATURE", False)
    FILE_SYSTEM.editConfig("SYS_CONFIG", "PYTHON_LAUNCH_COMMAND", "python3")
    FILE_SYSTEM.editConfig("SYS_CONFIG", "VERSION", "2.3.9")
    FILE_SYSTEM.editConfig("SYS_CONFIG", "UPDATE_TIME_LOG", [])
    LOGGER.addTextLog(f"User creation process finished for {username} with usernumber {userNumber}")
    return True
try:
    GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND = SYS_CONFIG["THEME"]
    GLOBAL_VARS.THEME_WN_CLR = GLOBAL_VARS.THEME_WINDOW_BG
except Exception as EXP:
    LOGGER.addRawLog(EXP, [SYS_CONFIG], "Unable to load theme")
    GLOBAL_VARS.THEME_WINDOW_BG = "Black"
    GLOBAL_VARS.THEME_FOREGROUND = "White"
    GLOBAL_VARS.THEME_WN_CLR = "Black"

GLOBAL_VARS.RUNNING_APPS =  FILE_SYSTEM.RUNNING_APPS
ICONS = GLOBAL_VARS.ICONS
PROCESS_IDS = (1000, 5000)
EXTERNAL_PID = (5000, 9999)
MESSAGEBOX_IDS = (1, 200)
PROGRESSBAR_IDS = (200, 400)
FILEASK_WINDOWS = (400, 600)
TASK_MANAGERS = (600, 650)
CONTROL_PANELS = (650, 700)
DIALOGUE_BOXES = (700, 850)

PIDsToGen = {
    "PROCESS_IDS": PROCESS_IDS,
    "MSGBOX_IDS": MESSAGEBOX_IDS, 
    "PROGRESSBAR_IDS": PROGRESSBAR_IDS,
    "FILEASK_IDS": FILEASK_WINDOWS,
    "DIALOGUE_IDS": DIALOGUE_BOXES,
    "EXTERNAL_IDS": EXTERNAL_PID
}

def generatePID(LIB_TO_USE: tuple[int, int]):
    PID = random.randint(LIB_TO_USE[0], LIB_TO_USE[1])
    for key in dict(GLOBAL_VARS.RUNNING_APPS).keys():
        while PID in dict(dict(GLOBAL_VARS.RUNNING_APPS)[key]).keys():
            PID = random.randint(LIB_TO_USE[0], LIB_TO_USE[1])
    return PID

def returnRunningApps():
    return FILE_SYSTEM.RUNNING_APPS
def giveIcon(appName: str, root, subsample=False, relaunch=False,):
    try:
        if not subsample: return ImageTk.PhotoImage(GLOBAL_VARS.ICONS[appName], master=root)
        else:
            root.ERM = IMAGE = None
            if isinstance(subsample, (tuple, list)): IMAGE = GLOBAL_VARS.ICONS[appName].resize([GLOBAL_VARS.ICONS[appName].size[0]//subsample[0], GLOBAL_VARS.ICONS[appName].size[1]//subsample[1]],)
            else: IMAGE =  GLOBAL_VARS.ICONS[appName].resize([GLOBAL_VARS.ICONS[appName].size[0]//subsample, GLOBAL_VARS.ICONS[appName].size[1]//subsample],)
            return ImageTk.PhotoImage(IMAGE, master=root)

    except Exception as exp:
        LOGGER.addRawLog(exp, [appName, GLOBAL_VARS.ICONS], "Wasn't able to load icon from stored GLOBAL_VARS.ICONS, giving icon manually")
        try:
            if not subsample: return tkinter.PhotoImage(file=f"ProgramFiles/Icons/{appName}.png", master=root)
            else: return tkinter.PhotoImage(file=f"ProgramFiles/Icons/{appName}.png", master=root).subsample(subsample)
        except Exception as EXP:
            LOGGER.addRawLog(EXP, [appName, tkinter.PhotoImage], "Unable to load icon, giving error icon!") 
            if not relaunch: return giveIcon("error", root, subsample, True)

def loadAllIcons(appsList: list, root):
    for app in appsList:
        realApp = GUIButtonCommand.AppImportNameCheck(app)
        try:
            #GLOBAL_VARS.ICONS[realApp] = tkinter.PhotoImage(file=f"ProgramFiles/Icons/{realApp}.png", master=root)
            GLOBAL_VARS.ICONS[realApp] = Image.open(f"ProgramFiles/Icons/{realApp}.png")
            root.erm = GLOBAL_VARS.ICONS[realApp]
        except Exception as EXP: LOGGER.addRawLog(EXP, [GLOBAL_VARS.ICONS, realApp], "Unable to load icon for app from loadAllIcons")

def setBorderTheme(START_MENU_BORDER_ACTIVE, START_MENU_BORDER_INACTIVE, DWM_WINDOW_BORDER_ACTIVE, DWM_WINDOW_BORDER_INACTIVE ):
    global GLOBAL_VARS
    """
    Changes the borders of various shi
    
    :param START_MENU_BORDER_ACTIVE: Colour of the border when the Start Menu is in focus
    :param START_MENU_BORDER_INACTIVE: Colour of the border when the Start Menu is NOT in focus
    :param DWM_WINDOW_BORDER_ACTIVE: Colour of the border when a DWM-Enabled window is in focus
    :param DWM_WINDOW_BORDER_INACTIVE: Colour of the border when a DWM-Enabled window is NOT in focus
    """
    FILE_SYSTEM.editConfig("USER_CONFIG", "THEME_WN_BORDERS", {"START_MENU_HG_CLR": START_MENU_BORDER_ACTIVE, "START_MENU_HGBG": START_MENU_BORDER_INACTIVE, "DWM_HG_CLR": DWM_WINDOW_BORDER_ACTIVE, "DWM_HGBG": DWM_WINDOW_BORDER_INACTIVE})
    GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.getConfig("USER_CONFIG")

def setTheme(WN_CLR=None, T_FG=None, T_BG=None, writeToFS=True, WIDGETS_TO_UPDATE=None):
    global GLOBAL_VARS
    """
    Sets theme to the shell from given variables, with an option to save the set theme or not (Basically persistence upon reboot)
    Only basic three, NOT the borders and stuff. Ya gotta use another method for that, the `setBorderTheme` function

    :param WN_CLR: Window colour
    :param T_FG: Foreground (Txt Colour)
    :param T_BG: Background
    :param writeToFS: Option to write changes to the FS
    """
    if not WN_CLR: WN_CLR = GLOBAL_VARS.THEME_WN_CLR
    if not T_FG: T_FG = GLOBAL_VARS.THEME_FOREGROUND
    if not T_BG: T_BG = GLOBAL_VARS.THEME_WINDOW_BG
    if not WIDGETS_TO_UPDATE: WIDGETS_TO_UPDATE = [GLOBAL_VARS.ROOT_WINDOW, GLOBAL_VARS.TASKBAR_FRAME]
    GLOBAL_VARS.THEME_WINDOW_BG = T_BG
    GLOBAL_VARS.THEME_FOREGROUND = T_FG
    GLOBAL_VARS.THEME_WN_CLR = WN_CLR
    dwm.changeThemeForAllApps(GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WN_CLR)
    for widgets in WIDGETS_TO_UPDATE:
        dwm._changeThemeForAllApps(GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND, widgets)
    if writeToFS:
        FILE_SYSTEM.editConfig("USER_CONFIG", "THEME", [WN_CLR, T_FG, T_BG])
        GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.getConfig("USER_CONFIG")


def setPresetTheme(themeName):
    global GLOBAL_VARS
    """
    Sets a preset theme to the shell, reading from "<CWD>/Themes/<themeName>"
    
    :param themeName: File name of the preset theme (Usually DARK_THEME/LIGHT_THEME)
    """
    with shelve.open(os.path.join(CWD, "Themes", themeName)) as reader:
        
        setTheme(reader["WINDOW_TITLE_COLOUR"], reader["FOREGROUND"], reader["BACKGROUND"], True)
        setBorderTheme(reader["START_MENU_BORDER_ACTIVE"], reader["START_MENU_BORDER_INACTIVE"], reader["DWM_WINDOW_BORDER_ACTIVE"], reader["DWM_WINDOW_BORDER_INACTIVE"])
        GLOBAL_VARS.THEME_WINDOW_BG = reader["BACKGROUND"]
        GLOBAL_VARS.THEME_FOREGROUND = reader["FOREGROUND"]
        GLOBAL_VARS.THEME_WN_CLR = reader["WINDOW_TITLE_COLOUR"]
        dwm._changeThemeForAllApps(GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.ROOT_WINDOW)
        dwm.changeThemeForAllApps(GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WN_CLR)
        dwm._changeThemeForAllApps(GLOBAL_VARS.THEME_WN_CLR, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.TASKBAR_FRAME)



class settings():
    def __init__(self, root: tkinter.Tk = GLOBAL_VARS.ROOT_WINDOW, openOnPage=None):
        self.SHOWN_HOMEPAGE = False
        self.SHOWN_PERSONALIZATION = False
        self.SHOWN_ADVANCED = False
        self.SHOWN_APPSLIST = False
        self.SHOWN_APPOPENERCHANGER = False
        self.ROOT = root
        self.total_memory = str(f"{psutil.virtual_memory().total/1000000000} GigaBytes")
        self.settingsWindow = tkinter.Toplevel(self.ROOT, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.PID = generatePID(CONTROL_PANELS)
        GLOBAL_VARS.RUNNING_APPS[GLOBAL_VARS.USERNAME][self.PID] = "Control Panel"
        dwm.createTopFrame(self.settingsWindow, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WN_CLR, "settings", "Control Panel", self.PID)
        AppIconManager.createRunningAppTaskbarIcon("settings", self.PID, username=GLOBAL_VARS.USERNAME)
        btnFrame = tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        btnFrame.grid(row=1, column=0)
        sidebar = SidebarButtons(btnFrame, GLOBAL_VARS.THEME_WINDOW_BG)
        homeBtn = sidebar.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Home", command=self.homePage, ID="home")
        homeBtn.grid(row=0, column=0)
        personalizeBtn = sidebar.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Personalization", command=self.personalization, ID="personalization")
        personalizeBtn.grid(row=1, column=0)
        appOpenerChangeBtn = sidebar.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="App Associations", command=self.changeFileOpeners, ID="appassociations")
        appOpenerChangeBtn.grid(row=2, column=0)
        startupApps = sidebar.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Startup Apps", command=self.addStartupApps, ID="startupapps")
        startupApps.grid(row=3, column=0)
        userManagementBtn = sidebar.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Users", command=self.addUserAccounts, ID="users")
        userManagementBtn.grid(row=4, column=0)
        taskbarSettingsBtn = sidebar.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Taskbar Settings", command=self.taskbarSettings, ID="taskbarsettings")
        taskbarSettingsBtn.grid(row=5, column=0)
        desktopSettingsBtn = sidebar.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Desktop Settings", command=self.desktopSettings, ID="desktopsettings")
        desktopSettingsBtn.grid(row=6, column=0)
        self.setting = tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        if openOnPage != None: sidebar.commandWrapper(openOnPage)
        else: self.homePage()
    def homePage(self):
        self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        self.SHOWN_HOMEPAGE = True
        infoText = f""" Windows 11 v2.3.5\nSystem RAM: {self.total_memory}\nBackground={GLOBAL_VARS.THEME_WINDOW_BG}\n"""
        f"""Foreground={GLOBAL_VARS.THEME_FOREGROUND}\n\nFor more info, please visit the respective categories! Thank you :)"""
        a = tkinter.Label(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=infoText).grid(row=0, column=0)
    def desktopSettings(self):
        self.setting.destroy()
        self.setting = tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        INDEX=0
        iconToAdd = None
        desktopAppsList = ttk.Combobox(self.setting)
        # for z in self.CurrentDesktopIconsList:
        #     CURRENT_LIST = GLOBAL_VARS.APPS_LIST
        #     try:
        #         CURRENT_LIST = CURRENT_LIST.pop(GLOBAL_VARS.APPS_LIST.index(z))
        #     except Exception as problem:
        #         pass
        CURRENT_LIST = list(GLOBAL_VARS.APPS_LIST)
        for app in GLOBAL_VARS.APPS_LIST:
            if app in GLOBAL_VARS.PINNED_APPS_DESKTOP:
                try: CURRENT_LIST.pop(CURRENT_LIST.index(app))
                except Exception: pass
        desktopAppsList['values'] = CURRENT_LIST
        def _cmd():
            if paramType.get() == "None" or paramType.get() == "":  AppIconManager.createDesktopAppIcon(iconToAdd, f"{iconToAdd}", param=None)
            else:
                func = eval(paramType.get())
                try: prm = (eval(param.get()))
                except: prm = param.get()
                AppIconManager.createDesktopAppIcon(iconToAdd, f"{iconToAdd}", param=func(prm))
        def updateVariable(event=None):
            nonlocal iconToAdd
            nonlocal INDEX
            iconToAdd = str(desktopAppsList.get())
        desktopAppsList.bind("<<ComboboxSelected>>", updateVariable)
        desktopAppsList['state'] = "readonly"
        desktopAppsList.grid(row=1, column=0, sticky="w")
        tkinter.Label(self.setting, text="Launch Parameters: ", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=2, column=0)
        addIconBtn = tkinter.Button(self.setting, text="Add Icon!", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=_cmd)
        addIconBtn.grid(row=1, column=1) 
        tkinter.Label(self.setting, text="Type of parameter (int/str)", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=3, column=0)
        tkinter.Label(self.setting, text="parameter", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=3, column=1)
        paramType = entryWidget.Entry(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        paramType.grid(row=4, column=0)
        param = entryWidget.Entry(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        param.grid(row=4, column=1)
    def taskbarSettings(self):
        self.setting.destroy()
        self.setting = tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        addWidgetsFrame = tkinter.LabelFrame(self.setting, text="Add widgets", 
                                            background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        addWidgetsFrame.grid(row=1, column=0)
        addClock = tkinter.Button(addWidgetsFrame, text="Clock", foreground=GLOBAL_VARS.THEME_FOREGROUND,
                                    background=GLOBAL_VARS.THEME_WINDOW_BG, command=GUIButtonCommand.currentTime)
        addClock.grid(row=1, column=0)
        pinItems = tkinter.LabelFrame(self.setting, text="Pin items",
                                        background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        pinItems.grid(row=2, column=0)
        PINNED_APPS = list(GLOBAL_VARS.PINNED_APPS)
        NOT_PINNED_APPS = []
        for app in GLOBAL_VARS.APPS_LIST:
            if app not in PINNED_APPS: NOT_PINNED_APPS.append(app)
        combobox = ttk.Combobox(pinItems, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, values=NOT_PINNED_APPS, state='readonly')
        combobox.grid(row=1, column=0)
        combobox.bind("<<ComboboxSelected>>", lambda e: AppIconManager.pinTaskbarApp(GUIButtonCommand.AppImportNameCheck(combobox.get())) )
        
    
    def personalization(self):
        self.SHOWN_PERSONALIZATION = True
        def changeThemeAspect(aspect: str):
            global SYS_CONFIG
            from ProgramFiles import colorchooser
            colorToUse = colorchooser.askcolor(title=f"Select {aspect} colour!", HostPID=self.PID)[1]
            if colorToUse == None: return
            labelToChange = globalVarChange = None
            if aspect == "background": labelToChange, GLOBAL_VARS.THEME_WINDOW_BG = crBg, colorToUse; globalVarChange = GLOBAL_VARS.THEME_WINDOW_BG; setTheme(T_BG=GLOBAL_VARS.THEME_WINDOW_BG)
            elif aspect == "foreground": labelToChange, GLOBAL_VARS.THEME_FOREGROUND = crFg, colorToUse; globalVarChange = GLOBAL_VARS.THEME_FOREGROUND; setTheme(T_FG=GLOBAL_VARS.THEME_FOREGROUND)
            elif aspect == "window colour": labelToChange, GLOBAL_VARS.THEME_WN_CLR = crWnClr, colorToUse; globalVarChange = GLOBAL_VARS.THEME_WN_CLR; setTheme(WN_CLR=GLOBAL_VARS.THEME_WN_CLR)
            labelToChange.configure(text=f"Current {aspect} = {globalVarChange}")
            if systemChangeTheme.get(): SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "THEME", [GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND])
            GLOBAL_VARS.ROOT_WINDOW.update()
        def changeWallpaper():
            from ProgramFiles.fileaskhandlers import askopenfilename
            nonlocal wallpaperText
            wallpaperChoose = askopenfilename("Open a wallpaper file (png)", (("PNG Files", "*.png"), ("All Files", "*.*")))
            img = GUIButtonCommand.getWallpaperImageResized(wallpaperChoose)
            GLOBAL_VARS.ROOT_WINDOW.image = img
            try:GLOBAL_VARS.WALLPAPER.configure(image=img)
            except: 
                GLOBAL_VARS.WALLPAPER = tkinter.Label(GLOBAL_VARS.ROOT_WINDOW, image=img)
                GLOBAL_VARS.WALLPAPER.grid(row=1, column=0, sticky="EWSN")
            GLOBAL_VARS.DESKTOP_FRAME.lift()
            wallpaperText = "Current Wallpaper: " + wallpaperChoose
            wallpaperPath.configure(text=wallpaperText)
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "WALLPAPER", wallpaperChoose)
        def removeWallpaper():
            nonlocal wallpaperText
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "WALLPAPER", None)
            try: GLOBAL_VARS.WALLPAPER.destroy()
            except: pass
            wallpaperText = "Current Wallpaper: No wallpapers set yet!"
            wallpaperPath.configure(text=wallpaperText)
        def usePresetThemes():
            wn = tkinter.Toplevel(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
            dwm.createTopFrame(wn, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WN_CLR, "settings", "Preset Themes", generatePID(DIALOGUE_BOXES), associatePIDProcess=self.PID)
            themesFrame = tkinter.Frame(wn, background=GLOBAL_VARS.THEME_WINDOW_BG)
            themesFrame.grid(row=1, column=0)
            details = tkinter.Frame(wn, background=GLOBAL_VARS.THEME_WINDOW_BG)
            details.grid(row=1, column=1)
            sidebar = SidebarButtons(themesFrame, GLOBAL_VARS.THEME_WINDOW_BG)
            def useSelectedPreset(themeName: str): setPresetTheme(themeName)
            useThemeBtn = tkinter.Button(wn, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Use Selected Preset!", justify="center", command=lambda: useSelectedPreset(sidebar.currentSelection))
            useThemeBtn.grid(row=2, column=1, sticky="NEWS")
            def currentSelectionChange(themeName):
                for child in details.winfo_children(): child.destroy()
                with shelve.open(os.path.join(CWD, "Themes", themeName)) as reader:
                    for x, keys in enumerate(dict(reader).keys()):
                        txtLbl = tkinter.Label(details, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=keys.replace("_", " ").title())
                        txtLbl.grid(row=x, column=0, sticky='W')
                        colourLbl = tkinter.Label(details, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=reader[keys])
                        colourLbl.grid(row=x, column=1, sticky='W')
                        previewFrame = tkinter.Frame(details, background=reader[keys], width=100, height=10)
                        previewFrame.grid(row=x, column=2)
                    
            for i, themes in enumerate(os.listdir(os.path.join(CWD, "Themes"))):
                button = sidebar.Button(themesFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=themes.replace("_", " ").title(), command=lambda theme=themes: currentSelectionChange(theme), ID=themes)
                button.grid(row=i, column=0)
            wn.mainloop()
        self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        crBg = tkinter.Label(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=f"Current Background = {GLOBAL_VARS.THEME_WINDOW_BG}")
        crBg.grid(row=0, column=0)
        changeBackground = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Change Background!", command=lambda: changeThemeAspect("background"))
        changeBackground.grid(row=0, column=1)
        crFg = tkinter.Label(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=f"Current foreground = {GLOBAL_VARS.THEME_FOREGROUND}")
        crFg.grid(row=1, column=0)
        changeForeground = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Change foreground!", command=lambda: changeThemeAspect("foreground"))
        changeForeground.grid(row=1, column=1)
        crWnClr = tkinter.Label(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=f"Current Window Title BG = {GLOBAL_VARS.THEME_WN_CLR}")
        crWnClr.grid(row=2, column=0)
        changeWindowColour = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Change Window Title BG!", command=lambda: changeThemeAspect("window colour"))
        changeWindowColour.grid(row=2, column=1)
        ttk.Style(self.settingsWindow).configure("TCheckbutton", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        systemChangeTheme = tkinter.IntVar()
        applyToSystem = ttk.Checkbutton(self.setting, text="Also apply changes to system theme!", variable=systemChangeTheme)
        applyToSystem.grid(row=3, column=0)
        usePrThemesBtn = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Use Preset Themes!", command=usePresetThemes, justify="center")
        usePrThemesBtn.grid(row=4, column=0, columnspan=2)
        wallpaperText = "Current Wallpaper: "
        if GLOBAL_VARS.USER_CONFIG["WALLPAPER"]: wallpaperText += GLOBAL_VARS.USER_CONFIG["WALLPAPER"]
        else: wallpaperText += "No wallpapers set yet!"
        wallpaperPath = tkinter.Label(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=wallpaperText)
        wallpaperPath.grid(row=5, column=0)
        changeWallpaperButton = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Change Wallpaper", command=changeWallpaper)
        changeWallpaperButton.grid(row=5, column=1)
        removeWallpaperButton = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Remove Wallpaper", command=removeWallpaper)
        removeWallpaperButton.grid(row=6, column=1)
    def changeFileOpeners(self, reLaunch=False):
        def __internals_AddNewEntry(*args):
            def __internals_AddNewEntry_AddAppNames(*args):
                
                app = comboBox.get()
                try: 
                    extension = textAssociationEntry.get()
                    CurrentConfig: dict = GLOBAL_VARS.USER_CONFIG["DEFAULTAPPASSOCIATION"]
                    CurrentConfig.update({extension: app})
                    GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "DEFAULTAPPASSOCIATION", CurrentConfig)
                    self.changeFileOpeners(True)
                except Exception as I:
                    LOGGER.addRawLog(I, [GLOBAL_VARS.USER_CONFIG, CurrentConfig, extension, app], "Error in adding new default app associations")
                    messagebox.showerror('Error creating default app association', f'Error creating default app association.\nProb: {I}', addNewEntryWn, MainPID=PID )
            addNewEntryWn = tkinter.Toplevel(self.settingsWindow)
            PID = generatePID(DIALOGUE_BOXES)
            dwm.createTopFrame(addNewEntryWn, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WN_CLR, "settings", "Add new app association wizard", PID , associatePIDProcess=self.PID)
            GLOBAL_VARS.RUNNING_APPS[GLOBAL_VARS.USERNAME][PID] = "Control Panel - New App Association Wizard"
            nEntFrm = tkinter.Frame(addNewEntryWn, background=GLOBAL_VARS.THEME_WINDOW_BG)
            nEntFrm.grid(row=1, column=0)
            textAssociationEntry = tkinter.Entry(nEntFrm, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
            textAssociationEntry.grid(row=0, column=0)
            comboBox = ttk.Combobox(nEntFrm)
            comboBox['values'] = GLOBAL_VARS.APPS_LIST
            comboBox['state'] = "readonly"
            comboBox.bind("<<ComboboxSelected>>", __internals_AddNewEntry_AddAppNames)
            comboBox.grid(row=0, column=1)
            addNewEntryWn.mainloop()
        self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        addEntryBtn = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Add New Entry", command=__internals_AddNewEntry)
        addEntryBtn.grid(row=0, column=0)
        for X, i in enumerate(dict(GLOBAL_VARS.USER_CONFIG["DEFAULTAPPASSOCIATION"]).keys()):
            innerFrame = tkinter.Frame(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG)
            innerFrame.grid(row=X+1, column=0)
            label = tkinter.Label(innerFrame, text=i, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, )
            label.grid(row=0, column=0)
            def changeDefAppEvent(app, e=None):
                nonlocal comboBox
                app = comboBox.get()
                try: 
                    CurrentConfig: dict = GLOBAL_VARS.USER_CONFIG["DEFAULTAPPASSOCIATION"]
                    CurrentConfig.update({i: app})
                    GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "DEFAULTAPPASSOCIATION", CurrentConfig)
                except Exception as I:
                    LOGGER.addRawLog(I, [GLOBAL_VARS.USER_CONFIG, CurrentConfig, i, app], "Error changing default app association")
                    messagebox.showerror('Error changing default app association', f'Error changing default app association.\n{I}', self.settingsWindow, MainPID=self.PID )
            comboBox = ttk.Combobox(innerFrame, values=GLOBAL_VARS.APPS_LIST, state='readonly', background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
            comboBox.bind("<<ComboboxSelected>>", lambda e=None: changeDefAppEvent(comboBox.get()))
            comboBox.grid(row=0, column=1)
    def addStartupApps(self):
        def _addApp(*args):
            appToAdd = combobox.get()
            startupApps.append(appToAdd)
            FILE_SYSTEM.editConfig("USER_CONFIG", "STARTUP_APPS", startupApps)
            self.addStartupApps()
        def _removeApp(*args):
            appToRemove= rmcombobox.get()
            startupApps.remove(appToRemove)
            FILE_SYSTEM.editConfig("USER_CONFIG", "STARTUP_APPS", startupApps)
            self.addStartupApps()
        self.setting.destroy()
        self.setting = tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG,)
        self.setting.grid(row=1, column=1)
        tkinter.Label(self.setting, text="Current startup apps:", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=0, column=0)
        startupApps = FILE_SYSTEM.getConfig("USER_CONFIG")["STARTUP_APPS"]
        startupApps = list(startupApps)
        apps = []
        for app in GLOBAL_VARS.APPS_LIST: 
            if app not in startupApps: apps.append(app)
        if len(startupApps) == 0: tkinter.Label(self.setting, text="No startup apps!", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=1, column=0)
        else:
            for index, startupapp in enumerate(startupApps):
                tkinter.Label(self.setting, text=startupapp, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=index+1, column=0)
        tkinter.Label(self.setting, text="Add startup apps!", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=0, column=1)
        combobox = ttk.Combobox(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, values=apps, state="readonly")
        combobox.grid(row=0, column=2)
        combobox.bind("<<ComboboxSelected>>", _addApp)
        tkinter.Label(self.setting, text="Remove startup apps!", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=1, column=1)
        rmcombobox = ttk.Combobox(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, values=startupApps, state="readonly")
        rmcombobox.grid(row=1, column=2)
        rmcombobox.bind("<<ComboboxSelected>>", _removeApp)
    def addUserAccounts(self):
        self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        PW11UserCreation(self.setting, self.addUserAccounts)

class AppIconManager:
    """ pinning of apps to taskbar / desktop and creating running taskbar icons"""
    @staticmethod
    def refreshDesktop():
        try:GLOBAL_VARS.ROOT_WINDOW.REF_LBL.destroy()
        except: pass
        GLOBAL_VARS.ROW_COUNT_DESKTOP_ICONS= 0
        GLOBAL_VARS.COLUMN_COUNT_DESKTOP_ICONS= 0
        for frame in dict(GLOBAL_VARS.DESKTOP_FRAME.children).values():
            frame.destroy()
        for button in dict(GLOBAL_VARS.APPS_FRAME.children).values():
            if not isinstance(button, tkinter.Button): continue
            button.destroy()
        for app, param in GLOBAL_VARS.PINNED_APPS_DESKTOP:
            try: AppIconManager.createDesktopAppIcon(f"{app}", f"{app}", False, param)
            except Exception as EXP:  messagebox.showerror("Error pinning app to desktop", f"{app} Cannot be pinned due to the following technical reason: \n {EXP}", root=GLOBAL_VARS.ROOT_WINDOW)
        for app in GLOBAL_VARS.PINNED_APPS:
            try: AppIconManager.pinTaskbarApp(f"{app}",False)
            except Exception as EXP: LOGGER.addRawLog(EXP, [app], "Error pinning app to taskbar"); messagebox.showerror("Error pinning app to taskbar", f"{app} Cannot be pinned due to the following technical reason: \n {EXP}", root=GLOBAL_VARS.ROOT_WINDOW)
        if GLOBAL_VARS.WALLPAPER != None and GLOBAL_VARS.WALLPAPER.cget("image") != None:
            rawImage = ImageTk.getimage(GLOBAL_VARS.WALLPAPER.BASE_IMAGE)
            GLOBAL_VARS.ROOT_WINDOW.REF_WALLPAPERCROP = rawImage
            GLOBAL_VARS.DESKTOP_FRAME.update()
            GLOBAL_VARS.DESKTOP_FRAME.update_idletasks()
            GLOBAL_VARS.TASKBAR_FRAME.update()
            GLOBAL_VARS.TASKBAR_FRAME.update_idletasks()
            x, y = GLOBAL_VARS.DESKTOP_FRAME.winfo_rootx(), GLOBAL_VARS.DESKTOP_FRAME.winfo_rooty()
            h, w = GLOBAL_VARS.DESKTOP_FRAME.winfo_height(), GLOBAL_VARS.DESKTOP_FRAME.winfo_width()
            newImg = ImageTk.PhotoImage(rawImage.crop((x,y,x+w, y+h)))
            GLOBAL_VARS.ROOT_WINDOW.REF_WALLPAPER = newImg
            GLOBAL_VARS.ROOT_WINDOW.REF_LBL = tkinter.Label(GLOBAL_VARS.DESKTOP_FRAME, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, image=newImg)
            GLOBAL_VARS.ROOT_WINDOW.REF_LBL.place(x=-15, y=-15)
            GLOBAL_VARS.ROOT_WINDOW.REF_LBL.ref = newImg
            for frame in GLOBAL_VARS.DESKTOP_FRAME.winfo_children():
                if isinstance(frame, tkinter.Frame): frame.lift(); GLOBAL_VARS.DESKTOP_FRAME.lift()

    @staticmethod
    def createRunningAppTaskbarIcon(app: str, PID:int, T_BG=None, T_FG=None, username="defaultuser0"):
        ROOT = GLOBAL_VARS.ROOT_WINDOW
        if T_BG and T_FG: 
            THEME_WBG = T_BG
            THEME_FG = T_FG
        else: THEME_WBG, THEME_FG = GLOBAL_VARS.THEME_WN_CLR, GLOBAL_VARS.THEME_FOREGROUND
        POS = len(list(dict(ParWFS._instances["root"].RUNNING_APPS[username]).keys()))
        realApp = GUIButtonCommand.AppImportNameCheck(app=app)
        appIcon = giveIcon(realApp, ROOT, 2)
        taskbarAppBtn = tkinter.Button(ParWFS._instances["root"].RunAppsFrame, text=app, background=THEME_WBG, foreground=THEME_FG, command=lambda e=realApp: GUIButtonCommand.FOCUS_focusApp(PID, realApp) , image=appIcon, compound='left')
        taskbarAppBtn.grid(row=0, column=POS)
        taskbarAppBtn.processInfo = (PID, app)
        taskbarAppBtn.windowInfo = 'focusIn'
        taskbarAppBtn.ICON = appIcon
        taskbarAppBtn.RETRIES = 0
        taskbarAppBtn.bind("<Enter>", lambda E: GUIButtonCommand.FOCUS_scrShotPreview(PID, realApp, E))
        taskbarAppBtn.bind("<Leave>", lambda E: tooltips.deleteToolTip(PID, ROOT))
    @staticmethod
    def pinTaskbarApp(appToPin, writeto=True):
        appName: str = appToPin
        appName = GUIButtonCommand.AppImportNameCheck(appToPin)
        if writeto:
            apList = GLOBAL_VARS.USER_CONFIG["PINNED"]
            apList[0].append(appName)
            GLOBAL_VARS.PINNED_APPS.append(appName)
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", apList)
        appIcon = giveIcon(appName, GLOBAL_VARS.ROOT_WINDOW, 2)
        appBtn = tkinter.Button(GLOBAL_VARS.APPS_FRAME, image=appIcon, background=GLOBAL_VARS.THEME_WN_CLR, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=lambda: GUIButtonCommand.launchItem(appToPin), anchor="w", justify="left")
        appBtn.imgRef = appIcon
        appBtn.APPNAME = appName
        appBtn.identifier = "taskbarappbtn"
        appBtn.grid(row=0, column=GLOBAL_VARS.PINNED_APPS.index(appToPin), sticky="NSW")
        perAppCM = tkinter.Menu(GLOBAL_VARS.APPS_FRAME, tearoff=False, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        perAppCM.add_command(label="Open", command=lambda: GUIButtonCommand.launchItem(appName))
        perAppCM.add_command(label="Remove Icon", command=lambda: AppIconManager.removeTaskbarAppIcon(appName))
        appBtn.bind("<Button-3>", lambda event: GUIButtonCommand.standardisedContextMenuPopup(perAppCM, event))
        GLOBAL_VARS.TASKBAR_APPS_CONTEXT_MENUS[appName] = perAppCM
    @staticmethod
    def removeDesktopAppIcon(appName: str, param=None):
        if not ([appName, param] in GLOBAL_VARS.PINNED_APPS_DESKTOP): return False
        try:
            apList = GLOBAL_VARS.USER_CONFIG["PINNED"] 
            apList[1].remove([appName, param])
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", apList)
            #GLOBAL_VARS.PINNED_APPS_DESKTOP.remove([appName, param])
        except Exception as EXP: LOGGER.addRawLog(EXP, [appName, param], "Error removing app from desktop");
        AppIconManager.refreshDesktop()

    @staticmethod
    def createDesktopAppIcon(appName: str, command: str, writeto=True, param=None, event=None):
        """ creates desktop icons!"""
        
        if GLOBAL_VARS.ROW_COUNT_DESKTOP_ICONS > GLOBAL_VARS.MAX_ROW_DESKTOP:
            if GLOBAL_VARS.COLUMN_COUNT_DESKTOP_ICONS > GLOBAL_VARS.MAX_COLUMN_DESKTOP: messagebox.showerror("Desktop pin", "Can't place the item! no more space left!", GLOBAL_VARS.ROOT_WINDOW)
            else: GLOBAL_VARS.COLUMN_COUNT_DESKTOP_ICONS += 1
        if [appName, param] not in GLOBAL_VARS.PINNED_APPS_DESKTOP or [GUIButtonCommand.AppImportNameCheck(appName), param] not in GLOBAL_VARS.PINNED_APPS_DESKTOP:
            if writeto:
                apList = GLOBAL_VARS.USER_CONFIG["PINNED"]
                apList[1].append([appName, param])
                GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", apList)
                #GLOBAL_VARS.PINNED_APPS_DESKTOP.append([appName, param])
            realAppName = GUIButtonCommand.AppImportNameCheck(app=appName)
            appFrame = tkinter.Frame(GLOBAL_VARS.DESKTOP_FRAME, background=GLOBAL_VARS.THEME_WINDOW_BG)
            appFrame.grid(row=GLOBAL_VARS.ROW_COUNT_DESKTOP_ICONS, column=GLOBAL_VARS.COLUMN_COUNT_DESKTOP_ICONS)
            GLOBAL_VARS.ROW_COUNT_DESKTOP_ICONS += 1
            if param == None: appIcon = giveIcon(realAppName, GLOBAL_VARS.ROOT_WINDOW)
            else: appIcon = giveIcon("file", GLOBAL_VARS.ROOT_WINDOW)
            appBtn = IconButton(appFrame, appIcon, GLOBAL_VARS.THEME_FOREGROUND,GLOBAL_VARS.THEME_WINDOW_BG, lambda: GUIButtonCommand.launchItem(command, param), True)
            appBtn.ref = appIcon
            
            appBtn.BUTTON.appName = appName
            appBtn.BUTTON.param = param
            appBtn.BUTTON.identifier="desktopappbtn"
            appBtn.BUTTON.row=GLOBAL_VARS.ROW_COUNT_DESKTOP_ICONS
            perAppCM = tkinter.Menu(appFrame, tearoff=False, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
            perAppCM.add_command(label="Open", command=lambda: GUIButtonCommand.launchItem(command, param))
            perAppCM.add_command(label="Remove Icon", command=lambda: AppIconManager.removeDesktopAppIcon(appName, param))
            GLOBAL_VARS.DESKTOP_APPS_CONTEXT_MENUS[f"{appName}-{param}-{GLOBAL_VARS.ROW_COUNT_DESKTOP_ICONS}"] =  perAppCM
            appBtn.bind("<Button-3>", lambda event: GUIButtonCommand.standardisedContextMenuPopup(perAppCM, event))
            txt = appName
            if param != None: 
                if isinstance(param, str) and len(param) > 15:
                    if GUIButtonCommand.AppImportNameCheck(appName) in ["notepad", "photoviewer", "shelveeditor", "<<anyapp>>"]: 
                        param.replace("\\", "/")
                        txt=param.split("/")[-1]
                    else: txt=param[-15:]
                else: txt=param
            appLbl = tkinter.Label(appFrame, text=txt, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
            appLbl.grid(row=1, column=0)
            appBtn.grid(row=0, column=0)
            try:
                if GLOBAL_VARS.WALLPAPER  == None or GLOBAL_VARS.WALLPAPER.cget("image") == None: raise Exception
                appFrame.lift()
                appFrame.update_idletasks()
                appFrame.update()
                appFrame.update_idletasks()
                posLEFT = appFrame.winfo_rootx()
                posUP = appFrame.winfo_rooty()
                posBOTTOM = posUP + appFrame.winfo_height()
                posRIGHT = posLEFT + appFrame.winfo_width()
                newImg = ImageTk.getimage(GLOBAL_VARS.WALLPAPER.BASE_IMAGE)
                appFrame.REF1 = newImg
                cropImg = newImg.crop((posLEFT, posUP, posRIGHT, posBOTTOM))
                appFrame.REF2 = cropImg
                imgToRender = ImageTk.PhotoImage(cropImg)
                appFrame.IMG_REF = imgToRender
                lbl = tkinter.Label(appFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, image=imgToRender)
                lbl.REF = imgToRender
                lbl.place(x=0, y=0)
                appBtn.BUTTON.lift()
                appLbl.lift()

            except Exception as EXP: print(f"{EXP}Not Working")
            if writeto: AppIconManager.refreshDesktop()
        else: messagebox.showerror(None, None, GLOBAL_VARS.ROOT_WINDOW, True, "APP_NOT_FOUND_ERROR")
    @staticmethod
    def removeTaskbarAppIcon(appName: str):
        if appName not in GLOBAL_VARS.PINNED_APPS :return
        try:
            apList = GLOBAL_VARS.USER_CONFIG["PINNED"]
            apList[0].remove(appName)
            GLOBAL_VARS.PINNED_APPS.remove(appName)
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", apList)
        except Exception as EXP: LOGGER.addRawLog(EXP, [appName], "Error removing app from taskbar")
        AppIconManager.refreshDesktop()

class ShutdownMenu():
    def __init__(self, root: tkinter.Tk, e=None):
        self.root=root
        shutdownWindow = tkinter.Toplevel(root, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.PID = generatePID(DIALOGUE_BOXES)
        GLOBAL_VARS.RUNNING_APPS[GLOBAL_VARS.USERNAME][self.PID] = "shutdownmenu"
        frame = dwm.createTopFrame(shutdownWindow, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WN_CLR, "shutdown", "Shutdown Menu", self.PID)
        frame.ALL_BUTTONS["minimize"].grid_forget()
        shutdownWindow.title("Shutdown/Restart the shell")
        a = tkinter.Label(shutdownWindow, text="What you want to do now?", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        a.grid(row=1, column=0)
        ShutdownICON = giveIcon("shutdown", shutdownWindow, 2)
        ShutdownBTN = tkinter.Button(shutdownWindow, image=ShutdownICON, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=self.shutdown)
        ShutdownBTN.IMGREF = ShutdownICON
        tooltips.createToolTipAtGivenPos(ShutdownBTN, 2, root, "Shuts down the shell")
        ShutdownBTN.grid(row=2, column=0)
        RestartICON = giveIcon("restart", shutdownWindow, 2)
        RestartBTN = tkinter.Button(shutdownWindow, image=RestartICON, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=self.restart)
        RestartBTN.IMGREF = RestartICON
        RestartBTN.grid(row=2, column=1)
        tooltips.createToolTipAtGivenPos(RestartBTN, 2, root, "Restarts the shell")
        self.safeModeRestartVar = tkinter.IntVar()
        ttk.Style().configure("TCheckbutton", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        safeModeRestartChk = ttk.Checkbutton(shutdownWindow, text="Restart in safe mode", variable=self.safeModeRestartVar, style="TCheckbutton")
        safeModeRestartChk.grid(row=2, column=2, padx=10)
        tkinter.Label(shutdownWindow, text="Shutdown", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=3, column=0)
        tkinter.Label(shutdownWindow, text="Restart", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=3, column=1)
        if (GLOBAL_VARS.USERNAME != "defaultuser0"): 
            logoutIcon = giveIcon("logout", shutdownWindow, 4)
            logoutBTN = tkinter.Button(shutdownWindow, image=logoutIcon, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Logout", command=self.logout)
            logoutBTN.grid(row=4, column=0)
            tkinter.Label(shutdownWindow, text="Logout", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=5, column=0)
            logoutBTN.imageRef = logoutIcon
        shutdownWindow.mainloop()

    def waitUntillTaskFinishes(self,func):
        if FILE_SYSTEM.TASK_IN_PROGRESS != [0, 0]: messagebox.showinfo("IO Operations pending!", "Please wait untill the file IO operations are completed. The system will automatically shutdown after.", root=self.root, MainPID=self.PID)
        def e():
            if FILE_SYSTEM.TASK_IN_PROGRESS == [0, 0]: func()
            self.root.after(100, e)
        self.root.after(100, e)
    def shutdown(self):
        try:
            if GLOBAL_VARS.USERNAME == "GUEST": FILE_SYSTEM.deleteFiles([[f"{CWD}/Users/GUEST"]])
        finally: 
            LOGGER.addTextLog("Shutdown initiated")
            LOGGER.updateFileLogs()
            self.waitUntillTaskFinishes(lambda: os._exit(0))
    def restart(self):
        if self.safeModeRestartVar.get() == 1:
            try: GLOBAL_VARS.ROOT_WINDOW.destroy()
            finally:
                def sigma(): os.system(f"""{PYTHON_COMMAND_ARG} "Windows 11.py" -safemode """)
                LOGGER.addTextLog("Shutdown initiated")
                LOGGER.updateFileLogs()
                self.waitUntillTaskFinishes(sigma)
        else:
            try: GLOBAL_VARS.ROOT_WINDOW.destroy()
            finally: 
                LOGGER.addTextLog("Shutdown initiated")
                LOGGER.updateFileLogs()
                os.system(f"""{PYTHON_COMMAND_ARG} "Windows 11.py" """)
    def logout(self):
        for apps in dict(GLOBAL_VARS.RUNNING_APPS[GLOBAL_VARS.USERNAME]).keys():
            dwm.focusOut(apps)
        GLOBAL_VARS.START_MENU_ACTIVE.destroy()
        dwm.close(self.PID)
        GLOBAL_VARS.ROOT_WINDOW.destroy()
        login()

class GUIButtonCommand:
    @staticmethod
    def launchItem(application: str, params= None, e=None): 
        if GUIButtonCommand.AppImportNameCheck(application) == "controlpanel":
            settings(openOnPage=params)
            return
        elif GUIButtonCommand.AppImportNameCheck(application) == "taskmanager":
            TaskManager(GLOBAL_VARS.ROOT_WINDOW)
            return
        if application == "Command Prompt" or application == "commandprompt":
            import ProgramFiles.commandprompt as CMD
            appToLaunchPID = generatePID(PROCESS_IDS)
            GLOBAL_VARS.RUNNING_APPS[GLOBAL_VARS.USERNAME][appToLaunchPID] = application
            AppIconManager.createRunningAppTaskbarIcon(application, appToLaunchPID, username=GLOBAL_VARS.USERNAME)
            try: CMD.main(FILE_SYSTEM, GLOBAL_VARS.USERNAME, params, FILE_SYSTEM.getConfig("USER_CONFIG"), appToLaunchPID)
            except: CMD.main(FILE_SYSTEM, GLOBAL_VARS.USERNAME,  params, dict({"THEME": ["Black", "White", "Black"]}), appToLaunchPID)   
        elif application == "<<ANYAPP>>":
            from ProgramFiles import fileRouters
            fileRouters.handleFiles(params, GLOBAL_VARS.USERNAME, FILE_SYSTEM.getConfig("USER_CONFIG"))    
        else: 
            appToLaunch = GUIButtonCommand.AppImportNameCheck(app=application)
            appImport = GLOBAL_VARS.APP_INSTANCE.getAppCache(f"ProgramFiles.{appToLaunch}")
            appPID = generatePID(PROCESS_IDS)
            GLOBAL_VARS.RUNNING_APPS[GLOBAL_VARS.USERNAME][appPID] = application
            AppIconManager.createRunningAppTaskbarIcon(application, appPID, username=GLOBAL_VARS.USERNAME) 
            if appImport.NEEDS_FILESYSTEM_ACCESS:appImport.main(FILE_SYSTEM, GLOBAL_VARS.USERNAME,  params, FILE_SYSTEM.getConfig("USER_CONFIG"), appPID)
            else: appImport.main(GLOBAL_VARS.USERNAME,  params, FILE_SYSTEM.getConfig("USER_CONFIG"), appPID)
    @staticmethod
    def FOCUS_focusApp(PID, realApp, E=None):
        try:
            dwm.focus(PID)
        except Exception as EXP:
            try:
                appImport = GLOBAL_VARS.APP_INSTANCE.getAppCache(f"ProgramFiles.{realApp}")
                if appImport.returnInformation(PID)["state"] == "normal": appImport.focusOut(PID)
                else: appImport.focusIn(PID)
            except Exception as EXCEPTION:
                LOGGER.addRawLog(EXCEPTION, [appImport, GLOBAL_VARS.APP_INSTANCE], "Error in focus in/out")
                messagebox.showerror("Error in focus in/out", EXCEPTION, GLOBAL_VARS.ROOT_WINDOW)
    @staticmethod
    def FOCUS_scrShotPreview(PID, realApp, event: tkinter.Event):
        oldFocus = None
        try:
            oldFocus = dwm.getFocus(PID)
            dwm.focusIn(PID)
            wnToFocus = dwm.returnWindow(PID)
        except Exception as EXP:
            LOGGER.addRawLog(EXP, [PID, realApp], "Unable to use DWM for focusing window - either app has no DWM or it is hung up")
            try:
                appImport = GLOBAL_VARS.APP_INSTANCE.getAppCache(f"ProgramFiles.{realApp}", False)
                oldFocus = appImport.returnInformation(PID)["state"]
                appImport.focusIn(PID)
                wnToFocus = appImport.INSTANCES[PID]
            except Exception as exp: 
                wnToFocus = None
                LOGGER.addRawLog(exp, [PID, realApp], "Unable to use normal app import focus too. either app has no implementation of method returnInformation or app is hung")
        if wnToFocus == None: return
        
        x = wnToFocus.winfo_x()
        y = wnToFocus.winfo_y()
        width = wnToFocus.winfo_width()
        height = wnToFocus.winfo_height()
        #if (str(platform.system()).lower() == "windows"):
        #    x += (wnToFocus.winfo_x()/4)
       #     y += (wnToFocus.winfo_y()/4)
        #   width += (wnToFocus.winfo_width()/4)
        #    height += (wnToFocus.winfo_height()/4)
        imageLoaded = False
        exp = ""
        try:
            image = ImageTk.PhotoImage(ImageGrab.grab(bbox=(x, y, x + width, y + height)).resize(tuple((350, 100))))
            GLOBAL_VARS.ROOT_WINDOW.E_IMG = image
        except Exception as EXP: LOGGER.addRawLog(EXP, [image], "Error in creating screen snip for window preview (ImageGrab.grab())"); exp=str(EXP)+"\n"; imageLoaded = False
        else:  imageLoaded = True
        ttl = None
        try:
            dwm.setFocus(PID, oldFocus)
            ttl = dwm.title(PID=PID)
        except Exception as EXP:
            LOGGER.addRawLog(EXP, [realApp], f"Unable to contact DWM for PID {PID}. Either app doesn't support dwm or something is wrong")
            appImport = GLOBAL_VARS.APP_INSTANCE.getAppCache(f"ProgramFiles.{realApp}")
            appImport.INSTANCES[PID].update()
            appImport.INSTANCES[PID].state(newstate=oldFocus)
            appImport.INSTANCES[PID].update()
            ttl = appImport.returnInformation(PID)["title"]
        if imageLoaded: tooltips._createToolTipAtGivenPos(PID, GLOBAL_VARS.ROOT_WINDOW, exp+ttl+f'\nPID: {PID}', GUIButtonCommand.FOCUS_focusApp, event, image=GLOBAL_VARS.ROOT_WINDOW.E_IMG, compound="top")
        else: tooltips._createToolTipAtGivenPos(PID, GLOBAL_VARS.ROOT_WINDOW, exp+ttl+f'\nPID: {PID}', GUIButtonCommand.FOCUS_focusApp, event)
    @staticmethod
    def AppImportNameCheck(app: str, dontLower=False):
        if "/" in app:
            appSplit = app.split("/")
            appToLaunch = app.replace("/", ".")
            realAppName = appSplit.pop(1)
            appToLaunch = appToLaunch.rstrip(realAppName)
            appSplit.append(realAppName.lower().replace(" ", ""))
            appToLaunch += appSplit[1]
        else:    
            if (dontLower): appToLaunch = app.replace(" ", "")
            else: appToLaunch = app.lower().replace(" ", "")
        return appToLaunch
    @staticmethod
    def handleExits(pid: int, RunningAppsList):
        try:
            for i in dict(RunningAppsList[0].children).values():
                if i.processInfo[0] == pid:i.destroy()
            for j in dict(RunningAppsList[1]).keys():
                if pid in dict(RunningAppsList[1])[j].keys():
                    del RunningAppsList[1][j][pid]
                    break
        except Exception as EXP: print(f"Error while handling exits for PID {pid}\nReason: {EXP}\nSkipping Exit Handles."); LOGGER.addRawLog(EXP, [pid, RunningAppsList], "Error while handling exits for given PID")
    @staticmethod
    def currentTime(*args):  
        cr_time = None

        if GLOBAL_VARS.USER_CONFIG["CLOCK-WIDGET"] == 0:
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "CLOCK-WIDGET", 1)
            GUIButtonCommand.clockWidgetPinning()
        else:
            try: 
               cr_time = None
               GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "CLOCK-WIDGET", 0)
               GLOBAL_VARS.CLOCK_LABEL.after_cancel(GLOBAL_VARS.CLOCK_LOOP_ID)
               GLOBAL_VARS.CLOCK_LABEL.destroy()
               
            except Exception as E: LOGGER.addRawLog(E, [cr_time, GLOBAL_VARS.CLOCK_LABEL, GLOBAL_VARS.USER_CONFIG], "Error destroying clock widget"); messagebox.showerror("Can't destroy clock widget!", f"Can't destroy clock widget due to the following reason: \n {E}", GLOBAL_VARS.ROOT_WINDOW)
    @staticmethod
    def standardisedContextMenuPopup(contextMenuObj: tkinter.Menu,  event=None, *args):
        """ the context menu popup"""
        try:
            contextMenuObj.tk_popup(event.x_root, event.y_root, 0)
            contextMenuObj.grab_set()
            contextMenuObj.grab_release()
        except Exception as PROBLEM:
            LOGGER.addRawLog(PROBLEM, [contextMenuObj, event], "Can't do tk_popup on context menu")
    @staticmethod
    def OSContextMenuPopup(event: tkinter.Event=None, *args):
        try:
            if (GLOBAL_VARS.ROOT_WINDOW.winfo_containing(event.x_root, event.y_root)).identifier == "taskbar": GLOBAL_VARS.TASKBAR_CONTEXT_MENU.focus()
            elif str((GLOBAL_VARS.ROOT_WINDOW.winfo_containing(event.x_root, event.y_root)).identifier) == "desktopappbtn":
                widget = (GLOBAL_VARS.ROOT_WINDOW.winfo_containing(event.x_root, event.y_root))
                GLOBAL_VARS.DESKTOP_APPS_CONTEXT_MENUS[f"{widget.appName}-{widget.param}-{widget.row}"].tk_popup(event.x_root, event.y_root)
            elif str((GLOBAL_VARS.ROOT_WINDOW.winfo_containing(event.x_root, event.y_root)).identifier) == "taskbarappbtn":
                widget = (GLOBAL_VARS.ROOT_WINDOW.winfo_containing(event.x_root, event.y_root))
                GLOBAL_VARS.TASKBAR_APPS_CONTEXT_MENUS[widget.APPNAME].tk_popup(event.x_root, event.y_root)
            else:
                try: GLOBAL_VARS.DESKTOP_CONTEXT_MENU.tk_popup(event.x_root, event.y_root, 0)
                finally: GLOBAL_VARS.DESKTOP_CONTEXT_MENU.grab_release()
        except  Exception as EXP: LOGGER.addRawLog(EXP, [event], "Can't open context menu")
    @staticmethod
    def getWallpaperImageResized(path: str):
        image = Image.open(path)
        resizedImage = image.resize((GLOBAL_VARS.ROOT_WINDOW.winfo_screenwidth(), GLOBAL_VARS.ROOT_WINDOW.winfo_screenheight()))
        actualImage= ImageTk.PhotoImage(resizedImage)
        return actualImage
    @staticmethod
    def clockWidgetPinning():
        def recurringClockFunc():
            cr_time = time.strftime("%H:%M:%S %p")
            
            GLOBAL_VARS.CLOCK_LABEL.configure(text=cr_time)
            GLOBAL_VARS.CLOCK_LOOP_ID = GLOBAL_VARS.CLOCK_LABEL.after(1000, recurringClockFunc)
            
        try:
            if GLOBAL_VARS.USER_CONFIG["CLOCK-WIDGET"] == 1: 
                cr_time = time.strftime("%H:%M:%S %p")
                GLOBAL_VARS.CLOCK_LABEL = tkinter.Label(GLOBAL_VARS.TASKBAR_FRAME, text=cr_time, background=GLOBAL_VARS.THEME_WN_CLR,
                                        foreground=GLOBAL_VARS.THEME_FOREGROUND, justify="right", anchor="e")
                GLOBAL_VARS.CLOCK_LABEL.grid(row=0, column=6, sticky="E")
                recurringClockFunc()
        except Exception as EXP: LOGGER.addRawLog(EXP, [GLOBAL_VARS.CLOCK_LABEL], "Unable  to pin clock widget")

def _AppLauncherForExternalApps(app: str, USER_CONFIG, params = None, userConfig= None,):
    PID = random.randint(5000, 9999)
    for usr in ParWFS._instances["root"].RUNNING_APPS.keys():
        while PID in ParWFS._instances["root"].RUNNING_APPS[usr].keys(): PID = random.randint(5000, 9999)
    ParWFS._instances["root"].RUNNING_APPS[userConfig][PID] = app
    ShelveRef = USER_CONFIG
    PER_PROGRAM_COMMAND_APPS_LIST = ShelveRef["APPS"][1]
    T_ACT_CLR, T_FG, T_BG = ShelveRef["THEME"]
    appToLaunch = GUIButtonCommand.AppImportNameCheck(app=app)
    progAppImport = f"{PER_PROGRAM_COMMAND_APPS_LIST[PER_PROGRAM_COMMAND_APPS_LIST.index(f'ProgramFiles.{appToLaunch}')]}"
    AppIconManager.createRunningAppTaskbarIcon(appToLaunch, PID, T_ACT_CLR, T_FG, userConfig)
    appImport = importlib.import_module(progAppImport)
    try:
        if appImport.NEEDS_FILESYSTEM_ACCESS: appImport.main(FILE_SYSTEM, userConfig, params, USER_CONFIG, PID)
        else: raise Exception("NO NEEDS_FILESYSTEM_ACCESS VAR")
    except Exception: appImport.main(userConfig, params, USER_CONFIG, PID)
class Scrollable(tkinter.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame: tkinter.Frame, width, height, mousewheel=True):
        self.canvas = tkinter.Canvas(frame, width=width, height=height, background=GLOBAL_VARS.THEME_WINDOW_BG, highlightthickness=0)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        #frame.focus_force()
        # base class initialization
        tkinter.Frame.__init__(self, frame, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.focus_force()
        frame.focus_force()
        self.focus_force()
        if mousewheel: 
            self.canvas.bind("<MouseWheel>", self._on_mousewheel)
            self.bind("<MouseWheel>", self._on_mousewheel)
            frame.bind("<MouseWheel>", self._on_mousewheel)

        self.canvas.bind('<Configure>', self.__fill_canvas)
        self.bind('<Configure>', self.__fill_canvas)
        frame.bind('<Configure>', self.__fill_canvas)
        self.focus()
        self.focus_force()

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tkinter.NW)
        ttk.Style().configure("TScrollbar", background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.update()

    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
    def _on_mousewheel(self, event): self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
class StartMenu: 
    def __init__(self, btn: tkinter.Button, taskbarFrame: tkinter.Frame, *e):
        if GLOBAL_VARS.START_MENU_ACTIVE:
            GLOBAL_VARS.START_MENU_ACTIVE.destroy()
            return
        GLOBAL_VARS.START_MENU_ACTIVE = self
        self.height = GLOBAL_VARS.ROOT_WINDOW.winfo_fpixels(f"{GLOBAL_VARS.ROOT_WINDOW.winfo_screenheight()/3}p")
        self.width = GLOBAL_VARS.ROOT_WINDOW.winfo_fpixels(f"{GLOBAL_VARS.ROOT_WINDOW.winfo_screenwidth()/5}p")
        btn.update()
        GLOBAL_VARS.ROOT_WINDOW.update()
        self.posX = btn.winfo_rootx()
        self.posY = taskbarFrame.winfo_height()
        BGCLR = GLOBAL_VARS.USER_CONFIG["THEME_WN_BORDERS"]
        HG_CLR = BGCLR["START_MENU_HG_CLR"]
        HGBG = BGCLR["START_MENU_HGBG"]
        self.startMenuFrame = tkinter.Frame(GLOBAL_VARS.ROOT_WINDOW, background=GLOBAL_VARS.THEME_WINDOW_BG, width=self.width, height=self.height, borderwidth=5, border=5, highlightcolor=HG_CLR, highlightbackground=HGBG, highlightthickness=3)
        self.startMenuFrame.place(x=self.posX, y=self.posY, bordermode="outside")
        self._LSideFrame = tkinter.Frame(self.startMenuFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, height=self.height, width=self.width/2)
        self._LSideFrame.grid(row=0, column=0)
        self.appsListFrame = tkinter.Frame(self._LSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, height=self.height, width=self.width/2)
        self.appsListFrame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.appsListFrame = Scrollable(self.appsListFrame, width=self.width/2, height=self.height)
        self.scrollbar = ttk.Scrollbar(self._LSideFrame, command=self.appsListFrame.canvas.yview)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True, anchor="e")
        self._RSideFrame = tkinter.Frame(self.startMenuFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, width=self.width/2, height=self.height)
        self._RSideFrame.grid(row=0, column=1)
        self.selectFolders = tkinter.Frame(self._RSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, height=self.height, width=self.width/2)
        self.selectFolders.grid(row=0, column=0)
        self.selectFolders = Scrollable(self.selectFolders, self.width/2, self.height, False)
        self.shutdownBtn = tkinter.Button(self._RSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Shutdown", command=lambda e=None: ShutdownMenu(GLOBAL_VARS.ROOT_WINDOW))
        self.shutdownBtn.grid(row=1, column=0)
        self.BUTTON_INSTANCES = []
        self.FLDR_BTN_INSTANCES = []
        self.IMAGE_INSTANCES = []
        tkinter.Label(self.appsListFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="All Apps", justify='center').pack()
        pfpUsrnameFrame = tkinter.Frame(self.selectFolders, background=GLOBAL_VARS.THEME_WINDOW_BG)
        pfpUsrnameFrame.pack()
        self.selectFolders.update()
        self.pfpImage = Image.open(fp=GLOBAL_VARS.USER_CONFIG["PFP"])
        self.pfpImage = ImageTk.PhotoImage(self.pfpImage.resize(tuple([int(self.width/4.5), int(self.width/4.5)])))
        pfp = tkinter.Label(pfpUsrnameFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, image=self.pfpImage, justify="center")
        pfp.pfpimg = self.pfpImage
        btn.pfpImage = self.pfpImage
        pfp.grid(row=0, column=0)
        pfpUsrnameFrame.update()
        pfp.update()
        self.selectFolders.update()
        _ = tkinter.Label(pfpUsrnameFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=GLOBAL_VARS.USERNAME)
        _.grid(row=1, column=0)
        _.update()
        self.selectFolders.update()
        def _lnchApp(app, prm=None): GUIButtonCommand.launchItem(GUIButtonCommand.AppImportNameCheck(app), prm)
        for x, i in enumerate(GLOBAL_VARS.APPS_LIST):
            img = giveIcon(GUIButtonCommand.AppImportNameCheck(i), GLOBAL_VARS.ROOT_WINDOW, 2)
            btn.e = img
            self.IMAGE_INSTANCES.append(img)
            self.appsListFrame.update()
            BUTTON = tkinter.Button(self.appsListFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=lambda e=i: _lnchApp(e), text=i, image=self.IMAGE_INSTANCES[x], compound="left", justify="left", anchor="w")
            BUTTON.e = img
            BUTTON.pack(fill='both', expand=True)
            BUTTON.bind("<MouseWheel>", self.appsListFrame._on_mousewheel)
            BUTTON.update()
            BUTTON.focus()
            BUTTON.focus_force()
            self.BUTTON_INSTANCES.append(BUTTON)
            self.BUTTON_INSTANCES[x].update()
            self.appsListFrame.update()
        self.appsListFrame.update()
        self.appsListFrame.focus_force()
        for x, i in enumerate(USER_FOLDERS_LIST):
            folderPath = os.path.join(CWD, "Users", GLOBAL_VARS.USERNAME, i).replace("\\", "/")
            self.selectFolders.update()
            BUTTON_FLDR = tkinter.Button(self.selectFolders, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=i, command=lambda e=folderPath: _lnchApp("File Manager", e), justify="left", anchor="w")
            BUTTON_FLDR.pack(fill='both', expand=True)
            BUTTON_FLDR.update()
            self.selectFolders.update()
        cntrlpanelbutton = tkinter.Button(self.selectFolders, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Control Panel", command=lambda: _lnchApp("Control Panel"), justify="left", anchor="w")
        cntrlpanelbutton.pack(fill="both", expand=True)
        self.appsListFrame.update()
        self.appsListFrame.focus_force()
        self.appsListFrame.update()
    def destroy(self):
        self.startMenuFrame.destroy()
        GLOBAL_VARS.START_MENU_ACTIVE = False

class TaskManager:
    def __init__(self, root):
        from ProgramFiles.treeview import Treeview
        self.ROOT = tkinter.Toplevel(root, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.fileView = Treeview(self.ROOT, style="Treeview")
        PID = generatePID(TASK_MANAGERS)
        dwm.createTopFrame(self.ROOT, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WN_CLR, "taskmanager", "Task Manager", PID)
        GLOBAL_VARS.RUNNING_APPS[GLOBAL_VARS.USERNAME][PID] = "Task Manager"
        AppIconManager.createRunningAppTaskbarIcon("Task Manager", PID, username=GLOBAL_VARS.USERNAME)
        self.ROOT.title("Task Manager")
        self.fileView.grid(row=1, column=0, sticky="w")
        self.fileView['column'] = "PID"
        self.fileView['column'] = "username"
        self.fileView.column("#0", anchor=tkinter.W, width=200)
        self.fileView.heading("#0", "Applications")
        self.fileView.column("PID", anchor=tkinter.W, width=100)
        self.fileView.heading("PID", text="Process IDs", anchor=tkinter.CENTER)
        self.fileView.column("username", anchor=tkinter.W, width=200)
        self.fileView.heading("username", text="Username", anchor=tkinter.CENTER)
        self.fileView.configure(style="Treeview")
        self.buttonsFrame = tkinter.Frame(self.ROOT, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.buttonsFrame.grid(row=2, column=0)
        self.endTaskButton = tkinter.Button(self.buttonsFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="End Application", command=self.endTaskBtn)
        self.endTaskButton.grid(row=0, column=0)
        self.focusBtn = tkinter.Button(self.buttonsFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Focus In/Out", command=self.focusInOut)
        self.focusBtn.grid(row=0, column=1)
        self.ROOT.after(500, self.updateEach1000Ms)
        self.ROOT.mainloop()
    def endTaskBtn(self):
        if self.fileView.focus() == None: return
        username = "".join(e for e in str(self.fileView.focus().IID).split(":")[1:])
        PID = int(str(self.fileView.focus().IID).split(":")[0])
        application = GLOBAL_VARS.RUNNING_APPS[username].get(PID)
        string = f"{application} <<<PID: {PID}>>> <<<USERNAME: {username}>>>"
        TaskManager.endTask(self.fileView.focus().IID)
        

    def updateEach1000Ms(self):
        self.ROOT.after(1000, self.updateEach1000Ms)
        SELECTED_SMTH = None
        try: SELECTED_SMTH = (self.fileView.focus()).IID; self.fileView.CURRENT_SELECTION = None
        except: pass
        for i in self.fileView.get_children(): self.fileView.delete(i)
        for usr in dict(GLOBAL_VARS.RUNNING_APPS).keys():
            for i, PID in enumerate(GLOBAL_VARS.RUNNING_APPS[usr].keys()):
                appToIns = GLOBAL_VARS.RUNNING_APPS[usr].get(PID)
                #appToIns += f" <<<PID: {PID}>>> <<<USERNAME: {usr}>>>"
                self.fileView.configure(style="Treeview")
                self.fileView.insert(parent='', iid=f"{PID}:{usr}", text=appToIns, index='end', values=[PID, usr],)
        if SELECTED_SMTH != None: self.fileView.focusByIID(SELECTED_SMTH)
        #self.fileView.selection_set([SELECTED_SMTH])
    def focusInOut(self, *arg):
        username = "".join(e for e in str(self.fileView.focus().IID).split(":")[1:])
        PID = int(str(self.fileView.focus().IID).split(":")[0])
        realApp = GUIButtonCommand.AppImportNameCheck(GLOBAL_VARS.RUNNING_APPS[username][PID])
        GUIButtonCommand.FOCUS_focusApp(PID, realApp)
    @staticmethod    
    def endTask(string:str, username=None):
        if username == None: username = GLOBAL_VARS.USERNAME
        application = int(string.split(":")[0])
        username = "".join(boi for boi in string.split(":")[1:])
        try: dwm.close(PID=int(application))
        except Exception as EXP:
            LOGGER.addRawLog(EXP, [application], "Unable to close app by DWM. Either app isn't managed by DWM or app is hung")
            try:
                appToEnd = str(GLOBAL_VARS.RUNNING_APPS[username][int(application)])
                appToEnd.replace(f"<<<PID: {application}>>>", "").replace(f"<<<USERNAME: {username}>>>")
                command = GLOBAL_VARS.COMMAND_APPS_LIST[GLOBAL_VARS.COMMAND_APPS_LIST.index(f"ProgramFiles.{ GUIButtonCommand.AppImportNameCheck(app=appToEnd)}")] 
                appImport = GLOBAL_VARS.APP_INSTANCE.getAppCache(f"ProgramFiles.{appToEnd}")
                appImport.endTask(int(application))
                del GLOBAL_VARS.RUNNING_APPS[username][int(application)]
            except Exception as E:
                LOGGER.addRawLog(E, [appToEnd, appImport, GLOBAL_VARS.APP_INSTANCE, GLOBAL_VARS.RUNNING_APPS], "Unable to close app via import and endTask(). File doesn't have an endTask() function implemented?")
                try: 
                    dwm.MANAGED_DWM_INSTANCES[int(application)][2].destroy()
                    del GLOBAL_VARS.RUNNING_APPS[username][int(application)]
                except Exception as U: LOGGER.addRawLog(U, [dwm.MANAGED_DWM_INSTANCES, GLOBAL_VARS.RUNNING_APPS], "Unable to close app via force DWM exiting.??"); messagebox.showerror("Error ending application", f"Error ending {application}. \nProblem: {U}\nFrom\n{E}\nFrom\n{EXP}", GLOBAL_VARS.ROOT_WINDOW)

class PW11UserCreation:
    """This can be used for accounts panel in settings menu AND as an OOBE agent"""
    def __init__(self, root: tkinter.Frame, relaunchFunction):
        self.root = root
        self.LSideFrame = tkinter.Frame(self.root, background=GLOBAL_VARS.THEME_WINDOW_BG,)
        self.LSideFrame.grid(row=0, column=0)
        self.RSideFrame = tkinter.Frame(self.root, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.RSideFrame.grid(row=0, column=1)
        self.LSide_UserListFrame = tkinter.Frame(self.LSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.LSide_UserListFrame.grid(row=0, column=0)
        self.LSide_NewUserBtn = tkinter.Button(self.LSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, text="Create a new user!", foreground=GLOBAL_VARS.THEME_FOREGROUND, command=self.createNewUserPanel)
        self.LSide_NewUserBtn.grid(row=1, column=0)
        self.RSide_UserContentFrame = tkinter.Frame(self.RSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.RSide_UserContentFrame.grid(row=0, column=0)
        self.USER_BUTTONS = []
        self.USER_PFPs = {}
        self.USERS_CREATED = 0
        self.relaunchFunction = relaunchFunction
        USER_CONFIGS: list[list[str, list[str, int]]] = []
        self.USRNAME_PASWD_STR: dict[str, str] = {}
        for file in Path(os.path.join(CWD, "Users")).glob("accConfiguration*.conf"):
            with open(file, "r") as reader:
                usrNo = "".join(char for char in reversed(str(file).split(".")[0]))
                idxForLastN = usrNo.index("n")
                usrNumber = usrNo[0:idxForLastN]
                usr, paswd = reader.readlines()
                usr = base64.urlsafe_b64decode(usr).decode("utf-8")
                if usr == "defaultuser0": continue
                USER_CONFIGS.append([usr, paswd])
                self.USRNAME_PASWD_STR[usr] = [paswd, usrNumber]
        for i, user in enumerate(USER_CONFIGS):
            FILE_SYSTEM.loadConfig(os.path.join(CWD, "Users", user[0], "USER_CONFIG"), user[0])
            config = FILE_SYSTEM.getConfig(user[0])
            IMG = Image.open(fp=config["PFP"])
            self.USER_PFPs[user[0]] = IMG
            IMG = ImageTk.PhotoImage(IMG.resize(tuple((int(IMG.width/2), int(IMG.height/2)))))
            FILE_SYSTEM.unloadConfig(user[0])
            btn = tkinter.Button(self.LSide_UserListFrame, text=user[0], background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, image=IMG, compound="left", command=lambda e=user[0]: self.showParticularUserPanel(e) )
            btn.grid(row=i, column=0)
            btn.INFO = user
            btn.IMG = IMG
    def _actualCreateUser(self, username, password, userNumber, overWrite=True):
        createUserAccount(username, password, userNumber, overWrite)
        self.USERS_CREATED += 1
        text="created"
        if not overWrite: text="over-written"
        messagebox.showinfo("Created user!", f"Succesfully {text} user with username {username}", GLOBAL_VARS.ROOT_WINDOW)
        self.relaunchFunction()
    def showParticularUserPanel(self, username):
        def editUserActions():
            passwordFrame.entryBox.configure(state="normal")
            editButton.configure(text="Save changes!", command=lambda: self._actualCreateUser(usrFrame.entryBox.get(), passwordFrame.entryBox.get(), int(usrNumBox.entryBox.get()), False))
        FILE_SYSTEM.loadConfig(os.path.join(CWD, "ProgramFiles", username, "USER_CONFIG"), username)
        config = FILE_SYSTEM.getConfig(username)
        IMG = Image.open(fp=config["PFP"])
        FILE_SYSTEM.unloadConfig(username)
        IMG = ImageTk.PhotoImage(IMG)
        usrPfp = tkinter.Label(self.RSide_UserContentFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, image=IMG, justify="center")
        usrPfp.IMG = IMG
        usrPfp.grid(row=0, column=0)
        usrFrame = entryWidget.LabelledEntryBox(self.RSide_UserContentFrame, "Username: ", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        usrFrame.grid(row=1, column=0)
        usrFrame.entryBox.insert(tkinter.END, username)
        passwordFrame = entryWidget.LabelledEntryBox(self.RSide_UserContentFrame, "Password: ", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        passwordFrame.grid(row=2, column=0)
        if GLOBAL_VARS.USERNAME != username: passwordFrame.configureEntry(show="*")
        passwordFrame.entryBox.insert(tkinter.END, base64.urlsafe_b64decode(self.USRNAME_PASWD_STR.get(username)[0]).decode())
        passwordFrame.configureEntry(state="disabled")

        usrNumBox = entryWidget.LabelledEntryBox(self.RSide_UserContentFrame, "User Number: ", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        usrNumBox.grid(row=3, column=0)
        usrNumBox.entryBox.insert(tkinter.END, self.USRNAME_PASWD_STR.get(username)[1])

        editButton = tkinter.Button(self.RSide_UserContentFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Edit user!", command=editUserActions)
        editButton.grid(row=4, column=0)
        deleteButton = tkinter.Button(self.RSide_UserContentFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Delete user!", command=lambda userNum=self.USRNAME_PASWD_STR.get(username)[1]: self.deleteUserAccount(userNum))
        deleteButton.grid(row=5, column=0)
    def deleteUserAccount(self, usernum):
        GUIButtonCommand.launchItem("Command Prompt", f"user -delete -{usernum}")
        
    def createNewUserPanel(self,):
        usrFrame = entryWidget.LabelledEntryBox(self.RSide_UserContentFrame, "Username: ", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        usrFrame.grid(row=1, column=0)
        passwordFrame = entryWidget.LabelledEntryBox(self.RSide_UserContentFrame, "Password: ", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        passwordFrame.grid(row=2, column=0)

        usrNumBox = entryWidget.LabelledEntryBox(self.RSide_UserContentFrame, "User Number: ", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        usrNumBox.grid(row=3, column=0)

        saveButton = tkinter.Button(self.RSide_UserContentFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Create the user!", command=lambda: self._actualCreateUser(usrFrame.entryBox.get(), passwordFrame.entryBox.get(), int(usrNumBox.entryBox.get()) ))
        saveButton.grid(row=4, column=0)

        usrFrame.update()
        usrFrame.update_idletasks()
        passwordFrame.update()
        passwordFrame.update_idletasks()
        usrNumBox.update()
        usrNumBox.update_idletasks()
print("Loaded GUI Option Modules...")
def startUpTasks(CONFIG, ROOT: tkinter.Tk):
    idx = 0
    afterCancelId = None
    def __startup():
        nonlocal idx, afterCancelId
        afterCancelId = ROOT.after(100, lambda i=None: __startup(CONFIG, ROOT))
        length = len(CONFIG["STARTUP_APPS"])
        if idx >= length: ROOT.after_cancel(afterCancelId); return 0
        idx += 1
        GUIButtonCommand.launchItem(CONFIG["STARTUP_APPS"][idx-1])
    __startup()
    
def main():
    print("Loaded operating system!")
    def safeModePREPTask(e=None):
        ROOT_WINDOW.destroy()
        safeMode()
    global SYS_CONFIG
    FILE_SYSTEM.loadConfig(f"Users/{GLOBAL_VARS.USERNAME}/USER_CONFIG", "USER_CONFIG")
    if FILE_SYSTEM.getConfig("SYS_CONFIG")["FS_STOP_PREMATURE"] == True:
        FILE_SYSTEM.loadFromPickle()
        messagebox.showinfo("I/O operation interrupt while shutdown, recovered.", "We detected that the shell has exited by force while the shell was performing an I/O operation via the ParWFS Library.\nIt has automatically restored the point where it left.\nPlease go to the target directory again and restart your operation!.", GLOBAL_VARS.ROOT_WINDOW)
    GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.getConfig("USER_CONFIG")
    GLOBAL_VARS.APPS_LIST, GLOBAL_VARS.COMMAND_APPS_LIST = GLOBAL_VARS.USER_CONFIG["APPS"]
    GLOBAL_VARS.THEME_WN_CLR, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WINDOW_BG = GLOBAL_VARS.USER_CONFIG["THEME"]
    GLOBAL_VARS.PINNED_APPS = GLOBAL_VARS.USER_CONFIG["PINNED"][0]
    GLOBAL_VARS.PINNED_APPS_DESKTOP = GLOBAL_VARS.USER_CONFIG["PINNED"][1]
    print("Loaded apps and user settings!")
    ROOT_WINDOW = tkinter.Tk()
    ROOT_WINDOW.configure(background=GLOBAL_VARS.THEME_WINDOW_BG)
    GLOBAL_VARS.APP_INSTANCE.ROOT = ROOT_WINDOW
    callHost.setLoadedApps(GLOBAL_VARS.APP_INSTANCE)
    loadAllIcons(GLOBAL_VARS.APPS_LIST, ROOT_WINDOW)
    loadAllIcons(["shutdown", "restart", "start", "logout"], ROOT_WINDOW)
    GLOBAL_VARS.TASKBAR_FRAME = tkinter.Frame(ROOT_WINDOW, background=GLOBAL_VARS.THEME_WN_CLR)
    GLOBAL_VARS.TASKBAR_FRAME.identifier = "taskbar"
    ROOT_WINDOW.identifier = "root_window"
    GLOBAL_VARS.ROOT_WINDOW = ROOT_WINDOW
    desktopFrame = tkinter.Frame(ROOT_WINDOW, background=GLOBAL_VARS.THEME_WINDOW_BG, border=15)
    if (GLOBAL_VARS.USER_CONFIG["WALLPAPER"]):
        image = GUIButtonCommand.getWallpaperImageResized(GLOBAL_VARS.USER_CONFIG["WALLPAPER"])
        ROOT_WINDOW.wallpaperImage = image
        GLOBAL_VARS.WALLPAPER = tkinter.Label(ROOT_WINDOW, image=image)
        GLOBAL_VARS.WALLPAPER.grid(row=1, column=0, sticky="EWSN")
        GLOBAL_VARS.WALLPAPER.BASE_IMAGE = image
        GLOBAL_VARS.WALLPAPER.identifier = "wallpaper"
    ROOT_WINDOW.grid_rowconfigure(1, weight=1)
    ROOT_WINDOW.grid_columnconfigure(0, weight=1)
    contextMenu = tkinter.Menu(GLOBAL_VARS.TASKBAR_FRAME, tearoff=False, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
    contextMenu.add_command(label="Taskbar settings", command=lambda: GUIButtonCommand.launchItem("controlpanel", "taskbarsettings") )
    contextMenu.identifier = "taskbar"
    def runningTaskbarAppsLOOP():  
        ROOT_WINDOW.after(300, runningTaskbarAppsLOOP)
        for widget in dict(runningAppsFrame.children).values():
            try:
                location = list(dict(GLOBAL_VARS.RUNNING_APPS)[GLOBAL_VARS.USERNAME].keys()).index(widget.processInfo[0])
                widget.grid_configure(row=0, column=location)
                appNameReal = GUIButtonCommand.AppImportNameCheck(widget.processInfo[1])
                try: widget.configure(text=dwm.title(None, widget.processInfo[0]))
                except:
                    appImport = GLOBAL_VARS.APP_INSTANCE.getAppCache(f"ProgramFiles.{appNameReal}", False)
                    widget.configure(text=appImport.returnInformation(widget.processInfo[0])['title'])
            except Exception as EXP: 
                if widget.RETRIES == 10: 
                    currentTitle = widget.cget("text")
                    widget.configure(text=f"{currentTitle} (Not Responding)")
                if widget.RETRIES > 20:
                    LOGGER.addRawLog(EXP, [widget, widget.processInfo], "App took too long to respond")
                    widget.destroy() # That means app took too long to respond!. 
                widget.RETRIES += 1
    ROOT_WINDOW.after(300, runningTaskbarAppsLOOP)
    appsFrame = tkinter.Frame(GLOBAL_VARS.TASKBAR_FRAME, background=GLOBAL_VARS.THEME_WN_CLR, border=5)
    img = Image.open(os.path.join(CWD, "ProgramFiles/Icons/start.png"))
    img = img.resize((int(img.width/2), int(img.height/2)))
    img = ImageTk.PhotoImage(img)
    shutDown = tkinter.Button(GLOBAL_VARS.TASKBAR_FRAME, text="Start", background=GLOBAL_VARS.THEME_WN_CLR, foreground=GLOBAL_VARS.THEME_FOREGROUND,
                                command=lambda: StartMenu(shutDown, GLOBAL_VARS.TASKBAR_FRAME), image=img, compound="left")
    shutDown.img = img
    shutDown.grid(row=0, column=0, padx=5)
    tooltips.createToolTipAtGivenPos(shutDown, 1, ROOT_WINDOW, "Shutdown or restart the shell!", )
    appsFrame.grid(row=0, column=1, sticky="n")
    FILE_SYSTEM.RunAppsFrame = runningAppsFrame = GLOBAL_VARS.RUNNING_APPS_FRAME = tkinter.Frame(GLOBAL_VARS.TASKBAR_FRAME, background=GLOBAL_VARS.THEME_WN_CLR, padx=10, border=5)
    runningAppsFrame.grid(row=0, column=4, sticky="W")
    GLOBAL_VARS.TASKBAR_FRAME.columnconfigure(5, weight=1)
    notificationsButton = tkinter.Button(GLOBAL_VARS.TASKBAR_FRAME, text="Notifications (0)", background=GLOBAL_VARS.THEME_WN_CLR, foreground=GLOBAL_VARS.THEME_FOREGROUND, command= lambda: GLOBAL_VARS.NOTIFICATIONS.showNotificationsList(), justify="right", anchor="e",)
    notificationsButton.grid(row=0, column=7, sticky="E", padx=5)
    GLOBAL_VARS.NOTIFICATION_BUTTON = notificationsButton
    GLOBAL_VARS.DESKTOP_FRAME = desktopFrame
    GLOBAL_VARS.APPS_FRAME = appsFrame
    GLOBAL_VARS.RUNNING_APPS_FRAME = runningAppsFrame
    desktopContextMenu = tkinter.Menu(appsFrame, tearoff=False, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
    desktopContextMenu.add_command(label="Refresh", command=AppIconManager.refreshDesktop)
    desktopContextMenu.add_command(label="Add new icon", command=lambda: GUIButtonCommand.launchItem("controlpanel", "desktopsettings"))
    GLOBAL_VARS.DESKTOP_CONTEXT_MENU = desktopContextMenu
    GLOBAL_VARS.TASKBAR_CONTEXT_MENU = contextMenu
    ROOT_WINDOW.bind("<Button-3>", GUIButtonCommand.OSContextMenuPopup)
    GLOBAL_VARS.TASKBAR_FRAME.bind("<Button-3>", lambda event: GUIButtonCommand.standardisedContextMenuPopup(contextMenu, event))
    GLOBAL_VARS.TASKBAR_FRAME.grid(row=0, column=0, sticky="NEW", )
    desktopFrame.grid(row=1, column=0, sticky="NW")
    desktopFrame.lift()
    GUIButtonCommand.clockWidgetPinning()
    ROOT_WINDOW.attributes('-fullscreen', True)
    ROOT_WINDOW.bind("<Escape>", safeModePREPTask)
    AppIconManager.refreshDesktop()
    startUpTasks(GLOBAL_VARS.USER_CONFIG, ROOT_WINDOW)
    FILE_SYSTEM.ROOT = ROOT_WINDOW
    for app in dict(GLOBAL_VARS.RUNNING_APPS)[GLOBAL_VARS.USERNAME].keys():
        if (not ((app in range(PROCESS_IDS[0], PROCESS_IDS[1])) or (app in range(EXTERNAL_PID[0], EXTERNAL_PID[1])))): continue
        AppIconManager.createRunningAppTaskbarIcon(GUIButtonCommand.AppImportNameCheck(dict(GLOBAL_VARS.RUNNING_APPS)[GLOBAL_VARS.USERNAME][app]), app, username=GLOBAL_VARS.USERNAME)
    
    if GLOBAL_VARS.NOTIFICATIONS == None:
        from ProgramFiles.notifications import notifications
        GLOBAL_VARS.NOTIFICATIONS = notifications
    GLOBAL_VARS.NOTIFICATIONS.notificationButton = GLOBAL_VARS.NOTIFICATION_BUTTON
    callHost.INIT_DWM()
    GLOBAL_VARS.RUNAPPSLIST = [GLOBAL_VARS.RUNNING_APPS_FRAME, GLOBAL_VARS.RUNNING_APPS]
    ROOT_WINDOW.mainloop()
import base64
def loginVerification(userNameText: str, passwordText: tkinter.Entry, userNum: int,  loginWindow: tkinter.Tk, e=None):
    print("Checking credentials")
    try:
        if int(userNum) != 0:
            with open(f"Users/accConfiguration{userNum}.conf", "r") as verify:
                GLOBAL_VARS.USERNAME, password = verify.readlines()
                GLOBAL_VARS.USERNAME = base64.urlsafe_b64decode(GLOBAL_VARS.USERNAME.rstrip('\n')).decode('utf-8')
                password = base64.urlsafe_b64decode(password.rstrip('\n')).decode('utf-8')
                if userNameText == GLOBAL_VARS.USERNAME and passwordText.get() == password:
                    loginWindow.destroy()
                    try: main()
                    except Exception as EXP: bsod(main, f"DESKTOP_LAUNCH_ERROR('{EXP}')")
                else: messagebox.showerror(None, None, loginWindow, True, "LOGIN_INCORRECT")
    except Exception as EXP: messagebox.showerror("loginVerification Error!", EXP); LOGGER.addRawLog(EXP, [loginVerification, userNameText, userNameText.get(), userNameText])

DARK_COLOURS = ["black", 'brown', 'blue', 'green', 'red', 'violet', 'purple', 'dark blue', 'dark green',
                'dark red', 'dark brown', ]
def login():
    print("Starting up OS...")
    global SYS_CONFIG
    SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)
    def safeModePREPTask(e=None):
        global SYS_CONFIG
        SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)
        loginWindow.destroy()
        safeMode()
    numUsers = -1
    CONFIG_FILES = []
    GLOBAL_VARS.RUNNING_APPS["defaultuser0"] = {}
    GLOBAL_VARS.USERNAME = "defaultuser0"
    for file in Path(os.path.join(CWD, "Users")).glob("accConfiguration*.conf"): numUsers += 1; CONFIG_FILES.append(str(file))
    loginWindow = tkinter.Tk()
    loginWindow.title("Login to Windows 11")
    loginWindow.configure(background=GLOBAL_VARS.THEME_WINDOW_BG)
    loginWindow.attributes('-fullscreen', True)
    loginWindow.bind("<Shift-F10>", lambda e=None: GUIButtonCommand.launchItem("Command Prompt"))
    if numUsers < 1:
        createUserAccount("defaultuser0", "SYSTEM", 0, True, ["Black", "White"])
        GLOBAL_VARS.USERNAME="defaultuser0"
        FILE_SYSTEM.loadConfig(os.path.join(CWD, "Users/defaultuser0/USER_CONFIG"), "USER_CONFIG")
        GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.getConfig("USER_CONFIG")
        tkinter.Label(loginWindow, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="It seems that you don't have an user account set up!\nPlease setup an account first to use the system!\nRedirecting to the OOBE in 10 seconds!").grid(row=0, column=0)
        def launchOOBE(): loginWindow.destroy(); OOBE()
        loginWindow.after(10000, launchOOBE)
    
    else:
        loadAllIcons(["shutdown", "restart"], loginWindow)
        loginWindow.grid_rowconfigure(0, weight=1) 
        loginWindow.grid_columnconfigure(0, weight=1)
        WALLPAPER_LBL = tkinter.Label(loginWindow)
        WALLPAPER_LBL.grid(row=0, column=0)
        userBtnFrame = tkinter.Frame(loginWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        userBtnFrame.grid(row=0, column=0)
        perUserFrame = tkinter.Frame(loginWindow, background=GLOBAL_VARS.THEME_WINDOW_BG) # grid: 0, 0
        def backToSelection():
            userBtnFrame.grid_forget()
            for child in dict(perUserFrame.children).values(): child.destroy()
            perUserFrame.grid_forget()
            userBtnFrame.grid(row=0, column=0)
        balls = -1
        loginWindow.PFP_LOGIN_IMAGES = []
        loginWindow.WALLPAPER_LOGIN_IMAGES = []
        WALLPAPER = None
        temp= None
        def selectUser(username:str, pfpFilePath:str, userNumber:int, wallpaperPath:str = None, bg:str=None, fg:str=None):
            userBtnFrame.grid_forget()
            perUserFrame.grid(row=0, column=0)
            pfpImage = Image.open(fp=pfpFilePath)
            pfpImage = ImageTk.PhotoImage(pfpImage.resize(tuple((int(pfpImage.width/2), int(pfpImage.height/2)))))
            loginWindow.PFP_LOGIN_IMAGES.append(pfpImage)
            UserButton = tkinter.Button(perUserFrame, text=username, background=bg, foreground=fg, image=pfpImage, compound="top", state="disabled")
            UserButton.grid(row=0, column=0)
            loginEntAndBtnFrame = tkinter.Frame(perUserFrame, background=bg)
            loginEntAndBtnFrame.grid(row=1, column=0)
            loginWindow.configure(background=bg)
            loginEntAndBtnFrame.configure(background=bg)
            perUserFrame.configure(background=bg)
            passwordText = tkinter.Entry(loginEntAndBtnFrame, foreground=fg, background=bg, show="*")
            passwordText.grid(row=0, column=0)
            passwordText.focus()
            passwordText.configure(insertbackground=fg, selectbackground=fg, selectforeground=bg)
            loginBt = tkinter.Button(loginEntAndBtnFrame, background=bg, foreground=fg, text="->")
            loginBt.configure(command=lambda e=None: loginVerification(username, passwordText, userNumber, loginWindow))
            loginBt.grid(row=0, column=1)
            backToUserSelect = tkinter.Button(perUserFrame, background=bg, foreground=fg, text="Back to user selection!", command=backToSelection)
            backToUserSelect.grid(row=2, column=0)
            loginWindow.configure(background=bg)
            loginEntAndBtnFrame.configure(background=bg)
            perUserFrame.configure(background=bg)
            if (wallpaperPath != None):
                    wallPaperimg = ImageTk.PhotoImage(Image.open(wallpaperPath).resize(tuple((int(loginWindow.winfo_screenwidth()), int(loginWindow.winfo_screenheight())))))
                    loginWindow.WALLPAPER_LOGIN_IMAGES.append(wallPaperimg)
                    WALLPAPER_LBL.configure(image=wallPaperimg)
            else:
                WALLPAPER_LBL.configure(image="")
            passwordText.bind("<Return>", lambda e=None: loginVerification(username, passwordText, userNumber, loginWindow))

        for files in CONFIG_FILES:
            balls += 1
            pfpFilepath = None
            userNum = None
            with open(files, "r") as reader:
                ball = reader.readlines()[0]
                e = (base64.urlsafe_b64decode(ball).decode("utf-8"))
                if e == "defaultuser0": continue
                userNum = int((str(files)[str(files).index("accConfiguration")+16:]).rstrip(".conf"))
                perUsrConfig = FILE_SYSTEM.loadConfig(f"Users/{e}/USER_CONFIG", f"{e}_LOGIN_USER_INFO")
                pfpFilepath = (perUsrConfig["PFP"])
                if (perUsrConfig["WALLPAPER"]):
                    wallPaperimg = ImageTk.PhotoImage(Image.open(perUsrConfig["WALLPAPER"]).resize(tuple((int(loginWindow.winfo_screenwidth()), int(loginWindow.winfo_screenheight())))))
                    loginWindow.WALLPAPER_LOGIN_IMAGES.append(wallPaperimg)
                    WALLPAPER_LBL.configure(image=wallPaperimg)
                if (not (e in dict(GLOBAL_VARS.RUNNING_APPS).keys())): GLOBAL_VARS.RUNNING_APPS[e] = {}
                FILE_SYSTEM.unloadConfig(f"{e}_LOGIN_USER_INFO")

                pfpImage = Image.open(fp=pfpFilepath)
                pfpImage = ImageTk.PhotoImage(pfpImage.resize(tuple((int(pfpImage.width/2), int(pfpImage.height/2)))))
                loginWindow.PFP_LOGIN_IMAGES.append(pfpImage)
                loginWindow.TEMP_IMAGE = pfpImage
                UserButton = tkinter.Button(userBtnFrame, text=e, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, image=pfpImage, compound="top", command=lambda f=e, g=pfpFilepath, h=userNum, i=perUsrConfig["WALLPAPER"], j=perUsrConfig["THEME"][2], k=perUsrConfig["THEME"][1]:selectUser(f, g, h, i, j, k))
                UserButton.IMAGE = pfpImage
                UserButton.grid(row=0, column=balls)
        shutdownBtn = tkinter.Button(loginWindow, text="Shutdown", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND,
                                    command=lambda: ShutdownMenu(loginWindow))
        btnWidth = loginWindow.winfo_screenwidth()/15
        btnHeight= loginWindow.winfo_screenheight()/15
        shutdownBtn.place(x=loginWindow.winfo_screenwidth()-btnWidth-15, y=loginWindow.winfo_screenheight()-btnHeight-15, width=btnWidth, height=btnHeight)


    loginWindow.bind("<Escape>", safeModePREPTask)
    loginWindow.mainloop()
def autoRecoveryEnv() -> None:
    recoveryWin = tkinter.Tk()
    recoveryWin.configure(background="Black")
    recoveryWin.attributes("-fullscreen", True)
    def launchCmd(e=None): import ProgramFiles.commandprompt; ProgramFiles.commandprompt.main(None, "AUTORECOVERYENV", None, {"THEME": ["Black", "White", "Black"]}, None, None, random.randint(1000, 9999), None)
    def reprSysCMDL(e=None):
        import ProgramFiles.commandprompt
        ROOT = tkinter.Tk()
        ROOT.configure(background=GLOBAL_VARS.THEME_WINDOW_BG)
        ROOT.title("Command Interpreter")
        text = tkinter.Text(ROOT, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, width=100)
        text.grid(row=0, column=0)
        yourCommand = tkinter.Entry(ROOT, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        yourCommand.configure(insertbackground=GLOBAL_VARS.THEME_FOREGROUND, selectforeground=GLOBAL_VARS.THEME_WINDOW_BG, selectbackground=GLOBAL_VARS.THEME_FOREGROUND, width=110)
        yourCommand.grid(row=1, column=0)
        cmdInstance = ProgramFiles.commandprompt.cmdCommands(text, yourCommand, root=ROOT)
        yourCommand.focus()
        cmdInstance.ADMINISTRATOR = True
        yourCommand.insert(tkinter.END, "sfcRepair -online")
        cmdInstance.sfcRepair()
        ROOT.mainloop()
    def continueToMain(e=None):
        recoveryWin.destroy()
        login()
    try:
        loadAllIcons(["continue", "repair", "commandprompt"], recoveryWin)
        continueICON = GLOBAL_VARS.ICONS["continue"]
        continueBTN = tkinter.Button(recoveryWin, image=continueICON, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=continueToMain, text='Continue to main', compound=tkinter.LEFT)
        continueBTN.IMGREF = continueICON
        continueBTN.grid(row=0, column=0)

        repairICON = GLOBAL_VARS.ICONS["repair"]
        repairBTN = tkinter.Button(recoveryWin, image=repairICON, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=reprSysCMDL, text='Repair system', compound=tkinter.LEFT)
        repairBTN.IMGREF = repairICON
        repairBTN.grid(row=1, column=0)

        cmdICON = GLOBAL_VARS.ICONS["commandprompt"]
        cmdBTN = tkinter.Button(recoveryWin, image=cmdICON, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=launchCmd, text='Launch Command Prompt', compound=tkinter.LEFT)
        cmdBTN.IMGREF = cmdICON
        cmdBTN.grid(row=0, column=1)
        recoveryWin.mainloop()
    except Exception: print("ERROR OCCURED WHILE LOADING AUTORECOVERYENV..."); recoveryWin.destroy(); safeMode(forceNoARENV=True)
def safeMode(forceNoARENV=False, forceNoBootRec=False) -> None:
    def a1():
        def resetConfigurations():
            userToreset = input("Enter the username of the user to reset the user too... [Type in defaultuser0 to only do system wise reset]")
            if userToreset.lower() != "defaultuser0":
                try:
                    with shelve.open(f"Users/{userToreset}/USER_CONFIG") as deleteIt: deleteIt.clear()
                except Exception as exp: LOGGER.addRawLog(exp, [userToreset], "Error while resetting for user"); print(f"ERROR OCCURED While resetting...!Error: {exp}")
            try:
                shelveFilesToDelete = [f"Users/{userToreset}/history", f"Users/{userToreset}/IPChat/_serverConfig", f"Users/{userToreset}/IPChat/serversList"]
                for shelveToDelete in shelveFilesToDelete:
                    try:
                        with shelve.open(shelveToDelete) as deleteIt: deleteIt.clear()
                    except Exception as EXP: LOGGER.addRawLog(EXP, [shelveFilesToDelete], "Unable to clear shelves")
            except Exception as exp: print(f"ERROR OCCURED While resetting...!Error: {exp}")
        print("=" * int(os.get_terminal_size()[0]))
        if NETWORKING:
            onlineOrOffline = input("Do you want to perform online repair? [Y/N](Y for online, N for offline, A for abort)")
            if onlineOrOffline == "Y" or onlineOrOffline == 'y':
                print("repairing system...")
                try:
                    Windows11MainDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/Windows 11.py", timeout=40)
                    resetConfigurations()
                    with open("Windows 11.py", "w") as writeTo:
                        try: writeTo.write(Windows11MainDownload.content.decode(encoding="UTF-8"))
                        except UnicodeEncodeError as UER:  print(f"UnicodeDecodeError occured while repairing 'Windows 11.py'\n--MSG:{UER}")
                except Exception as PROBLEM: LOGGER.addRawLog(PROBLEM, [onlineOrOffline], "Error doing online repairing"); print(f"Repairing Failed!\n<<<REASON: {PROBLEM}")
                finally: print("=" * int(os.get_terminal_size()[0]))
            elif onlineOrOffline == "N" or onlineOrOffline == "n":
                print("Resetting your system!")
                resetConfigurations()
                print("=" * int(os.get_terminal_size()[0]))
            else: print("=" * int(os.get_terminal_size()[0]))
        else:
            print("Resetting your system")
            resetConfigurations()
            print("Successfully resetted your system. Now, you MUST RUN the shell under the -config parameter. That can be done from Command Prompt! [Or from python code]")
            print("=" * int(os.get_terminal_size()[0]))

    def a2(): print("=" * int(os.get_terminal_size()[0])); login()    
    def a3():
        print("=" * int(os.get_terminal_size()[0]))
        print("CurrentWorkingDirectory: ", os.getcwd())
        appName = input("Enter the file name path to load!")
        os.system(f"python {appName} ")
        print("=" * int(os.get_terminal_size()[0]))
    def a4(): print("=" * int(os.get_terminal_size()[0])); print("Shutting down...") ; sys.exit(0)
    
    def a5():
        print("=" * int(os.get_terminal_size()[0]))
        opt = input("Do you want to restart in safe mode or normal mode?\n"
                    "1. Safe Mode\n"
                    "2. Normal Mode\n"
                    "Enter your option >_")
        if int(opt) == 1: 
            print("=" * int(os.get_terminal_size()[0]))
            os.system(f"""{PYTHON_COMMAND_ARG} "Windows 11.py" -safemode """)
        else: 
            os.system(f"""{PYTHON_COMMAND_ARG} "Windows 11.py" """)
            print("=" * int(os.get_terminal_size()[0]))
    def a6():
        print("=" * int(os.get_terminal_size()[0]))
        nonlocal NETWORKING
        try: requests.get("http://theoldnet.com")
        except Exception as prob: LOGGER.addRawLog(prob, [requests.get], "Unable to fetch website theoldnet.com, probably due to lack of network."); print(f"Operation failed!\nReason: {prob}")
        else: NETWORKING = True ; print("Enabled networking!")
        print("=" * int(os.get_terminal_size()[0]))

    def a7():
        print("=" * int(os.get_terminal_size()[0]))
        nonlocal NETWORKING
        NETWORKING = False
        print("Disabled networking!")
        print("=" * int(os.get_terminal_size()[0]))

    NETWORKING = False
    commandDict: dict[int, function] = { 1: a1, 2: a2, 3: a3, 4: a4, 5: a5, 6: a6, 7: a7,}
    try:
        if forceNoARENV: raise NotImplementedError("The program is forcing to use safe mode CLI... skipping Auto Recovery Environment...")
        autoRecoveryEnv()
        global SYS_CONFIG
        SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)
    except Exception as PRB:
        LOGGER.addRawLog(PRB, [autoRecoveryEnv, forceNoARENV], "Unable to launch auto recovery environment")
        try:
            if forceNoARENV and forceNoBootRec: raise NotImplementedError("Skipping attempt to launch fullscreen command prompt")
            def sendCommand(e=None):
                cmdInstance.showMsg(f"\n>{yourCommand.get()}")
                if " " not in yourCommand.get(): yourCommand.insert(tkinter.END, "  ")
                if yourCommand.get().split(" ")[0] in cmdInstance.COMMAND_LIST and cmdInstance.ACCEPT_COMMANDS: exec(f"cmdInstance.{yourCommand.get().split(' ')[0]}()")
                elif not cmdInstance.ACCEPT_COMMANDS: cmdInstance.clear()
                else: cmdInstance.showMsg(cmdInstance.COMMAND_NOT_FOUND)
            import ProgramFiles.commandprompt as cmd
            root= tkinter.Tk()
            root.configure(background=GLOBAL_VARS.THEME_WINDOW_BG)
            root.attributes("-fullscreen", True) 
            text = tkinter.Text(root, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, width=100)
            text.grid(row=0, column=0)
            yourCommand = tkinter.Entry(root, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
            yourCommand.configure(insertbackground=GLOBAL_VARS.THEME_FOREGROUND, selectforeground=GLOBAL_VARS.THEME_WINDOW_BG, selectbackground=GLOBAL_VARS.THEME_FOREGROUND, width=110)
            yourCommand.grid(row=1, column=0)
            cmdInstance = cmd.cmdCommands(text, yourCommand, root)
            yourCommand.focus()
            yourCommand.bind("<Return>", sendCommand)
            cmdInstance.showMsg("""\nYou're in a safe mode back up CLI mode. This is a fullscreen Command Prompt
\nThe system failed to boot. if you can diagnose & repair the system, you can use the available commands\n
Or else, type in the command 'restart' and your system will reboot""")
            root.mainloop()
        except Exception as PRB:
            LOGGER.addRawLog(PRB, [forceNoARENV, forceNoBootRec, cmdInstance], "Unable to launch full screen command prompt!")
            print(f"Cannot launch safe mode UI, going full CLI!\n PRB: {PRB}")
            time.sleep(5)
            try:
                import platform
                if platform.system() == "Windows": os.system("cls")
                else: os.system("clear")
            except Exception: pass
            finally:
                while True:
                    print("Safe mode activated!\n=-=-=-=WELCOME=-=-=-=")
                    while True:
                        userInput1 = int(input("""1. Reset your system\n2. Continue to boot to main\n3. Launch an app\n4. Shutdown the system\n5. Restart the system\n6. Enable networking\n7. Disable networking\nEnter your option >_"""))
                        if userInput1 in range(1, 8): commandDict[userInput1]()
    finally: SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)

class OOBE:
    def __init__(self, welcomeMessage="Welcome to the Out-of-box Experience!\nPlease setup an user account to use the system efficiently\nBegin by creating a new user account with the button below!\n\nPress Shift-F10 to open a command prompt!"):
        self.MAINROOT = tkinter.Tk()
        self.MAINROOT.attributes("-fullscreen", True)
        self.MAINROOT.config(background="Black")
        self.welcomeMessage = welcomeMessage
        self.WelcomeMessageLabel = tkinter.Label(self.MAINROOT, background="Black", foreground="White", text=self.welcomeMessage)
        self.WelcomeMessageLabel.grid(row=0, column=0)
        self.ROOT = tkinter.Toplevel(self.MAINROOT, background="Black")
        dwmTopFrame = dwm.createTopFrame(self.ROOT, "White", "Black", "start", "Out-of-box Experience", 10001, self.destroy)
        dwmTopFrame.ALL_BUTTONS["minimize"].configure(state="disabled")
        self.FRAME = tkinter.Frame(self.ROOT, background="Black")
        GLOBAL_VARS.APP_INSTANCE.ROOT = self.MAINROOT
        self.FRAME.grid(row=1, column=0)
        self.ROOT.focus_force()
        self.ROOT.focus()
        self.ROOT.update()
        self.ROOT.update_idletasks()
        self.FRAME.focus_force()
        self.FRAME.update()
        self.FRAME.update_idletasks()
        self.USER_ACCOUNTS_PANEL = PW11UserCreation(self.FRAME, self.destroy)
        self.ROOT.bind("<Shift-F10>", lambda e=None: GUIButtonCommand.launchItem("Command Prompt"))
        self.MAINROOT.bind_all("<Shift-F10>", lambda e=None: GUIButtonCommand.launchItem("Command Prompt"))
        #self.USER_ACCOUNTS_PANEL.RSide_UserContentFrame.update()
        #self.USER_ACCOUNTS_PANEL.RSide_UserContentFrame.update_idletasks()
        self.ROOT.lift()
        self.ROOT.mainloop()
        self.MAINROOT.mainloop()
    def destroy(self, *args):
        if (self.USER_ACCOUNTS_PANEL.USERS_CREATED != 0):
            self.MAINROOT.destroy()
            FILE_SYSTEM.editConfig("SYS_CONFIG", "SETUP_IN_PROGRESS", 0)
            login()
        else: 
            choice = messagebox.askyesorno("Exit?", "You have not created a first time user yet! Do you like to quit pre-maturely?", self.ROOT)
            if choice: self.MAINROOT.destroy()
            return

def _bsodInStartup(func, supportCode):
    if SYS_CONFIG["CBSRESTARTATTEMPT"] > 3:
            try: autoRecoveryEnv()
            except Exception as EXP: LOGGER.addRawLog(EXP, [SYS_CONFIG["CBSRESTARTATTEMPT"]], "Unable to launch auto recovery env - activating safeMode()"); safeMode()
    else: bsod(func, supportCode)

if __name__ == "__main__":
    arguements = sys.argv[1:]
    if not os.access("ProgramFiles", os.F_OK): _bsodInStartup(login, "MODULE_NOT_FOUND_ERROR('The required modules inside ProgramFiles folder doesn't exist!')")
    else:
        if not os.access("ProgramFiles/commandprompt.py", os.F_OK) or not os.access("ProgramFiles/errorHandler.py", os.F_OK): _bsodInStartup(login, "MODULE_NOT_FOUND_ERROR('The required modules inside ProgramFiles folder doesn't exist!')")
        else:
            if SYS_CONFIG["SETUP_IN_PROGRESS"]:
                createUserAccount("defaultuser0", "SYSTEM", 0, True, ["Black", "White", "Black"])
                GLOBAL_VARS.USERNAME="defaultuser0"
                FILE_SYSTEM.loadConfig(os.path.join(CWD, "Users/defaultuser0/USER_CONFIG"), "USER_CONFIG")
                GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.getConfig("USER_CONFIG")
                OOBE()
            elif "-safemode" in arguements: safeMode()
            elif "-safemodecli" in arguements: safeMode(True, True)
            elif "-safemodefullcmd" in arguements: safeMode(True)
            elif "-config" in arguements:
                GLOBAL_VARS.USERNAME = input("Enter the username to create first run settings: ")
                password = input("Enter your user's password: ")
                foreground = input("Enter your user's preffered foreground colour: ")
                background = input("Enter your user's preffered background colour: ")
                windowColour = input("Enter your user's preffered window background colour: ")
                userNumber = input("Enter your user's wanted user number (can be any number): ")
                createUserAccount(GLOBAL_VARS.USERNAME, password, userNumber, True, [background, foreground, windowColour])
                print("Initialized new entries!")
            elif "-configchange" in arguements:
                print("You have entered the configuration manager! Press CTRL+C anytime to exit!\n")
                configchoice = input("System or User config change?")
                if "system" in configchoice.lower():
                    infoSysSelectSTR = "SYS_CONFIG"
                    SYS_CONFIG = shelve.open("ProgramFiles/SYS_CONFIG", writeback=True)
                else:
                    infoSysSelectSTR = "GLOBAL_VARS.USER_CONFIG"
                    GLOBAL_VARS.USERNAME = input("Type in the username whose settings are going to be changed!: ")
                    GLOBAL_VARS.USER_CONFIG = shelve.open(f"Users/{GLOBAL_VARS.USERNAME}/USER_CONFIG", writeback=True)
                print("The respective configuration module has been imported!\n"
                        f"Now, type in '{infoSysSelectSTR}[<CONFIG_NAME>] = <CONFIG>;' and then press enter to finish\n"
                        "New code lines and line endings MUST BE represented by the ; character!")
                code_to_execute = input("Start here>")
                for i, code in enumerate(code_to_execute.split(";")):
                    try: exec(code)
                    except Exception as PROB: print(f"Error has occured! Error: {PROB}\n\nRestart the system with the same parameter to enter this mode!")
                    else: print(f"Line {i+1} executed successfully! Reboot your system and observe whether the changes applied correctly!")
                    
            else:
                try:
                    import tkinter, requests
                    if SYS_CONFIG["CBSRESTARTATTEMPT"] > 3:
                        try: autoRecoveryEnv()
                        except Exception as EXP: LOGGER.addRawLog(EXP, [SYS_CONFIG["CBSRESTARTATTEMPT"]], "Unable to launch auto recovery env - activating safeMode()"); safeMode()
                except Exception as PROBLEM:
                    LOGGER.addRawLog(PROBLEM, [SYS_CONFIG], "Unable to import a module - forcing safeMode()")
                    try:
                        import platform
                        if platform.system() == "Windows": os.system("cls")
                        else:  os.system("clear")
                    except Exception: pass
                    print(f"Safe mode activated due to one of the modules not present. \n DEBUG: {PROBLEM}")
                    time.sleep(5)
                    safeMode()
                else:
                    try: 
                        dwm.MANAGED_DWM_INSTANCES[0] = [None, None, GLOBAL_VARS, None, None, None]
                        login()
                    except Exception as EXP: _bsodInStartup(login, f"LOGIN_FAILURE('{EXP}')")