import tkinter

from ProgramFiles import callHost
try:
    from tkinterweb import HtmlFrame
except ModuleNotFoundError:
    import os
    os.system("pip3 install tkinterweb")
    from tkinterweb import HtmlFrame
import shelve
from datetime import datetime
from ProgramFiles.dwm import createTopFrame
PROCESS_RUNNING = True
INSTANCES = {}
NEEDS_FILESYSTEM_ACCESS = False
searchHistory = shelve.open("ProgramFiles/history")
searches = []
searchNo = -1
SHOWN_HISTORY = False
SHOWN_ABOUT = False
SHOWN_PERSONALIZATION = False
DARK_THEME = False 
THEME_WINDOW_BG, THEME_FOREGROUND = ["Black", "White"]
def browse(PID, e=None):
    global frame
    searches.append(text.get())
    def a(title):
        searchHistory[str(datetime.now())] = title
        INSTANCES[PID].title(title)
    def addToList(url):
        global searches
        global searchNo
        global text
        searches.append(str(url))
        searchNo += 1
        frame.load_url(url)
        frame.enable_dark_theme(True, True)
        text.delete(0, tkinter.END)
        text.insert(0, url)
    frame = HtmlFrame(mainFrame)
    frame.load_website(text.get()) 
    frame.on_link_click(addToList)
    if DARK_THEME: frame.enable_dark_theme(True, True)
    frame.on_title_change(a)
    frame.grid(row=1, column=0)
def optionsWindow(PID, e=None):
    global DARK_THEME
    def showHistory():
        global SHOWN_HISTORY
        global historyFrame
        SHOWN_HISTORY = True
        if SHOWN_ABOUT: aboutFrame.destroy()
        if SHOWN_PERSONALIZATION: perFrame.destroy()
        historyFrame = tkinter.Frame(optionsWn, background=THEME_WINDOW_BG, width=90, height=120)
        historyFrame.grid(row=0, column=1)
        for i, (time, search) in enumerate(searchHistory.items()):
            exec(f"a{i} = tkinter.Label(historyFrame, text='{search}', background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)")
            exec(f"a{i}.grid(row=i, column=0)")
            exec(f"n{i} = tkinter.Label(historyFrame, text=':{time}', background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)")
            exec(f"n{i}.grid(row=i, column=1)")
    def showAbout():
        global SHOWN_ABOUT
        global aboutFrame
        SHOWN_ABOUT = True
        if SHOWN_HISTORY: historyFrame.destroy()
        if SHOWN_PERSONALIZATION: perFrame.destroy()
        aboutFrame = tkinter.Frame(optionsWn, background=THEME_WINDOW_BG)
        aboutFrame.grid(row=0, column=1)
        about = tkinter.Label(aboutFrame, text=
        "Python Web browser v2.0\nThis doesn't use modern javascript, so JS has no support, period.",
        background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        about.grid(row=0, column=0)
    def darkThemeMenu(e=None):
        global DARK_THEME
        global SHOWN_PERSONALIZATION
        global perFrame
        global DARK_THEME
        perFrame = tkinter.Frame(optionsWn, background=THEME_WINDOW_BG)
        perFrame.grid(row=0, column=1)
        def changeTheme(e=None): frame.enable_dark_theme(True, True); DARK_THEME = True
        def revChanges(e=None): frame.enable_dark_theme(False, False); DARK_THEME = False
        change = tkinter.Button(perFrame, text="Experimental dark theme! (on)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=changeTheme)
        change.grid(row=0, column=0)
        revchange = tkinter.Button(perFrame, text="Experimental dark theme! (off)", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=revChanges)
        revchange.grid(row=1, column=0)
    optionsWn = tkinter.Toplevel(INSTANCES[PID], background=THEME_WINDOW_BG)
    btnFrame = tkinter.Frame(optionsWn, background=THEME_WINDOW_BG)
    btnFrame.grid(row=0, column=0)
    historyBtn = tkinter.Button(btnFrame, text="History", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=showHistory)
    historyBtn.grid(row=0, column=0)
    aboutBtn = tkinter.Button(btnFrame, text="About", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=showAbout)
    aboutBtn.grid(row=1, column=0)
    changeBtn = tkinter.Button(btnFrame, text="Personalization", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=darkThemeMenu)
    changeBtn.grid(row=2, column=0)
    optionsWn.mainloop()

def goBack(e=None):
    global frame
    if frame:
        frame.load_website(searches[searchNo-2])
        if DARK_THEME: frame.enable_dark_theme(True, True)
        global text
        text.delete(0, tkinter.END)
        text.insert(searches[searchNo-2])
def reloadWebsite(e=None):
    if frame:
        frame.load_website(searches[searchNo-1])
        if DARK_THEME: frame.enable_dark_theme(True, True)

def main(*args):
    global mainFrame
    global frame
    global text
    global THEME_FOREGROUND, THEME_WINDOW_BG
    THEME_WINDOW_BG, THEME_FOREGROUND = args[3]["THEME"]
    INSTANCES[args[-1]] = tkinter.Tk()
    INSTANCES[args[-1]].configure(background=THEME_WINDOW_BG)
    createTopFrame(INSTANCES[args[-1]], THEME_FOREGROUND, THEME_WINDOW_BG, "webbrowser", "Web Browser", args[-1])
    INSTANCES[args[-1]].title("Web Browser")
    mainFrame = tkinter.Frame(INSTANCES[args[-1]], background=THEME_WINDOW_BG)
    mainFrame.grid(row=2, column=0)
    btnFrame = tkinter.Frame(mainFrame, background=THEME_WINDOW_BG)
    btnFrame.grid(row=1, column=0)
    backButton = tkinter.Button(btnFrame, text="<-", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=goBack)
    backButton.grid(row=0, column=0)
    reloadButton = tkinter.Button(btnFrame, text="Reload", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=reloadWebsite)
    reloadButton.grid(row=0, column=1)
    text = tkinter.Entry(btnFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=90)
    text.grid(row=0, column=2)
    text.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
    btn = tkinter.Button(btnFrame, text="Go!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: browse(args[-1]))
    btn.grid(row=0, column=3)
    optionsICON = tkinter.PhotoImage(file=f'ProgramFiles/Icons/settings.png', master=INSTANCES[args[-1]]).subsample(2, 2)
    optionsBTN = tkinter.Button(btnFrame, image=optionsICON, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: optionsWindow(args[-1]))
    optionsBTN.IMGREF = optionsICON
    optionsBTN.grid(row=0, column=4)
    INSTANCES[args[-1]].mainloop()
    searchHistory.close()
    INSTANCES[args[-1]].destroy()
    return args[-1]
def focusIn(PID): INSTANCES[PID].state(newstate='normal'); return True
def focusOut(PID): INSTANCES[PID].state(newstate='iconic'); return True
def returnInformation(PID):
    return {
        "title": INSTANCES[PID].title(),
        "state": INSTANCES[PID].state()
        # Would add more stuff here in the future, such as memory usage and shi. 
    }
