import tkinter
import threading
import ParWFS
try:
    import ProgramFiles.callHost as callHost
    from ProgramFiles.entryWidget import Entry
    from ProgramFiles.buttons import SIDEBAR_BUTTON_INSTANCES
except Exception as EXP:
    from tkinter import Entry
    try: import callHost
    except: print("No callhost for you", EXP)

MANAGED_DWM_INSTANCES = {}

def _changeThemeForAllApps(newBg, newFg, widget: tkinter.BaseWidget):
    try:
        for wdg in widget.winfo_children():
            _changeThemeForAllApps(newBg, newFg, wdg)
    except: pass
            
    try:
        widget.configure(background=newBg)
        widget.configure(foreground=newFg)
    except Exception: pass
def changeThemeForAllApps(newBg, newFg, newWnTitleClr):
    try:
        for DWMFrame in MANAGED_DWM_INSTANCES.values():
            if DWMFrame[0] == None: continue
            _changeThemeForAllApps(newBg, newFg, DWMFrame[4].PARAMETER_CALL_INFORMATION["root"])
            DWMFrame[4].configure(background=newWnTitleClr)
            _changeThemeForAllApps(newWnTitleClr, newFg, DWMFrame[4])
            DWMFrame[4].ALL_BUTTONS["close"].configure(background="red", foreground="white")
    except: pass
    finally:
        for sidebarInstances in SIDEBAR_BUTTON_INSTANCES:
            sidebarInstances.defaultColour = newBg

def title(newTitle=None, PID=0):
    if newTitle: MANAGED_DWM_INSTANCES[PID][1].configure(text=newTitle); MANAGED_DWM_INSTANCES[PID][0] = newTitle
    return MANAGED_DWM_INSTANCES[PID][0]
def close(PID):
    MANAGED_DWM_INSTANCES[PID][2].destroy()
    for instance in MANAGED_DWM_INSTANCES[PID][5]: close(instance)
    if MANAGED_DWM_INSTANCES[PID][4].SUBPROCESS == True: MANAGED_DWM_INSTANCES[MANAGED_DWM_INSTANCES[PID][4].PARAMETER_CALL_INFORMATION["ParentPID"]][5].remove(PID)
    try: callHost.acknowledgeEndTask(PID)
    except Exception as exp: print(f"Cannot call host for end task acknowledgement!\n{exp}")
    del MANAGED_DWM_INSTANCES[PID]
def focusOut(PID, dontCloseAll=False):
    MANAGED_DWM_INSTANCES[PID][2].update()
    MANAGED_DWM_INSTANCES[PID][2].state(newstate="withdrawn")
    if dontCloseAll: return
    for instances in MANAGED_DWM_INSTANCES[PID][5]: focusOut(instances, dontCloseAll)
    return
def focusIn(PID, dontOpenAll=False):
    MANAGED_DWM_INSTANCES[PID][2].update()
    MANAGED_DWM_INSTANCES[PID][2].state(newstate="normal")
    MANAGED_DWM_INSTANCES[PID][2].lift()
    MANAGED_DWM_INSTANCES[PID][2].update()
    if dontOpenAll: return
    for instances in MANAGED_DWM_INSTANCES[PID][5]: focusIn(instances, dontOpenAll)
    return
def getFocus(PID):
    return MANAGED_DWM_INSTANCES[PID][2].state()
def setFocus(PID, newState, dontSetToAll=False):
    MANAGED_DWM_INSTANCES[PID][2].lift()
    MANAGED_DWM_INSTANCES[PID][2].update()
    MANAGED_DWM_INSTANCES[PID][2].state(newstate=newState)
    MANAGED_DWM_INSTANCES[PID][2].update()
    if dontSetToAll: return
    for instances in MANAGED_DWM_INSTANCES[PID][5]: setFocus(instances, newState, dontSetToAll)
    return
def returnWindow(PID) -> tkinter.Tk:
    return MANAGED_DWM_INSTANCES[PID][2]
