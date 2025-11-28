import tkinter
from tkinter import ttk
import os
from ProgramFiles.errorHandler import messagebox
import ProgramFiles.fileRouters as fileRouters 
import ProgramFiles.callHost as callHost
from ParWFS import ParWFS
from ProgramFiles.dwm import createTopFrame
from ProgramFiles.progressBars import ProgressOutOfMaxValueBar
from ProgramFiles.entryWidget import Entry
from ProgramFiles.treeview import Treeview
try: 
    import psutil
except:
    os.system("pip install psutil")
    import psutil
KNOWN_FILETYPES = {
    "py": "Python File",
    "txt": "Text File",
    "png": "PNG Image",
    "jpeg": "JPEG Image",
    "jpg": "JPG Image",
    "conf": "ParW11 Credential File"
}
NEEDS_FILESYSTEM_ACCESS = True
THEME_ACT_CLR, THEME_FOREGROUND, THEME_WINDOW_BG = ["Black","White", "Black"]
INSTANCES = {}
def focusIn(PID): INSTANCES[PID].overrideredirect(False); INSTANCES[PID].state(newstate='normal'); INSTANCES[PID].overrideredirect(True); return True
def focusOut(PID): INSTANCES[PID].overrideredirect(False); INSTANCES[PID].state(newstate='iconic'); INSTANCES[PID].overrideredirect(True); return True
def focusMaximise(PID): INSTANCES[PID].attributes("-topmost", True)
def endTask(PID):
    INSTANCES[PID].destroy()
    return True
def returnInformation(PID):
    return {
        "title": INSTANCES[PID].title(),
        "state": INSTANCES[PID].state()
        # Would add more stuff here in the future, such as memory usage and shi. 
    }
