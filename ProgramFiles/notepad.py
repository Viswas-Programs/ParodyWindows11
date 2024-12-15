import tkinter
try:
    from ProgramFiles.errorHandler import messagebox
    from ProgramFiles import callHost
except: 
    from errorHandler import messagebox
    import callHost
PROCESS_RUNNING = False
INSTANCES = {}
NEEDS_FILESYSTEM_ACCESS = False
def main(username, notifications, filename, *args):
    global PROCESS_RUNNING
    try:
        print(args[-1])
        user_config = args[0]["THEME"]
        import ProgramFiles.Notepad_v3.notepadGUI as notepad
        PROCESS_RUNNING = True
        INSTANCES[args[-1]] = tkinter.Tk()
        INSTANCES[args[-1]].title("Notepad GUI v3.0 STABLE")
        text = tkinter.Text(INSTANCES[args[-1]], height=20, width=100,
                            font=("Arial Rounded MT Bold",
                                18), )
        text.grid(row=0, column=0, pady=10)
        saveTo = tkinter.Text(INSTANCES[args[-1]], height=2, width=50,
                            font=("Arial Rounded MT Bold",
                                    12))
        saveTo.grid(row=1, column=0)
        notepad.NotepadRun(text_box=text, gui=INSTANCES[args[-1]], saveTo=saveTo, file_to_open=filename, THEME_BACKGROUND=user_config[0], THEME_FOREGROUND=user_config[1], PID=args[-1])
        print("notepadrun quit ig")
        PROCESS_RUNNING = False
    except Exception as exp:
        messagebox.showerror("Can't load app!", f"App not found! please re-install the app!\nPROB:{exp}", root=None)
    print("PROCESS ENDED FOR NOTEPAD")
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
        "state": INSTANCES[PID].state()
        # Would add more stuff here in the future, such as memory usage and shi. 
    }
if __name__ == "__main__":
    main("defaultuser0", None, None, dict({"THEME": ["Black", "White"]}), callHost.getRangeToGenPID(callHost.PRID) )