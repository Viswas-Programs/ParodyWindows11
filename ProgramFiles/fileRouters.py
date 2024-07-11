import shelve
import importlib
import os
import tkinter
from tkinter import ttk
from ProgramFiles.errorHandler import messagebox
from ProgramFiles.fileaskhandlers import askopenfilename
W11 = importlib.__import__("Windows 11")
def openWithSettings(root: tkinter.Tk | tkinter.Toplevel, fileName: str, USER_CONFIG: shelve, userName: str, notifications):
    def comboBoxHandler(e=None):
        app = launcherComboBox.get()
        OpenWithMenuWindow.destroy()
        W11._AppLauncherForExternalApps(app, USER_CONFIG,  fileName, userName, notifications )
    def askAppName():
        appToOpenWith = askopenfilename("Select a program to open with. ", (("Py Files", "*.py"), ("PyC Files", "*.pyc")))
        OpenWithMenuWindow.destroy()
        os.system(f"python {appToOpenWith} -fileOpen -{fileName}")
    THEME_WINDOW_BG, THEME_FOREGROUND = USER_CONFIG["THEME"]
    if (not root): 
        OpenWithMenuWindow = tkinter.Tk()
        OpenWithMenuWindow.configure(background=THEME_WINDOW_BG)
    else:  OpenWithMenuWindow = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
    FileNameLabel = tkinter.Label(OpenWithMenuWindow, text=f"Open {fileName} with: ", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    FileNameLabel.grid(row=0, column=0)
    launcherComboBox = ttk.Combobox(OpenWithMenuWindow)
    launcherComboBox['values'] = USER_CONFIG["APPS"][0]
    launcherComboBox['state'] = "readonly"
    launcherComboBox.bind("<<ComboboxSelected>>", comboBoxHandler)
    launcherComboBox.grid(row=0, column=1)
    OpenWithCustomApp = tkinter.Label(OpenWithMenuWindow, text="Or open with a custom app (os.system launch from Current CWD):", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    OpenWithCustomApp.grid(row=2, column=0)
    OpenWithCustomAppBtn = tkinter.Button(OpenWithMenuWindow, text="Use Custom App", command=askAppName, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    OpenWithCustomAppBtn.grid(row=2, column=1)
    OpenWithMenuWindow.mainloop()

def handleFiles(fileName: str, userConfig: str, notifications: any, USER_CONFIG: shelve):
    defaultProgramFileAssociations = USER_CONFIG
    fileExtension = fileName.split(".")[-1]
    fileName = fileName.replace("\\", "/")
    if (fileExtension != "py"):
        print(fileExtension)
        try:
            app: str= defaultProgramFileAssociations["DEFAULTAPPASSOCIATION"].get(fileExtension)
            print(app, fileExtension, defaultProgramFileAssociations["DEFAULTAPPASSOCIATION"])
            W11._AppLauncherForExternalApps(app,USER_CONFIG,  fileName, userConfig, notifications)
        except Exception as I: 
            openWithSettings(None, fileName, USER_CONFIG, userConfig, notifications=notifications)
    else: os.system(fileName)
