import tkinter
from tkinter import ttk
import os
from ProgramFiles.errorHandler import messagebox
from ProgramFiles import callHost
from ProgramFiles import dwm
THEME_WINDOW_BG, THEME_FOREGROUND = ["Black", "white"]
RETURN_VALUE = None
PROCESS_RUNNING = False
INSTANCES = {}
def main(*args):
    PID = callHost.getRangeToGenPID(callHost.FILEASK)
    callHost.addToRunningAppsList(PID, f"FileAskDialogueHost - {args[0]}")
    global PROCESS_RUNNING
    try:
        PROCESS_RUNNING = True
        global THEME_FOREGROUND
        global THEME_WINDOW_BG
        global actualFileTypes
        filepath = None
        def newFolder(PID, *event):
            toplevel = tkinter.Toplevel(INSTANCES[PID], background=THEME_WINDOW_BG)
            def createNewFolder(*event):
                try:
                    os.mkdir(newFolderEntry.get())
                    lookUpFiles(os.path.join(os.getcwd(), newFolderEntry.get()))
                except Exception as EXCEPTION: messagebox.showerror("ERROR!", EXCEPTION)
            tkinter.Label(toplevel, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Folder Name!").grid(row=0, column=0)
            newFolderEntry = tkinter.Entry(toplevel, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            newFolderEntry.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
            newFolderEntry.grid(row=1, column=0)
            btn = tkinter.Button(toplevel, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=createNewFolder, text="Create Folder")
            btn.grid(row=2, column=0)
            toplevel.mainloop()
        def lookUpFiles(path):
            nonlocal filepath
            global actualFileTypes
            addressBar.delete(0, tkinter.END)
            filepath = path
            addressBar.insert(tkinter.END, path)
            filesInFolder = os.listdir(path)
            for i in fileView.get_children():
                fileView.delete(i)
            for file in range(len(filesInFolder)):
                if (args[0] and args[0] == "folder-mode"):
                    if os.path.isdir(os.path.join(filepath, filesInFolder[file])):
                        fileView.configure(style="Treeview")
                        fileView.insert(parent='', iid=file, text='', index='end', values=[filesInFolder[file]],)
                else:
                    fileView.configure(style="Treeview")
                    if (actualFileTypes == "*"): fileView.insert(parent='', iid=file, text='', index='end', values=[filesInFolder[file]],)
                    elif (os.path.isdir(os.path.join(filepath, filesInFolder[file]))) or  filesInFolder[file].split(".")[-1] == actualFileTypes:
                        fileView.insert(parent='', iid=file, text='', index='end', values=[filesInFolder[file]],)
        def openFileOrFolder(PID, *event):
            nonlocal filepath
            global RETURN_VALUE
            selectedFileIndex = fileView.focus()
            selectedFile = fileView.item(selectedFileIndex, 'values')[0]
            if os.path.isdir(f"{os.path.join(filepath, selectedFile)}"):
                filepath = os.path.join(filepath, selectedFile)
                lookUpFiles(filepath)
            else:
                if not args[0] == "folder-mode": 
                    RETURN_VALUE = os.path.join(filepath, selectedFile)
                    INSTANCES[PID].quit()
                    return RETURN_VALUE
                else:
                    messagebox.showerror("Cant open files", "You cannot open/run files in this dialogue box. Please select a folder!", INSTANCES[PID])
        def selectFolder(PID, *event):
            global RETURN_VALUE
            if len(fileView.focus()) == 0:
                RETURN_VALUE = filepath
                print(RETURN_VALUE)
                INSTANCES[PID].quit()
                return RETURN_VALUE
            else: 
                selectedFolderIndx = fileView.focus()
                selectedFolder = fileView.item(selectedFolderIndx, 'values')[0]
                RETURN_VALUE = filepath + "/" +  selectedFolder
                INSTANCES[PID].quit()
                return RETURN_VALUE      

        def goBackFolder(path: str):  
            if "\\" in path:
                path = path.replace("\\", "/")
            folderSplit = path.split("/")
            if folderSplit[-1] == '':
                folderSplit.pop(-1)
            folderSplit.pop(-1)
            path = str().join(f"{folder}/" for folder in folderSplit)
            addressBar.delete(0, tkinter.END)
            addressBar.insert(tkinter.END, path)
            lookUpFiles(path=path)
        def fileModeRun():
            global actualFileTypes
            def _lookUpFile(*arg):
                global actualFileTypes
                actualFileTypes = launcherComboBox.get()
                lookUpFiles(addressBar.get())
            if args[0] == "file-mode":
                types = []
                for item in args[2]:
                    extension: str = item[1]
                    extension = extension.split(".")[-1]
                    types.append(extension)
                actualFileTypes = ""
                launcherComboBox = ttk.Combobox(commandBar)
                launcherComboBox['values'] = types
                launcherComboBox['state'] = "readonly"
                launcherComboBox.bind("<<ComboboxSelected>>", _lookUpFile)
                launcherComboBox.grid(row=0, column=1)
            return True
        INSTANCES[PID] = tkinter.Tk()
        INSTANCES[PID].configure(background=THEME_WINDOW_BG)
        dwm.createTopFrame(INSTANCES[PID], THEME_FOREGROUND, THEME_WINDOW_BG, "info", args[1], PID)
        INSTANCES[PID].title(args[1])
        ttk.Style(INSTANCES[PID]).configure("Treeview", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        mainFrame = tkinter.Frame(INSTANCES[PID], background=THEME_WINDOW_BG)
        mainFrame.grid(row=1, column=0)
        addressBar = tkinter.Entry(mainFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=100)
        addressBar.insert(tkinter.END, os.getcwd())
        goButton = tkinter.Button(mainFrame, text="Go!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=lambda: lookUpFiles(addressBar.get()))
        goButton.grid(row=0, column=1, sticky="nw")
        goBackButton = tkinter.Button(mainFrame, text="Go back!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                    command=lambda: goBackFolder(path=addressBar.get()))
        goBackButton.grid(row=0, column=2, sticky="nw", padx=2)
        addressBar.grid(row=0, column=0, sticky="n")
        commandBar = tkinter.Frame(mainFrame, background=THEME_WINDOW_BG)
        newFolderBtn = tkinter.Button(commandBar, text="New Folder!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda e=None: newFolder(PID))
        newFolderBtn.grid(row=0, column=0)
        if (args[0] == "folder-mode"):
            selectFolderBtn = tkinter.Button(commandBar, text="Select Folder", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda e=None: selectFolder(PID))
            selectFolderBtn.grid(row=0, column=1)
        # driveSelection = ttk.Treeview(mainFrame, style="Treeview")
        # driveSelection.grid(row=0, column=0, sticky="w")
        # driveSelection['column'] = "Drives"
        # driveSelection.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        # driveSelection.column("Drives", anchor=tkinter.W, width=100)
        # driveSelection.heading("Drives", text="Drives", anchor=tkinter.CENTER)
        def popup(event=None, *args):
            problem = None
            try:
                files.tk_popup(event.x_root, event.y_root, 0)
            except Exception as PROBLEM:
                problem = PROBLEM
                print(problem)
            finally:
                files.grab_release()
        files = tkinter.Menu(mainFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        files.add_command(label="Select", command=lambda e=None : openFileOrFolder(PID))
        commandBar.grid(row=1, column=0)
        fileView = ttk.Treeview(mainFrame, style="Treeview")
        fileView.grid(row=2, column=0, sticky="w")
        fileView['column'] = "Files"
        fileView.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        fileView.column("Files", anchor=tkinter.W, width=600)
        fileView.heading("Files", text="Files", anchor=tkinter.CENTER)
        fileView.bind("<Double-1>", lambda e=None : openFileOrFolder(PID))
        fileView.bind("<Button-3>", popup)
        fileView.configure(style="Treeview")
        fileModeRun()
        INSTANCES[PID].mainloop()
        INSTANCES[PID].destroy()
        PROCESS_RUNNING = False
        return RETURN_VALUE
    except Exception as exp:
        messagebox.showerror("Can't load app!", f"App can't run! please re-install the app!\nPROB:{exp}")
def focusIn(PID): INSTANCES[PID].state(newstate='normal'); 
def focusOut(PID): INSTANCES[PID].state(newstate='iconic'); 
def askdirectory(title="Open a Folder"):
    return main("folder-mode", title)
def askopenfilename(title="Open a File", filetypes: tuple = (("All files", "*.*"))):
    return main("file-mode", title, filetypes)
if __name__ == "__main__":
    main()