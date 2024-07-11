from __future__ import print_function
from datetime import datetime
import sys
import os
import shelve
import tkinter
import tkinter.ttk as ttk
import time
from tkinter import colorchooser
SYS_CONFIG = shelve.open("ProgramFiles/SYS_CONFIG",  writeback=True)
try:
    THEME_WINDOW_BG, THEME_FOREGROUND = SYS_CONFIG["THEME"]
except Exception:
    THEME_WINDOW_BG = "Black"
    THEME_FOREGROUND = "White"
print("Starting OS...")
RUNNING_APPS = []
def FTRConfigSettings(path, data: str=None, prepCodeBool=False, prepCode=None) -> tuple:
    if prepCodeBool: exec(prepCode)
    if os.access(path, os.F_OK):
        with open(path) as read_config:
            read_config_out = read_config.read()
            if bytes(read_config_out, encoding='utf-8').decode(encoding='utf-8') == "":
                with open(path, "w") as writeData: writeData.write(data)
                updateRead =  open(path, "r")
                read_config = updateRead
                updateRead.close()
            config = read_config_out.splitlines()
    else:
        with open(path, "w") as FTR_write_config: #FirstTimeRun_Write_config, full form.
            FTR_write_config.write(data)
            config = data.splitlines()
    return config
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
        import psutil
        self.SHOWN_HOMEPAGE = False
        self.SHOWN_PERSONALIZATION = False
        self.SHOWN_ADVANCED = False
        self.SHOWN_APPSLIST = False
        self.SHOWN_APPOPENERCHANGER = False
        self.total_memory = str(f"{psutil.virtual_memory().total/1000000000} GigaBytes")
        self.settingsWindow = tkinter.Toplevel(background=THEME_WINDOW_BG)
        btnFrame = tkinter.Frame(self.settingsWindow, background=THEME_WINDOW_BG)
        btnFrame.grid(row=0, column=0)
        homeBtn = tkinter.Button(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Home", command=self.homePage)
        homeBtn.grid(row=0, column=0)
        personalizeBtn = tkinter.Button(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Personalization", command=self.personalization)
        personalizeBtn.grid(row=1, column=0)
        appOpenerChangeBtn = tkinter.Button(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="App Associations", command=self.changeFileOpeners)
        appOpenerChangeBtn.grid(row=2, column=0)
        self.setting = tkinter.Frame(self.settingsWindow, background=THEME_WINDOW_BG)
        self.setting.grid(row=0, column=1)
    def homePage(self):
        if self.SHOWN_PERSONALIZATION or self.SHOWN_APPSLIST or self.SHOWN_APPOPENERCHANGER: self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=THEME_WINDOW_BG)
        self.setting.grid(row=0, column=1)
        self.SHOWN_HOMEPAGE = True
        infoText = f""" Windows 11 v2.3.5\nSystem RAM: {self.total_memory}\nBackground={THEME_WINDOW_BG}\n"""
        f"""Foreground={THEME_FOREGROUND}\n\nFor more info, please visit the respective categories! Thank you :)"""
        a = tkinter.Label(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=infoText).grid(row=0, column=0)
    def personalization(self):
        self.SHOWN_PERSONALIZATION = True
        def changeBg():
            global children
            global THEME_WINDOW_BG
            colorToUse = colorchooser.askcolor(title="Select background!")
            THEME_WINDOW_BG = colorToUse[1]
            crBg.configure(text=f"Current Background = {THEME_WINDOW_BG}")
            if systemChangeTheme.get(): 
                SYS_CONFIG["THEME"]= [THEME_WINDOW_BG, THEME_FOREGROUND]
            USER_CONFIG["THEME"] = [THEME_WINDOW_BG, THEME_FOREGROUND]
            USER_CONFIG.sync()
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
            colorToUse = self.colorchooser.askcolor(title="Select foreground!")
            THEME_FOREGROUND = colorToUse[1]
            crFg.configure(text=f"Current foreground = {THEME_FOREGROUND}")
            if systemChangeTheme.get(): 
                SYS_CONFIG["THEME"]= [THEME_WINDOW_BG, THEME_FOREGROUND]
            USER_CONFIG["THEME"] = [THEME_WINDOW_BG, THEME_FOREGROUND]
            USER_CONFIG.sync()
            for child in children:
                try:
                    child.configure(background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                    ROOT_WINDOW.configure(background=THEME_WINDOW_BG,)
                except Exception: pass
            ROOT_WINDOW.update()
        if self.SHOWN_HOMEPAGE or self.SHOWN_ADVANCED or self.SHOWN_PERSONALIZATION or self.SHOWN_APPOPENERCHANGER: self.setting.destroy()
        self.setting =  tkinter.Frame(self.settingsWindow, background=THEME_WINDOW_BG)
        self.setting.grid(row=0, column=1)
        crBg = tkinter.Label(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=f"Current Background = {THEME_WINDOW_BG}")
        crBg.grid(row=0, column=0)
        changeBackground = tkinter.Button(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Change Background!", command=changeBg)
        changeBackground.grid(row=0, column=1)
        crFg = tkinter.Label(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=f"Current foreground = {THEME_FOREGROUND}")
        crFg.grid(row=1, column=0)
        changeForeground = tkinter.Button(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Changr foreground!", command=changeFg)
        changeForeground.grid(row=1, column=1)
        ttk.Style().configure("TCheckbutton", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        systemChangeTheme = tkinter.IntVar()
        applyToSystem = ttk.Checkbutton(self.setting, text="Also apply changes to system theme!", variable=systemChangeTheme)
        applyToSystem.grid(row=2, column=0)
    def changeFileOpeners(self, reLaunch=False):
        def __internals_AddNewEntry(*args):
            def __internals_AddNewEntry_AddAppNames(*args):
                app = comboBox.get()
                try: 
                    extension = textAssociationEntry.get()
                    CurrentConfig: dict = USER_CONFIG["DEFAULTAPPASSOCIATION"]
                    CurrentConfig.update({extension: app})
                    USER_CONFIG["DEFAULTAPPASSOCIATION"] = CurrentConfig
                    USER_CONFIG.sync()
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
        self.setting.grid(row=0, column=1)
        addEntryBtn = tkinter.Button(self.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Add New Entry", command=__internals_AddNewEntry)
        addEntryBtn.grid(row=0, column=0)
        for X, i in enumerate(USER_CONFIG["DEFAULTAPPASSOCIATION"].keys()):
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
        USER_CONFIG["DEFAULTAPPASSOCIATION"] = CurrentConfig
        USER_CONFIG.sync()
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
    global launcherCombobox
    global APPS_LIST
    global PINNED_APPS
    global ROW_COUNT_DESKTOP_ICONS
    global COLUMN_COUNT_DESKTOP_ICONS
    global MAX_COLUMN_DESKTOP
    global MAX_ROW_DESKTOP
    def __init__(self, PINNED_APPS):
        self.CurrentDesktopIconsList = []
        self.PINNED_APPS = PINNED_APPS
        self.TASKBAR_ICON_COUNT = 0
    def launchItem(self, application: str, params= None, e=None):
        INDEX = len(RUNNING_APPS)
        RUNNING_APPS.insert(INDEX, application)
        appToLaunch = GUIButtonCommand.AppImportNameCheck(app=application)
        progAppImport = f"{COMMAND_APPS_LIST[COMMAND_APPS_LIST.index(f'ProgramFiles.{appToLaunch}')]}"
        exec(f"import {progAppImport}")
        if (params == None ): exec(f"ProgramFiles.{appToLaunch}.main('{username}', notification, {params},  USER_CONFIG)")
        else: exec(f"ProgramFiles.{appToLaunch}.main('{username}', notification, '{params}', USER_CONFIG)")
        RUNNING_APPS.pop(INDEX)
    def launchComboBoxEvent(self, e=None):
        Item = launcherComboBox.get()
        if Item == "Control Panel":
            settings()
        elif Item == "Task Manager":
            TaskManager(ROOT_WINDOW)
        else:
            self.launchItem(Item)
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
    def currentTime(self):
        global clock
        global ClockRepeatID
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
            USER_CONFIG["CLOCK-WIDGET"] = 1
            USER_CONFIG.sync()
            recurringClockFunction()

        else:
            try: 
               cr_time = None
               clock.after_cancel(ClockRepeatID)
               clock.destroy()
               USER_CONFIG["CLOCK-WIDGET"] = 0
               USER_CONFIG.sync()
            except Exception as E:
                messagebox.showerror("Can't destroy clock widget!", f"Can't destroy clock widget due to the following reason: \n {E}")
    def pinApps(self, appToPin, writeto=True):
        global appsFrame
        appName: str = appToPin
        appName = appName.replace(" ", "")
        self.TASKBAR_ICON_COUNT += 1
        exec(f"global {appName}BTN")
        
        if writeto:
            apList = USER_CONFIG["PINNED"][0]
            apList.append(appName)
            USER_CONFIG["PINNED"][0]  = apList
            USER_CONFIG.sync()
        exec(f"{appName}ICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/{appName}.png', master=ROOT_WINDOW).subsample(2, 2)")
        exec(f"{appName}BTN = tkinter.Button(appsFrame, image={appName}ICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: GuiInterfaceCommands.launchItem(f'{appToPin}'))")
        exec(f"{appName}BTN.IMGREF = {appName}ICON")
        exec(f"{appName}BTN.grid(row=0, column={self.TASKBAR_ICON_COUNT})")

    def taskbarselfGUI(self, e=None):
        global PINNED_APPS
        global GuiInterfaceCommands
        taskbarselfWindow = tkinter.Toplevel()
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
        problem = None
        try:
            contextMenu.tk_popup(event.x_root, event.y_root, 0)
        except Exception as PROBLEM:
            problem = PROBLEM
        finally:
            contextMenu.grab_release()
            if problem:
                notification.showNotification("Critical Error!", str(problem), datetime.now(), lambda: print("Hi"))
    def createAppIcon(self, appName: str, command: str, writeto=True, event=None):
        """ creates desktop icons!"""
        global desktopFrame
        global COLUMN_COUNT_DESKTOP_ICONS, ROW_COUNT_DESKTOP_ICONS
        if ROW_COUNT_DESKTOP_ICONS > MAX_ROW_DESKTOP:
            if COLUMN_COUNT_DESKTOP_ICONS > MAX_COLUMN_DESKTOP:
                messagebox.showerror("Desktop pin", "Can't place the item! no more space left!", ROOT_WINDOW)
            else:
                COLUMN_COUNT_DESKTOP_ICONS += 1
        if appName not in self.CurrentDesktopIconsList:
            if writeto:
                apList = USER_CONFIG["PINNED"][1]
                apList.append(appName)
                USER_CONFIG["PINNED"][1]  = apList
                USER_CONFIG.sync()
            appName = appName.replace(" ", "")
            exec(f"{appName}Frame = tkinter.Frame(desktopFrame, background=THEME_WINDOW_BG)")
            exec(f"{appName}Frame.grid(row=ROW_COUNT_DESKTOP_ICONS, column=COLUMN_COUNT_DESKTOP_ICONS)")
            ROW_COUNT_DESKTOP_ICONS += 1
            exec(f"{appName}ICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/{appName}.png')")
            exec(f"{appName}BTN = tkinter.Button({appName}Frame, image={appName}ICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: GuiInterfaceCommands.launchItem('{command}'))")
            exec(f"{appName}BTN.IMGREF = {appName}ICON")
            exec(f"{appName}BTN.grid(row=0, column=0)")
            exec(f"{appName}LABEL = tkinter.Label({appName}Frame, text=f'{appName}', background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)")
            exec(f"{appName}LABEL.grid(row=1, column=0)")
            self.CurrentDesktopIconsList.append(command)
        else:
            messagebox.showerror(None, None, ROOT_WINDOW, True, "APP_NOT_FOUND_ERROR")
    def refreshDesktop(self):
        pass
    def addNewIcon(self, *args):
        INDEX=0
        iconToAdd = None
        addNewIcon = tkinter.Toplevel(background=THEME_WINDOW_BG)
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
    def shutdownMenu(self, root, e=None):
        import shutil
        def shutdown():
            try:
                if username == "GUEST":
                    shutil.rmtree("ProgramFiles/GUEST")
                    os.rmdir("ProgramFiles/GUEST")
            finally:
                os._exit(0)
        def restart():
            if safeModeRestartVar.get() == 1:
                try:
                    children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
                    for child in children:
                        child.destroy()
                finally:
                    os.system("""python "Windows 11.py" -safemode """)
                    exit()
            else:
                try:
                    children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
                    for child in children:
                        child.destroy()
                finally:
                    os.system(""" python "Windows 11.py" """)
                    exit()

        shutdownWindow = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        a = tkinter.Label(shutdownWindow, text="What you want to do now?", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        a.grid(row=0, column=0)
        ShutdownICON = tkinter.PhotoImage(file = 'ProgramFiles/Icons/shutdown.png', master=root).subsample(2, 2)
        ShutdownBTN = tkinter.Button(shutdownWindow, image=ShutdownICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=shutdown)
        ShutdownBTN.IMGREF = ShutdownICON
        ShutdownBTN.grid(row=1, column=0)
        RestartICON = tkinter.PhotoImage(file='ProgramFiles/Icons/restart.png', master=root).subsample(2, 2)
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

def _AppLauncherForExternalApps(app: str, USER_CONFIG, params = None, userConfig= None, notifications=None):
    INDEX_TO_REMOVE_FROM = len(RUNNING_APPS)
    RUNNING_APPS.insert(INDEX_TO_REMOVE_FROM, app)
    ShelveRef = USER_CONFIG
    PER_PROGRAM_COMMAND_APPS_LIST = ShelveRef["APPS"][1]
    appToLaunch = GUIButtonCommand.AppImportNameCheck(app=app)
    progAppImport = f"{PER_PROGRAM_COMMAND_APPS_LIST[PER_PROGRAM_COMMAND_APPS_LIST.index(f'ProgramFiles.{appToLaunch}')]}"
    exec(f"import {progAppImport}")
    exec(f"ProgramFiles.{appToLaunch}.main('{userConfig}', notifications, '{params}', USER_CONFIG)")
    RUNNING_APPS.pop(INDEX_TO_REMOVE_FROM)

class TaskManager:
    def __init__(self, root):
        self.ROOT = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        self.fileView = ttk.Treeview(self.ROOT, style="Treeview")
        self.fileView.grid(row=0, column=0, sticky="w")
        self.fileView['column'] = "Applications"
        self.fileView.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        self.fileView.column("Applications", anchor=tkinter.W, width=600)
        self.fileView.heading("Applications", text="Applications", anchor=tkinter.CENTER)
        self.fileView.configure(style="Treeview")
        self.endTaskButton = tkinter.Button(self.ROOT, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="End Application", command=self.endTask)
        self.endTaskButton.grid(row=1, column=0)
        self.ROOT.after(500, self.updateEach1000Ms)
        self.ROOT.mainloop()
    def updateEach1000Ms(self):
        self.ROOT.after(1000, self.updateEach1000Ms)
        SELECTED_SMTH = self.fileView.focus()
        for i in self.fileView.get_children():
            self.fileView.delete(i)
        for i, app in enumerate(RUNNING_APPS):
            self.fileView.configure(style="Treeview")
            self.fileView.insert(parent='', iid=i, text='', index='end', values=[app],)
        self.fileView.focus(SELECTED_SMTH)
        self.fileView.selection_set([SELECTED_SMTH])
        
    def endTask(self):
        application = self.fileView.focus()
        try:
            command = COMMAND_APPS_LIST[COMMAND_APPS_LIST.index(f"ProgramFiles.{ GuiInterfaceCommands.AppImportNameCheck(app=RUNNING_APPS[int(application)])}")] 
            exec(f"import {command}")
            exec(f"{command}.endTask()")
            RUNNING_APPS.pop(int(application))
        except Exception as EXP: 
            messagebox.showerror("Error ending application", f"Error ending {application}. \nProblem: {EXP}")



print("Loaded GUI Option Modules...")
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
    SYS_CONFIG = shelve.open("ProgramFiles/SYS_CONFIG", writeback=True)
    USER_CONFIG = shelve.open(f"ProgramFiles/{username}/USER_CONFIG", writeback=True)

    APPS_LIST, COMMAND_APPS_LIST = USER_CONFIG["APPS"]
    THEME_WINDOW_BG, THEME_FOREGROUND = USER_CONFIG["THEME"]
    PINNED_APPS, PINNED_APPS_DESKTOP = USER_CONFIG["PINNED"]
    print("Loaded apps and user settings!")
    def popup(event=None, *args):
        """ the context menu popup"""
        problem = None
        try:
            desktopContextMenu.tk_popup(event.x_root, event.y_root, 0)
        except Exception as PROBLEM:
            problem = PROBLEM
        finally:
            desktopContextMenu.grab_release()
            if problem:
                notification.showNotification("Critical Error!", str(problem), datetime.now(), lambda: GuiInterfaceCommands.shutdownMenu())
    GuiInterfaceCommands = GUIButtonCommand(PINNED_APPS)
    ROOT_WINDOW = tkinter.Tk()
    ROOT_WINDOW.configure(background=THEME_WINDOW_BG)
    launcherComboBox = ttk.Combobox(ROOT_WINDOW)
    launcherComboBox['values'] = APPS_LIST
    launcherComboBox['state'] = "readonly"
    launcherComboBox.bind("<<ComboboxSelected>>", GuiInterfaceCommands.launchComboBoxEvent)
    def recurringClockFunc():
            global clock
            global ClockRepeatID
            cr_time = time.strftime("%H:%M:%S %p")
            clock = tkinter.Label(ROOT_WINDOW, text=cr_time, background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
    
            ClockRepeatID = clock.after(1000, recurringClockFunc)
            clock.grid(row=0, column=2, sticky="ne")
    launcherComboBox.grid(row=0, column=0, sticky="w")
    try:
        if USER_CONFIG["CLOCK-WIDGET"] == 1: recurringClockFunc()
    except: pass
    appsFrame = tkinter.Frame(ROOT_WINDOW, background=THEME_WINDOW_BG, border=5)
    contextMenu = tkinter.Menu(appsFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    contextMenu.add_command(label="Taskbar settings", command=GuiInterfaceCommands.taskbarselfGUI)
    shutDown = tkinter.Button(appsFrame, text="Shutdown", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=lambda: GuiInterfaceCommands.shutdownMenu(ROOT_WINDOW))
    shutDown.grid(row=0, column=0, padx=5)
    appsFrame.bind("<Button-3>", GuiInterfaceCommands.popup)
    appsFrame.grid(row=0, column=1, sticky="n")
    notificationsButton = tkinter.Button(ROOT_WINDOW, text="Notifications (0)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command= lambda: notification.showNotificationsList(notification))
    notificationsButton.grid(row=0, column=3, sticky="ne", padx=5)
    desktopFrame = tkinter.Frame(ROOT_WINDOW, background=THEME_WINDOW_BG, border=15)
    desktopContextMenu = tkinter.Menu(appsFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    desktopContextMenu.add_command(label="Refresh", command=GuiInterfaceCommands.refreshDesktop)
    desktopContextMenu.add_command(label="Add new icon", command=GuiInterfaceCommands.addNewIcon)
    desktopFrame.bind("<Button-3>", popup)
    desktopFrame.grid(row=1, column=0, sticky="news", columnspan=MAX_COLUMN_DESKTOP, rowspan=MAX_ROW_DESKTOP)
    ROOT_WINDOW.attributes('-fullscreen', True)
    ROOT_WINDOW.bind("<Escape>", safeModePREPTask)
    children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
    for app in PINNED_APPS_DESKTOP:
        try:
            GuiInterfaceCommands.createAppIcon(f"{app}", f"{app}", False)
        except Exception as EXP: messagebox.showerror("Error pinning app", f"{app} Cannot be pinned due to the following technical reason: \n {EXP}", root=ROOT_WINDOW)
    for app in PINNED_APPS:
        try:
            GuiInterfaceCommands.pinApps(f"{app}", False)
        except Exception as EXP: messagebox.showerror("Error pinning app to taskbar", f"Error pinning {app} in the taskbar.\nPROB:{EXP}", root=ROOT_WINDOW)
    ROOT_WINDOW.mainloop()
    SYS_CONFIG.close()
    USER_CONFIG.close()
def loginVerification(e=None):
    print("Checking credentials")
    global userNameText
    global passwordText
    global userNum
    global username
    if int(userNum.get()) != 0:
        with open(f"ProgramFiles/accConfiguration{userNum.get()}.conf", "r") as verify:
            username, password = verify.readlines()
            username = username.rstrip('\n')
            password = password.rstrip('\n')
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
        main()

DARK_COLOURS = ["black", 'brown', 'blue', 'green', 'red', 'violet', 'purple', 'dark blue', 'dark green',
                'dark red', 'dark brown', ]
def login():
    print("Starting up OS...")
    SYS_CONFIG["CBSRESTARTATTEMPT"] = 0
    def safeModePREPTask(e=None):
        SYS_CONFIG["CBSRESTARTATTEMPT"] = 0
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
    msg = tkinter.Label(loginWindow, text="Enter your Username: ", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    msg.grid(row=0, column=0)
    userNameText = tkinter.Entry(loginWindow, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    userNameText.grid(row=0, column=1)
    userNameText.focus()
    userNameText.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
    msg2 = tkinter.Label(loginWindow, text="Enter your Password", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    msg2.grid(row=1, column=0)
    passwordText = tkinter.Entry(loginWindow, foreground=THEME_FOREGROUND, background=THEME_WINDOW_BG)
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
            SYS_CONFIG["CBSRESTARTATTEMPT"] += 1
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
    def launchCmd(e=None): import ProgramFiles.commandprompt; ProgramFiles.commandprompt.main()
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
        exec(f"continueICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/continue.png')")
        exec(f"continueBTN = tkinter.Button(recoveryWin, image=continueICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=login, text='Continue to main', compound=tkinter.LEFT)")
        exec(f"continueBTN.IMGREF = continueICON")
        exec(f"continueBTN.grid(row=0, column=0)")

        exec(f"repairICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/repair.png')")
        exec(f"repairBTN = tkinter.Button(recoveryWin, image=repairICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=reprSysCMDL, text='Repair system', compound=tkinter.LEFT)")
        exec(f"repairBTN.IMGREF = repairICON")
        exec(f"repairBTN.grid(row=1, column=0)")

        exec(f"cmdICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/commandprompt.png')")
        exec(f"cmdBTN = tkinter.Button(recoveryWin, image=cmdICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=launchCmd, text='Launch Command Prompt', compound=tkinter.LEFT)")
        exec(f"cmdBTN.IMGREF = cmdICON")
        exec(f"cmdBTN.grid(row=0, column=1)")
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
        SYS_CONFIG["CBSRESTARTATTEMPT"] = 0
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
        SYS_CONFIG["CBSRESTARTATTEMPT"] = 0

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
                password = input("Enter your user's password")
                foreground = input("Enter your user's preffered foreground colour: ")
                background = input("Enter your user's preffered background colour: ")
                userNumber = input("Enter your user's wanted user number (can be any number)")
                import shelve
                SYS_CONFIG = shelve.open("ProgramFiles/SYS_CONFIG")
                try:
                    with open(f"ProgramFiles/accConfiguration{userNumber}.conf", "w") as WRITE:
                        WRITE.write(f"{username}\n{password}")
                    os.mkdir(f"ProgramFiles/{username}")
                    

                except Exception:
                    print("User already exists, skipping user creation tasks...")
                finally:
                    USER_CONFIG = shelve.open(f"ProgramFiles/{username}/USER_CONFIG", writeback=True)
                USER_CONFIG["APPS"] = [["Command Prompt", "Load External Apps", "Notepad", "Web Browser", "Update Manager", "IP Chat", "File Manager", "Software Store", "File Share", "Black Jack", "Alarms and Timer", "Photo Viewer", "Control Panel", "Task Manager"], ["ProgramFiles.alarmsandtimer", "ProgramFiles.blackjack", "ProgramFiles.commandprompt", "ProgramFiles.loadexternalapps", "ProgramFiles.ipchat", "ProgramFiles.notepad", "ProgramFiles.webbrowser", "ProgramFiles.updatemanager", "ProgramFiles.fileshare", "ProgramFiles.filemanager", "ProgramFiles.softwarestore", "ProgramFiles.photoviewer", "ProgramFiles.controlPanel", "ProgramFiles.taskManager"]]
                USER_CONFIG["PINNED"] = [["File Manager"], ["Notepad", "File Manager"]]
                USER_CONFIG["THEME"] = [background, foreground]
                USER_CONFIG["CLOCK-WIDGET"] = 0
                USER_CONFIG["DEFAULTAPPASSOCIATION"] = {"txt": "Notepad", "jpg": "Photo Viewer", "png": "Photo Viewer"}
                USER_CONFIG.sync()
                SYS_CONFIG["THEME"] = ["Black", "White"] 
                SYS_CONFIG["CBSRESTARTATTEMPT"] = 0
                print("Initialized new entries!")
            elif "-configchange" in arguements:
                print("You have entered the configuration manager! Press CTRL+C anytime to exit!\n")
                configchoice = input("System or User config change?")
                if "system" in configchoice.lower():
                    infoSysSelectSTR = "SYS_CONFIG"
                    SYS_CONFIG = shelve.open("ProgramFiles/SYS_CONFIG")
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
