import tkinter
import requests
import shutil
import os
from tkinter import ttk
from tkinter import messagebox as msgbox
import datetime
import time
import urllib3

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

def main():
    LAST_UPDATE = open("ProgramFiles/LAST_UPDATE.txt", "a+")
    CURRENT_VERSION = FTRConfigSettings("ProgramFiles/VERSION.txt", "0.1")
    THEME_WINDOW_BG, THEME_FOREGROUND = FTRConfigSettings("theme_config.txt", "Black\nWhite")
    root = tkinter.Tk()
    root.title("Update manager")
    root.configure(background=THEME_WINDOW_BG)
    changeeLogScrollbar = ttk.Scrollbar(root)
    changeeLogScrollbar.grid(row=0, column=1, sticky="nsw")
    try:
        changelogText = str(requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/CHANGELOG.txt").content.decode(encoding="utf-8"))
    except requests.exceptions.ConnectTimeout:
        msgbox.showerror("Erorr while connecting to server", "Error occured while trying to connect to"
                        "our servers. (DEBUG: the program encountered requests.exception.ConnectTimeout error!")
        changelogText = "ERROR: Cannot access the server for the required files and newest updates! Try again later!"
    changelogs = tkinter.Text(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, yscrollcommand=changeeLogScrollbar.set)
    changelogs.grid(row=0, column=0)
    changelogs.insert(1.0, changelogText)
    changelogs.configure(state="disabled")
    changeeLogScrollbar.configure(command=changelogs.yview, orient=tkinter.VERTICAL)
    try:
        NEW_VERSION = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/VERSION.txt")
        version, a = str(NEW_VERSION.content.decode(encoding='utf-8')).split("\n")
    except requests.exceptions.ConnectTimeout:
        msgbox.showerror("Erorr while connecting to server", "Error occured while trying to connect to"
                        "our servers. (DEBUG: the program encountered requests.exception.ConnectTimeout error!")
        version = 1.0
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
        try:
            fileList = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/FILE_CHANGES.txt").content.decode(encoding='utf-8').splitlines()
        except requests.exceptions.ConnectTimeout:
            msgbox.showerror("Erorr while connecting to server", "Error occured while trying to connect to"
                            "our servers. (DEBUG: the program encountered requests.exception.ConnectTimeout error!")
            fileList = ["NONE"]
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
        nonlocal version
        if version > CURRENT_VERSION:
            msgbox.showinfo("Update available", f"Windows 11 v{version} is ready to be installed!"
                            f"\n({CURRENT_VERSION} -> {version})")
            updateButton = tkinter.Button(root, text="Update to latest version!", command=updateToNew,
                                            background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            updateButton.grid(row=2, column=1)
        else:
            msgbox.showinfo("All caught up!", "You're all set, no updates (yet)")
    updateHistory = tkinter.Label(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=LAST_UPDATE.read())
    updateHistory.grid(row=0, column=1)
    tkinter.Label(root, text=f"Check for updates down below! your current version = {CURRENT_VERSION[0]}",
            background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=1, column=0)
    checkForUpdatesBtn = tkinter.Button(root, text="Check For Updates!", command=checkForUpdates,
                                        background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    checkForUpdatesBtn.grid(row=1, column=1)
    if LAST_UPDATE.read() == "": updateStatus = "No updates yet"
    else:
        updateStatus = LAST_UPDATE.readlines()[-1]
    tkinter.Label(root, text=f"Last update = {updateStatus}",
            background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).grid(row=2, column=0)
    root.mainloop()
    LAST_UPDATE.close()
if __name__ == "__main__":
    main()