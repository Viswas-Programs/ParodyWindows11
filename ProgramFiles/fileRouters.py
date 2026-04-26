import shelve
import importlib
import os
import tkinter
from tkinter import ttk
from ProgramFiles.errorHandler import messagebox
from ProgramFiles import callHost
from ProgramFiles.fileaskhandlers import askopenfilename
from ProgramFiles.dwm import createTopFrame
W11 = importlib.__import__("Windows 11")
def openWithSettings(root, fileName: str, USER_CONFIG: shelve, userName: str, ):
    def comboBoxHandler(e=None):
        app = launcherComboBox.get()
        OpenWithMenuWindow.destroy()
        W11._AppLauncherForExternalApps(app, USER_CONFIG,  fileName, userName,)
    def askAppName():
        appToOpenWith = askopenfilename("Select a program to open with. ", (("Py Files", "*.py"), ("PyC Files", "*.pyc")))
        OpenWithMenuWindow.destroy()
        os.system(f"python {appToOpenWith} -fileOpen -{fileName}")
    THEME_ACT_CLR, THEME_FOREGROUND, THEME_WINDOW_BG = USER_CONFIG["THEME"]
    if (not root): 
        OpenWithMenuWindow = tkinter.Tk()
        OpenWithMenuWindow.configure(background=THEME_WINDOW_BG)
    else:  OpenWithMenuWindow = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
    createTopFrame(OpenWithMenuWindow, THEME_FOREGROUND, THEME_ACT_CLR, "filemanager", "Open With: ", callHost.getRangeToGenPID(callHost.DIALOGUE_BOXES))
    FileNameLabel = tkinter.Label(OpenWithMenuWindow, text=f"Open {fileName} with: ", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    FileNameLabel.grid(row=1, column=0)
    launcherComboBox = ttk.Combobox(OpenWithMenuWindow)
    launcherComboBox['values'] = USER_CONFIG["APPS"][0]
    launcherComboBox['state'] = "readonly"
    launcherComboBox.bind("<<ComboboxSelected>>", comboBoxHandler)
    launcherComboBox.grid(row=1, column=1)
    OpenWithCustomApp = tkinter.Label(OpenWithMenuWindow, text="Or open with a custom app (os.system launch from Current CWD):", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    OpenWithCustomApp.grid(row=3, column=0)
    OpenWithCustomAppBtn = tkinter.Button(OpenWithMenuWindow, text="Use Custom App", command=askAppName, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    OpenWithCustomAppBtn.grid(row=3, column=1)
    OpenWithMenuWindow.mainloop()

def handleFiles(fileName: str, userConfig: str, USER_CONFIG: shelve):
    defaultProgramFileAssociations = USER_CONFIG
    fileExtension = fileName.split(".")[-1]
    fileName = fileName.replace("\\", "/")
    if (fileExtension != "py"):
        print(fileExtension)
        try:
            app: str= defaultProgramFileAssociations["DEFAULTAPPASSOCIATION"].get(fileExtension)
            if app == None: raise Exception("Manually raised: No app detected for the given file extension: " + fileExtension)
            callHost._sendCallToPID(1, 0, {"method": "EXEC_ACTION", "LAUNCH_APP": {"APP_NAME": app, "PARAMS": fileName} })
        except Exception as I: 
            print(I)
            openWithSettings(None, fileName, USER_CONFIG, userConfig)
    else: os.system(fileName)
