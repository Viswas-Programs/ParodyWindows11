import tkinter, shelve
THEME_WINDOW_BG, THEME_FOREGROUND = shelve.open("ProgramFiles/SYS_CONFIG")["THEME"]
returner_ASKYESNOCANCEL = "Job pend"
returner_SHOWERROR = "Job pend"

class messagebox:
    @staticmethod
    def showerror(header=None, msg=None, root=None, use_preset=False, type_preset=None, quitOnResponse=False):
        RETURNVAL = 0
        def returnOk(): 
            nonlocal RETURNVAL
            MsgBox.quit(); 
            if not isRootParamNone or quitOnResponse: 
                root.destroy(); 
            RETURNVAL =  1
        isRootParamNone = not not root
        if root == None:
            root = tkinter.Tk()
            root.configure(background=THEME_WINDOW_BG)
            root.state("withdrawn")
            root.title("DEBUG WINDOW")
        
        MsgBox = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        MsgBox.title(header)
        try:
            if use_preset: import ProgramFiles.errorHandles as errorHandles; msg = errorHandles.find_item(type_preset); header = "Error!"
        except Exception: msg = " "; header = " "
        errorICON = tkinter.PhotoImage(file='ProgramFiles/Icons/error.png', master=MsgBox)
        Msg = tkinter.Label(MsgBox, text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT)
        MsgBox.IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgBox, text="Ok", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnOk)
        Btn.pack(side='right', anchor='s')
        MsgBox.mainloop()
        MsgBox.destroy()
        return RETURNVAL
    @staticmethod
    def showinfo(header, msg, root, use_preset=False, type_preset=None, quitOnResponse=False):
        RETURNVAL = 0
        def returnOk(): 
            nonlocal RETURNVAL
            MsgBox.quit(); 
            if not isRootParamNone or quitOnResponse: 
                root.destroy(); 
            RETURNVAL= 1
        isRootParamNone = not not root
        if root == None:
            root = tkinter.Tk()
            root.configure(background=THEME_WINDOW_BG)
            root.state("withdrawn")
            root.title("DEBUG WINDOW")
        MsgBox = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        MsgBox.configure(background=THEME_WINDOW_BG)
        MsgBox.title(header)
        if use_preset: 
            try:
                import ProgramFiles.errorHandles as errorHandles; msg = errorHandles.find_item(type_preset)
            except ModuleNotFoundError: msg = "Cannot locate the error message to load!"; header='Error'
        errorICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/info.png', master=root)
        Msg = tkinter.Label(MsgBox, text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT)
        MsgBox.IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgBox, text="Ok", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnOk)
        Btn.pack(side='right', anchor='s')
        MsgBox.mainloop()
        MsgBox.destroy()
        return RETURNVAL
    @staticmethod
    def showwarning(header, msg, root, use_preset=False, type_preset=None, quitOnResponse=False):
        RETURNVAL = 0
        def returnOk(): 
            nonlocal RETURNVAL
            MsgBox.quit(); 
            if not isRootParamNone or quitOnResponse: 
                root.destroy(); 
            RETURNVAL = 1
        isRootParamNone = not not root
        if root == None:
            root = tkinter.Tk()
            root.configure(background=THEME_WINDOW_BG)
            root.state("withdrawn")
            root.title("DEBUG WINDOW")
        MsgBox = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        MsgBox.configure(background=THEME_WINDOW_BG)
        MsgBox.title(header)
        if use_preset: 
            try:
                import ProgramFiles.errorHandles as errorHandles; msg = errorHandles.find_item(type_preset)
            except ModuleNotFoundError: msg = ""; header=' '
        errorICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/warning.png', master=root)
        Msg = tkinter.Label(MsgBox, text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT)
        MsgBox.IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgBox, text="Ok", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnOk)
        Btn.pack(side='right', anchor='s')
        MsgBox.mainloop()
        MsgBox.destroy()
        return RETURNVAL
    @staticmethod
    def askyesorno(header, msg, root,):
        RETURNVAL = 0
        def returnOk(): 
            nonlocal RETURNVAL
            MsgBox.quit()
            RETURNVAL = 1
        def returnFalse(): 
            nonlocal RETURNVAL
            MsgBox.quit()
            RETURNVAL =  0
        if root == None:
            root = tkinter.Toplevel(background=THEME_WINDOW_BG)
            root.title("DEBUG WINDOW")
        MsgBox = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        MsgBox.configure(background=THEME_WINDOW_BG)
        MsgBox.title(header)
        errorICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/question.png', master=root)
        Msg = tkinter.Label(MsgBox, text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT)
        MsgBox.IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgBox, text="Yes", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnOk)
        Btn.pack(side='right', anchor='s')
        Btn = tkinter.Button(MsgBox, text="No", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnFalse)
        Btn.pack(side='right', anchor='s')
        MsgBox.mainloop()
        MsgBox.destroy()
        return RETURNVAL
    @staticmethod
    def askyesnocancel(header, msg, root=None, quitOnResponse=False):
        RETURNVAL = 0
        def returnFalse():
            nonlocal RETURNVAL
            MsgBox.quit()
            if not isRootParamNone or quitOnResponse: 
                root.destroy()
            RETURNVAL = 0
        def returnNothing(): 
            nonlocal RETURNVAL
            MsgBox.quit()
            if not isRootParamNone or quitOnResponse: root.destroy()
            RETURNVAL = None
        def returnOk():
            nonlocal RETURNVAL
            MsgBox.quit(); 
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
        MsgBox = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        MsgBox.configure(background=THEME_WINDOW_BG)
        MsgBox.title(header)
        errorICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/question.png', master=root)
        Msg = tkinter.Label(MsgBox, text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT)
        MsgBox.IMGREF = errorICON
        Msg.pack(side='left')
        Btn = tkinter.Button(MsgBox, text="Yes", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnOk)
        Btn.pack(side='right', anchor='s')
        NOBtn = tkinter.Button(MsgBox, text="No", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnFalse)
        NOBtn.pack(side='right', anchor='s')
        CANCELBtn = tkinter.Button(MsgBox, text="Cancel", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnNothing)
        CANCELBtn.pack(side='right', anchor='s')
        MsgBox.mainloop()
        MsgBox.destroy()
        return RETURNVAL