def main(FILESYSTEM: ParWFS, *args):
    try:
        if FILESYSTEM.getConfig("SYS_CONFIG")["FS_STOP_PREMATURE"] == True:
            print("HEREEE LES GOO!")
            FILESYSTEM.loadFromPickle()
            FILESYSTEM.editConfig("SYS_CONFIG", "FS_STOP_PREMATURE", False)
        print(args[-1])
        PROCESS_RUNNING = True
        global THEME_FOREGROUND
        global THEME_WINDOW_BG
        global THEME_ACT_CLR
        THEME_ACT_CLR, THEME_FOREGROUND, THEME_WINDOW_BG = args[3]["THEME"]
        filepath = None
        def newFolder(PID, *event):
            toplevel = tkinter.Toplevel(INSTANCES[PID], background=THEME_WINDOW_BG)
            def createNewFolder(*event):
                try:
                    os.mkdir(os.path.join(filepath, newFolderEntry.get()))
                    lookUpFiles(os.path.join(filepath, newFolderEntry.get()))
                except Exception as EXCEPTION: messagebox.showerror("ERROR!", EXCEPTION, INSTANCES[PID], MainPID=PID)
            internalPID = callHost.getRangeToGenPID(callHost.DIALOGUE_BOXES)
            createTopFrame(toplevel, THEME_FOREGROUND, THEME_ACT_CLR, "filemanager", "New Folder Menu", internalPID, associatePIDProcess=PID )
            tkinter.Label(toplevel, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, text="Folder Name!").grid(row=0, column=0)
            newFolderEntry = Entry(toplevel, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            newFolderEntry.configure(insertbackground=THEME_FOREGROUND, selectbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG)
            newFolderEntry.grid(row=1, column=0)
            btn = tkinter.Button(toplevel, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=createNewFolder, text="Create Folder")
            btn.grid(row=2, column=0)
            toplevel.mainloop()
        def lookUpFiles(path):
            nonlocal filepath
            addressBar.delete(0, tkinter.END)
            filepath = path
            addressBar.insert(tkinter.END, path)
            filesInFolder = os.listdir(path)
            for i in fileView.get_children():
                fileView.delete(i)
            for file in range(len(filesInFolder)):
                fileType = "File"
                if os.path.isdir(f"{os.path.join(filepath, filesInFolder[file])}"): fileType="DIRECTORY"
                else:
                    split = str(filesInFolder[file]).split(".")
                    extension = split[-1]
                    if len(split) > 1:
                        if extension in list(KNOWN_FILETYPES.keys()): fileType = KNOWN_FILETYPES[extension]
                        else: fileType=f"{extension.upper()} File"

                fileView.configure(style="Treeview")
                fileView.insert(parent='', iid=file, text=filesInFolder[file], index='end', values=[fileType],)
        def openFileOrFolder(*event):
            nonlocal filepath
            selectedFileIndex = fileView.focus()
            #selectedFile = fileView.item(selectedFileIndex, 'values')[0]
            selectedFile = fileView.item(selectedFileIndex)
            if os.path.isdir(f"{os.path.join(filepath, selectedFile)}"):
                filepath = os.path.join(filepath, selectedFile)
                lookUpFiles(filepath)
            else:
                fileRouters.handleFiles(os.path.join(filepath, selectedFile), args[0], args[1], args[3])

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
        INSTANCES[args[-1]] = tkinter.Tk()
        INSTANCES[args[-1]].title("File Manager")
        createTopFrame(INSTANCES[args[-1]], THEME_FOREGROUND, THEME_ACT_CLR, "filemanager", "File Manager", args[-1])
        ttk.Style(INSTANCES[args[-1]]).configure("Treeview", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        mainFrame = tkinter.Frame(INSTANCES[args[-1]], background=THEME_WINDOW_BG)
        mainFrame.grid(row=1, column=0)
        addressBar = Entry(mainFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=100)
        addressBar.insert(tkinter.END, os.getcwd())
        goButton = tkinter.Button(mainFrame, text="Go!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=lambda: lookUpFiles(addressBar.get()))
        goButton.grid(row=0, column=1, sticky="nw")
        goBackButton = tkinter.Button(mainFrame, text="Go back!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                    command=lambda: goBackFolder(path=addressBar.get()))
        goBackButton.grid(row=0, column=2, sticky="nw", padx=2)
        addressBar.grid(row=0, column=0, sticky="n")
        commandBar = tkinter.Frame(mainFrame, background=THEME_WINDOW_BG)
        newFolderBtn = tkinter.Button(commandBar, text="New Folder!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=lambda: newFolder(args[-1]))
        newFolderBtn.grid(row=0, column=0)
        fileContentFrame = tkinter.Frame(mainFrame, background=THEME_WINDOW_BG)
        fileContentFrame.grid(row=2, column=0)
        _DRVSELECTFRAME = tkinter.Frame(fileContentFrame, background=THEME_WINDOW_BG)
        _DRVSELECTFRAME.grid(row=0, column=0, sticky="w")
        tkinter.Label(_DRVSELECTFRAME, text="Mounted Partitions/Drives", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, justify='center').grid(row=0, column=0, sticky="we")
        driveSelection = tkinter.Listbox(_DRVSELECTFRAME, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND )
        driveSelection.grid(row=1, column=0, sticky="news")
        PARTITIONS = psutil.disk_partitions()
        for IDX, partition in enumerate(PARTITIONS):
            driveSelection.insert(IDX, partition.mountpoint)
        driveSelection.bind("<<ListboxSelect>>", lambda e=None: lookUpFiles(driveSelection.get(driveSelection.curselection()[0])))
        #driveSelection['column'] = "Drives"
        #driveSelection.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        #driveSelection.column("Drives", anchor=tkinter.W, width=100)
        #driveSelection.heading("Drives", text="Drives", anchor=tkinter.CENTER)
        def delete(*args):
            import shutil
            selectedFileIndex = fileView.focus()
            selectedFile = os.path.join(filepath, fileView.item(selectedFileIndex))
            FILESYSTEM.deleteFiles([[selectedFile, filepath]])
            fileView.delete(selectedFileIndex)
        def popup(event=None, *args):
            """ the context menu popup"""
            problem = None
            try:
                files.tk_popup(event.x_root, event.y_root, 0)
            except Exception as PROBLEM:
                messagebox.showerror("Error in right click menu", f"Error in right click menu. \nPROB:{PROBLEM}", INSTANCES[args[-1]], MainPID=args[-1])
            finally:
                files.grab_release()
        def copyFiles(ev=None):
            selectedFileIndex = fileView.focus()
            #selectedFile = fileView.item(selectedFileIndex, 'values')[0]
            selectedFile = fileView.item(selectedFileIndex)
            absFilePath = os.path.join(filepath, selectedFile)
            FILESYSTEM.copyFiles([[absFilePath, filepath]])
        def cutFiles(ev=None):
            selectedFileIndex = fileView.focus()
            #selectedFile = fileView.item(selectedFileIndex, 'values')[0]
            selectedFile = fileView.item(selectedFileIndex)
            absFilePath = os.path.join(filepath, selectedFile)
            FILESYSTEM.cutFiles([[absFilePath, filepath]])
        def pasteFiles(ev=None):
            progressBar = ProgressOutOfMaxValueBar(FILESYSTEM.calculateProgressForPaste(filepath), INSTANCES[args[-1]], "Pasting Files!", THEME_WINDOW_BG, THEME_FOREGROUND, False, FILESYSTEM.callStop, FILESYSTEM.callResume, parentPID=args[-1] )
            func = lambda: FILESYSTEM.pasteFiles(filepath, lambda e: progressBar.incrementer(e[0]))
            progressBar.function = func
            progressBar.runFunc()
            lookUpFiles(filepath)

        commandBar.grid(row=1, column=0)
        ttk.Style().configure("Treeview", width=100)
        fileView = Treeview(fileContentFrame, style="Treeview")
        fileView.grid(row=0, column=1, sticky="w")
        #fileView['column'] = "Files"
        fileView["column"] = "File Type"
        fileView.column("#0", width=600, anchor=tkinter.CENTER)
        fileView.heading("#0", "Files")
        #fileView.column("Files", width=600)
        #fileView.heading("Files", text="Files", anchor=tkinter.CENTER)
        fileView.heading("File Type", text="File Type", anchor=tkinter.CENTER)
        fileView.bind("<Double-1>", openFileOrFolder)
        fileView.bind("<Button-3>", popup)
        fileView.configure(style="Treeview")
        files = tkinter.Menu(mainFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        files.add_command(label="Open", command=openFileOrFolder)
        files.add_command(label="Open With", command=lambda: fileRouters.openWithSettings(INSTANCES[args[-1]], str(os.path.join(filepath, fileView.item(fileView.focus(), 'values')[0])).replace("\\", "/"), args[-2], args[0], args[1] ))
        files.add_command(label="Delete", command=delete)
        files.add_command(label="Copy", command=copyFiles)
        files.add_command(label="Cut", command=cutFiles)
        files.add_command(label="Paste", command=pasteFiles)
        lookUpFiles(addressBar.get())
        if (args[2]):
            lookUpFiles(args[2])
        INSTANCES[args[-1]].mainloop()
        return args[-1]
    except Exception as exp:
        messagebox.showerror("Can't load app!", f"App can't run! please re-install the app!\nPROB:{exp}")
    finally: 
        print("FILE MANAGER CLOSE LA", args[-1])
        return args[-1]
if __name__ == "__main__":
    main()
