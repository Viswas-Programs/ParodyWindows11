import tkinter
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
            bsodWind.geometry("600x480")
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
    from PIL import Image, ImageTk
    import psutil
    from ProgramFiles.fileaskhandlers import askopenfilename
    from ProgramFiles.buttons import IconButton
except Exception as E: 
    bsod(__name__, str(E) + "\nMODULE_NOT_FOUND_ERROR")
CWD = os.getcwd()
FILE_SYSTEM = ParWFS.ParWFS()
FILE_SYSTEM.loadConfig("ProgramFiles/SYS_CONFIG", "SYS_CONFIG")
SYS_CONFIG = FILE_SYSTEM.getConfig("SYS_CONFIG")
try:
    THEME_WINDOW_BG, THEME_FOREGROUND = SYS_CONFIG["THEME"]
except Exception:
    THEME_WINDOW_BG = "Black"
    THEME_FOREGROUND = "White"
print("Starting OS...")
RUNNING_APPS = FILE_SYSTEM.RUNNING_APPS
ICONS = {}
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
def giveIcon(appName: str, root):
    global ICONS
    try:
        return ICONS[appName]
    except Exception as exp:
        print(exp, ICONS.keys())
        return tkinter.PhotoImage(file=f"ProgramFiles/Icons/{appName}.png", master=root)
def loadAllIcons(appsList: list, root):
    global ICONS
    for app in appsList:
        realApp = GUIButtonCommand.AppImportNameCheck(app)
        try:
            ICONS[realApp] = tkinter.PhotoImage(file=f"ProgramFiles/Icons/{realApp}.png", master=root)
        except: pass