def focus(PID, focusFrom=None, *args):
    try:
        instance = MANAGED_DWM_INSTANCES[PID]
        instance[2].update()
        if instance[2].state() == "normal":
            if focusFrom in ("button", "taskmanager") and instance[4].SUBPROCESS: instance[4].MINIMIZE_CALL = 0
            instance[2].state(newstate="withdrawn")
            for instances in instance[5]: setFocus(instances, "withdrawn")
        else:
            instance[4].MINIMIZE_CALL = 1
            instance[2].update()
            instance[2].state(newstate="normal")
            instance[2].lift()
            for instances in instance[5]: 
                if MANAGED_DWM_INSTANCES[instances][4].MINIMIZE_CALL != 0: setFocus(instances, "normal")
    except Exception as EXP:
        print("ERROR OCCURED IN DWM FOCUS: ", EXP)

    instance[2].update()
    return (instance[2].state())
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

def receiveMessage(PID, messageContent):
    root = MANAGED_DWM_INSTANCES[PID][2]
    root.MESSAGES[PID] = messageContent
    if root.MESSAGES_CALLBACK != None:
        root.MESSAGES_CALLBACK(root.MESSAGES[PID])
    if root.MESSAGES_AUTODELETE:
        deleteMessages(PID)
    

def seeMessages(PID):
    return MANAGED_DWM_INSTANCES[PID][2].MESSAGES

def deleteMessages(PID, amount=None, oldToNew=True):
    amt = amount
    if amount == None:
        amt = 0
        for message in dict(MANAGED_DWM_INSTANCES[PID][2].MESSAGES).keys():  amt += 1
    indexAccess = range(0, amt)
    if not oldToNew: indexAccess = range(len(dict(MANAGED_DWM_INSTANCES[PID][2].MESSAGES).keys())-1, len(dict(MANAGED_DWM_INSTANCES[PID][2].MESSAGES).keys())-amt-1, -1 )
    for i in indexAccess:
        del MANAGED_DWM_INSTANCES[PID][2].MESSAGES[list(MANAGED_DWM_INSTANCES[PID][2].MESSAGES.keys())[i]]
    return MANAGED_DWM_INSTANCES[PID][2].MESSAGES

def disableCheckNewMessages(PID):
    if MANAGED_DWM_INSTANCES[PID][2].CHECK_MESSAGES_THREAD: MANAGED_DWM_INSTANCES[PID][2].CHECK_MESSAGES_RAN = False


