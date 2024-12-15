from threading import Thread
import tkinter
import math
from ProgramFiles import dwm
from ProgramFiles import callHost
class ProgressOutOfMaxValueBar:
    def __init__(self, info: list, root: tkinter.Tk, headerText, T_BG, T_FG, autoQuitWhenCompletion = True):
        self.info = info
        self.root = root
        self.currentVal = info[0]
        self.maxVal = info[1]
        self.loopRun=1

        self.copyThread = None
        self.loopCount = 0
        if self.maxVal > 100:  self.increment = math.ceil(self.maxVal/100)
        else: self.increment = math.ceil(100/self.maxVal)
        self.progressBarWindow = tkinter.Toplevel(self.root, background=T_BG)
        self.headerText = headerText
        self.PID = callHost.getRangeToGenPID(callHost.PRG_ID)
        callHost.addToRunningAppsList(self.PID, f"ProgressBarHost - {root.title()}")
        dwm.createTopFrame(self.progressBarWindow, T_FG, T_BG, "continue", self.headerText, self.PID)
        self.progressBarWindow.title(self.headerText)
        self.ProgressBarFRAME = tkinter.Frame(self.progressBarWindow, background=T_BG)
        self.ProgressBarFRAME.grid(row=1, column=0)
        self.headerTextLBL = tkinter.Label(self.ProgressBarFRAME, background=T_BG, foreground=T_FG, text=self.headerText, pady=10, padx=10)
        self.headerTextLBL.grid(row=0, column=0)
        self.ProgressText = f"Completed {self.currentVal} out of {self.maxVal} tasks!"
        self.ProgressLBL = tkinter.Label(self.ProgressBarFRAME, background=T_BG, foreground=T_FG, text=self.ProgressText)
        self.ProgressLBL.grid(row=1, column=0)
        self.widgetFrame= tkinter.Frame(self.ProgressBarFRAME, background=T_BG)
        self.widgetFrame.grid(row=2, column=0)
        self.widgets = []
        self.function = None
        self.autoQuit = autoQuitWhenCompletion
        for i in range(0, 99):
            a = tkinter.Label(self.widgetFrame, text="|", background="Red", foreground="Red")
            a.grid(row=0, column=i)
            self.widgets.append(a)
    def runFunc(self): 
        self.copyThread = Thread(target=self.function, name="fileCopier")
        self.root.after(500, self.copyThread.start)
        self.progressBarWindow.mainloop()
    def cleanUp(self):
        for widgets in self.widgetFrame.children.values():
            widgets.destroy()
            self.progressBarWindow.destroy()
    def incrementer(self, newValue):
        self.ProgressText = f"Completed {self.currentVal+1} out of {self.maxVal} tasks!"
        self.ProgressLBL.configure(text=self.ProgressText)
        if self.maxVal <= 100:
            try: 
                widgetsToUpdate = self.widgets[(self.currentVal*self.increment):(self.currentVal*self.increment)+self.increment]
                for widget in widgetsToUpdate: widget.configure(background="Green", foreground = "Green")
            except: pass
        else:
            self.loopRun += 1
            if self.loopRun >= self.increment:
                self.loopRun = 1
                try: self.widgets[self.loopCount].configure(background="Green", foreground="Green")
                except: pass
                self.loopCount += 1
            
        self.currentVal += 1
        if self.autoQuit:
            if self.currentVal >= self.maxVal: self.cleanUp()
    def completionIndication(self, finishingText):
        self.headerTextLBL.configure(text=finishingText)

