import tkinter
import os
try:
    from ProgramFiles import callHost
    from ProgramFiles.fileaskhandlers import askopenfilename, askdirectory
    import ProgramFiles.errorHandler as ERH
except: 
    try: # We know this function is getting called by main from this actual file instead of host shell because this exception should NEVER occur untill this condition. 
        import callHost
        from fileaskhandlers import askdirectory, askopenfilename
        import errorHandler as ERH
    except:  pass
    

INSTANCES = {}
THEME_WINDOW_BG, THEME_FOREGROUND = ["", ""]
FOLDER_MODE = False
SET_MS = 5000
SLIDESHOW_MODE = False

def openFile(prevOrNext, PID):
    global FOLDER_MODE, CURRENT_INDEX
    global photo
    if prevOrNext: 
        FOLDER_MODE = True
        if prevOrNext == 2: 
            CURRENT_INDEX -= 1
            if (CURRENT_INDEX < 0): CURRENT_INDEX = len(IMAGES)+CURRENT_INDEX
        elif prevOrNext == 1:
            if (CURRENT_INDEX + 1 > len(IMAGES)-1): CURRENT_INDEX = 0
            else: CURRENT_INDEX += 1
        else: CURRENT_INDEX = 0
        file1 = folder + "/" + IMAGES[CURRENT_INDEX] 
    else:
        FOLDER_MODE = False
        nextBtn.configure(state="disabled"); backBtn.configure(state='disabled')
        file1 = askopenfilename(title="Open an image file", filetypes=(("PNG Images", "*.png"), ("JPG Images", "*.jpg"), ("JPEG Images", "*.jpeg")))
        INSTANCES[PID].lift()
        INSTANCES[PID].focus_force()
    photo = tkinter.PhotoImage(file=file1, master=INSTANCES[PID])
    imageViewer.configure(image=photo)
    if prevOrNext: file1 += f" [CURRENT INDEX: {str(CURRENT_INDEX+1)}]"
    imageName.configure(text=file1)
    imageViewer.image = photo
    INSTANCES[PID].image = photo
def forceOpenFile(fileName: str, PID):
    photo = tkinter.PhotoImage(file=fileName, master=INSTANCES[PID])
    imageViewer.configure(image=photo)
    imageName.configure(text=fileName)
    imageViewer.image = photo
    INSTANCES[PID].image = photo

def openFolder(PID):
    global CURRENT_INDEX, IMAGES, folder, FOLDER_MODE
    folder = askdirectory(title="Open a folder")
    print(folder)
    INSTANCES[PID].lift()
    INSTANCES[PID].focus_force()
    files = os.listdir(folder)
    IMAGES = []
    CURRENT_INDEX = 0
    for file in files:
        if file.split(".")[len(file.split("."))-1] in ["png", "jpg", "jpeg"]:
            IMAGES.append(file)
    if len(IMAGES) == 0:
        imageName.configure(text="There are no supported images in the specified folder!")
        FOLDER_MODE = False
        return -1
    openFile(3)
    nextBtn.configure(state="normal", command=lambda: openFile(1)); backBtn.configure(state="normal",  command=lambda: openFile(2))
def aboutThis(PID):
    aboutWindow = tkinter.Toplevel(INSTANCES[PID], background=THEME_WINDOW_BG)
    theContent = tkinter.Label(aboutWindow, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, 
                               text="""This is a basic photo viewer program created for an app in "ParodyWindows11"\n
That's the creator's desktop shell / desktop UI like interface in Python. \n
LAST UPDATED: 04/03/2024. Made by HeheBoi420 (discord aswell)""")
    theContent.grid(row=0, column=0)
    aboutWindow.title("About Photo Viewer")
    aboutWindow.mainloop()

