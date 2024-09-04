import tkinter
from tkinter import ttk
import os
from ProgramFiles.errorHandler import messagebox
import ProgramFiles.fileRouters as fileRouters 
import ProgramFiles.callHost as callHost
from ParWFS import ParWFS
NEED_FILE_SYSTEM_ACCESS = True
THEME_WINDOW_BG, THEME_FOREGROUND = ["",""]
def main(FILESYSTEM: ParWFS, *args):
    try:
        print(args[-1])
        PROCESS_RUNNING = True
        global THEME_FOREGROUND
        global THEME_WINDOW_BG
        THEME_WINDOW_BG, THEME_FOREGROUND = args[3]["THEME"]
        filepath = None
        def newFolder(*event):
            toplevel = tkinter.Toplevel(background=THEME_WINDOW_BG)
            def createNewFolder(*event):
                try:
                    os.mkdir(os.path.join(filepath, newFolderEntry.get()))
                    lookUpFiles(os.path.join(filepath, newFolderEntry.get()))
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
            addressBar.delete(0, tkinter.END)
            filepath = path
            addressBar.insert(tkinter.END, path)
            filesInFolder = os.listdir(path)
            for i in fileView.get_children():
                fileView.delete(i)
            for file in range(len(filesInFolder)):
                fileView.configure(style="Treeview")
                fileView.insert(parent='', iid=file, text='', index='end', values=[filesInFolder[file]],)
        def openFileOrFolder(*event):
            nonlocal filepath
            selectedFileIndex = fileView.focus()
            selectedFile = fileView.item(selectedFileIndex, 'values')[0]
            if os.path.isdir(f"{os.path.join(filepath, selectedFile)}"):
                filepath = os.path.join(filepath, selectedFile)
                lookUpFiles(filepath)
            else:
                fileRouters.handleFiles(os.path.join(filepath, selectedFile), args[0], args[1], args[3], args[-1][0], args[-1][1])

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
        global fileManagerWindow
        fileManagerWindow = tkinter.Toplevel(background=THEME_WINDOW_BG)
        fileManagerWindow.title("File Manager")
        ttk.Style(fileManagerWindow).configure("Treeview", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        mainFrame = tkinter.Frame(fileManagerWindow, background=THEME_WINDOW_BG)
        mainFrame.grid(row=0, column=0)
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
        newFolderBtn = tkinter.Button(commandBar, text="New Folder!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, command=newFolder)
        newFolderBtn.grid(row=0, column=0)
        # driveSelection = ttk.Treeview(mainFrame, style="Treeview")
        # driveSelection.grid(row=0, column=0, sticky="w")
        # driveSelection['column'] = "Drives"
        # driveSelection.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        # driveSelection.column("Drives", anchor=tkinter.W, width=100)
        # driveSelection.heading("Drives", text="Drives", anchor=tkinter.CENTER)
        def delete(*args):
            import shutil
            selectedFileIndex = fileView.focus()
            selectedFile = os.path.join(filepath, fileView.item(selectedFileIndex, 'values')[0])
            FILESYSTEM.deleteFiles([[selectedFile, filepath]])
            fileView.delete(selectedFileIndex)
        def popup(event=None, *args):
            """ the context menu popup"""
            problem = None
            try:
                files.tk_popup(event.x_root, event.y_root, 0)
            except Exception as PROBLEM:
                messagebox.showerror("Error in right click menu", f"Error in right click menu. \nPROB:{PROBLEM}")
            finally:
                files.grab_release()
        def copyFiles(ev=None):
            selectedFileIndex = fileView.focus()
            selectedFile = fileView.item(selectedFileIndex, 'values')[0]
            absFilePath = os.path.join(filepath, selectedFile)
            FILESYSTEM.copyFiles([[absFilePath, filepath]])
        def cutFiles(ev=None):
            selectedFileIndex = fileView.focus()
            selectedFile = fileView.item(selectedFileIndex, 'values')[0]
            absFilePath = os.path.join(filepath, selectedFile)
            FILESYSTEM.cutFiles([[absFilePath, filepath]])
        def pasteFiles(ev=None):
            FILESYSTEM.pasteFiles(filepath)
            lookUpFiles(filepath)

        commandBar.grid(row=1, column=0)
        fileView = ttk.Treeview(mainFrame, style="Treeview")
        fileView.grid(row=2, column=0, sticky="w")
        fileView['column'] = "Files"
        fileView.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
        fileView.column("Files", anchor=tkinter.W, width=600)
        fileView.heading("Files", text="Files", anchor=tkinter.CENTER)
        fileView.bind("<Double-1>", openFileOrFolder)
        fileView.bind("<Button-3>", popup)
        fileView.configure(style="Treeview")
        files = tkinter.Menu(mainFrame, tearoff=False, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        files.add_command(label="Open", command=openFileOrFolder)
        files.add_command(label="Open With", command=lambda: fileRouters.openWithSettings(fileManagerWindow, str(os.path.join(filepath, fileView.item(fileView.focus(), 'values')[0])).replace("\\", "/"), args[-2], args[0], args[1] ))
        files.add_command(label="Delete", command=delete)
        files.add_command(label="Copy", command=copyFiles)
        files.add_command(label="Cut", command=cutFiles)
        files.add_command(label="Paste", command=pasteFiles)
        def destroy():
            callHost.acknowledgeEndTask(args[-2], args[-1])
            fileManagerWindow.destroy()
            return True
        fileManagerWindow.protocol("WM_DELETE_WINDOW", destroy)
        lookUpFiles(addressBar.get())
        fileManagerWindow.mainloop()
        return args[-1]
    except Exception as exp:
        messagebox.showerror("Can't load app!", f"App can't run! please re-install the app!\nPROB:{exp}")
    finally: 
        print("FILE MANAGER CLOSE LA", args[-1])
        return args[-1]
def focusIn(PID): fileManagerWindow.focus(); fileManagerWindow.state(newstate='normal'); return True
def focusOut(PID): fileManagerWindow.state(newstate='iconic'); return True
def endTask(PID):
    fileManagerWindow.destroy()
    return True
def returnInformation(PID):
    return {
        "title": fileManagerWindow.title(),
        # Would add more stuff here in the future, such as memory usage and shi. 
    }
if __name__ == "__main__":
    main()
