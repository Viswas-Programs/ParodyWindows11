import tkinter
import os
THEME_WINDOW_BG, THEME_FOREGROUND = open("theme_config.txt").read().split("\n")
class messagebox:
    def showerror(header=None, msg=None, root=None, use_preset=False, type_preset=None):
        def returnOk(): MsgBox.destroy(); return 1
        if root == None:
            root = tkinter.Toplevel(background=THEME_WINDOW_BG)
            root.title("DEBUG WINDOW")
        
        MsgBox = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        MsgBox.title(header)
        try:
            if use_preset: import ProgramFiles.errorHandles as errorHandles; msg = errorHandles.find_item(type_preset); header = "Error!"
        except Exception: msg = " "; header = " "
        exec(f"errorICON = tkinter.PhotoImage(file='ProgramFiles/Icons/error.png')")
        exec(f"Msg = tkinter.Label(MsgBox, text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT)")
        exec(f"MsgBox.IMGREF = errorICON")
        exec(f"Msg.pack(side='left')")
        exec(f'Btn = tkinter.Button(MsgBox, text="Ok", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnOk)')
        exec(f"Btn.pack(side='right', anchor='s')")
        MsgBox.mainloop()
    def showinfo(header, msg, root, use_preset=False, type_preset=None):
        def returnOk(): MsgBox.destroy(); return 1
        if root == None:
            root = tkinter.Toplevel(background=THEME_WINDOW_BG)
            root.title("DEBUG WINDOW")
        MsgBox = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
        MsgBox.configure(background=THEME_WINDOW_BG)
        MsgBox.title(header)
        if use_preset: 
            try:
                import ProgramFiles.errorHandles as errorHandles; msg = errorHandles.find_item(type_preset)
            except ModuleNotFoundError: msg = ""; header=' '
        exec(f"errorICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/info.png')")
        exec(f"Msg = tkinter.Label(MsgBox, text=str(msg), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, image=errorICON, compound=tkinter.LEFT)")
        exec(f"Msg.IMGREF = errorIcon")
        exec(f"Msg.pack(side='left')")
        exec(f'Btn = tkinter.Button(MsgBox, text="Ok", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=returnOk)')
        exec(f"Btn.pack(side='right', anchor='s')")
        MsgBox.mainloop()