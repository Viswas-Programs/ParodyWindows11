from datetime import datetime
import sys
import os
    
def FTRConfigSettings(path, data: str or None=None, prepCodeBool=False, prepCode=None) -> tuple:
    if prepCodeBool: exec(prepCode)
    if os.access(path, os.F_OK):
        with open(path) as read_config:
            config = read_config.read().splitlines()
    else:
        with open(path, "w") as FTR_write_config: #FirstTimeRun_Write_config, full form.
            FTR_write_config.write(data)
            config = data.splitlines()
    return config
THEME_WINDOW_BG, THEME_FOREGROUND = FTRConfigSettings("theme_config.txt", f"Black\nWhite")
searchHistory = FTRConfigSettings("ProgramFiles/history.txt", "")
searchHistory = list(searchHistory[0:])
# emailSetup = FTRConfigSettings("PRogramFiles/emails.txt", "SETUP NEEDED!")[0]
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
import subprocess
class Settings():
    from tkinter import colorchooser
    import tkinter
    def __init__(Settings):
        Settings.SHOWN_HOMEPAGE = False
        Settings.SHOWN_PERSONALIZATION = False
        Settings.SHOWN_ADVANCED = False
        Settings.total_memory = "ERROR FINDING MEMORY AMOUNT!"
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
        if Settings.SHOWN_PERSONALIZATION: Settings.setting.destroy()
        Settings.setting =  tkinter.Frame(Settings.settingsWindow, background=THEME_WINDOW_BG)
        Settings.setting.grid(row=0, column=1)
        Settings.SHOWN_HOMEPAGE = True
        infoText = f""" Windows 11 v2.0\nSystem RAM: {Settings.total_memory}\nBackground={THEME_WINDOW_BG}\n
        Foreground={THEME_FOREGROUND}\n\nFor more info, please visit the respective categories! Thank you :)"""
        a = tkinter.Label(Settings.setting, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=infoText).grid(row=0, column=0)
    def personalization(Settings):
        def changeBg():
            global children
            global THEME_WINDOW_BG
            colorToUse = Settings.colorchooser.askcolor(title="Select background!")
            THEME_WINDOW_BG = colorToUse[1]
            crBg.configure(text=f"Current Background = {THEME_WINDOW_BG}")
            with open("theme_config.txt", "w") as writeNewTheme: writeNewTheme.write(f"{THEME_WINDOW_BG}\n{THEME_FOREGROUND}")
            for child in children:
                try:
                    child.configure(background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                except Exception: pass
            ROOT_WINDOW.update()
        def changeFg():
            global children
            global THEME_FOREGROUND
            colorToUse = Settings.colorchooser.askcolor(title="Select foreground!")
            THEME_FOREGROUND = colorToUse[1]
            crFg.configure(text=f"Current foreground = {THEME_FOREGROUND}")
            with open("theme_config.txt", "w") as writeNewTheme: writeNewTheme.write(f"{THEME_WINDOW_BG}\n{THEME_FOREGROUND}")
            for child in children:
                try:
                    child.configure(background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
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
        
class Apps(object):
    global IPChatContacts
    isInstalledTKWEB = FTRConfigSettings("ProgramFiles/tkweb.txt", "Not installed")
    if isInstalledTKWEB[0] != "Installed":
        notification.createNotification("tkinterweb module is being installed for web browsers", datetime.now(), None)
        os.system(""" pip3 install tkinterWeb""")
        with open("ProgramFiles/tkweb.txt", "w") as updtext: updtext.write("Installed")
    def BlackJack():
        """
        blackjack game activator
        :return: None
        """
        import ProgramFiles.blackjack.blackjack as GUIBlackjack
        PROCESS_RUNNING = True
        GUIBlackjack.play()
        PROCESS_RUNNING = False

    def Notepad():
        import ProgramFiles.Notepad.Notepad as notepad
        PROCESS_RUNNING = True
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
        PROCESS_RUNNING = False

    def fileshare():
        import ProgramFiles.FileSharing.FileSharing as filesharing
        PROCESS_RUNNING = True
        filesharing.main()
        PROCESS_RUNNING = False

    def OnlineBanking():
        PROCESS_RUNNING = True
        def setup():
            import ProgramFiles.ParodyBank.v5.bankaccountdatabase as setupAcc
            setupAcc.main()
        def launch():
            import ProgramFiles.ParodyBank.v5.bankaccounts as launchApp
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
        PROCESS_RUNNING = False

    def FileManager():
        PROCESS_RUNNING = True
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
                os.system(f"{filepath}")

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
        PROCESS_RUNNING = False
    
    def UpdateManager():
        import ProgramFiles.updateManager as updateManager
        PROCESS_RUNNING = True
        updateManager.main(notification)
        PROCESS_RUNNING = False
    
    def LoadExternalApps(use_legacy=False):
        PROCESS_RUNNING = True
        externalApps = tkinter.Toplevel(background=THEME_WINDOW_BG)
        externalAppsName = []
        buttonText = "Look for external apps!"
        def refresh():
            global externalAppsList
            for i in externalAppsList.get_children():
                externalAppsList.delete(i)
            for dirpath, dirnames, filenames in os.walk(os.getcwd(), topdown=True):
                for file in Path(dirpath).glob("*SETUP.py"):
                    externalAppsName.append(file)
            for file in range(len(externalAppsName)):
                externalAppsList.configure(style="Treeview")
                for i in externalAppsList.get_children():
                    externalAppsList.delete(i)
                externalAppsList.insert(parent='', iid=file, text='', index='end', values=[externalAppsName[file]],)
        def load(file: str = None, e=None):
            if file == None:
                indexSelect = externalAppsList.focus()
                fileToStart = externalAppsList.item(indexSelect, 'values')[0]
            else:
                fileToStart = file
            # The old code, this code actually failed because of the os call, and when the program is running
            #Yeah, as the program is running, the OS will freeze untill the program is closed somehow
            #So this idea was scrapped to a better solution, to use the subprocess.Popen method to do the thing without freezing the OS
            # So below is the old, failed code.
            # Note: If you want to access this code from function calls (ie not editing source code directly), 
            # Then, use the "use_legacy" parameter of the LoadExternalApps function to use the legacy code. 
            # OR: There is a setting deep under the settings, enable (legacy code) option to use the legacy code.
            if use_legacy:
                cwd = os.getcwd()
                os.chdir("/")
                import platform
                if platform.system() == "Windows": rmstr = "C:\\"
                else: rmstr = os.path.abspath("/")
                os.system(f"""python3 "{fileToStart}" """)
                os.chdir(cwd)
            else:
                subprocess.Popen(["python3", f"{fileToStart}"])
        def show(e=None):
            global externalAppsList
            nonlocal buttonText
            nonlocal showRefreshBtn
            buttonText = "Refresh"
            showRefreshBtn.configure(text=buttonText, command=refresh)
            externalAppsList = ttk.Treeview(externalApps, style="Treeview")
            externalAppsList.grid(row=1, column=0, sticky="w")
            externalAppsList['column'] = "Apps"
            externalAppsList.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
            externalAppsList.column("Apps", anchor=tkinter.W, width=600)
            externalAppsList.heading("Apps", text="Apps", anchor=tkinter.CENTER)
            def a(e=None): load(None)
            externalAppsList.bind("<<TreeviewSelect>>", a)
            externalAppsList.configure(style="Treeview")
            refresh()
        def loadCustomApp():
            fileToOpen = filedialog.askopenfilename(title="Select app to run!", filetypes=(("Windows 11 Apps", "*.py"), ("All Files", "*.*")))
            load(file=fileToOpen)
        showRefreshBtn = tkinter.Button(externalApps, text=buttonText, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=show)
        showRefreshBtn.grid(row=0, column=0)
        loadCusttomBtn = tkinter.Button(externalApps, text="Load Custom App!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=loadCustomApp)
        loadCusttomBtn.grid(row=0, column=1)
        externalApps.mainloop()
        PROCESS_RUNNING = False
    def WebBrowser():
        PROCESS_RUNNING = True
        searchHistory = shelve.open("ProgramFiles/history")
        searches = []
        searchNo = -1
        DARK_THEME = False 

        def browse():
            global frame
            searches.append(text.get())
            from tkinterweb import HtmlFrame
            def a(title):
                searchHistory[str(datetime.now())] = title
                root.title(title)
            def addToList(url):
                nonlocal searches
                nonlocal searchNo
                nonlocal text
                searches.append(str(url))
                searchNo += 1
                frame.load_url(url)
                frame.enable_dark_theme(True, True)
                text.delete(0, tkinter.END)
                text.insert(0, url)
            frame = HtmlFrame(mainFrame)
            frame.load_website(text.get()) 
            frame.on_link_click(addToList)
            if DARK_THEME: frame.enable_dark_theme(True, True)
            frame.on_title_change(a)
            frame.grid(row=1, column=0)
        def optionsWindow(e=None):
            SHOWN_HISTORY = False
            SHOWN_ABOUT = False
            SHOWN_PERSONALIZATION = False
            nonlocal DARK_THEME
            def showHistory():
                nonlocal SHOWN_HISTORY
                global historyFrame
                SHOWN_HISTORY = True
                if SHOWN_ABOUT: aboutFrame.destroy()
                if SHOWN_PERSONALIZATION: perFrame.destroy()
                historyFrame = tkinter.Frame(optionsWn, background=THEME_WINDOW_BG, width=90, height=120)
                historyFrame.grid(row=0, column=1)
                for i, (time, search) in enumerate(searchHistory.items()):
                    exec(f"a{i} = tkinter.Label(historyFrame, text='{search}', background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)")
                    exec(f"a{i}.grid(row=i, column=0)")
                    exec(f"n{i} = tkinter.Label(historyFrame, text=':{time}', background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)")
                    exec(f"n{i}.grid(row=i, column=1)")
            def showAbout():
                nonlocal SHOWN_ABOUT
                global aboutFrame
                SHOWN_ABOUT = True
                if SHOWN_HISTORY: historyFrame.destroy()
                if SHOWN_PERSONALIZATION: perFrame.destroy()
                aboutFrame = tkinter.Frame(optionsWn, background=THEME_WINDOW_BG)
                aboutFrame.grid(row=0, column=1)
                about = tkinter.Label(aboutFrame, text=
                "Python Web browser v2.0\nThis doesn't use modern javascript, so JS has no support, period.",
                background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                about.grid(row=0, column=0)
            def darkThemeMenu(e=None):
                nonlocal DARK_THEME
                nonlocal SHOWN_PERSONALIZATION
                global perFrame
                nonlocal DARK_THEME
                perFrame = tkinter.Frame(optionsWn, background=THEME_WINDOW_BG)
                perFrame.grid(row=0, column=1)
                def changeTheme(e=None): frame.enable_dark_theme(True, True); DARK_THEME = True
                def revChanges(e=None): frame.enable_dark_theme(False, False); DARK_THEME = False
                change = tkinter.Button(perFrame, text="Experimental dark theme! (on)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=changeTheme)
                change.grid(row=0, column=0)
                revchange = tkinter.Button(perFrame, text="Experimental dark theme! (off)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=revChanges)
                revchange.grid(row=1, column=0)
            optionsWn = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
            btnFrame = tkinter.Frame(optionsWn, background=THEME_WINDOW_BG)
            btnFrame.grid(row=0, column=0)
            historyBtn = tkinter.Button(btnFrame, text="History", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=showHistory)
            historyBtn.grid(row=0, column=0)
            aboutBtn = tkinter.Button(btnFrame, text="About", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=showAbout)
            aboutBtn.grid(row=1, column=0)
            changeBtn = tkinter.Button(btnFrame, text="Personalization", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=darkThemeMenu)
            changeBtn.grid(row=2, column=0)
            optionsWn.mainloop()

        def goBack(e=None):
            if frame:
                frame.load_website(searches[searchNo-2])
                if DARK_THEME: frame.enable_dark_theme(True, True)
                nonlocal text
                text.delete(0, tkinter.END)
                text.insert(searches[searchNo-2])
        def reloadWebsite(e=None):
            if frame:
                frame.load_website(searches[searchNo-1])
                if DARK_THEME: frame.enable_dark_theme(True, True)

        root = tkinter.Toplevel(background=THEME_WINDOW_BG)
        mainFrame = tkinter.Frame(root, background=THEME_WINDOW_BG)
        mainFrame.grid(row=1, column=0)
        btnFrame = tkinter.Frame(mainFrame, background=THEME_WINDOW_BG)
        btnFrame.grid(row=0, column=0)
        backButton = tkinter.Button(btnFrame, text="<-", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=goBack)
        backButton.grid(row=0, column=0)
        reloadButton = tkinter.Button(btnFrame, text="Reload", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=reloadWebsite)
        reloadButton.grid(row=0, column=1)
        text = tkinter.Entry(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=90)
        text.grid(row=0, column=2)
        text.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
        btn = tkinter.Button(btnFrame, text="Go!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=browse)
        btn.grid(row=0, column=3)
        exec(f"optionsICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/Settings.png').subsample(2, 2)")
        exec(f"optionsBTN = tkinter.Button(btnFrame, image=optionsICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=optionsWindow)")
        exec(f"optionsBTN.IMGREF = optionsICON")
        exec(f"optionsBTN.grid(row=0, column=4)")
        root.mainloop()
        searchHistory.close()
        PROCESS_RUNNING = False
    def AlarmsAndTimer():
        import datetime
        alarmWindow = tkinter.Toplevel(background=THEME_WINDOW_BG)
        sidebar = tkinter.Frame(alarmWindow, background=THEME_WINDOW_BG)
        sidebar.grid(row=0, column=0)
        SHOWN_TIMER = False
        SHOWN_ALARMS = False
        def showTimer(e=None):
            def updateTime(e=None):
                timerTime = int(timerEntry.get())
                timerLabel = tkinter.Label(timerFrame, text=f"{timerTime}", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                timerLabel.grid(row=0, column=0)
                for t in range(0, timerTime):
                    if t == timerTime:
                        timerLabel.configure(text='0')
                    timerLabel.configure(text=f"{timerTime-t}")
                    timerFrame.update()
                    alarmWindow.update()
                    time.sleep(1)
                # while timerTime > 0:
                #     timerFrame.after(1000, updateLabel)
                #     if timerTime == 0:
                #         timerLabel.configure(text="0")
                #         break
                else:
                    messagebox.showerror("Timer finished", "Timer ran out!!!")

                    
            nonlocal SHOWN_ALARMS
            global timerFrame
            global alarmFrame
            if SHOWN_ALARMS: alarmFrame.destroy()
            SHOWN_ALARMS = False
            timerFrame = tkinter.Frame(alarmWindow, background=THEME_WINDOW_BG)
            timerFrame.grid(row=0, column=1)
            timerEntry = tkinter.Entry(timerFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            timerEntry.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
            timerEntry.grid(row=1, column=0)
            startTimerBtn = tkinter.Button(timerFrame, text="Start Timer!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=updateTime)
            startTimerBtn.grid(row=1, column=1)
            
        def showAlarms(e=None):
            nonlocal SHOWN_TIMER
            global timerFrame
            global alarmFrame
            if SHOWN_TIMER: timerFrame.destroy()
            SHOWN_TIMER = False
            alarmFrame = tkinter.Frame(alarmWindow, background=THEME_WINDOW_BG)
            alarmFrame.grid(row=0, column=1)
        timerBtn = tkinter.Button(sidebar, text="Timer", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=showTimer)
        timerBtn.grid(row=0, column=0)
        alarmBtn = tkinter.Button(sidebar, text="Alarm", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=showAlarms)
        alarmBtn.grid(row=1, column=0)
        alarmWindow.mainloop()
    def Mail():
        NOT_IMPLEMENTED = True
        def setup():
            if emailSetup == "SETUP NEEDED!":
                setupEmailAccount = tkinter.Toplevel(mailWindow, backgruond=THEME_WINDOW_BG)
                tkinter.Label(setupEmailAccount, text="Enter your email address", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=0, column=0)
                emailAddress = tkinter.Entry(setupEmailAccount, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                emailAddress.grid(row=0, column=1)
                emailAddress.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
                tkinter.Label(setupEmailAccount, text="Enter your password", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=1, column=0)
                password = tkinter.Entry(setupEmailAccount, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                password.grid(row=1, column=1)
                password.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
                tkinter.Label(setupEmailAccount, text="Enter your IMAP server", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=2, column=0)
                imapserver = tkinter.Entry(setupEmailAccount, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
                imapserver.grid(row=2, column=1)
                imapserver.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
                setupEmailAccount.mainloop()
        mailWindow = tkinter.Toplevel(background=THEME_WINDOW_BG)
        mailWindow.mainloop()
        if NOT_IMPLEMENTED:
            raise NotImplementedError("This particular app hasn't been developed fully yet!")
    def ControlPanel():
        settingInstance = Settings()
    def IPChat():
        from socket import AF_INET, socket, SOCK_STREAM
        from threading import Thread
        def receive():
            """Handles receiving of messages."""
            while True:
                try:
                    msg = client_socket.recv(BUFSIZ).decode("utf8")
                    msg_list.insert(tkinter.END, msg)
                except OSError:  # Possibly client has left the chat.
                    break


        def send(event=None):  # event is passed by binders.
            """Handles sending of messages."""
            msg = my_msg.get() 
            client_socket.send(bytes(msg, "utf8"))
            my_msg.set("") # Clears input field.
            if msg == "{quit}":
                client_socket.close()
                top.destroy()


        def on_closing(event=None):
            """This function is to be called when the window is closed."""
            try:
                my_msg.set("{quit}")
                send()
            except Exception as PROBLEM:
                messagebox.showerror("Program Can't Close!", f"<<DEBUG: {PROBLEM}>>\nThe chatter app cannot close the normal way (ie, saying 'leaving chat' automatically) due to error\nSo, program is force quitting... ")
                top.destroy()
        def configureServer(event=None):
            def configureS(e=None):
                nonlocal HOST
                nonlocal PORT
                HOST = ipAddressEntry.get()
                PORT = int(portEntry.get())
                with shelve.open("ProgramFiles/IPChat/_serverConfig") as writeServerConfig:
                    writeServerConfig['0'] = ipAddressEntry.get()
                    writeServerConfig['1'] = int(portEntry.get())
                print("Getting there")
                with shelve.open("ProgramFiles/IPChat/serversList") as updateList:
                    print("Came to the writing part")
                    updateList[ipAddressEntry.get()] = int(portEntry.get())
                    print(updateList[ipAddressEntry.get()])
                    print("IT WORKS")
                try:
                    nonlocal client_socket
                    client_socket.close()
                except Exception: pass
                else:
                    ADDR = (HOST, PORT)
                    client_socket = socket(AF_INET, SOCK_STREAM)
                    client_socket.connect(ADDR)

            serverConfWn = tkinter.Toplevel(background=THEME_WINDOW_BG)
            tkinter.Label(serverConfWn, text="Configure IP Address", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=0, column=0)
            ipAddressEntry = tkinter.Entry(serverConfWn, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            ipAddressEntry.grid(row=0, column=1)
            ipAddressEntry.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
            tkinter.Label(serverConfWn, text="Configure port", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=1, column=0)
            portEntry = tkinter.Entry(serverConfWn, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            portEntry.grid(row=1, column=1)
            portEntry.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
            submitButton = tkinter.Button(serverConfWn, text="Submit", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=configureS)
            submitButton.grid(row=2, column=1)
            serverConfWn.mainloop()
        def getServerList(e=None):
            def connect(e=None):
                try:
                    nonlocal client_socket
                    client_socket.close()
                except Exception:
                    messagebox.showerror("Can't connect", f"Cannot connect to {serverListLB.get(tkinter.ANCHOR)} at port {servers[serverListLB.get(tkinter.ANCHOR)]} due to error!")
                else:
                    ADDR = (serverListLB.get(tkinter.ANCHOR), servers[serverListLB.get(tkinter.ANCHOR)])
                    client_socket = socket(AF_INET, SOCK_STREAM)
                    client_socket.connect(ADDR)
            serverListWn = tkinter.Toplevel(background=THEME_WINDOW_BG)
            serverListLB = tkinter.Listbox(serverListWn, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            serverListLB.pack()
            with shelve.open("ProgramFiles/IPChat/serversList") as serversStored:
                global servers
                servers = serversStored
                print(serversStored)
                for server in serversStored.keys():
                    print(server)
                    serverListLB.insert(tkinter.END, server)
            serverListLB.bind("<<ListboxSelect>>", connect)
            serverListWn.mainloop()

        top = tkinter.Toplevel(background=THEME_WINDOW_BG)
        top.title("Chatter")
        altMenu = tkinter.Menu(top, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        top.configure(menu=altMenu)
        fileMenu = tkinter.Menu(altMenu, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        fileMenu.add_command(label="Configure Server", command=configureServer)
        fileMenu.add_command(label="Previously connected servers", command=getServerList)
        altMenu.add_cascade(label="File", menu=fileMenu)
        messages_frame = tkinter.Frame(top, background=THEME_WINDOW_BG)
        my_msg = tkinter.StringVar()  # For the messages to be sent.
        my_msg.set("Type your messages here.")
        scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
        msg_list = tkinter.Listbox(messages_frame, height=20, width=90, yscrollcommand=scrollbar.set, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        msg_list.pack()
        messages_frame.pack()

        entry_field = tkinter.Entry(top, textvariable=my_msg, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=90)
        entry_field.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
        entry_field.bind("<Return>", send)
        entry_field.pack()
        send_button = tkinter.Button(top, text="Send", command=send, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        send_button.pack()

        top.protocol("WM_DELETE_WINDOW", on_closing)

        #----Now comes the sockets part----
        with shelve.open("ProgramFiles/IPChat/_serverConfig") as _serverConfig:
            HOST = _serverConfig['0']
            PORT = _serverConfig['1']

        BUFSIZ = 1024
        ADDR = (HOST, PORT)
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(ADDR)
        except Exception as problem:
            messagebox.showerror("Error connecting to server", f"Error connecting to server '{HOST}' at port '{PORT}'\n"
            "This may be due to a configuration error, or the failure to add a server. Please reconfigure!")

        receive_thread = Thread(target=receive)
        receive_thread.start()
        top.mainloop()


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
        exec(f"global {appToPin}BTN")
        # exec(f"global {appToPin}BTN")
        self.PINNED_APPS.append(f"{appToPin}")
        appName = appToPin
        with open("ProgramFiles/pinnedApps.txt", "a") as pinnedApps:
            pinnedApps.write(f"{appToPin}\n")
        # exec(f"{appToPin}IMAGE = tkinter.PhotoImage('ProgramFiles/Icons/{appToPin}.png')\n")
        # exec(f"{appToPin} = tkinter.Button(appsFrame, image={appToPin}IMAGE, compound=tkinter.LEFT, command=Apps.{appToPin},"
        #     f"background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)\n"
        #     f"{appToPin}.IMGREF = {appToPin}IMAGE\n"
        #     f"{appToPin}.grid(row=0, column={len(self.PINNED_APPS) - 1})")
        # def launchApp(btn, arg=None):
        #     exec(f"global {appToPin}BTN")
        #     PROCESS_RUNNING = True
        #     btn.configure(compound=tkinter.LEFT, text=f'{appToPin}')
        #     exec(f'Apps.{appToPin}()')
        #     PROCESS_RUNNING = False
        #     btn.configure(compound=tkinter.LEFT, text='')
        exec(f"{appName}ICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/{appName}.png').subsample(2, 2)")
        exec(f"{appName}BTN = tkinter.Button(appsFrame, image={appName}ICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=Apps.{appToPin})")
        exec(f"{appName}BTN.IMGREF = {appName}ICON")
        exec(f"{appName}BTN.grid(row=0, column={len(self.PINNED_APPS) - 1})")

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
        # for z in self.CurrentDesktopIconsList:
        #     CURRENT_LIST = APPS_LIST
        #     try:
        #         CURRENT_LIST = CURRENT_LIST.pop(APPS_LIST.index(z))
        #     except Exception as problem:
        #         pass
        CURRENT_LIST = [APPS_LIST]
        for app in APPS_LIST:
            if app in self.CurrentDesktopIconsList:
                try:
                    CURRENT_LIST = CURRENT_LIST.pop(CURRENT_LIST.index(app))
                except Exception:
                    pass
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
    def shutdownMenu(self, e=None):
        global shutdownImage
        global restartImage
        def restart():
            if safeModeRestartVar.get() == 1:
                children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
                for child in children:
                    child.destroy()
                os.system("""python3 "Windows 11.py" -safemode """)
                exit()
            else:
                children = [launcherComboBox, contextMenu, appsFrame, notificationsButton, desktopFrame, desktopContextMenu, ROOT_WINDOW]
                for child in children:
                    child.destroy()
                os.system(""" python3 "Windows 11.py" """)
                exit()

        shutdownWindow = tkinter.Toplevel(background=THEME_WINDOW_BG)
        a = tkinter.Label(shutdownWindow, text="What you want to do now?", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        a.grid(row=0, column=0)
        exec(f"ShutdownICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/shutdown.png').subsample(2, 2)")
        exec(f"ShutdownBTN = tkinter.Button(shutdownWindow, image=ShutdownICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=exit)")
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
                notification.showNotification("Critical Error!", str(problem), datetime.now(), None)

    PINNED_APPS = FTRConfigSettings("ProgramFiles/pinnedApps.txt", str(pinned_apps))
    GuiInterfaceCommands = GUIButtonCommand()
    ROOT_WINDOW = tkinter.Tk()
    ROOT_WINDOW.configure(background=THEME_WINDOW_BG)
    launcherComboBox = ttk.Combobox(ROOT_WINDOW)
    APPS_LIST = ["Notepad", "fileshare", "OnlineBanking", "BlackJack", "FileManager", 
                "UpdateManager", "LoadExternalApps", "WebBrowser", "IPChat", "ControlPanel", "AlarmsAndTimer"]

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
    GuiInterfaceCommands.createAppIcon("Notepad", 'Apps.Notepad')
    GuiInterfaceCommands.createAppIcon("Files", 'Apps.FileManager')
    desktopContextMenu = tkinter.Menu(appsFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
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
    with open("ProgramFiles/accConfiguration.conf", "r") as verify:
        username, password = verify.readlines()
        username = username.rstrip('\n')
        password = password.rstrip('\n')
        if userNameText.get() == username and passwordText.get() == password:
            loginWindow.destroy()
            main()
        else:
            messagebox.showerror("Incorrect Username or Password", "The password or username (or both) are incorrect. try again!")

def checkTheme(widget):
    if THEME_WINDOW_BG in DARK_COLOURS:
        widget.configure(insertbackground=THEME_FOREGROUND,
                            selectbackground=THEME_FOREGROUND,
                            selectforeground=THEME_WINDOW_BG)
DARK_COLOURS = ["black", 'brown', 'blue', 'green', 'red', 'violet', 'purple', 'dark blue', 'dark green',
                'dark red', 'dark brown', ]
def login():
    from pathlib import Path
    from tkinter import filedialog
    import imaplib
    import email
    from email.header import decode_header
    import tkinterweb
    import tkinter
    from tkinter import messagebox
    import tkinterweb
    from tkinterweb import HtmlFrame
    import requests
    import shelve
    def safeModePREPTask(e=None):
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
    userNameText.bind("<Tab>", passwordText.focus)
    passwordText.bind("<Return>", loginVerification)
    loginBtn = tkinter.Button(loginWindow, text="Login", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=loginVerification)
    loginBtn.grid(row=2, column=1)
    shutdownBtn = tkinter.Button(loginWindow, text="Shutdown", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=lambda: GUIButtonCommand.shutdownMenu(GUIButtonCommand))
    shutdownBtn.grid(row=0, column=MAX_COLUMN_DESKTOP)
    loginWindow.attributes('-fullscreen', True)
    loginWindow.bind("<Escape>", safeModePREPTask)
    loginWindow.mainloop()
def safeMode():
        def a1():
            print("=" * int(os.get_terminal_size()[0]))
            print("repairing system...")
            try:
                Windows11MainDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/Windows 11.py", timeout=40)
                with open("Windows 11.py", "w") as writeTo:
                    try:
                        writeTo.write(Windows11MainDownload.content.decode(encoding="UTF-8"))
                    except UnicodeEncodeError as UER:
                        print(f"UnicodeDecodeError occured while repairing 'Windows 11.py'\n--MSG:{UER}")
            except Exception as PROBLEM:
                print(f"Repairing Failed!\nREASON: {PROBLEM}")
            finally:
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
        while True:
            print("Safe mode activated!\n=-=-=-=WELCOME=-=-=-=")
            while True:
                userInput1 = int(input("1. Repair your system\n"
                                "2. Continue to boot to main\n"
                                "3. Launch an app\n"
                                "4. Shutdown the system\n"
                                "5. Restart the system\n"
                                "Enter your option >_"))
                if userInput1 in range(1, 6):
                    exec(f"a{userInput1}()")
if __name__ == "__main__":
    arguements = sys.argv[1:]
    if "-safemode" in arguements:
        safeMode()
    else:
        try:
            from pathlib import Path
            from tkinter import filedialog
            import imaplib
            import email
            from email.header import decode_header
            import tkinterweb
            import tkinter
            from tkinter import messagebox
            import tkinterweb
            from tkinterweb import HtmlFrame
            import requests
            import shelve
            import socket
        except Exception as PROBLEM:
            print(f"Safe mode activated due to one of the modules not present. \n DEBUG: {PROBLEM}")
            safeMode()
        else:
            login()
