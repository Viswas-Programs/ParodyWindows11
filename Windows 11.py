from pathlib import Path
import tkinter
import importlib
def bsod(obj, supportCode) -> None:
    text = f"""A problem has occured on ParodyWin11 and has been shutdown to prevent further damage\n
If this is the first time you're seeing this stop screen, please make sure you have proper configuration files 
in the right place.\n\nIf the problem still exists, please contact your administrator or have a 
look at this informative page on stop codes! (support link)\n\nSupport: \nhttps://github.com/Viswas-Programs/ParodyWindows11/wiki/STOP_CODES\n\n
Technical information: {obj} Failed to load properly (Improperly loaded!)\nSupport Code: {supportCode}\n
Restarting in a moment..."""
    try:
        def restart():
            bsodWind.destroy()
            time.sleep(5)
            os.system(""" python "Windows 11.py" """)
            exit()
        try:
            SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", SYS_CONFIG["CBSRESTARTATTEMPT"] + 1)
            with open("ProgramFiles/CRASHLOGS", "a") as UPDATE_CRASH_LOGS: UPDATE_CRASH_LOGS.write(f"\n{supportCode} occured on {datetime.now()} on {obj}")
        except Exception as EXP: exp = EXP; 
        finally:
            bsodWind = tkinter.Tk()
            bsodWind.configure(background="blue")
            bsodWind.attributes("-fullscreen", True)
            tkinter.Label(bsodWind, background="Blue", foreground="White", text=text, font=("Arial Rounded MT Bold", 18)).pack(anchor=tkinter.W)
            
            try: 
                if exp: tkinter.Label(bsodWind, background="Blue", foreground="White", text=f"During above error, another error occured: {exp}", font=("Arial Rounded MT Bold", 18)).pack(anchor=tkinter.W)
            except Exception: pass
            bsodWind.after(10000, restart)
            bsodWind.mainloop()
    except Exception as EXP: print(text, EXP)
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
    from tkinter import colorchooser
    import random
    import ProgramFiles.tooltips as tooltips
    from PIL import Image, ImageTk, ImageGrab
    import psutil
    from ProgramFiles.fileaskhandlers import askopenfilename
    from ProgramFiles.buttons import IconButton
    import platform
except Exception as E: 
    bsod(__name__, str(E) + "\nMODULE_NOT_FOUND_ERROR")
CWD = os.getcwd()
FILE_SYSTEM = ParWFS.ParWFS()
FILE_SYSTEM.loadConfig("ProgramFiles/SYS_CONFIG", "SYS_CONFIG")
SYS_CONFIG = FILE_SYSTEM.getConfig("SYS_CONFIG")
USER_FOLDERS_LIST = ["My Documents", "My Pictures", "My Videos", "My Downloads"]
print("Starting OS...")
class PW11GlobalVars():
    """
    Contains all the variables in use for the shell's functions. These act as replacement to global variables.
    """
    def __init__(self):
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
        self.RUNNING_APPS = {}
        self.ICONS = {}
        self.THEME_WINDOW_BG = None
        self.THEME_FOREGROUND = None
        self.USERNAME = None
        self.APPS_LIST = []
        self.COMMAND_APPS_LIST = []
        self.USER_CONFIG = None
        self.PINNED_APPS_DESKTOP = []
        self.PINNED_APPS = []

GLOBAL_VARS = PW11GlobalVars()

try:
    GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND = SYS_CONFIG["THEME"]
except Exception:
    GLOBAL_VARS.THEME_WINDOW_BG = "Black"
    GLOBAL_VARS.THEME_FOREGROUND = "White"

GLOBAL_VARS.RUNNING_APPS =  FILE_SYSTEM.RUNNING_APPS
ICONS = GLOBAL_VARS.ICONS
PROCESS_IDS = (1000, 5000)
EXTERNAL_PID = (5000, 9999)
MESSAGEBOX_IDS = (0, 200)
PROGRESSBAR_IDS = (200, 400)
FILEASK_WINDOWS = (400, 600)
TASK_MANAGERS = (600, 650)
CONTROL_PANELS = (650, 700)
DIALOGUE_BOXES = (700, 850)
def returnRunningApps():
    return FILE_SYSTEM.RUNNING_APPS
def giveIcon(appName: str, root, subsample=False):
    try:
        if not subsample: return GLOBAL_VARS.ICONS[appName]
        else:
            return GLOBAL_VARS.ICONS[appName].subsample(subsample)
    except Exception as exp:
        print(exp)
        try:
            if not subsample: return tkinter.PhotoImage(file=f"ProgramFiles/Icons/{appName}.png", master=root)
            else: return tkinter.PhotoImage(file=f"ProgramFiles/Icons/{appName}.png", master=root).subsample(subsample)
        except EXP: print(EXP)
def loadAllIcons(appsList: list, root):
    for app in appsList:
        realApp = GUIButtonCommand.AppImportNameCheck(app)
        try:
            GLOBAL_VARS.ICONS[realApp] = tkinter.PhotoImage(file=f"ProgramFiles/Icons/{realApp}.png", master=root)
            root.erm = GLOBAL_VARS.ICONS[realApp]
        except: pass

