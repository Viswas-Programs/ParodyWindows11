import tkinter
import requests
import shutil
import os
from tkinter import ttk
from ProgramFiles import callHost
from ProgramFiles.errorHandler import messagebox as msgbox
import datetime
import time
INSTANCES = {}

def FTRConfigSettings(path, data=None) -> tuple:
    if os.access(path, os.F_OK):
        with open(path) as read_config:
            config = read_config.read().splitlines()
            if config != "\n":
                return config
            else:
                msgbox.showerror("DEBUG!", "The data hasn't been loaded yet, because the data doesn't exist in the load!")
    else:
        with open(path, "w") as FTR_write_config: #FirstTimeRun_Write_config, full form.
            FTR_write_config.write(data)
    return config

try:
    changelogText = str(requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/CHANGELOG.txt").content.decode(encoding="utf-8"))
    NEW_VERSION = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/VERSION.txt").content.decode(encoding='utf-8').splitlines()
    version, branch = NEW_VERSION[0], NEW_VERSION[1]
    fileList = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/FILE_CHANGES.txt").content.decode(encoding='utf-8').splitlines()
except requests.exceptions.ConnectTimeout:
    msgbox.showerror("Erorr while connecting to server", """Error occured while trying to connect to
our servers.\n(DEBUG: the program encountered requests.exception.ConnectTimeout error!)""")
    changelogText = "ERROR: Cannot access the server for the required files and newest updates! Try again later!"
    version = 1.0
    fileList = ["NONE"]
def main(username, notification, *args):
    LAST_UPDATE = open("ProgramFiles/update_config/LAST_UPDATE.txt", "w+")
    UPDATE_CHGLOG = LAST_UPDATE.read()
    CURRENT_VERSION = FTRConfigSettings("ProgramFiles/update_config/VERSION.txt", "0.1")[0]
    THEME_WINDOW_BG, THEME_FOREGROUND = args[1]["THEME"]
    INSTANCES[args[-2]] = tkinter.Tk()
    INSTANCES[args[-2]].title("Update manager")
    INSTANCES[args[-2]].configure(background=THEME_WINDOW_BG)
    changeeLogScrollbar = ttk.Scrollbar(INSTANCES[args[-2]])
    changeeLogScrollbar.grid(row=0, column=1, sticky="nsw")
    changelogs = tkinter.Text(INSTANCES[args[-2]], background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, yscrollcommand=changeeLogScrollbar.set)
    changelogs.grid(row=0, column=0)
    changelogs.insert(1.0, changelogText)
    changelogs.configure(state="disabled")
    changeeLogScrollbar.configure(command=changelogs.yview, orient=tkinter.VERTICAL)
    def updateToNew():
        SOURCE_FOLDER = os.getcwd()
        DESTINATION_FOLDER = f"{CURRENT_VERSION}"
        os.mkdir(DESTINATION_FOLDER)
        # from this point, till '=====', it's code copied from pynative.com. so don't blame me for the code!
        for file_name in os.listdir(SOURCE_FOLDER):
            # construct full file path
            source = os.path.join(SOURCE_FOLDER, file_name)
            destination = os.path.join(DESTINATION_FOLDER, file_name)
            # copy only files
            if os.path.isfile(source):
                shutil.copy(source, destination)
                os.remove(source) # =====
        if fileList[-1] == "":
            del fileList[-1]
        for file in fileList:
            if file != "NONE":
                exec(f"{file}DWN = requests.get('https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/{file}').content.decode(encoding='utf-8')")
                with open(file, "w") as writeUpdatedProgramHANDLE:
                    exec(f"writeUpdatedProgramHANDLE.write({file}DWN)")
            else:
                msgbox.showerror("Cannot access the file list!", "Due to errors, we are not able to get the file list!")
        # My code again
        # updateZip = requests.get("https://github.com/Viswas-Programs/ParodyWindows11/raw/update/updatedProgram.zip")
        # ExtractFiles = zipfile.ZipFile(BytesIO(updateZip.content))
        # ExtractFiles.extractall(os.getcwd())
        LAST_UPDATE.write(f"Program update on {time.strftime('%H:%M:%S') in {datetime.datetime.date()}}")
    def checkForUpdates():
        mainVersion = version.split(".")[0]
        subversion = version.split(".")[1]
        if version.split(".")[2]: subversion += version.split(".")[2]
        totalVersion = float(f"{mainVersion}.{subversion}")
        if float(totalVersion) > float(CURRENT_VERSION):
            notification.showNotification("Update available!", f"Windows 11 v{version} is ready to be installed!   {CURRENT_VERSION} => {version}", time.strftime("%H:%M:%S %p"), checkForUpdates)
            msgbox.showinfo("Update available", f"Windows 11 v{version} is ready to be installed!"
                            f"\n({CURRENT_VERSION} -> {version})")
            updateButton = tkinter.Button(INSTANCES[args[-2]], text="Update to latest version!", command=updateToNew,
                                            background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            updateButton.grid(row=2, column=1)
        else:
            msgbox.showinfo("All caught up!", "You're all set, no updates (yet)")
    updateHistory = tkinter.Label(INSTANCES[args[-2]], background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=UPDATE_CHGLOG)
    updateHistory.grid(row=0, column=1)
    tkinter.Label(INSTANCES[args[-2]], text=f"Check for updates down below! your current version = {CURRENT_VERSION}",
            background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=1, column=0)
    checkForUpdatesBtn = tkinter.Button(INSTANCES[args[-2]], text="Check For Updates!", command=checkForUpdates,
                                        background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    checkForUpdatesBtn.grid(row=1, column=1)
    if UPDATE_CHGLOG == "": updateStatus = "No updates yet"
    else:
        updateStatus = str(UPDATE_CHGLOG).split("\n")[-1]
    tkinter.Label(INSTANCES[args[-2]], text=f"Last update = {updateStatus}",
            background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=2, column=0)
    def destroy():
        callHost.acknowledgeEndTask(args[-2], args[-1])
        INSTANCES[args[-2]].destroy()
        return True
    INSTANCES[args[-2]].protocol("WM_DELETE_WINDOW", destroy)
    INSTANCES[args[-2]].mainloop()
    LAST_UPDATE.close()
    INSTANCES[args[-2]].destroy()
    return args[-1]
def focusIn(PID): INSTANCES[PID].state(newstate='normal'); return True
def focusOut(PID): INSTANCES[PID].state(newstate='iconic'); return True
def endTask(PID):
    INSTANCES[PID].destroy()
    return True
def returnInformation(PID):
    return {
        "title": INSTANCES[PID].title(),
        "state": INSTANCES[PID].state()
        # Would add more stuff here in the future, such as memory usage and shi. 
    }
if __name__ == "__main__":
    main(None)