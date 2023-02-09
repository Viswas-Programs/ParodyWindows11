from __future__ import print_function
from datetime import datetime
import sys
import os
    
def FTRConfigSettings(path, data: str=None, prepCodeBool=False, prepCode=None) -> tuple:
    if prepCodeBool: exec(prepCode)
    if os.access(path, os.F_OK):
        with open(path) as read_config:
            # print(bytes(read_config.read(), encoding='utf-8').decode(encoding='utf-8') == "")
            read_config_out = read_config.read()
            if bytes(read_config_out, encoding='utf-8').decode(encoding='utf-8') == "":
                print("in if")
                with open(path, "w") as writeData: writeData.write(data)
                updateRead =  open(path, "r")
                read_config = updateRead
                print("wrote data")
                updateRead.close()
            config = read_config_out.splitlines()
    else:
        with open(path, "w") as FTR_write_config: #FirstTimeRun_Write_config, full form.
            FTR_write_config.write(data)
            config = data.splitlines()
    return config
THEME_WINDOW_BG, THEME_FOREGROUND = FTRConfigSettings("theme_config.txt", f"Black\nWhite")
# emailSetup = FTRConfigSettings("PRogramFiles/emails.txt", "SETUP NEEDED!")[0]
import tkinter.ttk as ttk
import time
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
        messagebox.showinfo(title, msg, notificationsWindow)
        self.createNotification(msg=msg, time=time, action=action)
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
class Settings():
    from tkinter import colorchooser
    def __init__(Settings):
        import psutil
        Settings.SHOWN_HOMEPAGE = False
        Settings.SHOWN_PERSONALIZATION = False
        Settings.SHOWN_ADVANCED = False
        Settings.SHOWN_APPSLIST = False
        Settings.total_memory = str(f"{psutil.virtual_memory().total/1000000000} GigaBytes")
        Settings.settingsWindow = tkinter.Toplevel(background=THEME_WINDOW_BG)
        btnFrame = tkinter.Frame(Settings.settingsWindow, background=THEME_WINDOW_BG)
        btnFrame.grid(row=0, column=0)
        homeBtn = tkinter.Button(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Home", command=Settings.homePage)
        homeBtn.grid(row=0, column=0)
        personalizeBtn = tkinter.Button(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Personalization", command=Settings.personalization)
        personalizeBtn.grid(row=1, column=0)
        Settings.setting = tkinter.Frame(Settings.settingsWindow, background=THEME_WINDOW_BG)
        Settings.setting.grid(row=0, column=1)
    def homePage(Settings):
        if Settings.SHOWN_PERSONALIZATION or Settings.SHOWN_APPSLIST: Settings.setting.destroy()
        Settings.setting =  tkinter.Frame(Settings.settingsWindow, background=THEME_WINDOW_BG)
        Settings.setting.grid(row=0, column=1)
        Settings.SHOWN_HOMEPAGE = True
        infoText = f""" Windows 11 v2.0\nSystem RAM: {Settings.total_memory}\nBackground={THEME_WINDOW_BG}\n"""
        f"""Foreground={THEME_FOREGROUND}\n\nFor more info, please visit the respective categories! Thank you :)"""
        a = tkinter.Label(Settings.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=infoText).grid(row=0, column=0)
    def personalization(Settings):
        def changeBg():
            global children
            global THEME_WINDOW_BG
            colorToUse = Settings.colorchooser.askcolor(title="Select background!")
            THEME_WINDOW_BG = colorToUse[1]
            crBg.configure(text=f"Current Background = {THEME_WINDOW_BG}")
            if systemChangeTheme.get(): 
                with open("theme_config.txt", "w") as writeNewTheme: writeNewTheme.write(f"{THEME_WINDOW_BG}\n{THEME_FOREGROUND}")
            with open(f"ProgramFiles/{username}/theme_config.txt", "w") as writeNewTheme: writeNewTheme.write(f"{THEME_WINDOW_BG}\n{THEME_FOREGROUND}")
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
            colorToUse = Settings.colorchooser.askcolor(title="Select foreground!")
            THEME_FOREGROUND = colorToUse[1]
            crFg.configure(text=f"Current foreground = {THEME_FOREGROUND}")
            if systemChangeTheme.get(): 
                with open("theme_config.txt", "w") as writeNewTheme: writeNewTheme.write(f"{THEME_WINDOW_BG}\n{THEME_FOREGROUND}")
            with open(f"ProgramFiles/{username}/theme_config.txt", "w") as writeNewTheme: writeNewTheme.write(f"{THEME_WINDOW_BG}\n{THEME_FOREGROUND}")
            for child in children:
                try:
                    child.configure(background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                    ROOT_WINDOW.configure(background=THEME_WINDOW_BG,)
                except Exception: pass
            ROOT_WINDOW.update()
        if Settings.SHOWN_HOMEPAGE or Settings.SHOWN_ADVANCED or Settings.SHOWN_PERSONALIZATION: Settings.setting.destroy()
        Settings.setting =  tkinter.Frame(Settings.settingsWindow, background=THEME_WINDOW_BG)
        Settings.setting.grid(row=0, column=1)
        crBg = tkinter.Label(Settings.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=f"Current Background = {THEME_WINDOW_BG}")
        crBg.grid(row=0, column=0)
        changeBackground = tkinter.Button(Settings.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Change Background!", command=changeBg)
        changeBackground.grid(row=0, column=1)
        crFg = tkinter.Label(Settings.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=f"Current foreground = {THEME_FOREGROUND}")
        crFg.grid(row=1, column=0)
        changeForeground = tkinter.Button(Settings.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Changr foreground!", command=changeFg)
        changeForeground.grid(row=1, column=1)
        ttk.Style().configure("TCheckbutton", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        systemChangeTheme = tkinter.IntVar()
        applyToSystem = ttk.Checkbutton(Settings.setting, text="Also apply changes to system theme!", variable=systemChangeTheme)
        applyToSystem.grid(row=2, column=0)


ROW_COUNT_DESKTOP_ICONS = 0
COLUMN_COUNT_DESKTOP_ICONS = 0
MAX_ROW_DESKTOP = 10
MAX_COLUMN_DESKTOP = 15
class GUIButtonCommand(object):
    global launcherCombobox
    global APPS_LIST
    global PINNED_APPS
    global ROW_COUNT_DESKTOP_ICONS
    global COLUMN_COUNT_DESKTOP_ICONS
    global MAX_COLUMN_DESKTOP
    global MAX_ROW_DESKTOP
    def __init__(self):
        self.CurrentDesktopIconsList = []
        self.PINNED_APPS = PINNED_APPS
        self.TASKBAR_ICON_COUNT = 0
    def launchItem(self, app, e=None):
        progAppImport = f"{COMMAND_APPS_LIST[COMMAND_APPS_LIST.index(f'ProgramFiles.{app}')]}"
        print(progAppImport)
        exec(f"import {progAppImport}")
        exec(f"ProgramFiles.{app}.main()")
        print("App closed?")
    def launchComboBoxEvent(self, e=None):
        Item = launcherComboBox.get()
        if Item != "ControlPanel":
            self.launchItem(Item)
        else:
            Settings()
        
    def currentTime(self):
        cr_time = time.strftime("%H:%M:%S %p")
        clock = tkinter.Label(ROOT_WINDOW, text=cr_time, background=THEME_WINDOW_BG,
                                foreground=THEME_FOREGROUND)
        clock.after(1000, self.currentTime)
        clock.grid(row=0, column=2, sticky="ne")

    def pinApps(self, appToPin, writeto=True):
        global appsFrame
        self.TASKBAR_ICON_COUNT += 1
        exec(f"global {appToPin}BTN")
        # exec(f"global {appToPin}BTN")
        appName = appToPin
        if writeto:
            with open(f"ProgramFiles/{username}/pinnedAppsTaskbar.txt", "a") as pinnedApps:
                pinnedApps.write(f"\n{appToPin}")
        exec(f"{appName}ICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/{appName}.png').subsample(2, 2)")
        exec(f"{appName}BTN = tkinter.Button(appsFrame, image={appName}ICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: GUIButtonCommand.launchItem(GUIButtonCommand, f'{appToPin}'))")
        exec(f"{appName}BTN.IMGREF = {appName}ICON")
        exec(f"{appName}BTN.grid(row=0, column={self.TASKBAR_ICON_COUNT})")

    def taskbarSettingsGUI(self, e=None):
        global PINNED_APPS
        global GuiInterfaceCommands
        taskbarSettingsWindow = tkinter.Toplevel()
        taskbarSettingsWindow.configure(background=THEME_WINDOW_BG)
        taskbarSettingsWindow.title("Taskbar Settings")
        addWidgetsFrame = tkinter.LabelFrame(taskbarSettingsWindow, text="Add widgets", 
                                            background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        addWidgetsFrame.grid(row=0, column=0)
        addClock = tkinter.Button(addWidgetsFrame, text="Clock", foreground=THEME_FOREGROUND,
                                    background=THEME_WINDOW_BG, command=self.currentTime)
        addClock.grid(row=0, column=0)
        pinItems = tkinter.LabelFrame(taskbarSettingsWindow, text="Pin items",
                                        background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        pinItems.grid(row=1, column=0)
        r = -1
        PINNED_APPS = list(PINNED_APPS)
        for app in APPS_LIST:
            if app not in PINNED_APPS:
                r += 1
                if len(PINNED_APPS) == 1 or len(PINNED_APPS) == 2:
                    i = 0
                exec(f"{app} = tkinter.Button(pinItems, text='{app}', command=lambda: GuiInterfaceCommands.pinApps('{app}'),"
                    f"background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)\n{app}.grid(row=r, column=0)")
        taskbarSettingsWindow.mainloop()

    def popup(self, event=None, *args):
        """ the context menu popup"""
        print("called popup() function")
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
                with open(f"ProgramFiles/{username}/pinnedAppsDesktop.txt", "a") as updateDesktopIcons:
                    updateDesktopIcons.write(f"\n{appName}")
            exec(f"{appName}Frame = tkinter.Frame(desktopFrame, background=THEME_WINDOW_BG)")
            exec(f"{appName}Frame.grid(row=ROW_COUNT_DESKTOP_ICONS, column=COLUMN_COUNT_DESKTOP_ICONS)")
            ROW_COUNT_DESKTOP_ICONS += 1
            exec(f"{appName}ICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/{appName}.png')")
            exec(f"{appName}BTN = tkinter.Button({appName}Frame, image={appName}ICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: GUIButtonCommand.launchItem(GUIButtonCommand, '{command}'))")
            exec(f"{appName}BTN.IMGREF = {appName}ICON")
            exec(f"{appName}BTN.grid(row=0, column=0)")
            exec(f"{appName}LABEL = tkinter.Label({appName}Frame, text=f'{appName}', background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)")
            exec(f"{appName}LABEL.grid(row=1, column=0)")
            self.CurrentDesktopIconsList.append(command.split(".")[1])
        else:
            messagebox.showerror(None, None, ROOT_WINDOW, True, "APP_NOT_FOUND_ERROR")
    def refreshDesktop(self):
        pass
    def addNewIcon(self, *args):
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
            iconToAdd = str(desktopAppsList.get())
        desktopAppsList.bind("<<ComboboxSelected>>", updateVariable)
        desktopAppsList['state'] = "readonly"
        desktopAppsList.grid(row=0, column=0, sticky="w")      
        addIconBtn = tkinter.Button(addNewIcon, text="Add Icon!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: self.createAppIcon(iconToAdd, f"{iconToAdd}"))
        addIconBtn.grid(row=0, column=1) 
        addNewIcon.mainloop()
    def shutdownMenu(self, e=None):
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
                    os.system("""python3 "Windows 11.py" -safemode """)
                    exit()
            else:
                try:
                    children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
                    for child in children:
                        child.destroy()
                finally:
                    os.system(""" python3 "Windows 11.py" """)
                    exit()

        shutdownWindow = tkinter.Toplevel(background=THEME_WINDOW_BG)
        a = tkinter.Label(shutdownWindow, text="What you want to do now?", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        a.grid(row=0, column=0)
        exec(f"ShutdownICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/shutdown.png').subsample(2, 2)")
        exec(f"ShutdownBTN = tkinter.Button(shutdownWindow, image=ShutdownICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=shutdown)")
        exec(f"ShutdownBTN.IMGREF = ShutdownICON")
        exec(f"ShutdownBTN.grid(row=1, column=0)")
        exec(f"RestartICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/restart.png').subsample(2, 2)")
        exec(f"RestartBTN = tkinter.Button(shutdownWindow, image=RestartICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=restart)")
        exec(f"RestartBTN.IMGREF = RestartICON")
        exec(f"RestartBTN.grid(row=1, column=1)")
        safeModeRestartVar = tkinter.IntVar()
        ttk.Style().configure("TCheckbutton", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        safeModeRestartChk = ttk.Checkbutton(shutdownWindow, text="Restart in safe mode", variable=safeModeRestartVar, style="TCheckbutton")
        safeModeRestartChk.grid(row=1, column=2, padx=10)
        tkinter.Label(shutdownWindow, text="Shutdown", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=2, column=0)
        tkinter.Label(shutdownWindow, text="Restart", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=2, column=1)
        shutdownWindow.mainloop()


def main():
    global THEME_WINDOW_BG, THEME_FOREGROUND
    THEME_WINDOW_BG, THEME_FOREGROUND = FTRConfigSettings(f"ProgramFiles/{username}/theme_config.txt", "Black\nWhite")
    global children
    def safeModePREPTask(e=None):
        for child in children:
            child.destroy()
        safeMode()
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
    def popup(event=None, *args):
        """ the context menu popup"""
        print("called popup() function")
        problem = None
        try:
            desktopContextMenu.tk_popup(event.x_root, event.y_root, 0)
        except Exception as PROBLEM:
            problem = PROBLEM
        finally:
            desktopContextMenu.grab_release()
            if problem:
                notification.showNotification("Critical Error!", str(problem), datetime.now(), lambda: GuiInterfaceCommands.shutdownMenu())
    APPS_LIST = FTRConfigSettings(f"ProgramFiles/{username}/APPS_LIST.txt", "CommandPrompt\nNotepad\nfileshare\nOnlineBanking\nBlackJack\nFileManager\n" 
                "UpdateManager\nLoadExternalApps\nWebBrowser\nIPChat\nControlPanel\nAlarmsAndTimer\n")
    COMMAND_APPS_LIST = FTRConfigSettings(f"ProgramFiles/{username}/APPS_COMMAND_LST", "ProgramFiles.CommandPrompt\nProgramFiles.Notepad\nProgramFiles.fileshare\nProgramFiles.OnlineBanking.v5\nProgramFiles.BlackJack.BlackJack\nProgramFiles.FileManager\n" 
                "ProgramFiles.UpdateManager\nProgramFiles.LoadExternalApps\nProgramFiles.WebBrowser\nProgramFiles.IPChat\nApps.ControlPanel\nProgramFiles.AlarmsAndTimer\n")
    print(COMMAND_APPS_LIST)
    PINNED_APPS_DESKTOP = FTRConfigSettings(f"ProgramFiles/{username}/pinnedAppsDesktop.txt", "Notepad\nFileManager")
    PINNED_APPS = FTRConfigSettings(f"ProgramFiles/{username}/pinnedAppsTaskbar.txt", "FileManager")
    GuiInterfaceCommands = GUIButtonCommand()
    ROOT_WINDOW = tkinter.Tk()
    ROOT_WINDOW.configure(background=THEME_WINDOW_BG)
    launcherComboBox = ttk.Combobox(ROOT_WINDOW)
    launcherComboBox['values'] = APPS_LIST
    launcherComboBox['state'] = "readonly"
    launcherComboBox.bind("<<ComboboxSelected>>", GuiInterfaceCommands.launchComboBoxEvent)
    launcherComboBox.grid(row=0, column=0, sticky="w")
    appsFrame = tkinter.Frame(ROOT_WINDOW, background=THEME_WINDOW_BG, border=5)
    contextMenu = tkinter.Menu(appsFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    contextMenu.add_command(label="Taskbar settings", command=GuiInterfaceCommands.taskbarSettingsGUI)
    shutDown = tkinter.Button(appsFrame, text="Shutdown", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=GuiInterfaceCommands.shutdownMenu)
    shutDown.grid(row=0, column=0, padx=5)
    appsFrame.bind("<Button-3>", GuiInterfaceCommands.popup)
    appsFrame.grid(row=0, column=1, sticky="n")
    notificationsButton = tkinter.Button(ROOT_WINDOW, text="Notifications (0)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command= lambda: notification.showNotificationsList(notification))
    notificationsButton.grid(row=0, column=3, sticky="ne", padx=5)
    desktopFrame = tkinter.Frame(ROOT_WINDOW, background=THEME_WINDOW_BG, border=15)
    desktopContextMenu = tkinter.Menu(appsFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    for app in PINNED_APPS_DESKTOP:
        try:
            GuiInterfaceCommands.createAppIcon(f"{app}", f"{app}", False)
        except Exception: pass
    for app in PINNED_APPS:
        try:
            GuiInterfaceCommands.pinApps(f"{app}", False)
        except Exception: pass
    desktopContextMenu.add_command(label="Refresh", command=GuiInterfaceCommands.refreshDesktop)
    desktopContextMenu.add_command(label="Add new icon", command=GuiInterfaceCommands.addNewIcon)
    desktopFrame.bind("<Button-3>", popup)
    desktopFrame.grid(row=1, column=0, sticky="news", columnspan=MAX_COLUMN_DESKTOP, rowspan=MAX_ROW_DESKTOP)
    ROOT_WINDOW.attributes('-fullscreen', True)
    ROOT_WINDOW.bind("<Escape>", safeModePREPTask)
    children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
    ROOT_WINDOW.mainloop()
def loginVerification(e=None):
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
        os.mkdir("ProgramFiles/GUEST")
        main()

def checkTheme(widget):
    if THEME_WINDOW_BG in DARK_COLOURS:
        widget.configure(insertbackground=THEME_FOREGROUND,
                            selectbackground=THEME_FOREGROUND,
                            selectforeground=THEME_WINDOW_BG)
DARK_COLOURS = ["black", 'brown', 'blue', 'green', 'red', 'violet', 'purple', 'dark blue', 'dark green',
                'dark red', 'dark brown', ]
def login():
    import tkinter
    def safeModePREPTask(e=None):
        with open("ProgramFiles/CBSRESTARTATTEMPT", "w") as CBSRESTARTATTEMPT: CBSRESTARTATTEMPT.write("0")
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
                                command=lambda: GUIButtonCommand.shutdownMenu(GUIButtonCommand))
    shutdownBtn.grid(row=0, column=MAX_COLUMN_DESKTOP)
    loginWindow.attributes('-fullscreen', True)
    loginWindow.bind("<Escape>", safeModePREPTask)
    loginWindow.mainloop()

def bsod(obj, supportCode) -> None:
    text = f"A problem has occured on ParodyWin11 and has been shutdown to prevent further damage\n"\
            "If this is the first time you're seeing this stop screen, please make sure you have proper configuration files"\
            "in the right place.\n\nIf the problem still exists, please contact your administrator or have a "\
            "look at this informative page on stop codes! (support link)\n\nSupport: \nhttps://github.com/Viswas-Programs/ParodyWindows11/wiki/STOP_CODES\n\n"\
            f"Technical information: {obj} Failed to load properly (Improperly loaded!)\nSupport Code: {supportCode}\n"\
            "Restarting in a moment..."
    try:
        def restart():
            bsodWind.destroy()
            time.sleep(5)
            os.system(""" python3 "Windows 11.py" """)
            exit()
        import tkinter
        try:
            with open("ProgramFiles/CBSRESTARTATTEMPT", "r") as ATTEMPTREAD: attempts = int(ATTEMPTREAD.read())
            with open("ProgramFiles/CBSRESTARTATTEMPT", "w") as CBSRESTARTATTEMPT: CBSRESTARTATTEMPT.write(str(attempts+1))
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
            with open("ProgramFiles/CRASHLOGS", "a") as UPDATE_CRASH_LOGS: UPDATE_CRASH_LOGS.write(f"\n{supportCode} occured on {datetime.now()} on {obj}")
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
    def launchCmd(e=None): import ProgramFiles.CommandPrompt; ProgramFiles.CommandPrompt.main()
    def reprSysCMDL(e=None):
        import ProgramFiles.CommandPrompt
        ROOT = tkinter.Tk()
        ROOT.configure(background=THEME_WINDOW_BG)
        ROOT.title("Command Interpreter")
        text = tkinter.Text(ROOT, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=100)
        text.grid(row=0, column=0)
        yourCommand = tkinter.Entry(ROOT, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        yourCommand.configure(insertbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG, selectbackground=THEME_FOREGROUND, width=110)
        yourCommand.grid(row=1, column=0)
        cmdInstance = ProgramFiles.CommandPrompt.cmdCommands(text, yourCommand, root=ROOT)
        yourCommand.focus()
        cmdInstance.ADMINISTRATOR = True
        yourCommand.insert(tkinter.END, "sfcRepair -online")
        cmdInstance.sfcRepair()
        ROOT.mainloop()

    exec(f"continueICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/continue.png')")
    exec(f"continueBTN = tkinter.Button(recoveryWin, image=continueICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=login, text='Continue to main', compound=tkinter.LEFT)")
    exec(f"continueBTN.IMGREF = continueICON")
    exec(f"continueBTN.grid(row=0, column=0)")

    exec(f"repairICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/repair.png')")
    exec(f"repairBTN = tkinter.Button(recoveryWin, image=repairICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=reprSysCMDL, text='Repair system', compound=tkinter.LEFT)")
    exec(f"repairBTN.IMGREF = repairICON")
    exec(f"repairBTN.grid(row=1, column=0)")

    exec(f"cmdICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/CommandPrompt.png')")
    exec(f"cmdBTN = tkinter.Button(recoveryWin, image=cmdICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=launchCmd, text='Launch Command Prompt', compound=tkinter.LEFT)")
    exec(f"cmdBTN.IMGREF = cmdICON")
    exec(f"cmdBTN.grid(row=0, column=1)")
    recoveryWin.mainloop()
def safeMode() -> None:
        global attempts
        def a1():
            def resetConfigurations():
                try:
                    txtFilesToDelete = ["theme_config.txt", "ProgramFiles/tkweb.txt", "ProgramFiles/pinnedApps.txt"]
                    for fileToDelete in txtFilesToDelete:
                        try:
                            os.remove(fileToDelete)
                        except Exception: pass
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
                print("=" * int(os.get_terminal_size()[0]))

        def a2():
            print("=" * int(os.get_terminal_size()[0]))
            login()
            
        def a3():
            print("=" * int(os.get_terminal_size()[0]))
            print("CurrentWorkingDirectory: ", os.getcwd())
            appName = input("Enter the file name path to load!")
            os.system(f"python3 {appName} ")
            print("=" * int(os.get_terminal_size()[0]))
        
        def a4():
            print("=" * int(os.get_terminal_size()[0]))
            print("Shutting down...")
            exit()
        
        def a5():
            print("=" * int(os.get_terminal_size()[0]))
            opt = input("Do you want to restart in safe mode or normal mode?\n"
                        "1. Safe Mode\n"
                        "2. Normal Mode\n"
                        "Enter your option >_")
            if int(opt) == 1: 
                print("=" * int(os.get_terminal_size()[0]))
                os.system("""python3 "Windows 11.py" -safemode """)
                exit()
            else: 
                os.system("""python3 "Windows 11.py" """)
                print("=" * int(os.get_terminal_size()[0]))
                exit()
        def a6():
            print("=" * int(os.get_terminal_size()[0]))
            nonlocal NETWORKING
            NETWORKING = True
            print("Enabled networking!")
            print("=" * int(os.get_terminal_size()[0]))

        def a7():
            print("=" * int(os.get_terminal_size()[0]))
            nonlocal NETWORKING
            NETWORKING = False
            print("Disabled networking!")
            print("=" * int(os.get_terminal_size()[0]))
        NETWORKING = False
        with open("ProgramFiles/CBSRESTARTATTEMPT") as CBSRESTARTATTEMPT: attempts = int(CBSRESTARTATTEMPT.read())
        if attempts < 2:
            bsod(main, "MODULE_NOT_FOUND_ERROR")
        else:
            try:
                autoRecoveryEnv()
                with open("ProgramFiles/CBSRESTARTATTEMPT", "w") as CBSRESTARTATTEMPT: CBSRESTARTATTEMPT.write("0")
            except Exception as PRB: 
                print("Cannot launch safe mode UI, going full CLI!\n PRB: {}".format(PRB))
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
                            userInput1 = int(input("1. Reset your system\n"
                                            "2. Continue to boot to main\n"
                                            "3. Launch an app\n"
                                            "4. Shutdown the system\n"
                                            "5. Restart the system\n"
                                            "6. Enable networking\n"
                                            "7. Disable networking\n"
                                            "Enter your option >_"))
                            if userInput1 in range(1, 8):
                                exec(f"a{userInput1}()")
            finally: 
                with open("ProgramFiles/CBSRESTARTATTEMPT", "w") as CBSRESTARTATTEMPT: CBSRESTARTATTEMPT.write("0")

if __name__ == "__main__":
    arguements = sys.argv[1:]
    if not os.access("ProgramFiles", os.F_OK): bsod(login, "MODULE_NOT_FOUND_ERROR('The required modules inside ProgramFiles folder doesn't exist!')")
    else:
        if not os.access("ProgramFiles/CommandPrompt.py", os.F_OK) or not os.access("ProgramFiles/errorHandler.py", os.F_OK): bsod(login, "MODULE_NOT_FOUND_ERROR('The required modules inside ProgramFiles folder doesn't exist!')")
        else:
            if "-safemode" in arguements:
                safeMode()
            else:
                try:
                    import tkinter
                    from ProgramFiles.errorHandler import messagebox
                    import requests
                    import shelve
                    import os
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
