import tkinter
from tkinter import messagebox
import os


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
class Apps(object):
    def BlackJack():
        """
        blackjack game activator
        :return: None
        """
        import ProgramFiles.Games.blackjack.blackjack as GUIBlackjack
        GUIBlackjack.play()


    def GuessingGame():
        """ guessing game CLI"""
        import ProgramFiles.Games.CLI_Comp_Guess as CLIGuessingGame
        CLIGuessingGame.play()


    def ComputerGuesses():
        """ the computer guessing your number. don't have an indefinite answer :D"""
        import ProgramFiles.Games.CLI_Comp_Guess as CLICompGuess
        CLICompGuess.play()


    def MemoryHog():
        import ProgramFiles.Utilities.MemoryHoggerGUI as MemHgGUI
        MemHgGUI.thePointOfNoReturn()

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
        updateManager.main()
import tkinter.ttk as ttk
import time
class GUIButtonCommand(object):
    global launcherCombobox
    global APPS_LIST
    def launchComboBoxEvent(e):
        Item = launcherComboBox.get()
        exec(f"Apps.{Item}()")

    def currentTime():
        cr_time = time.strftime("%H:%M:%S %p")
        clock = tkinter.Label(ROOT_WINDOW, text=cr_time, background=THEME_WINDOW_BG,
                                foreground=THEME_FOREGROUND)
        clock.after(1000, GUIButtonCommand.currentTime)
        clock.grid(row=0, column=2, sticky="ne")

    def pinApps(appToPin):
        global PINNED_APPS
        PINNED_APPS = list(PINNED_APPS)
        PINNED_APPS.append(f"{appToPin}")
        with open("ProgramFiles/pinnedApps.txt", "a") as pinnedApps:
            pinnedApps.write(f"{appToPin},\n")
        exec(f"{appToPin} = tkinter.Button(appsFrame, text='{appToPin}', command=Apps.{appToPin},"
            f"background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)\n{appToPin}.grid(row=0, column={len(PINNED_APPS) - 1})")

    def taskbarSettingsGUI(e=None):
        global PINNED_APPS
        taskbarSettingsWindow = tkinter.Toplevel()
        taskbarSettingsWindow.configure(background=THEME_WINDOW_BG)
        taskbarSettingsWindow.title("Taskbar Settings")
        addWidgetsFrame = tkinter.LabelFrame(taskbarSettingsWindow, text="Add widgets", 
                                            background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        addWidgetsFrame.grid(row=0, column=0)
        addClock = tkinter.Button(addWidgetsFrame, text="Clock", foreground=THEME_FOREGROUND,
                                    background=THEME_WINDOW_BG, command=GUIButtonCommand.currentTime)
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
                exec(f"{app} = tkinter.Button(pinItems, text='{app}', command=lambda: GUIButtonCommand.pinApps('{app}'),"
                    f"background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)\n{app}.grid(row=r, column=0)")
        taskbarSettingsWindow.mainloop()

    def popup(event=None):
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

def main():
    global launcherComboBox
    global contextMenu
    global ROOT_WINDOW
    global APPS_LIST
    pinned_apps = []
    PINNED_APPS = FTRConfigSettings("ProgramFiles/pinnedApps.txt", str(pinned_apps))
    ROOT_WINDOW = tkinter.Tk()
    ROOT_WINDOW.configure(background=THEME_WINDOW_BG)
    launcherComboBox = ttk.Combobox(ROOT_WINDOW)
    APPS_LIST = ["Notepad", "fileshare", "OnlineBanking", "BlackJack", "ComputerGuesses", 
                "GuessingGame", "MemoryHog", "FileManager", "UpdateManager"]

    launcherComboBox['values'] = APPS_LIST
    launcherComboBox['state'] = "readonly"
    launcherComboBox.bind("<<ComboboxSelected>>", GUIButtonCommand.launchComboBoxEvent)
    launcherComboBox.grid(row=0, column=0, sticky="w")
    appsFrame = tkinter.Frame(ROOT_WINDOW, background=THEME_WINDOW_BG, border=5)
    contextMenu = tkinter.Menu(appsFrame, tearoff=False)
    contextMenu.add_command(label="Taskbar settings", command=GUIButtonCommand.taskbarSettingsGUI)
    shutDown = tkinter.Button(appsFrame, text="Shutdown", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=ROOT_WINDOW.quit)
    shutDown.grid(row=0, column=0, padx=5)
    appsFrame.bind("<Button-3>", GUIButtonCommand.popup)
    appsFrame.grid(row=0, column=1, sticky="n")

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
