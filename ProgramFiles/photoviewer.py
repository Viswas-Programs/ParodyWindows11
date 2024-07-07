import tkinter
import os
from ProgramFiles.fileaskhandlers import askopenfilename, askdirectory
import ProgramFiles.errorHandler as ERH
THEME_WINDOW_BG, THEME_FOREGROUND = open("theme_config.txt").read().split("\n")
FOLDER_MODE = False
SET_MS = 5000
SLIDESHOW_MODE = False

def openFile(prevOrNext):
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
        root.lift()
        root.focus_force()
    photo = tkinter.PhotoImage(file=file1, master=root)
    imageViewer.configure(image=photo)
    if prevOrNext: file1 += f" [CURRENT INDEX: {str(CURRENT_INDEX+1)}]"
    imageName.configure(text=file1)
    imageViewer.image = photo
    root.image = photo
def forceOpenFile(fileName: str):
    photo = tkinter.PhotoImage(file=fileName, master=root)
    imageViewer.configure(image=photo)
    imageName.configure(text=fileName)
    imageViewer.image = photo
    root.image = photo

def openFolder():
    global CURRENT_INDEX, IMAGES, folder, FOLDER_MODE
    folder = askdirectory(title="Open a folder")
    print(folder)
    root.lift()
    root.focus_force()
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
def aboutThis():
    aboutWindow = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
    theContent = tkinter.Label(aboutWindow, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, 
                               text="""This is a basic photo viewer program created for an app in "ParodyWindows11"\n
That's the creator's desktop shell / desktop UI like interface in Python. \n
LAST UPDATED: 04/03/2024. Made by HeheBoi420 (discord aswell)""")
    theContent.grid(row=0, column=0)
    aboutWindow.title("About Photo Viewer")
    aboutWindow.mainloop()

def changeMsSlideShow():
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

    editWindow = tkinter.Toplevel(root, background=THEME_WINDOW_BG)
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
    global SLIDESHOW_MODE
    global imageViewer, root, imageName, nextBtn, backBtn
    root = tkinter.Tk()
    root.configure(background=THEME_WINDOW_BG)
    _MENU = tkinter.Menu(root, background=THEME_WINDOW_BG, foreground=THEME_WINDOW_BG)
    root.configure(menu=_MENU)
    fileMenu = tkinter.Menu(_MENU, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    fileMenu.add_command(label="Open a file", command=lambda: openFile(0))
    fileMenu.add_command(label="Open a folder", command=openFolder)
    fileMenu.add_command(label="Slide show settings", command=changeMsSlideShow)
    aboutMenu = tkinter.Menu(_MENU, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    aboutMenu.add_command(label="About This", command=aboutThis)
    _MENU.add_cascade(label="File", menu=fileMenu)
    _MENU.add_cascade(label="About", menu=aboutMenu)
    backBtn = tkinter.Button(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="<<Previous Image<<")
    backBtn.configure(state="disabled")
    backBtn.grid(row=0, column=0)
    imageName = tkinter.Label(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    imageName.grid(row=0, column=1)
    nextBtn = tkinter.Button(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text=">>Next Image>>")
    nextBtn.configure(state="disabled")
    nextBtn.grid(row=0, column=2)
    imageViewer = tkinter.Label(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    imageViewer.grid(row=1, column=1)
    def loopUp(): 
        root.after(SET_MS, loopUp)
        if SLIDESHOW_MODE and FOLDER_MODE: openFile(1)
    root.after(SET_MS, loopUp)
    root.state("zoomed")
    root.title("Photo Viewer")
    if (fileopenHandle): forceOpenFile(fileopenHandle)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()
    root.destroy()
    return True

def endTask():
    root.destroy()
    return True
if __name__ == "__main__":
    main()