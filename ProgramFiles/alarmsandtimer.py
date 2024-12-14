import tkinter
from datetime import datetime
import time
from ProgramFiles import callHost
from ProgramFiles.errorHandler import messagebox
THEME_WINDOW_BG, THEME_FOREGROUND = ["", ""]
SHOWN_TIMER = False
SHOWN_ALARMS = False
INSTANCES = {}
NEEDS_FILESYSTEM_ACCESS = False
def showTimer(PID, e=None):
    def updateTime(e=None):
        timerTime = int(timerEntry.get())
        timerLabel = tkinter.Label(timerFrame, text=f"{timerTime}", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        timerLabel.grid(row=0, column=0)
        for t in range(0, timerTime):
            if t == timerTime:
                timerLabel.configure(text='0')
            timerLabel.configure(text=f"{timerTime-t}")
            timerFrame.update()
            INSTANCES[PID].update()
            time.sleep(1)
        # while timerTime > 0:
        #     timerFrame.after(1000, updateLabel)
        #     if timerTime == 0:
        #         timerLabel.configure(text="0")
        #         break
        else:
            messagebox.showinfo("Timer finished", "Timer ran out!!!", root=INSTANCES[PID])

            
    global SHOWN_ALARMS
    global timerFrame
    global alarmFrame
    if SHOWN_ALARMS: alarmFrame.destroy()
    SHOWN_ALARMS = False
    timerFrame = tkinter.Frame(INSTANCES[PID], background=THEME_WINDOW_BG)
    timerFrame.grid(row=1, column=1)
    timerEntry = tkinter.Entry(timerFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    timerEntry.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
    timerEntry.grid(row=1, column=0)
    startTimerBtn = tkinter.Button(timerFrame, text="Start Timer!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=updateTime)
    startTimerBtn.grid(row=1, column=1)
    
def showAlarms(PID, e=None):
    global SHOWN_TIMER
    global timerFrame
    global alarmFrame
    if SHOWN_TIMER: timerFrame.destroy()
    SHOWN_TIMER = False
    alarmFrame = tkinter.Frame(INSTANCES[PID], background=THEME_WINDOW_BG)
    alarmFrame.grid(row=1, column=1)
def focusIn(PID): INSTANCES[PID].overrideredirect(False); INSTANCES[PID].state(newstate='normal'); INSTANCES[PID].overrideredirect(True); return True
def focusOut(PID): INSTANCES[PID].overrideredirect(False); INSTANCES[PID].state(newstate='iconic'); INSTANCES[PID].overrideredirect(True); return True
def focusMaximise(PID): INSTANCES[PID].attributes("-topmost", True)
def endTask(PID):
    INSTANCES[PID].destroy()
    return True
def returnInformation(PID):
    return{
        "title": INSTANCES[PID].title(),
        "state": INSTANCES[PID].state()
    }
def main(*args):
    global THEME_WINDOW_BG, THEME_FOREGROUND
    global sidebar
    THEME_WINDOW_BG, THEME_FOREGROUND = args[3]["THEME"]
    INSTANCES[args[-1]] = tkinter.Tk()
    INSTANCES[args[-1]].configure(background=THEME_WINDOW_BG)
    import ProgramFiles.dwm as DWM
    DWM.createTopFrame(INSTANCES[args[-1]], THEME_FOREGROUND, THEME_WINDOW_BG, "alarmsandtimer", "Alarms and Timers", args[-1])
    INSTANCES[args[-1]].title("Alarms and Timer")
    sidebar = tkinter.Frame(INSTANCES[args[-1]], background=THEME_WINDOW_BG)
    sidebar.grid(row=1, column=0)
    timerBtn = tkinter.Button(sidebar, text="Timer", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: showTimer(args[-1]))
    timerBtn.grid(row=0, column=0)
    ##alarmBtn = tkinter.Button(sidebar, text="Alarm", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=showAlarms)
    ##alarmBtn.grid(row=1, column=0)
    INSTANCES[args[-1]].mainloop()
    INSTANCES[args[-1]].destroy()
    return args[-1]
if __name__ == "__main__":
    main()
