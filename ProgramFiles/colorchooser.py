import tkinter
from ProgramFiles import callHost, dwm, entryWidget
THEME_BG, THEME_FG, THEME_WNCLR = callHost.getTheme()
#import entryWidget
#THEME_BG, THEME_FG = ("Black", "White")

def __updateKeyRelease(widgetList: list[entryWidget.LabelledEntryBox], hexWidget: entryWidget.LabelledEntryBox, showFrame: tkinter.Frame):
    hexWidget.entryBox.delete("0", tkinter.END)
    HEX_STRING = "#"
    for i in widgetList: 
        try:
            if int(i.get()) >255 or int(i.get()) <0: raise Exception("BALLS")
        except Exception: i.entryBox.delete("0", tkinter.END); i.entryBox.insert(tkinter.END, "0")
        if int(i.get()) > 10: HEX_STRING += str(hex(int(i.get()))).removeprefix("0x").lstrip("0")
        elif int(i.get()) > 0: HEX_STRING += "0"+ i.get().lstrip("0")
        else: HEX_STRING += "00"
    hexWidget.entryBox.insert(tkinter.END, HEX_STRING)
    showFrame.configure(background=HEX_STRING)

def __updateHexEntKey(hexWidget: entryWidget.LabelledEntryBox, showFrame: tkinter.Frame):
    rawstr = hexWidget.get()
    print(rawstr)
    if (not (len(rawstr) in [4, 7])) or (rawstr[0] != "#") or (rawstr.count("#") != 1): return None
    showFrame.configure(background=rawstr) 


def askcolor(title, HostPID):
    win = tkinter.Tk()
    returnval = None
    def __updateReturnValue():
        nonlocal returnval
        returnval = ((red.get(), green.get(), blue.get()), showFrame.cget("background"))
        win.quit() 

    PID = callHost.getRangeToGenPID(callHost.DIALOGUE_BOXES)
    
    win.configure(background=THEME_BG)
    dwm.createTopFrame(win, THEME_FG, THEME_BG, "info", "Colour Chooser", PID, associatePIDProcess=HostPID)
    mainFrame = tkinter.Frame(win, background=THEME_BG)
    mainFrame.grid(row=1,  column=0)
    textBoxesFrame = tkinter.Frame(mainFrame, background=THEME_BG)
    textBoxesFrame.grid(row=0, column=0)

    red = entryWidget.LabelledEntryBox(textBoxesFrame, "Red:", background=THEME_BG, foreground=THEME_FG)
    red.grid(row=0, column=0)
    green = entryWidget.LabelledEntryBox(textBoxesFrame, "Green:",  background=THEME_BG, foreground=THEME_FG)
    green.grid(row=1, column=0)
    blue = entryWidget.LabelledEntryBox(textBoxesFrame, "Blue:",  background=THEME_BG, foreground=THEME_FG)
    blue.grid(row=2, column=0)

    hexBox = entryWidget.LabelledEntryBox(mainFrame, "Hex Code:", background=THEME_BG, foreground=THEME_FG)
    hexBox.grid(row=1, column=0)
    hexBox.entryBox.insert(tkinter.END, "#000000")

    showFrame = tkinter.Frame(mainFrame, background="#000000", width=textBoxesFrame.winfo_width(), height=textBoxesFrame.winfo_height())
    showFrame.grid(row=0, column=1)
    
    hexBox.entryBox.bind("<KeyRelease>", lambda e=None: __updateHexEntKey(hexBox, showFrame))

    widgets = [red, green, blue]
    for i in widgets:
        i.entryBox.insert(tkinter.END, "0")
        i.entryBox.bind("<KeyRelease>", lambda i=None, e=widgets: __updateKeyRelease(e, hexBox, showFrame))


    confirmBtn = tkinter.Button(mainFrame, background=THEME_BG, foreground=THEME_FG, text="Confirm Colour", command=__updateReturnValue)
    confirmBtn.grid(row=1, column=1)

    win.mainloop()
    try: win.destroy()
    except: pass
    finally: return returnval

if __name__ == "__main__": askcolor("Sigma", 0)