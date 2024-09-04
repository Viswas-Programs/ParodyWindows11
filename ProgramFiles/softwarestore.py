import requests
import tkinter
import tkinter.messagebox as messagebox
import os
import json
import tkinter.ttk as ttk
import shelve

from ProgramFiles import callHost

global usrname
global USER_CONFIG
USER_CONFIG: shelve
INSTANCES = {}
THEME_WINDOW_BG, THEME_FOREGROUND = ["", ""]
def showDescription(e=None):
    def uninstallProgram(e=None):
        try:
            AppToRemove = list(USER_CONFIG["APPS"][1]).index(item)
            del USER_CONFIG["APPS"][0][AppToRemove]
            del USER_CONFIG["APPS"][1][AppToRemove]
            uninstaller = requests.get(appsList[item][2]).content.decode(encoding='utf-8')
            exec(uninstaller)
        except Exception as PRB:
            messagebox.showerror("Error", f"Error occured while uninstalling '{item}': {PRB}")
    def installProgram(e=None):
        try:
            installProgram = requests.get(appsList[item][1], timeout=10)
            exec(installProgram.content.decode(encoding='utf-8'))
        except Exception as PRB:
            messagebox.showerror("ERROR! While installing app....", f"Can't install app '{item}'! Retry Again.\n DEBUG:<< {PRB} >> ")
    global externalAppsList
    wn = tkinter.Toplevel(background=THEME_WINDOW_BG)
    item = str(externalAppsList.item(externalAppsList.focus(), 'values')[0])
    wn.title(appsList[item][0])
    tkinter.Label(wn, text=appsList[item][0], background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND).pack()
    if item not in USER_CONFIG["APPS"][1]:
        tkinter.Button(wn, text="Install", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=installProgram).pack()
    else:
        tkinter.Button(wn, text="Uninstall", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=uninstallProgram).pack()
    wn.mainloop()
def main(username, notification, *args):
    global THEME_FOREGROUND, THEME_WINDOW_BG, USER_CONFIG
    global usrname
    usrname = username
    global externalAppsList
    global appsList
    USER_CONFIG = args[1]
    THEME_WINDOW_BG, THEME_FOREGROUND = USER_CONFIG["THEME"]
    INSTANCES[args[-2]] = tkinter.Tk()
    try:
        appsList = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/softwareStoreApps.json", timeout=10)
        appsList = appsList.json()
    except Exception as PROB:
        messagebox.showerror("ERROR!", f"Can't load apps list from internet! using locals\nERR: {PROB}")
        try:
            print(os.getcwd())
            with open("ProgramFiles/localAppsList.json", "r") as applistLocal:
                appsList = json.load(applistLocal)
        except Exception as PRB:
            messagebox.showerror("Can't load local apps list!", f"Error: {PRB}")
        INSTANCES[args[-2]].configure(background=THEME_WINDOW_BG)
    INSTANCES[args[-2]].title("Software Store")
    externalAppsList = ttk.Treeview(INSTANCES[args[-2]], style="Treeview")
    externalAppsList.grid(row=1, column=0, sticky="w")
    externalAppsList['column'] = "Apps"
    externalAppsList.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
    externalAppsList.column("Apps", anchor=tkinter.W, width=600)
    externalAppsList.heading("Apps", text="Apps", anchor=tkinter.CENTER)
    externalAppsList.bind("<<TreeviewSelect>>", showDescription)
    externalAppsList.configure(style="Treeview")
    for i, app in enumerate(appsList):
        externalAppsList.insert(parent='', iid=i, text='', index=i, values=[app],)
    def destroy():
        callHost.acknowledgeEndTask(args[-2], args[-1])
        INSTANCES[args[-2]].destroy()
        return True
    INSTANCES[args[-2]].protocol("WM_DELETE_WINDOW", destroy)
    INSTANCES[args[-2]].mainloop()
    INSTANCES[args[-2]].destroy()
    return args[-1]
def focusIn(PID): INSTANCES[PID].state(newstate='normal'); INSTANCES[PID].focus(); return True
def focusOut(PID): INSTANCES[PID].state(newstate='iconic'); return True
def endTask(PID):
    INSTANCES[PID].destroy()
    return True
def returnInformation(PID):
    return {
        "title": INSTANCES[PID].title(),
        # Would add more stuff here in the future, such as memory usage and shi. 
    }
if __name__ == "__main__":
    main()
