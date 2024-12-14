import tkinter, shelve 
from ProgramFiles import dwm
from ProgramFiles import callHost
THEME_WINDOW_BG, THEME_FOREGROUND = shelve.open("ProgramFiles/SYS_CONFIG")["THEME"]

INSTANCES = {}
class messagebox:
    @staticmethod
    def showerror(header=None, msg=None, root=None, use_preset=False, type_preset=None, quitOnResponse=False):
        RETURNVAL = 0
        def returnOk(PID): 
            nonlocal RETURNVAL
            INSTANCES[PID].quit(); 
            if not isRootParamNone or quitOnResponse: 
                root.destroy(); 
            RETURNVAL =  1
        isRootParamNone = not not root
        if root == None:
            root = tkinter.Tk()
            root.configure(background=THEME_WINDOW_BG)
            root.state("withdrawn")
            root.title("DEBUG WINDOW")
        PID = callHost.getRangeToGenPID(callHost.MSGBOX)
        INSTANCES[PID] = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        dwm.createTopFrame(INSTANCES[PID], THEME_FOREGROUND, THEME_WINDOW_BG, "error", header, PID)
        callHost.addToRunningAppsList(PID, f"MessageBox Host - {root.title()}")
        INSTANCES[PID].title(header)
        try:
            if use_preset: import ProgramFiles.errorHandles as errorHandles; msg = errorHandles.find_item(type_preset); header = "Error!"
        except Exception: msg = " "; header = " "
        errorICON = tkinter.PhotoImage(file='ProgramFiles/Icons/error.png', master=INSTANCES[PID])
        MsgFrame = tkinter.Frame(INSTANCES[PID], background=THEME_WINDOW_BG)
        Msg = tkinter.Label(MsgFrame, text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT, width=(root.winfo_screenwidth()/2))
        INSTANCES[PID].IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgFrame, text="Ok", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: returnOk(PID))
        Btn.pack(side='right', anchor='s')
        MsgFrame.grid(row=1, column=0)
        INSTANCES[PID].mainloop()
        try: INSTANCES[PID].destroy()
        except: pass
        finally: return RETURNVAL
    @staticmethod
    def showinfo(header, msg, root, use_preset=False, type_preset=None, quitOnResponse=False):
        RETURNVAL = 0
        PID = callHost.getRangeToGenPID(callHost.MSGBOX)
        def returnOk(PID): 
            nonlocal RETURNVAL
            INSTANCES[PID].quit(); 
            if not isRootParamNone or quitOnResponse: 
                root.destroy(); 
            RETURNVAL= 1
        isRootParamNone = not not root
        if root == None:
            root = tkinter.Tk()
            root.configure(background=THEME_WINDOW_BG)
            root.state("withdrawn")
            root.title("DEBUG WINDOW")
        PID = callHost.getRangeToGenPID(callHost.MSGBOX)
        INSTANCES[PID] = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        INSTANCES[PID].configure(background=THEME_WINDOW_BG)
        dwm.createTopFrame(INSTANCES[PID], THEME_FOREGROUND, THEME_WINDOW_BG, "info", header, PID)
        callHost.addToRunningAppsList(PID, f"MessageBox Host - {root.title()}")
        INSTANCES[PID].title(header)
        MsgFrame = tkinter.Frame(INSTANCES[PID], background=THEME_WINDOW_BG)
        if use_preset: 
            try:
                import ProgramFiles.errorHandles as errorHandles; msg = errorHandles.find_item(type_preset)
            except ModuleNotFoundError: msg = "Cannot locate the error message to load!"; header='Error'
        errorICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/info.png', master=root)
        Msg = tkinter.Label(MsgFrame, text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT, width=(root.winfo_screenwidth()/2))
        INSTANCES[PID].IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgFrame, text="Ok", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: returnOk(PID))
        Btn.pack(side='right', anchor='s')
        MsgFrame.grid(row=1, column=0)
        INSTANCES[PID].mainloop()
        try: INSTANCES[PID].destroy()
        except: pass
        finally: return RETURNVAL
    @staticmethod
    def showwarning(header, msg, root, use_preset=False, type_preset=None, quitOnResponse=False):
        RETURNVAL = 0
        PID = callHost.getRangeToGenPID(callHost.MSGBOX)
        def returnOk(PID): 
            nonlocal RETURNVAL
            INSTANCES[PID].quit(); 
            if not isRootParamNone or quitOnResponse: 
                root.destroy(); 
            RETURNVAL = 1
        isRootParamNone = not not root
        if root == None:
            root = tkinter.Tk()
            root.configure(background=THEME_WINDOW_BG)
            root.state("withdrawn")
            root.title("DEBUG WINDOW")
        INSTANCES[PID] = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        INSTANCES[PID].configure(background=THEME_WINDOW_BG)
        dwm.createTopFrame(INSTANCES[PID], THEME_FOREGROUND, THEME_WINDOW_BG, "warning", header, PID)
        callHost.addToRunningAppsList(PID, f"MessageBox Host - {root.title()}")
        INSTANCES[PID].title(header)
        if use_preset: 
            try:
                import ProgramFiles.errorHandles as errorHandles; msg = errorHandles.find_item(type_preset)
            except ModuleNotFoundError: msg = ""; header=' '
        errorICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/warning.png', master=root)
        MsgFrame = tkinter.Frame(INSTANCES[PID], background=THEME_WINDOW_BG)
        MsgFrame.grid(row=1, column=0)
        Msg = tkinter.Label(MsgFrame , text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT, width=(root.winfo_screenwidth()/2))
        INSTANCES[PID].IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgFrame, text="Ok", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: returnOk(PID))
        Btn.pack(side='right', anchor='s')
        INSTANCES[PID].mainloop()
        try: INSTANCES[PID].destroy()
        except: pass
        finally: return RETURNVAL
    @staticmethod
    def askyesorno(header, msg, root,):
        PID = callHost.getRangeToGenPID(callHost.MSGBOX)
        RETURNVAL = 0
        def returnOk(PID): 
            nonlocal RETURNVAL
            INSTANCES[PID].quit()
            RETURNVAL = 1
        def returnFalse(): 
            nonlocal RETURNVAL
            INSTANCES[PID].quit()
            RETURNVAL =  0
        if root == None:
            root = tkinter.Toplevel(background=THEME_WINDOW_BG)
            root.title("DEBUG WINDOW")
        INSTANCES[PID] = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        INSTANCES[PID].configure(background=THEME_WINDOW_BG)
        dwm.createTopFrame(INSTANCES[PID], THEME_FOREGROUND, THEME_WINDOW_BG, "question", header, PID)
        callHost.addToRunningAppsList(PID, f"MessageBox Host - {root.title()}")
        INSTANCES[PID].title(header)
        errorICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/question.png', master=root)
        MsgFrame = tkinter.Frame(INSTANCES[PID], background=THEME_WINDOW_BG)
        MsgFrame.grid(row=1, column=0)
        Msg = tkinter.Label(MsgFrame , text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT, width=(root.winfo_screenwidth()/2))
        INSTANCES[PID].IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgFrame, text="Yes", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: returnOk(PID))
        Btn.pack(side='right', anchor='s')
        Btn = tkinter.Button(MsgFrame, text="No", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnFalse)
        Btn.pack(side='right', anchor='s')
        INSTANCES[PID].mainloop()
        try: INSTANCES[PID].destroy()
        except: pass
        finally: return RETURNVAL
    @staticmethod
    def askyesnocancel(header, msg, root=None, quitOnResponse=False):
        PID = callHost.getRangeToGenPID(callHost.MSGBOX)
        RETURNVAL = 0
        def returnFalse():
            nonlocal RETURNVAL
            INSTANCES[PID].quit()
            if not isRootParamNone or quitOnResponse: 
                root.destroy()
            RETURNVAL = 0
        def returnNothing(): 
            nonlocal RETURNVAL
            INSTANCES[PID].quit()
            if not isRootParamNone or quitOnResponse: root.destroy()
            RETURNVAL = None
        def returnOk(PID):
            nonlocal RETURNVAL
            INSTANCES[PID].quit(); 
            if not isRootParamNone: 
                root.destroy(); 
            RETURNVAL = 1
        isRootParamNone = not not root
        if root == None:
            root = tkinter.Tk()
            root.configure(background=THEME_WINDOW_BG)
            root.state("withdrawn")
            root.title("DEBUG WINDOW")
        print("starting")
        INSTANCES[PID] = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        INSTANCES[PID].configure(background=THEME_WINDOW_BG)
        dwm.createTopFrame(INSTANCES[PID], THEME_FOREGROUND, THEME_WINDOW_BG, "question", header, PID)
        callHost.addToRunningAppsList(PID, f"MessageBox Host - {root.title()}")
        INSTANCES[PID].title(header)
        errorICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/question.png', master=root)
        MsgFrame = tkinter.Frame(INSTANCES[PID], background=THEME_WINDOW_BG)
        MsgFrame.grid(row=1, column=0)
        Msg = tkinter.Label(MsgFrame , text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT, width=(root.winfo_screenwidth()/2))
        INSTANCES[PID].IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgFrame, text="Yes", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: returnOk(PID))
        Btn.pack(side='right', anchor='s')
        NOBtn = tkinter.Button(MsgFrame, text="No", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnFalse)
        NOBtn.pack(side='right', anchor='s')
        CANCELBtn = tkinter.Button(MsgFrame, text="Cancel", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnNothing)
        CANCELBtn.pack(side='right', anchor='s')
        INSTANCES[PID].mainloop()
        try: INSTANCES[PID].destroy()
        except: pass
        finally: return RETURNVAL
