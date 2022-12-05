import tkinter
from tkinter import messagebox
import os
from pathlib import Path
from tkinter import filedialog


def FTRConfigSettings(path, data: str or None=None) -> tuple:
    if os.access(path, os.F_OK):
        with open(path) as read_config:
            config = read_config.read().splitlines()
    else:
        with open(path, "w") as FTR_write_config: #FirstTimeRun_Write_config, full form.
            FTR_write_config.write(data)
            config = data.splitlines()
    return config
THEME_WINDOW_BG, THEME_FOREGROUND = FTRConfigSettings("theme_config.txt", f"White\nBlack")
import tkinter.ttk as ttk
import time
ROW_COUNT_NOTIFICATION_WINDOW = 0
class Notifications(object):
    global ROW_COUNT_NOTIFICATION_WINDOW
    global notificationsButton
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
        messagebox.showinfo(title, msg)
        self.createNotification(msg=msg, time=time, action=action)
    def showNotificationsList(self, event=None):
        notificationsWindow = tkinter.Toplevel(background="black")
        notificationsButton.configure(text="Notifications (0)")
        if len(self.NotificationsList) == 0:
            a = tkinter.Label(notificationsWindow, text="No notifications (yet)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            a.grid(row=0, column=0)
        for index, notif in enumerate(self.NotificationsList):
            exec(f'a{index} = tkinter.Label(notificationsWindow, text=f"{notif}\t: {self.TimeofNotification[index]}", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND')
            exec(f'a{index}.grid(row=ROW_COUNT_NOTIFICATION_WINDOW, column=0)')
            exec(f"a{index}.bind('<Button-1>', self.actions[index])")
        notificationsWindow.mainloop()
        self.NotificationsList, self.actions, self.TimeofNotification = [], [], []
notification = Notifications()
class Apps(object):
    def BlackJack():
        """
        blackjack game activator
        :return: None
        """
        import ProgramFiles.Games.blackjack.blackjack as GUIBlackjack
        GUIBlackjack.play()

    def Notepad():
        import ProgramFiles.Utilities.Notepad.Notepad as notepad
        def main():
            """ main """
            root = tkinter.Tk()
            root.title("Notepad GUI v3.0 STABLE")
            text = tkinter.Text(root, height=20, width=100,
                                font=("Arial Rounded MT Bold",
                                    18), )
            text.grid(row=0, column=0, pady=10)
            saveTo = tkinter.Text(root, height=2, width=50,
                                font=("Arial Rounded MT Bold",
                                        12))
            saveTo.grid(row=1, column=0)
            notepad.NotepadRun(text_box=text, gui=root, saveTo=saveTo)
        if __name__ == "__main__":
            main()

    def fileshare():
        import ProgramFiles.Utilities.FileSharing.FileSharing as filesharing
        filesharing.main()

    def OnlineBanking():
        def setup():
            import ProgramFiles.Utilities.ParodyBank.v5.bankaccountdatabase as setupAcc
            setupAcc.main()
        def launch():
            import ProgramFiles.Utilities.ParodyBank.v5.bankaccounts as launchApp
            launchApp.main()
        a = tkinter.Toplevel()
        a.configure(background=THEME_WINDOW_BG)
        msg = tkinter.Label(a, text="Do you want to setup the program, or to directly launch the app?")
        msg.grid(row=0, column=0)
        setup_btn = tkinter.Button(a, text="Setup Bank Account", command=setup,
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        setup_btn.grid(row=1, column=0)
        launch_main = tkinter.Button(a, text="Launch App", command=launch,
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        launch_main.grid(row=1, column=1)
        a.mainloop()

    def FileManager():
        global THEME_FOREGROUND
        global THEME_WINDOW_BG
        filepath = None
        def lookUpFiles(path):
            nonlocal filepath
            addressBar.delete(0, tkinter.END)
            filepath = path
            addressBar.insert(tkinter.END, path)
            filesInFolder = os.listdir(path)
            for i in fileView.get_children():
                fileView.delete(i)
            for file in range(len(filesInFolder)):
                fileView.configure(style="Treeview")
                fileView.insert(parent='', iid=file, text='', index='end', values=[filesInFolder[file]],)
        def openFileOrFolder(*event):
            nonlocal filepath
            SFI = fileView.selection()
            selectedFileIndex = fileView.focus()
            selectedFile = fileView.item(selectedFileIndex, 'values')[0]
            print(selectedFile, SFI, SFI[0])
            if os.path.isdir(f"{os.path.join(filepath, selectedFile)}"):
                filepath = os.path.join(filepath, selectedFile)
                lookUpFiles(filepath)
            else:
                os.startfile(f"{filepath}")

        def goBackFolder(path: str):  
            if "\\" in path:
                path = path.replace("\\", "/")
                print(path)
            folderSplit = path.split("/")
            if folderSplit[-1] == '':
                folderSplit.pop(-1)
            folderSplit.pop(-1)
            print(folderSplit)
            path = str().join(f"{folder}/" for folder in folderSplit)
            print(path)
            addressBar.delete(0, tkinter.END)
            addressBar.insert(tkinter.END, path)
            lookUpFiles(path=path)
        fileManagerWindow = tkinter.Toplevel(ROOT_WINDOW, background=THEME_WINDOW_BG)
        fileManagerWindow.title("File Manager")
        ttk.Style(fileManagerWindow).configure("Treeview", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        mainFrame = tkinter.Frame(fileManagerWindow, background=THEME_WINDOW_BG)
        mainFrame.grid(row=0, column=0)
        addressBar = tkinter.Entry(mainFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=100)
        addressBar.insert(tkinter.END, os.getcwd())
        checkTheme(addressBar)
        goButton = tkinter.Button(mainFrame, text="Go!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=lambda: lookUpFiles(addressBar.get()))
        goButton.grid(row=0, column=1, sticky="nw")
        goBackButton = tkinter.Button(mainFrame, text="Go back!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                    command=lambda: goBackFolder(path=addressBar.get()))
        goBackButton.grid(row=0, column=2, sticky="nw", padx=2)
        addressBar.grid(row=0, column=0, sticky="n")
        # driveSelection = ttk.Treeview(mainFrame, style="Treeview")
        # driveSelection.grid(row=0, column=0, sticky="w")
        # driveSelection['column'] = "Drives"
        # driveSelection.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        # driveSelection.column("Drives", anchor=tkinter.W, width=100)
        # driveSelection.heading("Drives", text="Drives", anchor=tkinter.CENTER)
        fileView = ttk.Treeview(mainFrame, style="Treeview")
        fileView.grid(row=1, column=0, sticky="w")
        fileView['column'] = "Files"
        fileView.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        fileView.column("Files", anchor=tkinter.W, width=600)
        fileView.heading("Files", text="Files", anchor=tkinter.CENTER)
        fileView.bind("<<TreeviewSelect>>", openFileOrFolder)
        fileView.configure(style="Treeview")
        fileManagerWindow.mainloop()
    
    def UpdateManager():
        import ProgramFiles.updateManager as updateManager
        updateManager.main(notification)
    
    def LoadExternalApps():
        externalApps = tkinter.Toplevel(background="Black")
        externalAppsName = []
        buttonText = "Look for external apps!"
        def refresh():
            global externalAppsList
            for file in Path(os.getcwd()).glob("*SETUP.py"):
                externalAppsName.append(file)
            for i in externalAppsList.get_children():
                externalAppsList.delete(i)
            for file in range(len(externalAppsName)):
                externalAppsList.configure(style="Treeview")
                externalAppsList.insert(parent='', iid=file, text='', index='end', values=[externalAppsName[file]],)
        def load(file: str = None):
            if file == None:
                indexSelect = externalAppsList.focus()
                fileToStart = externalAppsList.item(indexSelect, 'values')[0]
            else:
                fileToStart = file
            cwd = os.getcwd()
            os.chdir("/")
            import platform
            if platform.system() == "Windows": rmstr = "C:\\"
            else: rmstr = os.path.abspath("/")
            os.system(f"python3 '{fileToStart.removeprefix(rmstr)}'")
            os.chdir(cwd)
        def show():
            global externalAppsList
            nonlocal buttonText
            nonlocal showRefreshBtn
            buttonText = "Refresh"
            showRefreshBtn.configure(text=buttonText)
            externalAppsList = ttk.Treeview(externalApps, style="Treeview")
            externalAppsList.grid(row=1, column=0, sticky="w")
            externalAppsList['column'] = "Apps"
            externalAppsList.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
            externalAppsList.column("Apps", anchor=tkinter.W, width=600)
            externalAppsList.heading("Apps", text="Apps", anchor=tkinter.CENTER)
            externalAppsList.bind("<<TreeviewSelect>>", load)
            externalAppsList.configure(style="Treeview")
        def loadCustomApp():
            fileToOpen = filedialog.askopenfilename(title="Select app to run!", filetypes=(("Windows 11 Apps", "*.py"), ("All Files", "*.*")))
            load(file=fileToOpen)
        showRefreshBtn = tkinter.Button(externalApps, text=buttonText, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=show)
        showRefreshBtn.grid(row=0, column=0)
        loadCusttomBtn = tkinter.Button(externalApps, text="Load Custom App!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=loadCustomApp)
        loadCusttomBtn.grid(row=0, column=1)
        externalApps.mainloop()
            



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
    def launchComboBoxEvent(self, e):
        Item = launcherComboBox.get()
        exec(f"Apps.{Item}()")

    def currentTime(self):
        cr_time = time.strftime("%H:%M:%S %p")
        clock = tkinter.Label(ROOT_WINDOW, text=cr_time, background=THEME_WINDOW_BG,
                                foreground=THEME_FOREGROUND)
        clock.after(1000, self.currentTime)
        clock.grid(row=0, column=2, sticky="ne")

    def pinApps(self, appToPin):
        global appsFrame
        self.PINNED_APPS.append(f"{appToPin}")
        with open("ProgramFiles/pinnedApps.txt", "a") as pinnedApps:
            pinnedApps.write(f"{appToPin},\n")
        exec(f"{appToPin} = tkinter.Button(appsFrame, text='{appToPin}', command=Apps.{appToPin},"
            f"background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)\n{appToPin}.grid(row=0, column={len(self.PINNED_APPS) - 1})")

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
                messagebox.showerror("Error", str(problem))
    def createAppIcon(self, appName: str, command: str, event=None):
        """ creates desktop icons!"""
        global desktopFrame
        global COLUMN_COUNT_DESKTOP_ICONS, ROW_COUNT_DESKTOP_ICONS
        if ROW_COUNT_DESKTOP_ICONS > MAX_ROW_DESKTOP:
            if COLUMN_COUNT_DESKTOP_ICONS > MAX_COLUMN_DESKTOP:
                messagebox.showerror("Can't place the item! no more space left!")
            else:
                COLUMN_COUNT_DESKTOP_ICONS += 1
        if appName not in self.CurrentDesktopIconsList:
            exec(f"{appName}Frame = tkinter.Frame(desktopFrame, background=THEME_WINDOW_BG)")
            exec(f"{appName}Frame.grid(row=ROW_COUNT_DESKTOP_ICONS, column=COLUMN_COUNT_DESKTOP_ICONS)")
            ROW_COUNT_DESKTOP_ICONS += 1
            exec(f"{appName}ICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/{appName}.png')")
            exec(f"{appName}BTN = tkinter.Button({appName}Frame, image={appName}ICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command={command})")
            exec(f"{appName}BTN.IMGREF = {appName}ICON")
            exec(f"{appName}BTN.grid(row=0, column=0)")
            exec(f"{appName}LABEL = tkinter.Label({appName}Frame, text=f'{appName}', background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)")
            exec(f"{appName}LABEL.grid(row=1, column=0)")
            self.CurrentDesktopIconsList.append(command.split(".")[1])
        else:
            messagebox.showerror("App already exists!", "the app already exists!")
    def refreshDesktop(self):
        pass
    def addNewIcon(self, *args):
        iconToAdd = None
        addNewIcon = tkinter.Toplevel(background=THEME_WINDOW_BG)
        desktopAppsList = ttk.Combobox(addNewIcon)
        for i, z in enumerate(self.CurrentDesktopIconsList):
            CURRENT_LIST = APPS_LIST
            try:
                CURRENT_LIST = CURRENT_LIST.pop(APPS_LIST.index(z))
            except Exception as problem:
                print(f"<<DEBUG: ERROR OCCURED!\n<<ERROR: {problem} >>\n")
            desktopAppsList['values'] = CURRENT_LIST
        def updateVariable(event=None):
            nonlocal iconToAdd
            iconToAdd = str(desktopAppsList.get())
        desktopAppsList.bind("<<ComboboxSelected>>", updateVariable)
        desktopAppsList['state'] = "readonly"
        desktopAppsList.grid(row=0, column=0, sticky="w")      
        addIconBtn = tkinter.Button(addNewIcon, text="Add Icon!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: self.createAppIcon(iconToAdd, f"Apps.{iconToAdd}"))
        addIconBtn.grid(row=0, column=1)
        addNewIcon.mainloop()


def main():
    global launcherComboBox
    global contextMenu
    global ROOT_WINDOW
    global APPS_LIST
    global notificationsButton
    global desktopFrame
    global PINNED_APPS
    global GuiInterfaceCommands
    global appsFrame
    pinned_apps = []
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
                messagebox.showerror("Error", str(problem))

    PINNED_APPS = FTRConfigSettings("ProgramFiles/pinnedApps.txt", str(pinned_apps))
    GuiInterfaceCommands = GUIButtonCommand()
    ROOT_WINDOW = tkinter.Tk()
    ROOT_WINDOW.configure(background=THEME_WINDOW_BG)
    launcherComboBox = ttk.Combobox(ROOT_WINDOW)
    APPS_LIST = ["Notepad", "fileshare", "OnlineBanking", "BlackJack", "FileManager", 
                "UpdateManager", "LoadExternalApps"]

    launcherComboBox['values'] = APPS_LIST
    launcherComboBox['state'] = "readonly"
    launcherComboBox.bind("<<ComboboxSelected>>", GuiInterfaceCommands.launchComboBoxEvent)
    launcherComboBox.grid(row=0, column=0, sticky="w")
    appsFrame = tkinter.Frame(ROOT_WINDOW, background=THEME_WINDOW_BG, border=5)
    contextMenu = tkinter.Menu(appsFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    contextMenu.add_command(label="Taskbar settings", command=GuiInterfaceCommands.taskbarSettingsGUI)
    shutDown = tkinter.Button(appsFrame, text="Shutdown", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=ROOT_WINDOW.quit)
    shutDown.grid(row=0, column=0, padx=5)
    appsFrame.bind("<Button-3>", GuiInterfaceCommands.popup)
    appsFrame.grid(row=0, column=1, sticky="n")
    notificationsButton = tkinter.Button(ROOT_WINDOW, text="Notifications (0)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command= lambda: notification.showNotificationsList(notification))
    notificationsButton.grid(row=0, column=3, sticky="ne", padx=5)
    desktopFrame = tkinter.Frame(ROOT_WINDOW, background=THEME_WINDOW_BG, border=15)
    GuiInterfaceCommands.createAppIcon("Notepad", 'Apps.Notepad')
    GuiInterfaceCommands.createAppIcon("Files", 'Apps.FileManager')
    desktopContextMenu = tkinter.Menu(appsFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    desktopContextMenu.add_command(label="Refresh", command=GuiInterfaceCommands.refreshDesktop)
    desktopContextMenu.add_command(label="Add new icon", command=GuiInterfaceCommands.addNewIcon)
    ROOT_WINDOW.bind("<Button-3>", popup)
    desktopFrame.grid(row=1, column=0)
    ROOT_WINDOW.mainloop()
def loginVerification():
    global userNameText
    global passwordText
    with open("ProgramFiles/accConfiguration.conf", "r") as verify:
        username, password = verify.readlines()
        username = username.removesuffix('\n')
        password = password.removesuffix('\n')
        if userNameText.get() == username and passwordText.get() == password:
            loginWindow.destroy()
            main()
        else:
            messagebox.showerror("Incorrect Username or Password", "The password or username (or both) are incorrect. try again!")

def checkTheme(*widgets):
    global widget
    if THEME_WINDOW_BG in DARK_COLOURS:
        for widget in widgets:
            widget.configure(insertbackground="white",
                                selectbackground='white',
                                selectforeground='black')
DARK_COLOURS = ['black', 'brown', 'blue', 'green', 'red', 'violet', 'purple', 'dark blue', 'dark green',
                'dark red', 'dark brown', ]
loginWindow = tkinter.Tk()
loginWindow.title("Login to Windows 11")
loginWindow.configure(background=THEME_WINDOW_BG)
msg = tkinter.Label(loginWindow, text="Enter your Username: ", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
msg.grid(row=0, column=0)
userNameText = tkinter.Entry(loginWindow, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
userNameText.grid(row=0, column=1)
userNameText.configure(insertbackground="white", selectbackground='white', selectforeground='black')
msg2 = tkinter.Label(loginWindow, text="Enter your Password", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
msg2.grid(row=1, column=0)
passwordText = tkinter.Entry(loginWindow, foreground=THEME_FOREGROUND, background=THEME_WINDOW_BG)
passwordText.grid(row=1, column=1)
passwordText.configure(insertbackground="white", selectbackground='white', selectforeground='black')
checkTheme(userNameText, passwordText)
loginBtn = tkinter.Button(loginWindow, text="Login", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                            command=loginVerification)
loginBtn.grid(row=2, column=1)
loginWindow.mainloop()