class Notifications(object):
    def __init__(self):
        self.NotificationsList = []
        self.TimeofNotification = []
        self.actions = []
    def createNotification(self, msg: str, time: str, action: str):
        self.NotificationsList.append(msg)
        self.TimeofNotification.append(time)
        self.actions.append(action)
        GLOBAL_VARS.ROW_COUNT_NOTIFICATION_WINDOW += 1
        GLOBAL_VARS.NOTIFICATION_BUTTON.configure(text=f"Notifications ({len(self.NotificationsList)})")
    def showNotification(self, title: str, msg: str, time: str, action: str) -> None:
        from ProgramFiles.errorHandler import messagebox
        self.createNotification(msg=msg, time=time, action=action)
        messagebox.showinfo(title, msg, GLOBAL_VARS.ROOT_WINDOW)
    def showNotificationsList(self, event=None):
        notificationsWindow = tkinter.Toplevel(background=GLOBAL_VARS.THEME_WINDOW_BG)
        GLOBAL_VARS.NOTIFICATION_BUTTON.configure(text="Notifications (0)")
        if len(self.NotificationsList) == 0:
            a = tkinter.Label(notificationsWindow, text="No notifications (yet)", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
            a.grid(row=0, column=0)
        for index, notif in enumerate(self.NotificationsList):
            lbl = tkinter.Label(notificationsWindow, text=f"{notif}\t: {self.TimeofNotification[index]}", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
            lbl.grid(row=index, column=0)
            lbl.bind('<Button-1>', self.actions[index])
        notificationsWindow.mainloop()
        self.NotificationsList, self.actions, self.TimeofNotification = [], [], []
notification = Notifications()
print("Starting up Notification Services...")
class settings():
    def __init__(self):
        self.SHOWN_HOMEPAGE = False
        self.SHOWN_PERSONALIZATION = False
        self.SHOWN_ADVANCED = False
        self.SHOWN_APPSLIST = False
        self.SHOWN_APPOPENERCHANGER = False
        self.total_memory = str(f"{psutil.virtual_memory().total/1000000000} GigaBytes")
        self.settingsWindow = tkinter.Toplevel(GLOBAL_VARS.ROOT_WINDOW, background=GLOBAL_VARS.THEME_WINDOW_BG)
        PID = random.randint(CONTROL_PANELS[0], CONTROL_PANELS[1])
        while PID in GLOBAL_VARS.RUNNING_APPS.keys():
            PID = random.randint(CONTROL_PANELS[0], CONTROL_PANELS[1])
        GLOBAL_VARS.RUNNING_APPS[PID] = "Control Panel"
        dwm.createTopFrame(self.settingsWindow, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WINDOW_BG, "settings", "Control Panel", PID)
        GUIButtonCommand.createRunningAppTaskbarIcon("settings", PID)
        btnFrame = tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        btnFrame.grid(row=1, column=0)
        homeBtn = tkinter.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Home", command=self.homePage)
        homeBtn.grid(row=0, column=0)
        personalizeBtn = tkinter.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Personalization", command=self.personalization)
        personalizeBtn.grid(row=1, column=0)
        appOpenerChangeBtn = tkinter.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="App Associations", command=self.changeFileOpeners)
        appOpenerChangeBtn.grid(row=2, column=0)
        startupApps = tkinter.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Startup Apps", command=self.addStartupApps)
        startupApps.grid(row=3, column=0)
        userManagementBtn = tkinter.Button(btnFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Users", command=self.addUserAccounts)
        userManagementBtn.grid(row=4, column=0)
        self.setting = tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        self.homePage()
    def homePage(self):
        self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        self.SHOWN_HOMEPAGE = True
        infoText = f""" Windows 11 v2.3.5\nSystem RAM: {self.total_memory}\nBackground={GLOBAL_VARS.THEME_WINDOW_BG}\n"""
        f"""Foreground={GLOBAL_VARS.THEME_FOREGROUND}\n\nFor more info, please visit the respective categories! Thank you :)"""
        a = tkinter.Label(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=infoText).grid(row=0, column=0)
    def personalization(self):
        self.SHOWN_PERSONALIZATION = True
        def changeBg():
            
            global SYS_CONFIG
            colorToUse = colorchooser.askcolor(title="Select background!")
            GLOBAL_VARS.THEME_WINDOW_BG = colorToUse[1]
            crBg.configure(text=f"Current Background = {GLOBAL_VARS.THEME_WINDOW_BG}")
            if systemChangeTheme.get(): 
                SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "THEME", [GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND])
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "THEME", [GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND])
            dwm.changeThemeForAllApps(GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND)
            dwm._changeThemeForAllApps(GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.ROOT_WINDOW)
            try:
                GLOBAL_VARS.ROOT_WINDOW.configure(background=GLOBAL_VARS.THEME_WINDOW_BG,)
                GLOBAL_VARS.APPS_FRAME.configure(background=GLOBAL_VARS.THEME_WINDOW_BG)
                GLOBAL_VARS.DESKTOP_FRAME.configure(background=GLOBAL_VARS.THEME_WINDOW_BG)
            except Exception: pass
            GLOBAL_VARS.ROOT_WINDOW.update()
        def changeFg():
            global SYS_CONFIG
            colorToUse = colorchooser.askcolor(title="Select foreground!")
            GLOBAL_VARS.THEME_FOREGROUND = colorToUse[1]
            print(GLOBAL_VARS.THEME_FOREGROUND)
            crFg.configure(text=f"Current foreground = {GLOBAL_VARS.THEME_FOREGROUND}")
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "THEME", [GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND])
            if systemChangeTheme.get(): 
                SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "THEME", [GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND])
            dwm.changeThemeForAllApps(GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND)
            dwm._changeThemeForAllApps(GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.ROOT_WINDOW)
            GLOBAL_VARS.ROOT_WINDOW.update()
        def changeWallpaper():
            nonlocal wallpaperText
            
            wallpaperChoose = askopenfilename("Open a wallpaper file (png)", (("PNG Files", "*.png"), ("All Files", "*.*")))
            img = GUIButtonCommand.getWallpaperImageResized(wallpaperChoose)
            GLOBAL_VARS.ROOT_WINDOW.image = img
            try:
                GLOBAL_VARS.WALLPAPER.configure(image=img)

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
            try: 
                GLOBAL_VARS.WALLPAPER.destroy()
            except: pass
            wallpaperText = "Current Wallpaper: No wallpapers set yet!"
            wallpaperPath.configure(text=wallpaperText)
        self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        crBg = tkinter.Label(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=f"Current Background = {GLOBAL_VARS.THEME_WINDOW_BG}")
        crBg.grid(row=0, column=0)
        changeBackground = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Change Background!", command=changeBg)
        changeBackground.grid(row=0, column=1)
        crFg = tkinter.Label(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=f"Current foreground = {GLOBAL_VARS.THEME_FOREGROUND}")
        crFg.grid(row=1, column=0)
        changeForeground = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Change foreground!", command=changeFg)
        changeForeground.grid(row=1, column=1)
        ttk.Style(self.settingsWindow).configure("TCheckbutton", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        systemChangeTheme = tkinter.IntVar()
        applyToSystem = ttk.Checkbutton(self.setting, text="Also apply changes to system theme!", variable=systemChangeTheme)
        applyToSystem.grid(row=2, column=0)
        wallpaperText = "Current Wallpaper: "
        if GLOBAL_VARS.USER_CONFIG["WALLPAPER"]: wallpaperText += GLOBAL_VARS.USER_CONFIG["WALLPAPER"]
        else: wallpaperText += "No wallpapers set yet!"
        wallpaperPath = tkinter.Label(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text=wallpaperText)
        wallpaperPath.grid(row=3, column=0)
        changeWallpaperButton = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Change Wallpaper", command=changeWallpaper)
        changeWallpaperButton.grid(row=3, column=1)
        removeWallpaperButton = tkinter.Button(self.setting, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Remove Wallpaper", command=removeWallpaper)
        removeWallpaperButton.grid(row=4, column=1)
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
                    messagebox.showerror('Error changing default app association', f'Error changing default app association.\nProb: {I}', addNewEntryWn )
            addNewEntryWn = tkinter.Toplevel(self.settingsWindow)
            nEntFrm = tkinter.Frame(addNewEntryWn, background=GLOBAL_VARS.THEME_WINDOW_BG)
            nEntFrm.grid(row=0, column=0)
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
                    messagebox.showerror('Error changing default app association', f'Error changing default app association.\n{I}', self.settingsWindow )
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
        PW11UserCreation(self.setting)


class GUIButtonCommand:
    @staticmethod
    def launchItem(application: str, params= None, e=None): 
        if GUIButtonCommand.AppImportNameCheck(application) == "controlpanel":
            settings()
            return
        elif GUIButtonCommand.AppImportNameCheck(application) == "taskmanager":
            TaskManager(GLOBAL_VARS.ROOT_WINDOW)
            return
        if application == "Command Prompt":
            import ProgramFiles.commandprompt as CMD
            appToLaunchPID = random.randint(a=PROCESS_IDS[0], b=PROCESS_IDS[1])
            while appToLaunchPID in GLOBAL_VARS.RUNNING_APPS.keys():
                appToLaunchPID = random.randint(a=PROCESS_IDS[0], b=PROCESS_IDS[1])
            GLOBAL_VARS.RUNNING_APPS[appToLaunchPID] = application
            GUIButtonCommand.createRunningAppTaskbarIcon(application, appToLaunchPID)
            try: CMD.main(FILE_SYSTEM, GLOBAL_VARS.USERNAME, notification, None, FILE_SYSTEM.getConfig("USER_CONFIG"), appToLaunchPID, [GLOBAL_VARS.RUNNING_APPS_FRAME, GLOBAL_VARS.RUNNING_APPS] )
            except: CMD.main(FILE_SYSTEM, GLOBAL_VARS.USERNAME, notification, None, dict({"THEME": ["Black", "White"]}), appToLaunchPID, [GLOBAL_VARS.RUNNING_APPS_FRAME, GLOBAL_VARS.RUNNING_APPS] )        
        else: 
            appToLaunch = GUIButtonCommand.AppImportNameCheck(app=application)
            #progAppImport = f"{GLOBAL_VARS.COMMAND_APPS_LIST[GLOBAL_VARS.COMMAND_APPS_LIST.index(f'ProgramFiles.{appToLaunch}')]}"
            appImport = importlib.import_module(f"ProgramFiles.{appToLaunch}")
            appPID = random.randint(PROCESS_IDS[0], PROCESS_IDS[1])
            while appPID in GLOBAL_VARS.RUNNING_APPS.keys():
                appPID = random.randint(a=PROCESS_IDS[0], b=PROCESS_IDS[1])
            GLOBAL_VARS.RUNNING_APPS[appPID] = application
            GUIButtonCommand.createRunningAppTaskbarIcon(application, appPID) 
            if appImport.NEEDS_FILESYSTEM_ACCESS:
                appImport.main(FILE_SYSTEM, GLOBAL_VARS.USERNAME, notification, params, FILE_SYSTEM.getConfig("USER_CONFIG"), appPID)
            else:
                appImport.main(GLOBAL_VARS.USERNAME, notification, params, FILE_SYSTEM.getConfig("USER_CONFIG"), appPID)
    @staticmethod
    def FOCUS_focusApp(PID, realApp, E=None):
        try:
            dwm.focus(PID)
        except:
            try:
                appImport = importlib.import_module(f"ProgramFiles.{realApp}")
                if appImport.returnInformation(PID)["state"] == "normal": appImport.focusOut(PID)
                else: appImport.focusIn(PID)
            except Exception as EXCEPTION:
                messagebox.showerror("Error in focus in/out", EXCEPTION, GLOBAL_VARS.ROOT_WINDOW)
    @staticmethod
    def FOCUS_scrShotPreview(PID, realApp, event: tkinter.Event):
        oldFocus = None
        try:
            oldFocus = dwm.getFocus(PID)
            dwm.focusIn(PID)
            wnToFocus = dwm.returnWindow(PID)
        except: 
            appImport = importlib.import_module(f"ProgramFiles.{realApp}")
            oldFocus = appImport.returnInformation(PID)["state"]
            appImport.focusIn(PID)
            wnToFocus = appImport.INSTANCES[{PID}]
        x = wnToFocus.winfo_x()
        y = wnToFocus.winfo_y()
        width = wnToFocus.winfo_width()
        height = wnToFocus.winfo_height()
        if (str(platform.system()).lower() == "windows"):
            x += (wnToFocus.winfo_x()/4)
            y += (wnToFocus.winfo_y()/4)
            width += (wnToFocus.winfo_width()/4)
            height += (wnToFocus.winfo_height()/4)
        image = ImageTk.PhotoImage(ImageGrab.grab(bbox=(x, y, x + width, y + height)).resize(tuple((350, 100))))
        GLOBAL_VARS.ROOT_WINDOW.E_IMG = image
        ttl = None
        try:
            dwm.setFocus(PID, oldFocus)
            ttl = dwm.title(PID=PID)
        except:
            appImport = importlib.import_module(f"ProgramFiles.{realApp}")
            appImport.INSTANCES[{PID}].update()
            appImport.INSTANCES[{PID}].state(newstate=oldFocus)
            appImport.INSTANCES[{PID}].update()
            ttl = appImport.returnInformation(PID)["title"]
        tooltips._createToolTipAtGivenPos({PID}, GLOBAL_VARS.ROOT_WINDOW, ttl+f'\\nPID: {PID}', GUIButtonCommand.FOCUS_focusApp, event, image=GLOBAL_VARS.ROOT_WINDOW.E_IMG, compound="top")
    @staticmethod
    def createRunningAppTaskbarIcon(app: str, PID:int, T_BG=None, T_FG=None):
        ROOT = GLOBAL_VARS.ROOT_WINDOW
        if T_BG and T_FG: 
            THEME_WBG = T_BG
            THEME_FG = T_FG
        else: THEME_WBG, THEME_FG = GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND
        POS = len(GLOBAL_VARS.RUNNING_APPS)
        realApp = GUIButtonCommand.AppImportNameCheck(app=app)
        appIcon = giveIcon(realApp, ROOT, 2)
        taskbarAppBtn = tkinter.Button(ParWFS._instances["root"].RunAppsFrame, text=app, background=THEME_WBG, foreground=THEME_FG, command=lambda e=realApp: GUIButtonCommand.FOCUS_focusApp(PID, realApp) , image=appIcon, compound='left')
        taskbarAppBtn.grid(row=0, column=POS)
        taskbarAppBtn.processInfo = (PID, app)
        taskbarAppBtn.windowInfo = 'focusIn'
        taskbarAppBtn.ICON = appIcon
        taskbarAppBtn.bind("<Enter>", lambda E: GUIButtonCommand.FOCUS_scrShotPreview(PID, realApp, E))
        taskbarAppBtn.bind("<Leave>", lambda E: tooltips.deleteToolTip(PID, ROOT))
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
        for i in dict(RunningAppsList[0].children).values():
            if i.processInfo[0] == pid:
                i.destroy()
        del RunningAppsList[1][pid]
    @staticmethod
    def currentTime(*args):
        
        cr_time = None
        if GLOBAL_VARS.USER_CONFIG["CLOCK-WIDGET"] == 0:
            def recurringClockFunction(e=None):
                nonlocal cr_time
                cr_time = time.strftime("%H:%M:%S %p")
                GLOBAL_VARS.CLOCK_LABEL = tkinter.Label(GLOBAL_VARS.ROOT_WINDOW, text=cr_time, background=GLOBAL_VARS.THEME_WINDOW_BG,
                                        foreground=GLOBAL_VARS.THEME_FOREGROUND)
                GLOBAL_VARS.CLOCK_LOOP_ID = GLOBAL_VARS.CLOCK_LABEL.after(1000, recurringClockFunction)
                GLOBAL_VARS.CLOCK_LABEL.grid(row=0, column=2, sticky="ne")
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "CLOCK-WIDGET", 1)
            recurringClockFunction()

        else:
            try: 
               cr_time = None
               GLOBAL_VARS.CLOCK_LABEL.after_cancel(GLOBAL_VARS.CLOCK_LOOP_ID)
               GLOBAL_VARS.CLOCK_LABEL.destroy()
               GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "CLOCK-WIDGET", 0)
            except Exception as E:
                messagebox.showerror("Can't destroy clock widget!", f"Can't destroy clock widget due to the following reason: \n {E}")
    @staticmethod
    def pinApps(appToPin, writeto=True):
        
        appName: str = appToPin
        appName = GUIButtonCommand.AppImportNameCheck(appToPin)
        
        if writeto:
            apList = GLOBAL_VARS.USER_CONFIG["PINNED"]
            apList[0].append(appName)
            GLOBAL_VARS.PINNED_APPS.append(appName)
            GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", apList)
        appIcon = giveIcon(appName, GLOBAL_VARS.ROOT_WINDOW, 2)
        appBtn = tkinter.Button(GLOBAL_VARS.APPS_FRAME, image=appIcon, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=lambda: GUIButtonCommand.launchItem(appToPin) )
        appBtn.imgRef = appIcon
        appBtn.grid(row=0, column=GLOBAL_VARS.PINNED_APPS.index(appToPin))
    @staticmethod
    def taskbarselfGUI(e=None):
        # SHIT CODE, WILL PROBABLY CHANGE TO A COMBOBOX PRETTY SOON
        taskbarselfWindow = tkinter.Toplevel(GLOBAL_VARS.ROOT_WINDOW)
        taskbarselfWindow.configure(background=GLOBAL_VARS.THEME_WINDOW_BG)
        taskbarselfWindow.title("Taskbar app pinning")
        addWidgetsFrame = tkinter.LabelFrame(taskbarselfWindow, text="Add widgets", 
                                            background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        addWidgetsFrame.grid(row=0, column=0)
        addClock = tkinter.Button(addWidgetsFrame, text="Clock", foreground=GLOBAL_VARS.THEME_FOREGROUND,
                                    background=GLOBAL_VARS.THEME_WINDOW_BG, command=GUIButtonCommand.currentTime)
        addClock.grid(row=0, column=0)
        pinItems = tkinter.LabelFrame(taskbarselfWindow, text="Pin items",
                                        background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        pinItems.grid(row=1, column=0)
        r = -1
        PINNED_APPS = list(GLOBAL_VARS.PINNED_APPS)
        NOT_PINNED_APPS = []
        for app in GLOBAL_VARS.APPS_LIST:
            if app not in PINNED_APPS:
                NOT_PINNED_APPS.append(app)
        combobox = ttk.Combobox(pinItems, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, values=NOT_PINNED_APPS, state='readonly')
        combobox.grid(row=0, column=0)
        combobox.bind("<<ComboboxSelected>>", lambda e: GUIButtonCommand.pinApps(combobox.get()) )
        taskbarselfWindow.mainloop()
    @staticmethod
    def standardisedContextMenuPopup(contextMenuObj: tkinter.Menu,  event=None, *args):
        """ the context menu popup"""
        try:
            contextMenuObj.tk_popup(event.x_root, event.y_root, 0)
            print(contextMenuObj.grab_status())
            contextMenuObj.grab_set()
            contextMenuObj.grab_release()
        except Exception as PROBLEM:
            print(PROBLEM)
    @staticmethod
    def OSContextMenuPopup(event: tkinter.Event=None, *args):
        if (GLOBAL_VARS.ROOT_WINDOW.winfo_containing(event.x_root, event.y_root)).identifier == "taskbar": 
            GLOBAL_VARS.TASKBAR_CONTEXT_MENU.focus()
        else:
            try:
                GLOBAL_VARS.DESKTOP_CONTEXT_MENU.tk_popup(event.x_root, event.y_root, 0)
                print(PROBLEM)
            finally:
                GLOBAL_VARS.DESKTOP_CONTEXT_MENU.grab_release()
    @staticmethod
    def createAppIcon(appName: str, command: str, writeto=True, event=None):
        """ creates desktop icons!"""
        
        if GLOBAL_VARS.ROW_COUNT_DESKTOP_ICONS > GLOBAL_VARS.MAX_ROW_DESKTOP:
            if GLOBAL_VARS.COLUMN_COUNT_DESKTOP_ICONS > GLOBAL_VARS.MAX_COLUMN_DESKTOP:
                messagebox.showerror("Desktop pin", "Can't place the item! no more space left!", GLOBAL_VARS.ROOT_WINDOW)
            else:
                GLOBAL_VARS.COLUMN_COUNT_DESKTOP_ICONS += 1
        if appName not in GLOBAL_VARS.PINNED_APPS_DESKTOP or GUIButtonCommand.AppImportNameCheck(appName) not in GLOBAL_VARS.PINNED_APPS_DESKTOP:
            if writeto:
                apList = GLOBAL_VARS.USER_CONFIG["PINNED"]
                apList[1].append(appName)
                GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", apList)
                GLOBAL_VARS.PINNED_APPS_DESKTOP.append(appName)
            realAppName = GUIButtonCommand.AppImportNameCheck(app=appName)
            appFrame = tkinter.Frame(GLOBAL_VARS.DESKTOP_FRAME, background=GLOBAL_VARS.THEME_WINDOW_BG)
            appFrame.grid(row=GLOBAL_VARS.ROW_COUNT_DESKTOP_ICONS, column=GLOBAL_VARS.COLUMN_COUNT_DESKTOP_ICONS)
            GLOBAL_VARS.ROW_COUNT_DESKTOP_ICONS += 1
            appIcon = giveIcon(realAppName, GLOBAL_VARS.ROOT_WINDOW)
            appBtn = IconButton(appFrame, image=appIcon, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=lambda: GUIButtonCommand.launchItem(command))
            appBtn.ref = appIcon
            appBtn.grid(row=0, column=0)
            appLbl = tkinter.Label(appFrame, text=appName, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
            appLbl.grid(row=1, column=0)
        else:
            messagebox.showerror(None, None, GLOBAL_VARS.ROOT_WINDOW, True, "APP_NOT_FOUND_ERROR")
    @staticmethod
    def getWallpaperImageResized(path: str):
        image = Image.open(path)
        resizedImage = image.resize((GLOBAL_VARS.ROOT_WINDOW.winfo_screenwidth(), GLOBAL_VARS.ROOT_WINDOW.winfo_screenheight()))
        actualImage= ImageTk.PhotoImage(resizedImage)
        return actualImage
    @staticmethod
    def refreshDesktop():
        for frame in dict(GLOBAL_VARS.DESKTOP_FRAME.children).values():
            frame.destroy()
        for app in GLOBAL_VARS.PINNED_APPS_DESKTOP:
            try:
                GUIButtonCommand.createAppIcon(f"{app}", f"{app}", False)
            except Exception as EXP: messagebox.showerror("Error pinning app", f"{app} Cannot be pinned due to the following technical reason: \n {EXP}", root=GLOBAL_VARS.ROOT_WINDOW)
    @staticmethod
    def addNewIcon(*args):
        INDEX=0
        iconToAdd = None
        addNewIcon = tkinter.Toplevel(GLOBAL_VARS.ROOT_WINDOW, background=GLOBAL_VARS.THEME_WINDOW_BG)
        desktopAppsList = ttk.Combobox(addNewIcon)
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
        def updateVariable(event=None):
            nonlocal iconToAdd
            nonlocal INDEX
            iconToAdd = str(desktopAppsList.get())
        desktopAppsList.bind("<<ComboboxSelected>>", updateVariable)
        desktopAppsList['state'] = "readonly"
        desktopAppsList.grid(row=0, column=0, sticky="w")
        addIconBtn = tkinter.Button(addNewIcon, text="Add Icon!", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=lambda: GUIButtonCommand.createAppIcon(iconToAdd, f"{iconToAdd}"))
        addIconBtn.grid(row=0, column=1) 
        addNewIcon.mainloop()
    @staticmethod
    def shutdownMenu(root: tkinter.Tk, e=None):
        def waitUntillTaskFinishes(func):
            if FILE_SYSTEM.TASK_IN_PROGRESS != [0, 0]:
                messagebox.showinfo("IO Operations pending!", "Please wait untill the file IO operations are completed. The system will automatically shutdown after.", root=root)
            def e():
                if FILE_SYSTEM.TASK_IN_PROGRESS == [0, 0]: func()
                root.after(100, e)
            root.after(100, e)
        def shutdown():
            try:
                if GLOBAL_VARS.USERNAME == "GUEST":
                    FILE_SYSTEM.deleteFiles([[f"{CWD}/ProgramFiles/GUEST"]])
            finally:
                waitUntillTaskFinishes(lambda: os._exit(0))
        def restart():
            if safeModeRestartVar.get() == 1:
                try:
                    GLOBAL_VARS.ROOT_WINDOW.destroy()
                finally:
                    def sigma():
                        os.system("""python "Windows 11.py" -safemode """)
                        exit()
                    waitUntillTaskFinishes(sigma)
            else:
                try:
                    GLOBAL_VARS.ROOT_WINDOW.destroy()
                finally:
                    os.system(""" python "Windows 11.py" """)
                    exit()

        shutdownWindow = tkinter.Toplevel(root, background=GLOBAL_VARS.THEME_WINDOW_BG)
        shutdownWindow.title("Shutdown/Restart the shell")
        a = tkinter.Label(shutdownWindow, text="What you want to do now?", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        a.grid(row=0, column=0)
        ShutdownICON = GLOBAL_VARS.ICONS["shutdown"].subsample(2, 2)
        ShutdownBTN = tkinter.Button(shutdownWindow, image=ShutdownICON, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=shutdown)
        ShutdownBTN.IMGREF = ShutdownICON
        tooltips.createToolTipAtGivenPos(ShutdownBTN, 2, root, "Shuts down the shell")
        ShutdownBTN.grid(row=1, column=0)
        RestartICON = GLOBAL_VARS.ICONS["restart"].subsample(2, 2)
        RestartBTN = tkinter.Button(shutdownWindow, image=RestartICON, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=restart)
        RestartBTN.IMGREF = RestartICON
        RestartBTN.grid(row=1, column=1)
        safeModeRestartVar = tkinter.IntVar()
        ttk.Style().configure("TCheckbutton", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
        safeModeRestartChk = ttk.Checkbutton(shutdownWindow, text="Restart in safe mode", variable=safeModeRestartVar, style="TCheckbutton")
        safeModeRestartChk.grid(row=1, column=2, padx=10)
        tkinter.Label(shutdownWindow, text="Shutdown", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=2, column=0)
        tkinter.Label(shutdownWindow, text="Restart", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND).grid(row=2, column=1)
        shutdownWindow.mainloop()

def _AppLauncherForExternalApps(app: str, USER_CONFIG, params = None, userConfig= None, notifications=None,):
    PID = random.randint(5000, 9999)
    while PID in ParWFS._instances["root"].RUNNING_APPS.keys():
        PID = random.randint(5000, 9999)
    ParWFS._instances["root"].RUNNING_APPS[PID] = app
    ShelveRef = USER_CONFIG
    PER_PROGRAM_COMMAND_APPS_LIST = ShelveRef["APPS"][1]
    T_BG, T_FG = ShelveRef["THEME"]
    appToLaunch = GUIButtonCommand.AppImportNameCheck(app=app)
    progAppImport = f"{PER_PROGRAM_COMMAND_APPS_LIST[PER_PROGRAM_COMMAND_APPS_LIST.index(f'ProgramFiles.{appToLaunch}')]}"
    GUIButtonCommand.createRunningAppTaskbarIcon(appToLaunch, PID, T_BG, T_FG)
    appImport = importlib.import_module(progAppImport)
    if appImport.NEEDS_FILESYSTEM_ACCESS:
        appImport.main(FILE_SYSTEM, userConfig, notifications, params, USER_CONFIG, PID)
    else:
        appImport.main(userConfig, notifications, params, USER_CONFIG, PID)
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
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
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

        self.startMenuFrame = tkinter.Frame(GLOBAL_VARS.ROOT_WINDOW, background=GLOBAL_VARS.THEME_WINDOW_BG, width=self.width, height=self.height, borderwidth=5, border=5, highlightcolor="white", highlightthickness=3)
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
        #self._RSideFrame = Scrollable(self._RSideFrame, self.width/2, self.height/2, False)
        self.selectFolders = tkinter.Frame(self._RSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, height=self.height, width=self.width/2)
        self.selectFolders.grid(row=0, column=0)
        self.selectFolders = Scrollable(self.selectFolders, self.width/2, self.height, False)
        self.shutdownBtn = tkinter.Button(self._RSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="Shutdown", command=lambda e=None: GUIButtonCommand.shutdownMenu(GLOBAL_VARS.ROOT_WINDOW))
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
            img = GLOBAL_VARS.ICONS[GUIButtonCommand.AppImportNameCheck(i)]
            img = img.subsample(2, 2)
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
        self.ROOT = tkinter.Toplevel(root, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.fileView = ttk.Treeview(self.ROOT, style="Treeview")
        PID = random.randint(TASK_MANAGERS[0], TASK_MANAGERS[1])
        while PID in GLOBAL_VARS.RUNNING_APPS.keys():
            PID = random.randint(TASK_MANAGERS[0], TASK_MANAGERS[1])
        dwm.createTopFrame(self.ROOT, GLOBAL_VARS.THEME_FOREGROUND, GLOBAL_VARS.THEME_WINDOW_BG, "taskmanager", "Task Manager", PID)
        GLOBAL_VARS.RUNNING_APPS[PID] = "Task Manager"
        GUIButtonCommand.createRunningAppTaskbarIcon("Task Manager", PID)
        self.ROOT.title("Task Manager")
        self.fileView.grid(row=1, column=0, sticky="w")
        self.fileView['column'] = "Applications"
        self.fileView.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        self.fileView.column("Applications", anchor=tkinter.W, width=600)
        self.fileView.heading("Applications", text="Applications", anchor=tkinter.CENTER)
        self.fileView.configure(style="Treeview")
        self.endTaskButton = tkinter.Button(self.ROOT, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, text="End Application", command=self.endTask)
        self.endTaskButton.grid(row=2, column=0)
        self.ROOT.after(500, self.updateEach1000Ms)
        self.ROOT.mainloop()
    def updateEach1000Ms(self):
        self.ROOT.after(1000, self.updateEach1000Ms)
        SELECTED_SMTH = self.fileView.focus()
        for i in self.fileView.get_children():
            self.fileView.delete(i)
        for i, PID in enumerate(GLOBAL_VARS.RUNNING_APPS):
            appToIns = GLOBAL_VARS.RUNNING_APPS.get(PID)
            appToIns += f" <<<PID: {PID}>>> "
            self.fileView.configure(style="Treeview")
            self.fileView.insert(parent='', iid=PID, text='', index='end', values=[appToIns],)
        self.fileView.focus(SELECTED_SMTH)
        self.fileView.selection_set([SELECTED_SMTH])
        
    def endTask(self):
        application = self.fileView.focus()
        try:
            dwm.close(PID=int(application))
            
        except Exception as EXP:
            print(EXP) 
            try:
                appToEnd = str(GLOBAL_VARS.RUNNING_APPS[int(application)])
                appToEnd.replace(f"<<<PID: {application}>>>", "")
                command = GLOBAL_VARS.COMMAND_APPS_LIST[GLOBAL_VARS.COMMAND_APPS_LIST.index(f"ProgramFiles.{ GUIButtonCommand.AppImportNameCheck(app=appToEnd)}")] 
                appImport = importlib.import_module(command)
                appImport.endTask(int(application))
                del GLOBAL_VARS.RUNNING_APPS[int(application)]
            except Exception as E:
                print(E)
                try: 
                    dwm.MANAGED_DWM_INSTANCES[int(application)][2].destroy()
                    del GLOBAL_VARS.RUNNING_APPS[int(application)]
                except Exception as U:
                    messagebox.showerror("Error ending application", f"Error ending {application}. \nProblem: {U}\nFrom\n{E}\nFrom\n{EXP}", self.ROOT)

class PW11UserCreation:
    """This can be used for accounts panel in settings menu AND as an OOBE agent"""
    def __init__(self, root: tkinter.Frame):
        self.root = root
        self.LSideFrame = tkinter.Frame(self.root, background=GLOBAL_VARS.THEME_WINDOW_BG,)
        self.LSideFrame.grid(row=0, column=0)
        self.RSideFrame = tkinter.Frame(self.root, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.LSide_UserListFrame = tkinter.Frame(self.LSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.LSide_UserListFrame.grid(row=0, column=0)
        self.LSide_NewUserBtn = tkinter.Button(self.LSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, text="Create a new user!", foreground=GLOBAL_VARS.THEME_FOREGROUND)
        self.LSide_NewUserBtn.grid(row=1, column=0)
        self.RSide_UserContentFrame = tkinter.Frame(self.RSideFrame, background=GLOBAL_VARS.THEME_WINDOW_BG)
        self.RSide_UserContentFrame.grid(row=0, column=0)
        self.USER_BUTTONS = []
        self.USER_PFPs = []
        USER_CONFIGS: list[list[str, str]] = []
        for file in Path(os.path.join(CWD, "ProgramFiles")).glob("accConfiguration*.conf"):
            with open(file, "r") as reader:
                usr, paswd = reader.readlines()
                usr = base64.urlsafe_b64decode(usr).decode("utf-8")
                USER_CONFIGS.append([usr, paswd])
        for i, user in enumerate(USER_CONFIGS):
            FILE_SYSTEM.loadConfig(os.path.join(CWD, "ProgramFiles", user[0], "USER_CONFIG"), user[0])
            config = FILE_SYSTEM.getConfig(user[0])
            IMG = Image.open(fp=config["PFP"])
            IMG = ImageTk.PhotoImage(IMG.resize(tuple((int(IMG.width/2), int(IMG.height/2)))))
            FILE_SYSTEM.unloadConfig(user[0])
            btn = tkinter.Button(self.LSide_UserListFrame, text=user[0], background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, image=IMG, compound="left")
            btn.grid(row=i, column=0)
            btn.INFO = user
            btn.IMG = IMG
            self.USER_PFPs.append(IMG)



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
    
def main():
    print("Loaded operating system!")
    def safeModePREPTask(e=None):
        ROOT_WINDOW.destroy()
        safeMode()
    global SYS_CONFIG
    FILE_SYSTEM.loadConfig(f"ProgramFiles/{GLOBAL_VARS.USERNAME}/USER_CONFIG", "USER_CONFIG")
    GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.getConfig("USER_CONFIG")
    GLOBAL_VARS.APPS_LIST, GLOBAL_VARS.COMMAND_APPS_LIST = GLOBAL_VARS.USER_CONFIG["APPS"]
    GLOBAL_VARS.THEME_WINDOW_BG, GLOBAL_VARS.THEME_FOREGROUND = GLOBAL_VARS.USER_CONFIG["THEME"]
    GLOBAL_VARS.PINNED_APPS = GLOBAL_VARS.USER_CONFIG["PINNED"][0]
    GLOBAL_VARS.PINNED_APPS_DESKTOP = GLOBAL_VARS.USER_CONFIG["PINNED"][1]
    print("Loaded apps and user settings!")
    ROOT_WINDOW = tkinter.Tk()
    ROOT_WINDOW.configure(background=GLOBAL_VARS.THEME_WINDOW_BG)
    loadAllIcons(GLOBAL_VARS.APPS_LIST, ROOT_WINDOW)
    loadAllIcons(["shutdown", "restart", "start"], ROOT_WINDOW)
    taskbarFrame = tkinter.Frame(ROOT_WINDOW, background=GLOBAL_VARS.THEME_WINDOW_BG)
    taskbarFrame.identifier = "taskbar"
    ROOT_WINDOW.identifier = "root_window"
    GLOBAL_VARS.ROOT_WINDOW = ROOT_WINDOW
    desktopFrame = tkinter.Frame(ROOT_WINDOW, background=GLOBAL_VARS.THEME_WINDOW_BG, border=15)
    if (GLOBAL_VARS.USER_CONFIG["WALLPAPER"]):
        image = GUIButtonCommand.getWallpaperImageResized(GLOBAL_VARS.USER_CONFIG["WALLPAPER"])
        ROOT_WINDOW.wallpaperImage = image
        GLOBAL_VARS.WALLPAPER = tkinter.Label(ROOT_WINDOW, image=image)
        GLOBAL_VARS.WALLPAPER.grid(row=1, column=0, sticky="EWSN")
        GLOBAL_VARS.WALLPAPER.identifier = "wallpaper"
    ROOT_WINDOW.grid_rowconfigure(1, weight=1)
    ROOT_WINDOW.grid_columnconfigure(0, weight=1)
    contextMenu = tkinter.Menu(taskbarFrame, tearoff=False, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
    contextMenu.add_command(label="Taskbar settings", command=GUIButtonCommand.taskbarselfGUI)
    contextMenu.identifier = "taskbar"
    def runningTaskbarAppsLOOP():  
        ROOT_WINDOW.after(300, runningTaskbarAppsLOOP)
        for widget in dict(runningAppsFrame.children).values():
            try:
                location = list(GLOBAL_VARS.RUNNING_APPS.keys()).index(widget.processInfo[0])
                widget.grid_configure(row=0, column=location)
                appNameReal = GUIButtonCommand.AppImportNameCheck(widget.processInfo[1])
                try: widget.configure(text=dwm.title(None, widget.processInfo[0]))
                except:
                    appImport = importlib.import_module(f"ProgramFiles.{appNameReal}")
                    widget.configure(text=appImport.returnInformation(widget.processInfo[0])['title'])
            except Exception as EXP: 
                print(EXP)
                widget.destroy()
    ROOT_WINDOW.after(300, runningTaskbarAppsLOOP)
    def recurringClockFunc():
            cr_time = time.strftime("%H:%M:%S %p")
            GLOBAL_VARS.CLOCK_LABEL = tkinter.Label(taskbarFrame, text=cr_time, background=GLOBAL_VARS.THEME_WINDOW_BG,
                                    foreground=GLOBAL_VARS.THEME_FOREGROUND)
    
            GLOBAL_VARS.CLOCK_LOOP_ID = GLOBAL_VARS.CLOCK_LABEL.after(1000, recurringClockFunc)
            GLOBAL_VARS.CLOCK_LABEL.grid(row=0, column=2, sticky="ne")
    try:
        if GLOBAL_VARS.USER_CONFIG["CLOCK-WIDGET"] == 1: recurringClockFunc()
    except: pass
    appsFrame = tkinter.Frame(taskbarFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, border=5)
    img = Image.open(os.path.join(CWD, "ProgramFiles/Icons/start.png"))
    img = img.resize((int(img.width/2), int(img.height/2)))
    img = ImageTk.PhotoImage(img)
    shutDown = tkinter.Button(taskbarFrame, text="Start", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND,
                                command=lambda: StartMenu(shutDown, taskbarFrame), image=img, compound="left")
    shutDown.img = img
    shutDown.grid(row=0, column=0, padx=5)
    tooltips.createToolTipAtGivenPos(shutDown, 1, ROOT_WINDOW, "Shutdown or restart the shell!", )
    appsFrame.grid(row=0, column=1, sticky="n")
    FILE_SYSTEM.RunAppsFrame = runningAppsFrame = GLOBAL_VARS.RUNNING_APPS_FRAME = tkinter.Frame(taskbarFrame, background=GLOBAL_VARS.THEME_WINDOW_BG, padx=10, border=5)
    runningAppsFrame.grid(row=0, column=4, sticky="n")
    notificationsButton = tkinter.Button(taskbarFrame, text="Notifications (0)", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command= lambda: notification.showNotificationsList(notification))
    notificationsButton.grid(row=0, column=3, sticky="ne", padx=5)
    GLOBAL_VARS.NOTIFICATION_BUTTON = notificationsButton
    GLOBAL_VARS.DESKTOP_FRAME = desktopFrame
    GLOBAL_VARS.APPS_FRAME = appsFrame
    GLOBAL_VARS.RUNNING_APPS_FRAME = runningAppsFrame
    desktopContextMenu = tkinter.Menu(appsFrame, tearoff=False, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
    desktopContextMenu.add_command(label="Refresh", command=GUIButtonCommand.refreshDesktop)
    desktopContextMenu.add_command(label="Add new icon", command=GUIButtonCommand.addNewIcon)
    GLOBAL_VARS.DESKTOP_CONTEXT_MENU = desktopContextMenu
    GLOBAL_VARS.TASKBAR_CONTEXT_MENU = contextMenu
    ROOT_WINDOW.bind("<Button-3>", GUIButtonCommand.OSContextMenuPopup)
    taskbarFrame.bind("<Button-3>", lambda event: GUIButtonCommand.standardisedContextMenuPopup(contextMenu, event))
    taskbarFrame.grid(row=0, column=0, sticky="EW")
    desktopFrame.grid(row=1, column=0, sticky="NW")
    desktopFrame.lift()
    
    ROOT_WINDOW.attributes('-fullscreen', True)
    ROOT_WINDOW.bind("<Escape>", safeModePREPTask)
    GUIButtonCommand.refreshDesktop()
    for app in GLOBAL_VARS.PINNED_APPS:
        try: GUIButtonCommand.pinApps(app, False)
        except Exception as EXP: messagebox.showerror("Error pinning app to taskbar", f"Error pinning {app} in the taskbar.\nPROB:{EXP}", root=ROOT_WINDOW)
    startUpTasks(GLOBAL_VARS.USER_CONFIG, ROOT_WINDOW)
    FILE_SYSTEM.ROOT = ROOT_WINDOW
    ROOT_WINDOW.mainloop()
import base64
def loginVerification(userNameText: tkinter.Entry, passwordText: tkinter.Entry, userNum: tkinter.Entry,  loginWindow: tkinter.Tk, e=None):
    print("Checking credentials")
    try:
        if int(userNum.get()) != 0:
            with open(f"ProgramFiles/accConfiguration{userNum.get()}.conf", "r") as verify:
                GLOBAL_VARS.USERNAME, password = verify.readlines()
                GLOBAL_VARS.USERNAME = base64.urlsafe_b64decode(GLOBAL_VARS.USERNAME.rstrip('\n')).decode('utf-8')
                password = base64.urlsafe_b64decode(password.rstrip('\n')).decode('utf-8')
                if userNameText.get() == GLOBAL_VARS.USERNAME and passwordText.get() == password:
                    loginWindow.destroy()
                    try:
                        main()
                    except Exception as EXP: bsod(main, f"DESKTOP_LAUNCH_ERROR('{EXP}')")
                else:
                    messagebox.showerror(None, None, loginWindow, True, "LOGIN_INCORRECT")
        else:
            loginWindow.destroy()
            GLOBAL_VARS.USERNAME = "GUEST"
            try:
                os.mkdir("ProgramFiles/GUEST")
            except FileExistsError:
                # The user data somehow exists? let's use that then!
                pass # pass for now!
            try:
                main()
            except Exception as EXP: bsod(main, f"DESKTOP_LAUNCH_ERROR('{EXP}')")
    except Exception as EXP:
        messagebox.showerror("loginVerification Error!", EXP)

DARK_COLOURS = ["black", 'brown', 'blue', 'green', 'red', 'violet', 'purple', 'dark blue', 'dark green',
                'dark red', 'dark brown', ]
def login():
    print("Starting up OS...")
    global SYS_CONFIG
    SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)
    def safeModePREPTask(e=None):
        global SYS_CONFIG
        SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)
        msg.destroy()
        msg2.destroy()
        userNameText.destroy()
        passwordText.destroy()
        loginBtn.destroy()
        shutdownBtn.destroy()
        loginWindow.destroy()
        safeMode()
    loginWindow = tkinter.Tk()
    loginWindow.title("Login to Windows 11")
    loginWindow.configure(background=GLOBAL_VARS.THEME_WINDOW_BG)
    loadAllIcons(["shutdown", "restart"], loginWindow)
    msg = tkinter.Label(loginWindow, text="Enter your Username: ", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
    msg.grid(row=0, column=0)
    userNameText = tkinter.Entry(loginWindow, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
    userNameText.grid(row=0, column=1)
    userNameText.focus()
    userNameText.configure(insertbackground=GLOBAL_VARS.THEME_FOREGROUND, selectbackground=GLOBAL_VARS.THEME_FOREGROUND, selectforeground=GLOBAL_VARS.THEME_WINDOW_BG)
    msg2 = tkinter.Label(loginWindow, text="Enter your Password", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
    msg2.grid(row=1, column=0)
    passwordText = tkinter.Entry(loginWindow, foreground=GLOBAL_VARS.THEME_FOREGROUND, background=GLOBAL_VARS.THEME_WINDOW_BG, show="*")
    passwordText.grid(row=1, column=1)
    passwordText.configure(insertbackground=GLOBAL_VARS.THEME_FOREGROUND, selectbackground=GLOBAL_VARS.THEME_FOREGROUND, selectforeground=GLOBAL_VARS.THEME_WINDOW_BG)
    def passwordTextFocus(*e): passwordText.focus()
    userNameText.bind("<Tab>", passwordTextFocus)
    userNameText.bind("<Return>", lambda: passwordTextFocus)
    msg3 = tkinter.Label(loginWindow, text="Enter your user number", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND)
    userNum = tkinter.Entry(loginWindow, foreground=GLOBAL_VARS.THEME_FOREGROUND, background=GLOBAL_VARS.THEME_WINDOW_BG)
    userNum.grid(row=2, column=1)
    userNum.configure(insertbackground=GLOBAL_VARS.THEME_FOREGROUND, selectbackground=GLOBAL_VARS.THEME_FOREGROUND, selectforeground=GLOBAL_VARS.THEME_WINDOW_BG)
    msg3.grid(row=2, column=0)
    userNum.bind("<Return>", lambda e=None: loginVerification(userNameText, passwordText, userNum, loginWindow))
    loginBtn = tkinter.Button(loginWindow, text="Login", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND,
                                command=lambda e=None: loginVerification(userNameText, passwordText, userNum, loginWindow))
    loginBtn.grid(row=3, column=1)
    shutdownBtn = tkinter.Button(loginWindow, text="Shutdown", background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND,
                                command=lambda: GUIButtonCommand.shutdownMenu(loginWindow))
    shutdownBtn.grid(row=0, column=GLOBAL_VARS.MAX_COLUMN_DESKTOP)
    loginWindow.attributes('-fullscreen', True)
    loginWindow.bind("<Escape>", safeModePREPTask)
    loginWindow.mainloop()
def autoRecoveryEnv() -> None:
    recoveryWin = tkinter.Tk()
    recoveryWin.configure(background="Black")
    recoveryWin.attributes("-fullscreen", True)
    def launchCmd(e=None): import ProgramFiles.commandprompt; ProgramFiles.commandprompt.main("AUTORECOVERYENV", None, None, [None, None], None, None, random.randint(1000, 9999), None)
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
    try:
        loadAllIcons(["continue", "repair", "commandprompt"], recoveryWin)
        continueICON = GLOBAL_VARS.ICONS["continue"]
        continueBTN = tkinter.Button(recoveryWin, image=continueICON, background=GLOBAL_VARS.THEME_WINDOW_BG, foreground=GLOBAL_VARS.THEME_FOREGROUND, command=login, text='Continue to main', compound=tkinter.LEFT)
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
            userToreset = input("Enter the GLOBAL_VARS.USERNAME of the user to reset the user too... [Type in defaultuser0 to only do system wise reset]")
            if userToreset.lower() != "defaultuser0":
                try:
                    with shelve.open(f"ProgramFiles/{userToreset}/USER_CONFIG") as deleteIt: deleteIt.clear()
                except Exception as exp:
                    print(f"ERROR OCCURED While resetting...!Error: {exp}")
            try:
                shelveFilesToDelete = ["ProgramFiles/history", "ProgramFiles/IPChat/_serverConfig", "ProgramFiles/IPChat/serversList"]
                for shelveToDelete in shelveFilesToDelete:
                    try:
                        with shelve.open(shelveToDelete) as deleteIt:
                            deleteIt.clear()
                    except Exception: pass
            except Exception as exp:
                print(f"ERROR OCCURED While resetting...!Error: {exp}")
        print("=" * int(os.get_terminal_size()[0]))
        if NETWORKING:
            onlineOrOffline = input("Do you want to perform online repair? [Y/N](Y for online, N for offline, A for abort)")
            if onlineOrOffline == "Y" or onlineOrOffline == 'y':
                print("repairing system...")
                try:
                    Windows11MainDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/Windows 11.py", timeout=40)
                    resetConfigurations()
                    with open("Windows 11.py", "w") as writeTo:
                        try:
                            writeTo.write(Windows11MainDownload.content.decode(encoding="UTF-8"))
                        except UnicodeEncodeError as UER:
                            print(f"UnicodeDecodeError occured while repairing 'Windows 11.py'\n--MSG:{UER}")
                except Exception as PROBLEM:
                    print(f"Repairing Failed!\n<<<REASON: {PROBLEM}")
                finally:
                    print("=" * int(os.get_terminal_size()[0]))
            elif onlineOrOffline == "N" or onlineOrOffline == "n":
                print("Resetting your system!")
                resetConfigurations()
                print("=" * int(os.get_terminal_size()[0]))
            else:
                print("=" * int(os.get_terminal_size()[0]))
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
            os.system("""python "Windows 11.py" -safemode """)
            exit()
        else: 
            os.system("""python "Windows 11.py" """)
            print("=" * int(os.get_terminal_size()[0]))
            exit()
    def a6():
        print("=" * int(os.get_terminal_size()[0]))
        nonlocal NETWORKING
        try: requests.get("http://theoldnet.com")
        except Exception as prob: print(f"Operation failed!\nReason: {prob}")
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

if __name__ == "__main__":
    arguements = sys.argv[1:]
    if not os.access("ProgramFiles", os.F_OK): bsod(login, "MODULE_NOT_FOUND_ERROR('The required modules inside ProgramFiles folder doesn't exist!')")
    else:
        if not os.access("ProgramFiles/commandprompt.py", os.F_OK) or not os.access("ProgramFiles/errorHandler.py", os.F_OK): bsod(login, "MODULE_NOT_FOUND_ERROR('The required modules inside ProgramFiles folder doesn't exist!')")
        else:
            if "-safemode" in arguements: safeMode()
            elif "-safemodecli" in arguements: safeMode(True, True)
            elif "-safemodefullcmd" in arguements: safeMode(True)
            elif "-config" in arguements:
                GLOBAL_VARS.USERNAME = input("Enter the GLOBAL_VARS.USERNAME to create first run settings: ")
                password = input("Enter your user's password: ")
                foreground = input("Enter your user's preffered foreground colour: ")
                background = input("Enter your user's preffered background colour: ")
                userNumber = input("Enter your user's wanted user number (can be any number): ")
                import shelve
                FILE_SYSTEM.loadConfig("ProgramFiles/SYS_CONFIG", "SYS_CONFIG")
                SYS_CONFIG = FILE_SYSTEM.getConfig("SYS_CONFIG")
                try:
                    with open(f"ProgramFiles/accConfiguration{userNumber}.conf", "wb") as WRITE:
                        Rusername= base64.urlsafe_b64encode(GLOBAL_VARS.USERNAME.encode("utf-8"))
                        Rpassword = base64.urlsafe_b64encode(password.encode("utf-8"))
                        WRITE.writelines([Rusername, "\n".encode("utf-8"),  Rpassword])
                    os.mkdir(f"ProgramFiles/{GLOBAL_VARS.USERNAME}")
                except Exception: print("User already exists, skipping user creation tasks...")
                finally:
                    FILE_SYSTEM.loadConfig(f"ProgramFiles/{GLOBAL_VARS.USERNAME}/USER_CONFIG", "USER_CONFIG")
                    GLOBAL_VARS.USER_CONFIG = FILE_SYSTEM.getConfig("USER_CONFIG")
                try: 
                    try: 
                        os.mkdir(f"Users")
                        os.mkdir(f"Users/{GLOBAL_VARS.USERNAME}")
                    except: 
                        try: os.mkdir(f"Users/{GLOBAL_VARS.USERNAME}")
                        except: pass
                    for i in USER_FOLDERS_LIST: os.mkdir(f"Users/{GLOBAL_VARS.USERNAME}/{i}")
                except Exception: print("User folders already exist, skipping...")
                FILE_SYSTEM.editConfig("USER_CONFIG", "APPS", [["Command Prompt", "Load External Apps", "Notepad", "Web Browser", "Update Manager", "IP Chat", "File Manager", "Software Store", "File Share", "Black Jack", "Alarms and Timer", "Photo Viewer", "Control Panel", "Task Manager"], ["ProgramFiles.alarmsandtimer", "ProgramFiles.blackjack", "ProgramFiles.commandprompt", "ProgramFiles.loadexternalapps", "ProgramFiles.ipchat", "ProgramFiles.notepad", "ProgramFiles.webbrowser", "ProgramFiles.updatemanager", "ProgramFiles.fileshare", "ProgramFiles.filemanager", "ProgramFiles.softwarestore", "ProgramFiles.photoviewer", "ProgramFiles.controlPanel", "ProgramFiles.taskManager"]])
                FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", [["File Manager"], ["Notepad", "File Manager"]])
                FILE_SYSTEM.editConfig("USER_CONFIG", "THEME", [background, foreground])
                FILE_SYSTEM.editConfig("USER_CONFIG", "CLOCK-WIDGET", 0)
                FILE_SYSTEM.editConfig("USER_CONFIG", "DEFAULTAPPASSOCIATION", {"txt": "Notepad", "jpg": "Photo Viewer", "png": "Photo Viewer"})
                FILE_SYSTEM.editConfig("USER_CONFIG", "WALLPAPER", None)
                FILE_SYSTEM.editConfig("USER_CONFIG", "STARTUP_APPS", [])
                FILE_SYSTEM.editConfig("USER_CONFIG", "PFP", os.path.join(CWD, "ProgramFiles/Icons/defaultpfp.png"))
                FILE_SYSTEM.editConfig("SYS_CONFIG", "THEME", ["Black", "White"]) 
                FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)
                print("Initialized new entries!")
            elif "-configchange" in arguements:
                print("You have entered the configuration manager! Press CTRL+C anytime to exit!\n")
                configchoice = input("System or User config change?")
                if "system" in configchoice.lower():
                    infoSysSelectSTR = "SYS_CONFIG"
                    SYS_CONFIG = shelve.open("ProgramFiles/SYS_CONFIG", writeback=True)
                else:
                    infoSysSelectSTR = "USER_CONFIG"
                    GLOBAL_VARS.USERNAME = input("Type in the GLOBAL_VARS.USERNAME whose settings are going to be changed!: ")
                    GLOBAL_VARS.USER_CONFIG = shelve.open(f"ProgramFiles/{GLOBAL_VARS.USERNAME}/USER_CONFIG", writeback=True)
                print("The respective configuration module has been imported!\n"
                        f"Now, type in 'GLOBAL_VARS.{infoSysSelectSTR}[<CONFIG_NAME>] = <CONFIG>;' and then press enter to finish\n"
                        "New code lines and line endings MUST BE represented by the ; character!")
                code_to_execute = input("Start here>")
                for i, code in enumerate(code_to_execute.split(";")):
                    try: exec(code)
                    except Exception as PROB: print(f"Error has occured! Error: {PROB}\n\nRestart the system with the same parameter to enter this mode!")
                    else: print(f"Line {i+1} executed successfully! Reboot your system and observe whether the changes applied correctly!")
                    
            else:
                try:
                    import tkinter
                    from ProgramFiles.errorHandler import messagebox
                    import requests
                    if SYS_CONFIG["CBSRESTARTATTEMPT"] > 3:
                        try: autoRecoveryEnv()
                        except: safeMode()
                except Exception as PROBLEM:
                    try:
                        import platform
                        if platform.system() == "Windows": os.system("cls")
                        else:  os.system("clear")
                    except Exception: pass
                    print(f"Safe mode activated due to one of the modules not present. \n DEBUG: {PROBLEM}")
                    time.sleep(5)
                    safeMode()
                else:
                    try: login()
                    except Exception as EXP: bsod(login, f"LOGIN_FAILURE('{EXP}')")
