import tkinter
import ProgramFiles.callHost as callHost
from ProgramFiles.entryWidget import Entry
MANAGED_DWM_INSTANCES = {}

def _changeThemeForAllApps(newBg, newFg, widget: tkinter.BaseWidget):
    for wdg in widget.winfo_children():
        _changeThemeForAllApps(newBg, newFg, wdg)
    try:
        widget.configure(background=newBg)
        widget.configure(foreground=newFg)
    except Exception: pass
def changeThemeForAllApps(newBg, newFg):
    roots = []
    for appLists in MANAGED_DWM_INSTANCES.values():
        roots.append(appLists[2])
    for root in roots:
        _changeThemeForAllApps(newBg, newFg, root)
    closeBtns = []
    for closeBtn in MANAGED_DWM_INSTANCES.values():
        closeBtns.append(closeBtn[3])
    for closeBn in closeBtns:
        closeBn.configure(background="red", foreground="white")
def title(newTitle=None, PID=0):
    if newTitle: MANAGED_DWM_INSTANCES[PID][1].configure(text=newTitle); MANAGED_DWM_INSTANCES[PID][0] = newTitle
    return MANAGED_DWM_INSTANCES[PID][0]
def close(PID):
    MANAGED_DWM_INSTANCES[PID][2].destroy()
    try: callHost.acknowledgeEndTask(PID)
    except Exception as exp: print(f"Cannot call host for end task acknowledgement!\n{exp}")
def focusOut(PID):
    MANAGED_DWM_INSTANCES[PID][2].state(newstate="withdrawn")
def focusIn(PID):
    MANAGED_DWM_INSTANCES[PID][2].update()
    MANAGED_DWM_INSTANCES[PID][2].state(newstate="normal")
    MANAGED_DWM_INSTANCES[PID][2].lift()
    MANAGED_DWM_INSTANCES[PID][2].update()
def getFocus(PID):
    return MANAGED_DWM_INSTANCES[PID][2].state()
def setFocus(PID, newState):
    MANAGED_DWM_INSTANCES[PID][2].lift()
    MANAGED_DWM_INSTANCES[PID][2].update()
    MANAGED_DWM_INSTANCES[PID][2].state(newstate=newState)
    MANAGED_DWM_INSTANCES[PID][2].update()
def returnWindow(PID) -> tkinter.Tk:
    return MANAGED_DWM_INSTANCES[PID][2]
def focus(PID, *args):
    print(MANAGED_DWM_INSTANCES[PID][2].state())
    MANAGED_DWM_INSTANCES[PID][2].update()
    if MANAGED_DWM_INSTANCES[PID][2].state() == "normal":
        MANAGED_DWM_INSTANCES[PID][2].state(newstate="withdrawn")
    else:
        MANAGED_DWM_INSTANCES[PID][2].state(newstate="normal")
        MANAGED_DWM_INSTANCES[PID][2].lift()
    MANAGED_DWM_INSTANCES[PID][2].update()
    return (MANAGED_DWM_INSTANCES[PID][2].state())
def focusMaximise(PID):
    # Force maximise ig, after you downsize you wont be able to extend the app with dynamic widgets sadly, so use this like a one-time F11 or smth man. 
    if f"{MANAGED_DWM_INSTANCES[PID][2].winfo_screenwidth()}x{MANAGED_DWM_INSTANCES[PID][2].winfo_screenheight()}" in MANAGED_DWM_INSTANCES[PID][2].geometry():
        MANAGED_DWM_INSTANCES[PID][2].geometry(MANAGED_DWM_INSTANCES[PID][2].MAX_RETURN)
    else: 
        MANAGED_DWM_INSTANCES[PID][2].MAX_RETURN = MANAGED_DWM_INSTANCES[PID][2].geometry()
        MANAGED_DWM_INSTANCES[PID][2].geometry(f"{MANAGED_DWM_INSTANCES[PID][2].winfo_screenwidth()}x{MANAGED_DWM_INSTANCES[PID][2].winfo_screenheight()}+0+0")
        MANAGED_DWM_INSTANCES[PID][2].OLD_GEO = MANAGED_DWM_INSTANCES[PID][2].geometry()
    MANAGED_DWM_INSTANCES[PID][2].update()
    MANAGED_DWM_INSTANCES[PID][2].lift()
def createTopFrame(root: tkinter.Tk, T_FG, T_BG, iconName, appName, PID, destroyFunc=None):
    root.geometry("+200+200")
    def start_move(event):
        root.x = event.x
        root.y = event.y
    def stop_move(event):
        root.x = None
        root.y = None
    def _handleDrag(event):
        deltax = event.x - root.x
        deltay = event.y - root.y
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"+{x}+{y}")
    def ttl(newTitle=None, *args):
        title(newTitle, PID)
    if not destroyFunc: destroyFunc = close
    root.title = ttl
    root.overrideredirect(True)
    root.update()
    root.update_idletasks()
    #root.wm_attributes('-type', 'splash')
    DWMFrame = tkinter.Frame(root, background=T_BG, borderwidth=5, highlightthickness=2, highlightcolor="grey")
    root.configure(highlightthickness=2, highlightcolor="grey")
    DWMFrame.rowconfigure(0, weight=1)
    for i in range(1, root.winfo_screenwidth()+1):
        DWMFrame.columnconfigure(i, weight=i)
    DWMFrame.grid(row=0, column=0, sticky="EW", columnspan=root.winfo_screenwidth())
    DWMBtnFrame = tkinter.Frame(DWMFrame, background=T_BG)
    DWMBtnFrame.grid(row=0, column=root.winfo_screenwidth())
    DWMFrame.BACKGROUND = T_BG
    DWMFrame.FOREGROUND = T_FG
    DWMFrame.PID = PID
    DWMFrame.ROOT = root
    img = callHost.getReqIcon(iconName, root)
    root.Entry = Entry
    img = img.subsample(3, 3)
    DWMFrame.img = img
    lbl = tkinter.Label(DWMFrame, text=appName, background=T_BG, foreground=T_FG, image=img, compound='left')
    lbl.grid(row=0, column=0, sticky="W")
    minimizeBtn = tkinter.Button(DWMBtnFrame, text=" _ ", background=T_BG, foreground=T_FG, border=2, borderwidth=1, command=lambda: focus(PID))
    minimizeBtn.grid(row=0, column=1, sticky="E")
    #maximizeBtn = tkinter.Button(DWMBtnFrame, text=" 🗖 ", background=T_BG, foreground=T_FG, border=2, borderwidth=1, command=lambda: focusMaximise(PID))
    #maximizeBtn.grid(row=0, column=2, sticky="E")
    closeBtn = tkinter.Button(DWMBtnFrame, text=" X ", background="Red", foreground="White", border=2, borderwidth=1, command=lambda: destroyFunc(PID))
    closeBtn.grid(row=0, column=3, sticky="E")
    DWMFrame.bind("<ButtonPress-1>", start_move)
    DWMFrame.bind("<ButtonRelease-1>", stop_move)
    DWMFrame.bind("<B1-Motion>", _handleDrag)
    lbl.bind("<ButtonPress-1>", start_move)
    lbl.bind("<ButtonRelease-1>", stop_move)
    lbl.bind("<B1-Motion>", _handleDrag)
    root.OLD_GEO = root.MAX_RETURN = root.geometry()
    root.QUIT_FUNC = root.quit
    def _quit(): root.QUIT_FUNC(); callHost.acknowledgeEndTask(PID); 
    root.quit = _quit
    # resizer()
    MANAGED_DWM_INSTANCES[PID] = [appName, lbl, root, closeBtn]
    return DWMFrame
    