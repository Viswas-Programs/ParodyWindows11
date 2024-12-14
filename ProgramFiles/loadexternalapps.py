import tkinter
import os
import subprocess
import tkinter.ttk as ttk
from pathlib import Path
from ProgramFiles import fileaskhandlers
from ProgramFiles.dwm import createTopFrame
from ProgramFiles import callHost
THEME_WINDOW_BG, THEME_FOREGROUND = ["",""]
PROCESS_RUNNING = True
INSTANCES = {}
NEEDS_FILESYSTEM_ACCESS = False
def endTask(PID):
    INSTANCES[PID].destroy()
    return True
def focusIn(PID): INSTANCES[PID].overrideredirect(False); INSTANCES[PID].state(newstate='normal'); INSTANCES[PID].overrideredirect(True); return True
def focusOut(PID): INSTANCES[PID].overrideredirect(False); INSTANCES[PID].state(newstate='iconic'); INSTANCES[PID].overrideredirect(True); return True
def focusMaximise(PID): INSTANCES[PID].attributes("-topmost", True)
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
    fileToOpen = fileaskhandlers.askopenfilename(title="Select app to run!", filetypes=(("Windows 11 Apps", "*.py"), ("All Files", "*.*")))
    load(file=fileToOpen)
def main(*args):
    global externalAppsName
    global buttonText
    global THEME_FOREGROUND, THEME_WINDOW_BG
    global showRefreshBtn
    THEME_WINDOW_BG, THEME_FOREGROUND = args[3]["THEME"]
    INSTANCES[args[-1]] = tkinter.Tk()
    INSTANCES[args[-1]].configure(background=THEME_WINDOW_BG)
    createTopFrame(INSTANCES[args[-1]], THEME_FOREGROUND, THEME_WINDOW_BG, "loadexternalapps", "Load External Apps", args[-1])
    INSTANCES[args[-1]].title("Load External Apps", args[-1])
    externalAppsName = []
    buttonText = "Look for external apps!"
    showRefreshBtn = tkinter.Button(INSTANCES[args[-1]], text=buttonText, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: show(args[-1]))
    showRefreshBtn.grid(row=1, column=0)
    loadCusttomBtn = tkinter.Button(INSTANCES[args[-1]], text="Load Custom App!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=loadCustomApp)
    loadCusttomBtn.grid(row=1, column=1)
    INSTANCES[args[-1]].mainloop()
    INSTANCES[args[-1]].destroy()
    PROCESS_RUNNING = False
    return args[-1]

def returnInformation(PID):
    return {
        "title": INSTANCES[PID].title(),
        "state": INSTANCES[PID].state()
        # Would add more stuff here in the future, such as memory usage and shi. 
    }
