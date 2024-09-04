import tkinter
import os
import subprocess
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import filedialog

from ProgramFiles import callHost
THEME_WINDOW_BG, THEME_FOREGROUND = ["",""]
PROCESS_RUNNING = True
INSTANCES = {}
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
        externalAppsList.insert(parent='', iid=file, text='', index=file, values=[externalAppsName[file]],)
def load(file = None, e=None):
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
    process = subprocess.Popen(["python3", f"{fileToStart}"])
def show(PID, e=None):
    global externalAppsList
    global buttonText
    global showRefreshBtn
    buttonText = "Refresh"
    showRefreshBtn.configure(text=buttonText, command=refresh)
    externalAppsList = ttk.Treeview(INSTANCES[PID], style="Treeview")
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
def main(*args):
    global externalAppsName
    global buttonText
    global THEME_FOREGROUND, THEME_WINDOW_BG
    global showRefreshBtn
    THEME_WINDOW_BG, THEME_FOREGROUND = args[3]["THEME"]
    INSTANCES[args[-2]] = tkinter.Tk()
    INSTANCES[args[-2]].configure(background=THEME_WINDOW_BG)
    INSTANCES[args[-2]].title("Load External Apps")
    externalAppsName = []
    buttonText = "Look for external apps!"
    showRefreshBtn = tkinter.Button(INSTANCES[args[-2]], text=buttonText, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: show(args[-2]))
    showRefreshBtn.grid(row=0, column=0)
    loadCusttomBtn = tkinter.Button(INSTANCES[args[-2]], text="Load Custom App!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=loadCustomApp)
    loadCusttomBtn.grid(row=0, column=1)
    def destroy():
        callHost.acknowledgeEndTask(args[-2], args[-1])
        INSTANCES[args[-2]].destroy()
        return True
    INSTANCES[args[-2]].protocol("WM_DELETE_WINDOW", destroy)
    INSTANCES[args[-2]].mainloop()
    INSTANCES[args[-2]].destroy()
    PROCESS_RUNNING = False
    return args[-1]

def endTask(PID):
    INSTANCES[PID].destroy()
    return True
def focusIn(PID):
    INSTANCES[PID].focus()
    INSTANCES[PID].state(newstate='normal')
    return True
def focusOut(PID):
    INSTANCES[PID].state(newstate='iconic')
    return True
def returnInformation(PID):
    return {
        "title": INSTANCES[PID].title(),
        # Would add more stuff here in the future, such as memory usage and shi. 
    }