def createTopFrame(root: tkinter.Tk, T_FG, T_BG, iconName, appName, PID, destroyFunc=None, associatePIDProcess=None, callbackForInternalMsg=None, autoDeleteOldMsg=True):
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
    def ttl(newTitle=None, *args): title(newTitle, PID)
    if not destroyFunc: destroyFunc = close
    root.TITLE_FUNC = root.title
    root.title = ttl
    root.overrideredirect(True)
    root.update()
    root.update_idletasks()
    root.MESSAGES = {}
    root.MESSAGES_CALLBACK = callbackForInternalMsg
    root.MESSAGES_AUTODELETE = autoDeleteOldMsg
        
    #root.wm_attributes('-type', 'splash')
    try:  BRCLRS = ParWFS._instances["root"].getConfig("USER_CONFIG")["THEME_WN_BORDERS"]
    except: BRCLRS = {"DWM_HG_CLR": "Black", "DWM_HGBG": "Black"}
    HG_CLR = BRCLRS["DWM_HG_CLR"]
    HGBG = BRCLRS["DWM_HGBG"]
    DWMFrame = tkinter.Frame(root, background=T_BG, borderwidth=5, highlightthickness=2, highlightcolor=HG_CLR, highlightbackground=HGBG)
    root.configure(highlightthickness=2, highlightcolor=HG_CLR, highlightbackground=HGBG)
    DWMFrame.rowconfigure(0, weight=1)
    for i in range(1, root.winfo_width()+1):
        DWMFrame.columnconfigure(i, weight=i+1)
    DWMFrame.grid(row=0, column=0, sticky="EW", columnspan=root.winfo_width())
    DWMBtnFrame = tkinter.Frame(DWMFrame, background=T_BG)
    DWMBtnFrame.grid(row=0, column=root.winfo_width())
    DWMFrame.PARAMETER_CALL_INFORMATION = {
        "root": root,
        "foreground": T_FG,
        "background": T_BG,
        "iconName": iconName,
        "appName": appName,
        "PID": PID,
        "destroyFunc": destroyFunc,
        "ParentPID": associatePIDProcess
    }
    root.Entry = Entry
    lbl = tkinter.Label(DWMFrame, text=appName, background=T_BG, foreground=T_FG, compound='left')
    lbl.img = img = callHost.getReqIcon(iconName, root, 2)
    try: 
        lbl.configure(image=img, )
        lbl.image = img
        root.update_idletasks()
        root.update()
    except Exception as EXP: print(EXP)
    lbl.grid(row=0, column=0, sticky="W")
    minimizeBtn = tkinter.Button(DWMBtnFrame, text=" _ ", background=T_BG, foreground=T_FG, border=2, borderwidth=1, command=lambda: focus(PID, "button"))
    minimizeBtn.grid(row=0, column=1, sticky="E")
    maximizeBtn = tkinter.Button(DWMBtnFrame, text=" 🗖 ", background=T_BG, foreground=T_FG, border=2, borderwidth=1, command=lambda: focusMaximise(PID))
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
    DWMFrame.MINIMIZE_CALL = 1 #0 to not focus in/out automatically if parent is focused in/out, 1 is to focus in/out when parent is focused in/out.
    DWMFrame.SUBPROCESS = False
    DWMFrame.ALL_BUTTONS = {
        "close": closeBtn,
        "minimize": minimizeBtn,
        "maximize": maximizeBtn
    }
    def _quit(): 
        root.QUIT_FUNC()
        callHost.acknowledgeEndTask(PID)
        try: MANAGED_DWM_INSTANCES[associatePIDProcess][5].remove(PID)
        except Exception: pass
    root.quit = _quit
    root.update()
    root.update_idletasks()
    # resizer()
    if associatePIDProcess != None: 
        DWMFrame.SUBPROCESS = True
        MANAGED_DWM_INSTANCES[associatePIDProcess][5].append(PID)
    MANAGED_DWM_INSTANCES[PID] = [appName, lbl, root, closeBtn, DWMFrame, []]
    return DWMFrame

def dissociateSubProcess(MainPID, SubPID):
    try: MANAGED_DWM_INSTANCES[MainPID][5].remove(SubPID)
    except Exception as EXP: print(EXP)

def dissociateFrameFromDWM(PID):
    MANAGED_DWM_INSTANCES[PID][2].overrideredirect(False)
    MANAGED_DWM_INSTANCES[PID][2].quit = MANAGED_DWM_INSTANCES[PID][2].QUIT_FUNC
    MANAGED_DWM_INSTANCES[PID][2].title = MANAGED_DWM_INSTANCES[PID][2].TITLE_FUNC
    MANAGED_DWM_INSTANCES[PID][4].destroy()

def dissociateAllDWMApps():
    for PIDs in dict(MANAGED_DWM_INSTANCES).keys(): print(PIDs); dissociateFrameFromDWM(PIDs)

def reRegisterAllDWMApps():
    for PIDs in MANAGED_DWM_INSTANCES.keys():
        INSTANCE = MANAGED_DWM_INSTANCES[PIDs]
        PARAMTER_CALL_INFO = INSTANCE[4].PARAMETER_CALL_INFORMATION
        createTopFrame(INSTANCE, 
                       PARAMTER_CALL_INFO["foreground"], 
                       PARAMTER_CALL_INFO["background"], 
                       PARAMTER_CALL_INFO["iconName"], 
                       PARAMTER_CALL_INFO["appName"], 
                       PARAMTER_CALL_INFO["PID"],
                       PARAMTER_CALL_INFO["destroyFunc"],
                       PARAMTER_CALL_INFO["ParentPID"])