def changeMsSlideShow(PID):
    def setSlideshowMode():
        global SET_MS, SLIDESHOW_MODE
        SLIDESHOW_MODE = not SLIDESHOW_MODE
        status.configure(text=f"Status: {SLIDESHOW_MODE}")
        labelText()
    def setSlideshowMS():
        global SET_MS, SLIDESHOW_MODE
        try:
            if int(ms.get()) > 0:
                SET_MS = int(ms.get())
                print(SET_MS, SLIDESHOW_MODE)
                ERH.messagebox.showinfo("Success", "Succesfully changed slideshow delay time. ", editWindow, quitOnResponse=True)
            else:
                ERH.messagebox.showerror("Error!", "The provided delay is less than or equal to 0!", editWindow)
        except Exception as EXP:
            ERH.messagebox.showerror("Error!", f"Error occured while setting delay! \n Problem: \n{EXP}")

    editWindow = tkinter.Toplevel(INSTANCES[PID], background=THEME_WINDOW_BG)
    status = tkinter.Label(editWindow, text=f"Status: {SLIDESHOW_MODE}", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    status.grid(row=0, column=0)
    lblText = ""
    def labelText():
        nonlocal lblText
        if SLIDESHOW_MODE: lblText = "Disable slide show mode"
        else: lblText = "Enable slide show mode"
        return lblText
    changeStatus = tkinter.Button(editWindow, text=labelText(), background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=setSlideshowMode)
    changeStatus.grid(row=0, column=1)
    ms = tkinter.Entry(editWindow, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    ms.grid(row=1, column=0)
    setMs = tkinter.Button(editWindow, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Set ms!", command=setSlideshowMS)
    setMs.grid(row=1, column=1)
    editWindow.mainloop()
def main(username, notification, fileopenHandle, *args):
    global THEME_WINDOW_BG, THEME_FOREGROUND
    global SLIDESHOW_MODE
    global imageViewer, imageName, nextBtn, backBtn
    THEME_WINDOW_BG, THEME_FOREGROUND = args[0]["THEME"]
    INSTANCES[args[-2]] = tkinter.Tk()
    INSTANCES[args[-2]].configure(background=THEME_WINDOW_BG)
    _MENU = tkinter.Menu(INSTANCES[args[-2]], background=THEME_WINDOW_BG, foreground=THEME_WINDOW_BG)
    INSTANCES[args[-2]].configure(menu=_MENU)
    fileMenu = tkinter.Menu(_MENU, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    fileMenu.add_command(label="Open a file", command=lambda: openFile(0, args[-2]))
    fileMenu.add_command(label="Open a folder", command=lambda: openFolder(args[-2]))
    fileMenu.add_command(label="Slide show settings", command=lambda: changeMsSlideShow(args[-2]))
    aboutMenu = tkinter.Menu(_MENU, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    aboutMenu.add_command(label="About This", command=lambda: aboutThis(args[-2]))
    _MENU.add_cascade(label="File", menu=fileMenu)
    _MENU.add_cascade(label="About", menu=aboutMenu)
    backBtn = tkinter.Button(INSTANCES[args[-2]], background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="<<Previous Image<<")
    backBtn.configure(state="disabled")
    backBtn.grid(row=0, column=0)
    imageName = tkinter.Label(INSTANCES[args[-2]], background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    imageName.grid(row=0, column=1)
    nextBtn = tkinter.Button(INSTANCES[args[-2]], background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=">>Next Image>>")
    nextBtn.configure(state="disabled")
    nextBtn.grid(row=0, column=2)
    imageViewer = tkinter.Label(INSTANCES[args[-2]], background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    imageViewer.grid(row=1, column=1)
    def loopUp(): 
        INSTANCES[args[-2]].after(SET_MS, loopUp)
        if SLIDESHOW_MODE and FOLDER_MODE: openFile(1, args[-2])
    INSTANCES[args[-2]].after(SET_MS, loopUp)
    INSTANCES[args[-2]].state("zoomed")
    INSTANCES[args[-2]].title("Photo Viewer")
    if (fileopenHandle): forceOpenFile(fileopenHandle, args[-2])
    def destroy():
        callHost.acknowledgeEndTask(args[-2], args[-1])
        INSTANCES[args[-2]].destroy()
        return True
    INSTANCES[args[-2]].protocol("WM_DELETE_WINDOW", destroy)
    INSTANCES[args[-2]].mainloop()
    INSTANCES[args[-2]].destroy()
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
    main("uh", None, None, {"THEME": ["Black", "White"]}, None, None, 7991, None)