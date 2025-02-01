from ProgramFiles import callHost
from ProgramFiles.dwm import createTopFrame
import tkinter
INSTANCES = {}
def focusIn(PID): INSTANCES[PID].overrideredirect(False); INSTANCES[PID].state(newstate='normal'); INSTANCES[PID].overrideredirect(True); return True
def focusOut(PID): INSTANCES[PID].overrideredirect(False); INSTANCES[PID].state(newstate='iconic'); INSTANCES[PID].overrideredirect(True); return True
def focusMaximise(PID): INSTANCES[PID].attributes("-topmost", True)


def main(*args):
    INSTANCES[args[-1]] = tkinter.Tk()
    THEME_WINDOW_BG, THEME_FOREGROUND = args[2]["THEME"]
    INSTANCES[args[-1]].configure(background=THEME_WINDOW_BG)
    INSTANCES[args[-1]].overrideredirect(True)
    createTopFrame(INSTANCES[args[-1]], THEME_FOREGROUND, THEME_WINDOW_BG, "shelveeditor", "Shelve Editor", args[-1])
    INSTANCES[args[-1]].mainloop()