ROW_COUNT_NOTIFICATION_WINDOW = 0
class Notifications(object):
    global ROW_COUNT_NOTIFICATION_WINDOW
    global notificationsButton
    global notificationsWindow
    def __init__(self):
        self.NotificationsList = []
        self.TimeofNotification = []
        self.actions = []
    def createNotification(self, msg: str, time: str, action: str):
        global ROW_COUNT_NOTIFICATION_WINDOW
        self.NotificationsList.append(msg)
        self.TimeofNotification.append(time)
        self.actions.append(action)
        ROW_COUNT_NOTIFICATION_WINDOW += 1
        notificationsButton.configure(text=f"Notifications ({len(self.NotificationsList)})")
    def showNotification(self, title: str, msg: str, time: str, action: str) -> None:
        from ProgramFiles.errorHandler import messagebox
        self.createNotification(msg=msg, time=time, action=action)
        messagebox.showinfo(title, msg, ROOT_WINDOW)
    def showNotificationsList(self, event=None):
        global notificationsWindow
        notificationsWindow = tkinter.Toplevel(background=THEME_WINDOW_BG)
        notificationsButton.configure(text="Notifications (0)")
        if len(self.NotificationsList) == 0:
            a = tkinter.Label(notificationsWindow, text="No notifications (yet)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            a.grid(row=0, column=0)
        for index, notif in enumerate(self.NotificationsList):
            exec(f'a{index} = tkinter.Label(notificationsWindow, text=f"{notif}\t: {self.TimeofNotification[index]}", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)')
            exec(f'a{index}.grid(row=index, column=0)')
            exec(f"a{index}.bind('<Button-1>', self.actions[index])")
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
        self.settingsWindow = tkinter.Toplevel(ROOT_WINDOW, background=THEME_WINDOW_BG)
        PID = random.randint(CONTROL_PANELS[0], CONTROL_PANELS[1])
        while PID in RUNNING_APPS.keys():
            PID = random.randint(CONTROL_PANELS[0], CONTROL_PANELS[1])
        RUNNING_APPS[PID] = "Control Panel"
        dwm.createTopFrame(self.settingsWindow, THEME_FOREGROUND, THEME_WINDOW_BG, "settings", "Control Panel", PID)
        GUIButtonCommand.createRunningAppTaskbarIcon("settings", PID)
        btnFrame = tkinter.Frame(self.settingsWindow, background=THEME_WINDOW_BG)
        btnFrame.grid(row=1, column=0)
        homeBtn = tkinter.Button(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Home", command=self.homePage)
        homeBtn.grid(row=0, column=0)
        personalizeBtn = tkinter.Button(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Personalization", command=self.personalization)
        personalizeBtn.grid(row=1, column=0)
        appOpenerChangeBtn = tkinter.Button(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="App Associations", command=self.changeFileOpeners)
        appOpenerChangeBtn.grid(row=2, column=0)
        self.setting = tkinter.Frame(self.settingsWindow, background=THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
    def homePage(self):
        if self.SHOWN_PERSONALIZATION or self.SHOWN_APPSLIST or self.SHOWN_APPOPENERCHANGER: self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        self.SHOWN_HOMEPAGE = True
        infoText = f""" Windows 11 v2.3.5\nSystem RAM: {self.total_memory}\nBackground={THEME_WINDOW_BG}\n"""
        f"""Foreground={THEME_FOREGROUND}\n\nFor more info, please visit the respective categories! Thank you :)"""
        a = tkinter.Label(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=infoText).grid(row=0, column=0)
    def personalization(self):
        self.SHOWN_PERSONALIZATION = True
        def changeBg():
            global children
            global THEME_WINDOW_BG
            global  USER_CONFIG, SYS_CONFIG
            colorToUse = colorchooser.askcolor(title="Select background!")
            THEME_WINDOW_BG = colorToUse[1]
            crBg.configure(text=f"Current Background = {THEME_WINDOW_BG}")
            if systemChangeTheme.get(): 
                SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "THEME", [THEME_WINDOW_BG, THEME_FOREGROUND])
            USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "THEME", [THEME_WINDOW_BG, THEME_FOREGROUND])
            for child in children:
                try:
                    child.configure(background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                    ROOT_WINDOW.configure(background=THEME_WINDOW_BG,)
                    appsFrame.configure(background=THEME_WINDOW_BG)
                    desktopFrame.configure(background=THEME_WINDOW_BG)
                except Exception: pass
            ROOT_WINDOW.update()
        def changeFg():
            global children
            global THEME_FOREGROUND
            global  USER_CONFIG, SYS_CONFIG
            colorToUse = colorchooser.askcolor(title="Select foreground!")
            THEME_FOREGROUND = colorToUse[1]
            crFg.configure(text=f"Current foreground = {THEME_FOREGROUND}")
            if systemChangeTheme.get(): 
                SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "THEME", [THEME_WINDOW_BG, THEME_FOREGROUND])
            USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "THEME", [THEME_WINDOW_BG, THEME_FOREGROUND])
            for child in children:
                try:
                    child.configure(background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                    ROOT_WINDOW.configure(background=THEME_WINDOW_BG,)
                except Exception: pass
            ROOT_WINDOW.update()
        def changeWallpaper():
            global wallpaper
            nonlocal wallpaperText
            global USER_CONFIG
            wallpaperChoose = askopenfilename("Open a wallpaper file (png)", (("PNG Files", "*.png"), ("All Files", "*.*")))
            img = GUIButtonCommand.getWallpaperImageResized(wallpaperChoose)
            ROOT_WINDOW.image = img
            try:
                wallpaper.configure(image=img)

            except: 
                wallpaper = tkinter.Label(ROOT_WINDOW, image=img)
                wallpaper.grid(row=1, column=0, sticky="EWSN")
            desktopFrame.lift()
            wallpaperText = "Current Wallpaper: " + wallpaperChoose
            wallpaperPath.configure(text=wallpaperText)
            USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "WALLPAPER", wallpaperChoose)
        def removeWallpaper():
            nonlocal wallpaperText
            global USER_CONFIG
            USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "WALLPAPER", None)
            try: 
                wallpaper.destroy()
            except: pass
            wallpaperText = "Current Wallpaper: No wallpapers set yet!"
            wallpaperPath.configure(text=wallpaperText)
        if self.SHOWN_HOMEPAGE or self.SHOWN_ADVANCED or self.SHOWN_PERSONALIZATION or self.SHOWN_APPOPENERCHANGER: self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        crBg = tkinter.Label(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=f"Current Background = {THEME_WINDOW_BG}")
        crBg.grid(row=0, column=0)
        changeBackground = tkinter.Button(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Change Background!", command=changeBg)
        changeBackground.grid(row=0, column=1)
        crFg = tkinter.Label(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=f"Current foreground = {THEME_FOREGROUND}")
        crFg.grid(row=1, column=0)
        changeForeground = tkinter.Button(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Changr foreground!", command=changeFg)
        changeForeground.grid(row=1, column=1)
        ttk.Style(self.settingsWindow).configure("TCheckbutton", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        systemChangeTheme = tkinter.IntVar()
        applyToSystem = ttk.Checkbutton(self.setting, text="Also apply changes to system theme!", variable=systemChangeTheme)
        applyToSystem.grid(row=2, column=0)
        wallpaperText = "Current Wallpaper: "
        if USER_CONFIG["WALLPAPER"]: wallpaperText += USER_CONFIG["WALLPAPER"]
        else: wallpaperText += "No wallpapers set yet!"
        wallpaperPath = tkinter.Label(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=wallpaperText)
        wallpaperPath.grid(row=3, column=0)
        changeWallpaperButton = tkinter.Button(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Change Wallpaper", command=changeWallpaper)
        changeWallpaperButton.grid(row=3, column=1)
        removeWallpaperButton = tkinter.Button(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Remove Wallpaper", command=removeWallpaper)
        removeWallpaperButton.grid(row=4, column=1)
    def changeFileOpeners(self, reLaunch=False):
        def __internals_AddNewEntry(*args):
            def __internals_AddNewEntry_AddAppNames(*args):
                global USER_CONFIG
                app = comboBox.get()
                try: 
                    extension = textAssociationEntry.get()
                    CurrentConfig: dict = USER_CONFIG["DEFAULTAPPASSOCIATION"]
                    CurrentConfig.update({extension: app})
                    USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "DEFAULTAPPASSOCIATION", CurrentConfig)
                    self.changeFileOpeners(True)
                except Exception as I:
                    messagebox.showerror('Error changing default app association', f'Error changing default app association.\nProb: {I}', addNewEntryWn )
            addNewEntryWn = tkinter.Toplevel(self.settingsWindow)
            nEntFrm = tkinter.Frame(addNewEntryWn, background=THEME_WINDOW_BG)
            nEntFrm.grid(row=0, column=0)
            textAssociationEntry = tkinter.Entry(nEntFrm, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            textAssociationEntry.grid(row=0, column=0)
            comboBox = ttk.Combobox(nEntFrm)
            comboBox['values'] = APPS_LIST
            comboBox['state'] = "readonly"
            comboBox.bind("<<ComboboxSelected>>", __internals_AddNewEntry_AddAppNames)
            comboBox.grid(row=0, column=1)
            addNewEntryWn.mainloop()
        self.SHOWN_APPOPENERCHANGER = True
        if self.SHOWN_HOMEPAGE or self.SHOWN_ADVANCED or self.SHOWN_PERSONALIZATION or reLaunch: self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=THEME_WINDOW_BG)
        self.setting.grid(row=1, column=1)
        addEntryBtn = tkinter.Button(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Add New Entry", command=__internals_AddNewEntry)
        addEntryBtn.grid(row=0, column=0)
        for X, i in enumerate(dict(USER_CONFIG["DEFAULTAPPASSOCIATION"]).keys()):
            exec(f""" 
innerFrame{X} = tkinter.Frame(frame, background=THEME_WINDOW_BG)
innerFrame{X}.grid(row=X+1, column=0)
label{X} = tkinter.Label(innerFrame{X}, text=i, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
label{X}.grid(row=0, column=0)
def changeDefAppEvent{X}(e=None):
    global comboBox{X}
    app = comboBox{X}.get()
    try: 
        CurrentConfig: dict = USER_CONFIG["DEFAULTAPPASSOCIATION"]
        CurrentConfig.update({"{i: app}"})
        USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "DEFAULTAPPASSOCIATION", CurrentConfig)
    except Exception as I:
        messagebox.showerror('Error changing default app association', 'Error changing default app association.', root_wn )
global comboBox{X}
comboBox{X} = ttk.Combobox(innerFrame{X})
comboBox{X}['values'] = APPS_LIST
comboBox{X}['state'] = "readonly"
comboBox{X}.bind("<<ComboboxSelected>>", changeDefAppEvent{X})
comboBox{X}.grid(row=0, column=1)
""", {"root_wn": self.settingsWindow, "frame": self.setting, "USER_CONFIG": USER_CONFIG, "tkinter": tkinter, "THEME_WINDOW_BG": THEME_WINDOW_BG, "THEME_FOREGROUND": THEME_FOREGROUND, "messagebox": messagebox, "ttk": ttk, "i": i, "X": X, "APPS_LIST": APPS_LIST})
    
ROW_COUNT_DESKTOP_ICONS = 0
COLUMN_COUNT_DESKTOP_ICONS = 0
MAX_ROW_DESKTOP = 10
MAX_COLUMN_DESKTOP = 15
class GUIButtonCommand:
    global launcherComboBox
    global APPS_LIST
    global PINNED_APPS
    global ROW_COUNT_DESKTOP_ICONS
    global COLUMN_COUNT_DESKTOP_ICONS
    global MAX_COLUMN_DESKTOP
    global MAX_ROW_DESKTOP
    global RUNNING_APPS
    def __init__(self, PINNED_APPS):
        self.CurrentDesktopIconsList = []
        self.PINNED_APPS = PINNED_APPS
        self.TASKBAR_ICON_COUNT = 0
    @staticmethod
    def launchItem(application: str, params= None, e=None): 
        global RUNNING_APPS, runningAppsFrame
        if application == "Command Prompt":
            import ProgramFiles.commandprompt as CMD
            appToLaunchPID = random.randint(a=PROCESS_IDS[0], b=PROCESS_IDS[1])
            while appToLaunchPID in RUNNING_APPS.keys():
                appToLaunchPID = random.randint(a=PROCESS_IDS[0], b=PROCESS_IDS[1])
            RUNNING_APPS[appToLaunchPID] = application
            GUIButtonCommand.createRunningAppTaskbarIcon(application, appToLaunchPID)
            try: CMD.main(FILE_SYSTEM, username, notification, None, FILE_SYSTEM.getConfig("USER_CONFIG"), appToLaunchPID, [runningAppsFrame, RUNNING_APPS] )
            except: CMD.main(FILE_SYSTEM, username, notification, None, dict({"THEME": ["Black", "White"]}), appToLaunchPID, [runningAppsFrame, RUNNING_APPS] )        
        else: 
            appToLaunch = GUIButtonCommand.AppImportNameCheck(app=application)
            progAppImport = f"{COMMAND_APPS_LIST[COMMAND_APPS_LIST.index(f'ProgramFiles.{appToLaunch}')]}"
            exec(f"import {progAppImport}")
            exec(f"{appToLaunch}PID = random.randint(1000, 9999)")
            exec(f"""
while {appToLaunch}PID in RUNNING_APPS.keys():
    {appToLaunch}PID = random.randint(a=PROCESS_IDS[0], b=PROCESS_IDS[1])
RUNNING_APPS[{appToLaunch}PID] = application""")
            exec(f"GUIButtonCommand.createRunningAppTaskbarIcon(application, {appToLaunch}PID)")
            exec(f"""if {progAppImport}.NEEDS_FILESYSTEM_ACCESS:
    if (params == None ): ProgramFiles.{appToLaunch}.main(FILE_SYSTEM, username, notification, {params},  FILE_SYSTEM.getConfig("USER_CONFIG"), {appToLaunch}PID)
    else:   ProgramFiles.{appToLaunch}.main(FILE_SYSTEM, username, notification, '{params}',  FILE_SYSTEM.getConfig("USER_CONFIG"), {appToLaunch}PID)
else:
    if (params == None ): ProgramFiles.{appToLaunch}.main(username, notification, {params},  FILE_SYSTEM.getConfig("USER_CONFIG"), {appToLaunch}PID)
    else:   ProgramFiles.{appToLaunch}.main(username, notification, '{params}',  FILE_SYSTEM.getConfig("USER_CONFIG"), {appToLaunch}PID)
        """)
    def launchComboBoxEvent(self, e=None):
        Item = launcherComboBox.get()
        if Item == "Control Panel":
            settings()
        elif Item == "Task Manager":
            TaskManager(ROOT_WINDOW)
        else:
            self.launchItem(Item)
    @staticmethod
    def createRunningAppTaskbarIcon(app: str, PID:int):
        realApp = GUIButtonCommand.AppImportNameCheck(app=app)
        print(RUNNING_APPS, len(RUNNING_APPS))
        exec(f"""
def focus():
    try:
        dwm.focus({PID})
    except:
        print("DWM NOT EXISTING IN APP")
        import ProgramFiles.{realApp}
        if ProgramFiles.{realApp}.returnInformation({PID})["state"] == "normal": ProgramFiles.{realApp}.focusOut({PID})
        else: ProgramFiles.{realApp}.focusIn({PID})
{realApp}ICON = giveIcon('{realApp}', ROOT_WINDOW).subsample(2, 2)
taskBar{realApp}RnAppBtn = tkinter.Button(runningAppsFrame, text='{app}', background='{THEME_WINDOW_BG}', foreground='{THEME_FOREGROUND}', command=focus, image={realApp}ICON, compound='left')
taskBar{realApp}RnAppBtn.grid(row=0, column={len(RUNNING_APPS)})
taskBar{realApp}RnAppBtn.processInfo = (PID, '{app}')
taskBar{realApp}RnAppBtn.windowInfo = 'focusIn'
""", {"tkinter": tkinter, "runningAppsFrame": runningAppsFrame, "GUIButtonCommand": GUIButtonCommand, "random":random, "RUNNING_APPS": RUNNING_APPS, "PID": PID, "ROOT_WINDOW": ROOT_WINDOW, "ICONS": ICONS, "dwm": dwm, "giveIcon": giveIcon})
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
    def currentTime(self):
        global clock
        global ClockRepeatID
        global USER_CONFIG
        cr_time = None
        if USER_CONFIG["CLOCK-WIDGET"] == 0:
            def recurringClockFunction(e=None):
                global ClockRepeatID
                nonlocal cr_time
                cr_time = time.strftime("%H:%M:%S %p")
                clock = tkinter.Label(ROOT_WINDOW, text=cr_time, background=THEME_WINDOW_BG,
                                        foreground=THEME_FOREGROUND)
                ClockRepeatID = clock.after(1000, recurringClockFunction)
                clock.grid(row=0, column=2, sticky="ne")
            USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "CLOCK-WIDGET", 1)
            recurringClockFunction()

        else:
            try: 
               cr_time = None
               clock.after_cancel(ClockRepeatID)
               clock.destroy()
               USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "CLOCK-WIDGET", 0)
            except Exception as E:
                messagebox.showerror("Can't destroy clock widget!", f"Can't destroy clock widget due to the following reason: \n {E}")
    def pinApps(self, appToPin, writeto=True):
        global appsFrame
        global USER_CONFIG
        appName: str = appToPin
        appName = GUIButtonCommand.AppImportNameCheck(appToPin)
        self.TASKBAR_ICON_COUNT += 1
        exec(f"global {appName}BTN")
        
        if writeto:
            apList = USER_CONFIG["PINNED"]
            apList[0].append(appName)
            USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", apList)
        exec(f"global {appName}ICON")
        exec(f"{appName}ICON = ICONS['{appName}'].subsample(2, 2)")
        exec(f"{appName}BTN = tkinter.Button(appsFrame, image={appName}ICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: GuiInterfaceCommands.launchItem(f'{appToPin}'))")
        exec(f"{appName}BTN.IMGREF = {appName}ICON")
        exec(f"{appName}BTN.grid(row=0, column={self.TASKBAR_ICON_COUNT})")

    def taskbarselfGUI(self, e=None):
        global PINNED_APPS
        global GuiInterfaceCommands
        taskbarselfWindow = tkinter.Toplevel(ROOT_WINDOW)
        taskbarselfWindow.configure(background=THEME_WINDOW_BG)
        taskbarselfWindow.title("Taskbar app pinning")
        addWidgetsFrame = tkinter.LabelFrame(taskbarselfWindow, text="Add widgets", 
                                            background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        addWidgetsFrame.grid(row=0, column=0)
        addClock = tkinter.Button(addWidgetsFrame, text="Clock", foreground=THEME_FOREGROUND,
                                    background=THEME_WINDOW_BG, command=self.currentTime)
        addClock.grid(row=0, column=0)
        pinItems = tkinter.LabelFrame(taskbarselfWindow, text="Pin items",
                                        background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        pinItems.grid(row=1, column=0)
        r = -1
        PINNED_APPS = list(PINNED_APPS)
        for app in APPS_LIST:
            if app not in PINNED_APPS:
                r += 1
                if len(PINNED_APPS) == 1 or len(PINNED_APPS) == 2:
                    i = 0
                appN = app.replace(" ", "")
                exec(f"{appN} = tkinter.Button(pinItems, text='{appN}', background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: GuiInterfaceCommands.pinApps('{app}'),"
                    f")\n{appN}.grid(row=r, column=0)")
        taskbarselfWindow.mainloop()

    def popup(self, event=None, *args):
        """ the context menu popup"""
        try:
            contextMenu.tk_popup(event.x_root, event.y_root, 0)
            print(contextMenu.grab_status())
            contextMenu.grab_set()
            contextMenu.grab_release()
        except Exception as PROBLEM:
            print(PROBLEM)
    def createAppIcon(self, appName: str, command: str, writeto=True, event=None):
        """ creates desktop icons!"""
        global desktopFrame
        global COLUMN_COUNT_DESKTOP_ICONS, ROW_COUNT_DESKTOP_ICONS
        global USER_CONFIG
        if ROW_COUNT_DESKTOP_ICONS > MAX_ROW_DESKTOP:
            if COLUMN_COUNT_DESKTOP_ICONS > MAX_COLUMN_DESKTOP:
                messagebox.showerror("Desktop pin", "Can't place the item! no more space left!", ROOT_WINDOW)
            else:
                COLUMN_COUNT_DESKTOP_ICONS += 1
        if appName not in self.CurrentDesktopIconsList:
            if writeto:
                apList = USER_CONFIG["PINNED"]
                apList[1].append(appName)
                USER_CONFIG = FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", apList)
            realAppName = GUIButtonCommand.AppImportNameCheck(app=appName)
            exec(f"{realAppName}Frame = tkinter.Frame(desktopFrame, background=THEME_WINDOW_BG)")
            exec(f"{realAppName}Frame.grid(row=ROW_COUNT_DESKTOP_ICONS, column=COLUMN_COUNT_DESKTOP_ICONS)")
            ROW_COUNT_DESKTOP_ICONS += 1
            exec(f"{realAppName}ICON = ICONS['{realAppName}']")
            exec(f"{realAppName}BTN = IconButton({realAppName}Frame, image={realAppName}ICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: GuiInterfaceCommands.launchItem('{command}'))")
            exec(f"{realAppName}BTN.IMGREF = {realAppName}ICON")
            exec(f"{realAppName}BTN.grid(row=0, column=0)")
            exec(f"{realAppName}LABEL = tkinter.Label({realAppName}Frame, text=f'{appName}', background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)")
            exec(f"{realAppName}LABEL.grid(row=1, column=0)")
            self.CurrentDesktopIconsList.append(command)
        else:
            messagebox.showerror(None, None, ROOT_WINDOW, True, "APP_NOT_FOUND_ERROR")
    @staticmethod
    def getWallpaperImageResized(path: str):
        image = Image.open(path)
        resizedImage = image.resize((ROOT_WINDOW.winfo_screenwidth(), ROOT_WINDOW.winfo_screenheight()))
        actualImage= ImageTk.PhotoImage(resizedImage)
        return actualImage
    def refreshDesktop(self, pinnedAppsDesktop):
        self.CurrentDesktopIconsList = []
        global ROW_COUNT_DESKTOP_ICONS, COLUMN_COUNT_DESKTOP_ICONS
        ROW_COUNT_DESKTOP_ICONS = 0
        COLUMN_COUNT_DESKTOP_ICONS = 0
        for frame in dict(desktopFrame.children).values():
            frame.destroy()
        for app in pinnedAppsDesktop:
            try:
                GuiInterfaceCommands.createAppIcon(f"{app}", f"{app}", False)
            except Exception as EXP: messagebox.showerror("Error pinning app", f"{app} Cannot be pinned due to the following technical reason: \n {EXP}", root=ROOT_WINDOW)
    def addNewIcon(self, *args):
        INDEX=0
        iconToAdd = None
        addNewIcon = tkinter.Toplevel(ROOT_WINDOW, background=THEME_WINDOW_BG)
        desktopAppsList = ttk.Combobox(addNewIcon)
        # for z in self.CurrentDesktopIconsList:
        #     CURRENT_LIST = APPS_LIST
        #     try:
        #         CURRENT_LIST = CURRENT_LIST.pop(APPS_LIST.index(z))
        #     except Exception as problem:
        #         pass
        CURRENT_LIST = list(APPS_LIST)
        for app in APPS_LIST:
            if app in self.CurrentDesktopIconsList:
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
        addIconBtn = tkinter.Button(addNewIcon, text="Add Icon!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: self.createAppIcon(iconToAdd, f"{iconToAdd}"))
        addIconBtn.grid(row=0, column=1) 
        addNewIcon.mainloop()
    def shutdownMenu(self, root: tkinter.Tk, e=None):
        def waitUntillTaskFinishes(func):
            if FILE_SYSTEM.TASK_IN_PROGRESS != [0, 0]:
                messagebox.showinfo("IO Operations pending!", "Please wait untill the file IO operations are completed. The system will automatically shutdown after.", root=root)
            def e():
                if FILE_SYSTEM.TASK_IN_PROGRESS == [0, 0]: func()
                root.after(100, e)
            root.after(100, e)
        def shutdown():
            try:
                if username == "GUEST":
                    FILE_SYSTEM.deleteFiles([[f"{CWD}/ProgramFiles/GUEST"]])
            finally:
                waitUntillTaskFinishes(lambda: os._exit(0))
        def restart():
            if safeModeRestartVar.get() == 1:
                try:
                    children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
                    for child in children:
                        child.destroy()
                finally:
                    def sigma():
                        os.system("""python "Windows 11.py" -safemode """)
                        exit()
                    waitUntillTaskFinishes(sigma)
            else:
                try:
                    children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
                    for child in children:
                        child.destroy()
                finally:
                    os.system(""" python "Windows 11.py" """)
                    exit()

        shutdownWindow = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        shutdownWindow.title("Shutdown/Restart the shell")
        a = tkinter.Label(shutdownWindow, text="What you want to do now?", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        a.grid(row=0, column=0)
        ShutdownICON = ICONS["shutdown"].subsample(2, 2)
        ShutdownBTN = tkinter.Button(shutdownWindow, image=ShutdownICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=shutdown)
        ShutdownBTN.IMGREF = ShutdownICON
        tooltips.createToolTipAtGivenPos(ShutdownBTN, 2, root, "Shuts down the shell")
        ShutdownBTN.grid(row=1, column=0)
        RestartICON = ICONS["restart"].subsample(2, 2)
        RestartBTN = tkinter.Button(shutdownWindow, image=RestartICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=restart)
        RestartBTN.IMGREF = RestartICON
        RestartBTN.grid(row=1, column=1)
        safeModeRestartVar = tkinter.IntVar()
        ttk.Style().configure("TCheckbutton", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        safeModeRestartChk = ttk.Checkbutton(shutdownWindow, text="Restart in safe mode", variable=safeModeRestartVar, style="TCheckbutton")
        safeModeRestartChk.grid(row=1, column=2, padx=10)
        tkinter.Label(shutdownWindow, text="Shutdown", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=2, column=0)
        tkinter.Label(shutdownWindow, text="Restart", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=2, column=1)
        shutdownWindow.mainloop()

def _AppLauncherForExternalApps(app: str, USER_CONFIG, params = None, userConfig= None, notifications=None,):
    PID = random.randint(5000, 9999)
    while PID in ParWFS._instances["root"].RUNNING_APPS.keys():
        PID = random.randint(5000, 9999)
    ParWFS._instances["root"].RUNNING_APPS[PID] = app
    ShelveRef = USER_CONFIG
    PER_PROGRAM_COMMAND_APPS_LIST = ShelveRef["APPS"][1]
    appToLaunch = GUIButtonCommand.AppImportNameCheck(app=app)
    progAppImport = f"{PER_PROGRAM_COMMAND_APPS_LIST[PER_PROGRAM_COMMAND_APPS_LIST.index(f'ProgramFiles.{appToLaunch}')]}"
    exec(f"import {progAppImport}")
    exec(f"ProgramFiles.{appToLaunch}.main(userConfig, notifications, '{params}', USER_CONFIG, {PID})")

class TaskManager:
    def __init__(self, root):
        self.ROOT = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        self.fileView = ttk.Treeview(self.ROOT, style="Treeview")
        PID = random.randint(TASK_MANAGERS[0], TASK_MANAGERS[1])
        while PID in RUNNING_APPS.keys():
            PID = random.randint(TASK_MANAGERS[0], TASK_MANAGERS[1])
        dwm.createTopFrame(self.ROOT, THEME_FOREGROUND, THEME_WINDOW_BG, "taskmanager", "Task Manager", PID)
        RUNNING_APPS[PID] = "Task Manager"
        GUIButtonCommand.createRunningAppTaskbarIcon("Task Manager", PID)
        self.ROOT.title("Task Manager")
        self.fileView.grid(row=1, column=0, sticky="w")
        self.fileView['column'] = "Applications"
        self.fileView.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        self.fileView.column("Applications", anchor=tkinter.W, width=600)
        self.fileView.heading("Applications", text="Applications", anchor=tkinter.CENTER)
        self.fileView.configure(style="Treeview")
        self.endTaskButton = tkinter.Button(self.ROOT, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="End Application", command=self.endTask)
        self.endTaskButton.grid(row=2, column=0)
        self.ROOT.after(500, self.updateEach1000Ms)
        self.ROOT.mainloop()
    def updateEach1000Ms(self):
        self.ROOT.after(1000, self.updateEach1000Ms)
        SELECTED_SMTH = self.fileView.focus()
        for i in self.fileView.get_children():
            self.fileView.delete(i)
        for i, PID in enumerate(RUNNING_APPS):
            appToIns = RUNNING_APPS.get(PID)
            appToIns += f" <<<PID: {PID}>>> "
            self.fileView.configure(style="Treeview")
            self.fileView.insert(parent='', iid=PID, text='', index='end', values=[appToIns],)
        self.fileView.focus(SELECTED_SMTH)
        self.fileView.selection_set([SELECTED_SMTH])
        
    def endTask(self):
        application = self.fileView.focus()
        try:
            appToEnd = str(RUNNING_APPS[int(application)])
            appToEnd.replace(f"<<<PID: {application}>>>", "")
            command = COMMAND_APPS_LIST[COMMAND_APPS_LIST.index(f"ProgramFiles.{ GuiInterfaceCommands.AppImportNameCheck(app=appToEnd)}")] 
            exec(f"import {command}")
            exec(f"{command}.endTask(int({application}))")
            del RUNNING_APPS[int(application)]
        except Exception as EXP:
            print(EXP) 
            try:
                dwm.close(PID=int(application))
            except Exception as E:
                print(E)
                try: 
                    dwm.MANAGED_DWM_INSTANCES[int(application)][2].destroy()
                    del RUNNING_APPS[int(application)]
                except Exception as U:
                    messagebox.showerror("Error ending application", f"Error ending {application}. \nProblem: {U}\nFrom\n{E}\nFrom\n{EXP}", self.ROOT)
print("Loaded GUI Option Modules...")
idx = 0
afterCancelId = None
def startUpTasks(CONFIG, ROOT: tkinter.Tk):
    global idx, afterCancelId
    afterCancelId = ROOT.after(100, lambda i=None: startUpTasks(CONFIG, ROOT))
    length = len(CONFIG["STARTUP_APPS"])
    if idx >= length: ROOT.after_cancel(afterCancelId); return 0
    idx += 1
    GUIButtonCommand.launchItem(CONFIG["STARTUP_APPS"][idx-1])
    
def main():
    print("Loaded operating system!")
    global THEME_WINDOW_BG, THEME_FOREGROUND
    global children
    def safeModePREPTask(e=None):
        for child in children:
            child.destroy()
        safeMode()
    global SYS_CONFIG
    global USER_CONFIG
    global launcherComboBox
    global contextMenu
    global ROOT_WINDOW
    global APPS_LIST
    global notificationsButton
    global desktopFrame
    global PINNED_APPS
    global GuiInterfaceCommands
    global appsFrame
    global desktopContextMenu
    global COMMAND_APPS_LIST
    global RUNNING_APPS
    global runningAppsFrame
    global wallpaper
    FILE_SYSTEM.loadConfig(f"ProgramFiles/{username}/USER_CONFIG", "USER_CONFIG")
    USER_CONFIG = FILE_SYSTEM.getConfig("USER_CONFIG")
    APPS_LIST, COMMAND_APPS_LIST = USER_CONFIG["APPS"]
    THEME_WINDOW_BG, THEME_FOREGROUND = USER_CONFIG["THEME"]
    PINNED_APPS, PINNED_APPS_DESKTOP = USER_CONFIG["PINNED"]
    print("Loaded apps and user settings!")
    def popup(event=None, *args):
        """ the context menu popup"""
        if (ROOT_WINDOW.winfo_containing(event.x_root, event.y_root)).identifier == "taskbar": 
            #GuiInterfaceCommands.popup(event=event)
            contextMenu.focus()
        else:
            try:
                desktopContextMenu.tk_popup(event.x_root, event.y_root, 0)
                print(PROBLEM)
            finally:
                desktopContextMenu.grab_release()
    GuiInterfaceCommands = GUIButtonCommand(PINNED_APPS)
    ROOT_WINDOW = tkinter.Tk()
    ROOT_WINDOW.configure(background=THEME_WINDOW_BG)
    loadAllIcons(APPS_LIST, ROOT_WINDOW)
    loadAllIcons(["shutdown", "restart"], ROOT_WINDOW)
    taskbarFrame = tkinter.Frame(ROOT_WINDOW, background=THEME_WINDOW_BG)
    taskbarFrame.identifier = "taskbar"
    ROOT_WINDOW.identifier = "root_window"
    desktopFrame = tkinter.Frame(ROOT_WINDOW, background=THEME_WINDOW_BG, border=15)
    if (USER_CONFIG["WALLPAPER"]):
        image = GUIButtonCommand.getWallpaperImageResized(USER_CONFIG["WALLPAPER"])
        ROOT_WINDOW.wallpaperImage = image
        wallpaper = tkinter.Label(ROOT_WINDOW, image=image)
        wallpaper.grid(row=1, column=0, sticky="EWSN")
        wallpaper.identifier = "wallpaper"
    ROOT_WINDOW.grid_rowconfigure(1, weight=1)
    ROOT_WINDOW.grid_columnconfigure(0, weight=1)
    launcherComboBox = ttk.Combobox(taskbarFrame)
    launcherComboBox['values'] = APPS_LIST
    launcherComboBox['state'] = "readonly"
    launcherComboBox.bind("<<ComboboxSelected>>", GuiInterfaceCommands.launchComboBoxEvent)
    contextMenu = tkinter.Menu(taskbarFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    contextMenu.add_command(label="Taskbar settings", command=GuiInterfaceCommands.taskbarselfGUI)
    contextMenu.identifier = "taskbar"
    def runningTaskbarAppsLOOP():  
        ROOT_WINDOW.after(300, runningTaskbarAppsLOOP)
        for widget in dict(runningAppsFrame.children).values():
            try:
                location = list(RUNNING_APPS.keys()).index(widget.processInfo[0])
                widget.grid_configure(row=0, column=location)
                appNameReal = GUIButtonCommand.AppImportNameCheck(widget.processInfo[1])
                try: widget.configure(text=dwm.title(None, widget.processInfo[0]))
                except:
                    exec(f"import ProgramFiles.{appNameReal}\nwidget.configure(text=ProgramFiles.{appNameReal}.returnInformation({widget.processInfo[0]})['title'])")
            except Exception as EXP: 
                print(EXP)
                widget.destroy()
    ROOT_WINDOW.after(300, runningTaskbarAppsLOOP)
    def recurringClockFunc():
            global clock
            global ClockRepeatID
            cr_time = time.strftime("%H:%M:%S %p")
            clock = tkinter.Label(taskbarFrame, text=cr_time, background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
    
            ClockRepeatID = clock.after(1000, recurringClockFunc)
            clock.grid(row=0, column=2, sticky="ne")
    launcherComboBox.grid(row=0, column=0, sticky="w")
    try:
        if USER_CONFIG["CLOCK-WIDGET"] == 1: recurringClockFunc()
    except: pass
    appsFrame = tkinter.Frame(taskbarFrame, background=THEME_WINDOW_BG, border=5)
    shutDown = tkinter.Button(appsFrame, text="Shutdown", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=lambda: GuiInterfaceCommands.shutdownMenu(ROOT_WINDOW))
    shutDown.grid(row=0, column=0, padx=5)
    tooltips.createToolTipAtGivenPos(shutDown, 1, ROOT_WINDOW, "Shutdown or restart the shell!", )
    appsFrame.grid(row=0, column=1, sticky="n")
    FILE_SYSTEM.RunAppsFrame = runningAppsFrame = tkinter.Frame(taskbarFrame, background=THEME_WINDOW_BG, padx=10, border=5)
    runningAppsFrame.grid(row=0, column=4, sticky="n")
    notificationsButton = tkinter.Button(taskbarFrame, text="Notifications (0)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command= lambda: notification.showNotificationsList(notification))
    notificationsButton.grid(row=0, column=3, sticky="ne", padx=5)
    desktopContextMenu = tkinter.Menu(appsFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    desktopContextMenu.add_command(label="Refresh", command=lambda: GuiInterfaceCommands.refreshDesktop(PINNED_APPS_DESKTOP))
    desktopContextMenu.add_command(label="Add new icon", command=GuiInterfaceCommands.addNewIcon)
    ROOT_WINDOW.bind("<Button-3>", popup)
    taskbarFrame.bind("<Button-3>", GuiInterfaceCommands.popup)
    taskbarFrame.grid(row=0, column=0, sticky="EW")
    desktopFrame.grid(row=1, column=0, sticky="NW")
    desktopFrame.lift()
    
    ROOT_WINDOW.attributes('-fullscreen', True)
    ROOT_WINDOW.bind("<Escape>", safeModePREPTask)
    children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
    GuiInterfaceCommands.refreshDesktop(PINNED_APPS_DESKTOP)
    for app in PINNED_APPS:
        try: GuiInterfaceCommands.pinApps(f"{app}", False)
        except Exception as EXP: messagebox.showerror("Error pinning app to taskbar", f"Error pinning {app} in the taskbar.\nPROB:{EXP}", root=ROOT_WINDOW)
    startUpTasks(USER_CONFIG, ROOT_WINDOW)
    ROOT_WINDOW.mainloop()
import base64
def loginVerification(e=None):
    print("Checking credentials")
    global userNameText
    global passwordText
    global userNum
    global username
    try:
        if int(userNum.get()) != 0:
            with open(f"ProgramFiles/accConfiguration{userNum.get()}.conf", "r") as verify:
                username, password = verify.readlines()
                username = base64.urlsafe_b64decode(username.rstrip('\n')).decode('utf-8')
                password = base64.urlsafe_b64decode(password.rstrip('\n')).decode('utf-8')
                if userNameText.get() == username and passwordText.get() == password:
                    loginWindow.destroy()
                    try:
                        main()
                    except Exception as EXP: bsod(main, f"DESKTOP_LAUNCH_ERROR('{EXP}')")
                else:
                    messagebox.showerror(None, None, loginWindow, True, "LOGIN_INCORRECT")
        else:
            loginWindow.destroy()
            username = "GUEST"
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
    global userNameText
    global passwordText
    global userNum
    global loginWindow
    loginWindow = tkinter.Tk()
    loginWindow.title("Login to Windows 11")
    loginWindow.configure(background=THEME_WINDOW_BG)
    loadAllIcons(["shutdown", "restart"], loginWindow)
    msg = tkinter.Label(loginWindow, text="Enter your Username: ", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    msg.grid(row=0, column=0)
    userNameText = tkinter.Entry(loginWindow, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    userNameText.grid(row=0, column=1)
    userNameText.focus()
    userNameText.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
    msg2 = tkinter.Label(loginWindow, text="Enter your Password", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    msg2.grid(row=1, column=0)
    passwordText = tkinter.Entry(loginWindow, foreground=THEME_FOREGROUND, background=THEME_WINDOW_BG, show="*")
    passwordText.grid(row=1, column=1)
    passwordText.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
    def passwordTextFocus(*e): passwordText.focus()
    userNameText.bind("<Tab>", passwordTextFocus)
    userNameText.bind("<Return>", lambda: passwordTextFocus)
    msg3 = tkinter.Label(loginWindow, text="Enter your user number", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    userNum = tkinter.Entry(loginWindow, foreground=THEME_FOREGROUND, background=THEME_WINDOW_BG)
    userNum.grid(row=2, column=1)
    userNum.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
    msg3.grid(row=2, column=0)
    userNum.bind("<Return>", loginVerification)
    loginBtn = tkinter.Button(loginWindow, text="Login", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=loginVerification)
    loginBtn.grid(row=3, column=1)
    shutdownBtn = tkinter.Button(loginWindow, text="Shutdown", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=lambda: GUIButtonCommand.shutdownMenu(GUIButtonCommand, loginWindow))
    shutdownBtn.grid(row=0, column=MAX_COLUMN_DESKTOP)
    loginWindow.attributes('-fullscreen', True)
    loginWindow.bind("<Escape>", safeModePREPTask)
    loginWindow.mainloop()
cmdImg = None
img = None
reprImg = None
def autoRecoveryEnv() -> None:
    global cmdImg
    global img
    global reprImg
    recoveryWin = tkinter.Tk()
    recoveryWin.configure(background="Black")
    recoveryWin.attributes("-fullscreen", True)
    def launchCmd(e=None): import ProgramFiles.commandprompt; ProgramFiles.commandprompt.main("AUTORECOVERYENV", None, None, [None, None], None, None, random.randint(1000, 9999), None)
    def reprSysCMDL(e=None):
        import ProgramFiles.commandprompt
        ROOT = tkinter.Tk()
        ROOT.configure(background=THEME_WINDOW_BG)
        ROOT.title("Command Interpreter")
        text = tkinter.Text(ROOT, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=100)
        text.grid(row=0, column=0)
        yourCommand = tkinter.Entry(ROOT, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        yourCommand.configure(insertbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG, selectbackground=THEME_FOREGROUND, width=110)
        yourCommand.grid(row=1, column=0)
        cmdInstance = ProgramFiles.commandprompt.cmdCommands(text, yourCommand, root=ROOT)
        yourCommand.focus()
        cmdInstance.ADMINISTRATOR = True
        yourCommand.insert(tkinter.END, "sfcRepair -online")
        cmdInstance.sfcRepair()
        ROOT.mainloop()
    try:
        loadAllIcons(["continue", "repair", "commandprompt"], recoveryWin)
        continueICON = ICONS["continue"]
        continueBTN = tkinter.Button(recoveryWin, image=continueICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=login, text='Continue to main', compound=tkinter.LEFT)
        continueBTN.IMGREF = continueICON
        continueBTN.grid(row=0, column=0)

        repairICON = ICONS["repair"]
        repairBTN = tkinter.Button(recoveryWin, image=repairICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=reprSysCMDL, text='Repair system', compound=tkinter.LEFT)
        repairBTN.IMGREF = repairICON
        repairBTN.grid(row=1, column=0)

        cmdICON = ICONS["commandprompt"]
        cmdBTN = tkinter.Button(recoveryWin, image=cmdICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=launchCmd, text='Launch Command Prompt', compound=tkinter.LEFT)
        cmdBTN.IMGREF = cmdICON
        cmdBTN.grid(row=0, column=1)
        recoveryWin.mainloop()
    except Exception: print("ERROR OCCURED WHILE LOADING AUTORECOVERYENV..."); recoveryWin.destroy(); safeMode(forceNoARENV=True)
def safeMode(forceNoARENV=False) -> None:
    def a1():
        def resetConfigurations():
            userToreset = input("Enter the username of the user to reset the user too... [Type in defaultuser0 to only do system wise reset]")
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
    def a4(): print("=" * int(os.get_terminal_size()[0])); print("Shutting down...") ; sys._exit(0)
    
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
    try:
        if forceNoARENV: raise NotImplementedError("The program is forcing to use safe mode CLI... skipping Auto Recovery Environment...")
        autoRecoveryEnv()
        global SYS_CONFIG
        SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)
    except Exception as PRB:
        try:
            def sendCommand(e=None):
                cmdInstance.showMsg(f"\n>{yourCommand.get()}")
                if " " not in yourCommand.get():
                    yourCommand.insert(tkinter.END, "  ")
                if yourCommand.get().split(" ")[0] in cmdInstance.COMMAND_LIST and cmdInstance.ACCEPT_COMMANDS:
                    exec(f"cmdInstance.{yourCommand.get().split(' ')[0]}()")
                elif not cmdInstance.ACCEPT_COMMANDS: cmdInstance.clear()
                else: cmdInstance.showMsg(cmdInstance.COMMAND_NOT_FOUND)
            import ProgramFiles.commandprompt as cmd
            root= tkinter.Tk()
            root.configure(background=THEME_WINDOW_BG)
            root.attributes("-fullscreen", True) 
            text = tkinter.Text(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=100)
            text.grid(row=0, column=0)
            yourCommand = tkinter.Entry(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            yourCommand.configure(insertbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG, selectbackground=THEME_FOREGROUND, width=110)
            yourCommand.grid(row=1, column=0)
            cmdInstance = cmd.cmdCommands(text, yourCommand, root)
            yourCommand.focus()
            yourCommand.bind("<Return>", sendCommand)
            cmdInstance.showMsg("""\nYou're in a safe mode back up CLI mode. This is a fullscreen Command Prompt
\nThe system failed to boot. if you can diagnose & repair the system, you can use the available commands\n
Or else, type in the command 'restart' and your system will reboot""")
        except Exception as PRB:
            print(f"Cannot launch safe mode UI, going full CLI!\n PRB: {PRB}")
            time.sleep(5)
            try:
                import platform
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
            except Exception: pass
            finally:
                while True:
                    print("Safe mode activated!\n=-=-=-=WELCOME=-=-=-=")
                    while True:
                        userInput1 = int(input("""1. Reset your system\n
2. Continue to boot to main\n
3. Launch an app\n
4. Shutdown the system\n
5. Restart the system\n
6. Enable networking\n
7. Disable networking\n
  Enter your option >_"""))
                        if userInput1 in range(1, 8):
                            exec(f"a{userInput1}()")
    finally: 
        SYS_CONFIG = FILE_SYSTEM.editConfig("SYS_CONFIG", "CBSRESTARTATTEMPT", 0)

if __name__ == "__main__":
    arguements = sys.argv[1:]
    if not os.access("ProgramFiles", os.F_OK): bsod(login, "MODULE_NOT_FOUND_ERROR('The required modules inside ProgramFiles folder doesn't exist!')")
    else:
        if not os.access("ProgramFiles/commandprompt.py", os.F_OK) or not os.access("ProgramFiles/errorHandler.py", os.F_OK): bsod(login, "MODULE_NOT_FOUND_ERROR('The required modules inside ProgramFiles folder doesn't exist!')")
        else:
            if "-safemode" in arguements:
                safeMode()
            elif "-config" in arguements:
                username = input("Enter the username to create first run settings: ")
                password = input("Enter your user's password: ")
                foreground = input("Enter your user's preffered foreground colour: ")
                background = input("Enter your user's preffered background colour: ")
                userNumber = input("Enter your user's wanted user number (can be any number): ")
                import shelve
                FILE_SYSTEM.loadConfig("ProgramFiles/SYS_CONFIG", "SYS_CONFIG")
                SYS_CONFIG = FILE_SYSTEM.getConfig("SYS_CONFIG")
                try:
                    with open(f"ProgramFiles/accConfiguration{userNumber}.conf", "wb") as WRITE:
                        Rusername = base64.urlsafe_b64encode(username.encode("utf-8"))
                        Rpassword = base64.urlsafe_b64encode(password.encode("utf-8"))
                        WRITE.writelines([Rusername, "\n".encode("utf-8"),  Rpassword])
                    os.mkdir(f"ProgramFiles/{username}")
                    

                except Exception:
                    print("User already exists, skipping user creation tasks...")
                finally:
                    FILE_SYSTEM.loadConfig(f"ProgramFiles/{username}/USER_CONFIG", "USER_CONFIG")
                    USER_CONFIG = FILE_SYSTEM.getConfig("USER_CONFIG")
                FILE_SYSTEM.editConfig("USER_CONFIG", "APPS", [["Command Prompt", "Load External Apps", "Notepad", "Web Browser", "Update Manager", "IP Chat", "File Manager", "Software Store", "File Share", "Black Jack", "Alarms and Timer", "Photo Viewer", "Control Panel", "Task Manager"], ["ProgramFiles.alarmsandtimer", "ProgramFiles.blackjack", "ProgramFiles.commandprompt", "ProgramFiles.loadexternalapps", "ProgramFiles.ipchat", "ProgramFiles.notepad", "ProgramFiles.webbrowser", "ProgramFiles.updatemanager", "ProgramFiles.fileshare", "ProgramFiles.filemanager", "ProgramFiles.softwarestore", "ProgramFiles.photoviewer", "ProgramFiles.controlPanel", "ProgramFiles.taskManager"]])
                FILE_SYSTEM.editConfig("USER_CONFIG", "PINNED", [["File Manager"], ["Notepad", "File Manager"]])
                FILE_SYSTEM.editConfig("USER_CONFIG", "THEME", [background, foreground])
                FILE_SYSTEM.editConfig("USER_CONFIG", "CLOCK-WIDGET", 0)
                FILE_SYSTEM.editConfig("USER_CONFIG", "DEFAULTAPPASSOCIATION", {"txt": "Notepad", "jpg": "Photo Viewer", "png": "Photo Viewer"})
                FILE_SYSTEM.editConfig("USER_CONFIG", "WALLPAPER", None)
                FILE_SYSTEM.editConfig("USER_CONFIG", "STARTUP_APPS", [])
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
                    username = input("Type in the username whose settings are going to be changed!: ")
                    USER_CONFIG = shelve.open(f"ProgramFiles/{username}/USER_CONFIG", writeback=True)
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
                    import tkinter
                    from ProgramFiles.errorHandler import messagebox
                    import requests
                    if SYS_CONFIG["CBSRESTARTATTEMPT"] > 3:
                        try: 
                            autoRecoveryEnv()
                        except:
                            safeMode()
                except Exception as PROBLEM:
                    try:
                        import platform
                        if platform.system() == "Windows":
                            os.system("cls")
                        else:
                            os.system("clear")
                    except Exception: pass
                    print(f"Safe mode activated due to one of the modules not present. \n DEBUG: {PROBLEM}")
                    time.sleep(5)
                    safeMode()
                else:
                    try:
                        login()
                    except Exception as EXP: bsod(login, f"LOGIN_FAILURE('{EXP}')")
