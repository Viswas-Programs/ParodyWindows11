import tkinter
import os
import shelve
import sys
import subprocess
import threading
import base64
import inspect
SHELL_MODULES_LOADED = False
try:
    from ProgramFiles import callHost
    from ParWFS import ParWFS
    from  ProgramFiles.entryWidget import Entry
except:
    from tkinter import Entry
else: SHELL_MODULES_LOADED = True
INSTANCES = {}
USER_FOLDERS_LIST = ["My Documents", "My Pictures", "My Videos", "My Downloads"]
NEEDS_FILESYSTEM_ACCESS = True
class RedirectOutput:
    def __init__(self, cmdInstance):
        self.cmdInstance = cmdInstance
    def write(self, text: str):
        self.cmdInstance.showMsg(text)
        
class cmdCommands(object):
    def __init__(self, stdout: tkinter.Text, stdin: Entry, root: tkinter.Tk, FS=None, username="NotDefined", PID=99999) -> None:
        try:
            with shelve.open("ProgramFiles/SYS_CONFIG") as SYS_CONFIG: self.VERSION = SYS_CONFIG["VERSION"]
        except Exception:
            try: 
                CurFS: ParWFS = None
                if FS: CurFS = FS
                else: raise NotImplementedError("No filesystem found for checking version strings!")
                SYS_CONFIG = CurFS.getConfig("SYS_CONFIG")
                self.VERSION = SYS_CONFIG["VERSION"]
            except Exception: self.VERSION = "2.3.9"; self.showMsg("\nUNABLE TO LOAD VERSION STRING! USING HARDCODED VALUES\n")
        self.ROOT = root
        self.FILE_SYSTEM = FS
        self.ADMINISTRATOR = False
        self.UP_ARROW_COUNT = 0
        self.ACCEPT_COMMANDS = True
        self.stdout = stdout
        self.stdin = stdin
        self.LINE_COUNT = 0.0
        self.username = username
        self.PID = PID
        self.INTERNAL_COMMANDS = ["downArrowBind", "upArrowBind", "getParams", "launchCmd", "__init__", "clearStdIn"]
        self.COMMAND_LIST = [attr for attr in dir(self) if (inspect.ismethod(getattr(self,attr)) and attr not in self.INTERNAL_COMMANDS)]
        self.INPUTTED_COMMANDS_LIST = []
        self.CWD = os.getcwd()
        self.COMMAND_NOT_FOUND = "\nThe following command doesn't exist!"
        self.showMsg(f"Welcome to ParodyWindows11 Command Interpreter (OS Version {self.VERSION})\nCurrent Working Directory: {os.getcwd()}\n>")
        if not SHELL_MODULES_LOADED: self.showMsg("\nModules which are used to interact with the parent shell could NOT be imported! Some commands may NOT work correctly!\n>")
        try: self.ROOT.bind("<Up>", self.upArrowBind); self.ROOT.bind("<Down>", self.downArrowBind)
        except Exception as exp: print(exp)
        return None
    def help(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.showMsg("\nHere's a list of all available commands:")
        for command in self.COMMAND_LIST: self.showMsg(f"\n->{command}")
        self.clearStdIn()
    def cmd(self, directInvoke=False):
        try: self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        except: pass
        if directInvoke or self.stdin.get().split(' ')[1].lstrip("-") == "restart":
            if self.ROOT: self.ROOT.destroy()
            self.ROOT = tkinter.Tk()
            self.ROOT.configure(background=THEME_WINDOW_BG)
            if SHELL_MODULES_LOADED:
                try: from ProgramFiles import dwm
                except: 
                    try: import dwm
                    except: pass
                finally: 
                    try: dwm.createTopFrame(self.ROOT, THEME_FOREGROUND, THEME_WINDOW_BG, "commandprompt", "Command Prompt", self.PID)
                    except: pass
            self.ROOT.title("Command Interpreter")
            self.stdout = tkinter.Text(self.ROOT, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=120)
            self.stdout.grid(row=1, column=0)
            self.stdout.insert(tkinter.END, f"Welcome to ParodyWindows 11 Command Interpreter (OS Version {self.VERSION})\nCurrent Working Directory: {os.getcwd()}")
            self.stdin = Entry(self.ROOT, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
            self.stdin.configure(insertbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG, selectbackground=THEME_FOREGROUND, width=110)
            self.stdin.grid(row=2, column=0)
            self.stdin.focus()
            self.stdin.bind("<Return>", self.launchCmd)
            if not SHELL_MODULES_LOADED: self.showMsg("\nModules which are used to interact with the parent shell could NOT be imported! Some commands may NOT work correctly!\n>")
            try: self.ROOT.bind("<Up>", self.upArrowBind); self.ROOT.bind("<Down>", self.downArrowBind)
            except Exception as exp: print(exp)
            self.ROOT.mainloop()
        else:
            self.clear()
            self.clearStdIn()
            self.showMsg(f"\nWelcome to ParodyWindows11 Command Interpreter (OS Version {self.VERSION})\nCurrent Working Directory: {os.getcwd()}")
    def whoami(self): self.INPUTTED_COMMANDS_LIST.append(self.stdin.get()); self.clearStdIn(); self.showMsg(f"\nCurrent running user: {self.username}")
    def user(self, directInvoke=False):
            self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
            from pathlib import Path
            import base64
            if directInvoke: parameter = directInvoke
            else:parameter = self.getParams(1, " ").lstrip('-')
            if parameter == "create":
                if not self.ADMINISTRATOR: self.showMsg("\nPlease enable administrator before editing or creating a new user!"); return
                try: 
                    usersFolder = os.path.join(self.CWD, f"Users")
                    username = self.getParams(3, '-')
                    userNum = self.getParams(2, '-')
                    os.mkdir(os.path.join(os.path.join(self.CWD, "ProgramFiles"), username))
                    try: 
                        os.mkdir(usersFolder)
                        os.mkdir(f"{usersFolder}/{username}")
                    except: 
                        try: os.mkdir(f"{usersFolder}/{username}")
                        except: pass
                    for i in USER_FOLDERS_LIST:
                        os.mkdir(f"{usersFolder}/{username}/{i}") 
                except Exception: pass
                finally:
                    with open(os.path.join(self.CWD, f"ProgramFiles/accConfiguration{userNum}.conf"), "wb") as writeConfig:
                        writeConfig.writelines([base64.urlsafe_b64encode(username.encode("utf-8")), "\n".encode("utf-8") , base64.urlsafe_b64encode((self.getParams(4, '-')).encode("utf-8"))])
                    USER_CONFIG = shelve.open(f"ProgramFiles/{username}/USER_CONFIG")
                    USER_CONFIG["APPS"] = [["Command Prompt", "Load External Apps", "Notepad", "Web Browser", "Update Manager", "IP Chat", "File Manager", "Software Store", "File Share", "Black Jack", "Alarms and Timer", "Photo Viewer", "Control Panel", "Task Manager"], ["ProgramFiles.alarmsandtimer", "ProgramFiles.blackjack", "ProgramFiles.commandprompt", "ProgramFiles.loadexternalapps", "ProgramFiles.ipchat", "ProgramFiles.notepad", "ProgramFiles.webbrowser", "ProgramFiles.updatemanager", "ProgramFiles.fileshare", "ProgramFiles.filemanager", "ProgramFiles.softwarestore", "ProgramFiles.photoviewer", "ProgramFiles.controlPanel", "ProgramFiles.taskmanager"]]
                    USER_CONFIG["PINNED"] = ["File Manager"], ["Notepad", "File Manager"]
                    USER_CONFIG["THEME"] = ["Black", "White"]
                    USER_CONFIG["CLOCK-WIDGET"] = 0
                    USER_CONFIG["DEFAULTAPPASSOCIATION"] = {"txt": "Notepad", "jpg": "Photo Viewer", "png": "Photo Viewer"}
                    USER_CONFIG["WALLPAPER"] = None
                    USER_CONFIG["STARTUP_APPS"] = []
                    USER_CONFIG["PFP"] = os.path.join(self.CWD, "ProgramFiles/Icons/defaultpfp.png")
                    USER_CONFIG.close()
                    self.clearStdIn()
                    self.showMsg("\nUser created successfully!")
            elif parameter == "list":
                self.showMsg("\nCurrent User List: ")
                for file in Path(os.path.join(self.CWD, "ProgramFiles")).glob("accConfiguration*.conf"):
                    with open(file, "r") as showUsers:
                        self.showMsg(f"\n-> {base64.urlsafe_b64decode(showUsers.readlines()[0]).decode("utf-8")} ")
            elif parameter == "delete":
                if (not directInvoke): 
                    if (not self.ADMINISTRATOR): self.showMsg("\nPlease enable administrator before deleting an user!"); return
                if self.FILE_SYSTEM:
                    FS: ParWFS = self.FILE_SYSTEM
                    ROOT_DIR = self.CWD
                    USER_NUM_TO_DELETE = self.getParams(2, " ").lstrip('-')
                    USERNAME_TO_DELETE = ""
                    USER_CONF_FILEPATH = os.path.join(ROOT_DIR, f"ProgramFiles/accConfiguration{USER_NUM_TO_DELETE}.conf")
                    with open(USER_CONF_FILEPATH, "r") as reader: USERNAME_TO_DELETE = base64.urlsafe_b64decode(reader.readlines()[0]).decode("utf-8")
                    FS.deleteFiles([[os.path.join(ROOT_DIR, "ProgramFiles", USERNAME_TO_DELETE), ROOT_DIR ], [os.path.join(ROOT_DIR, "Users", USERNAME_TO_DELETE), ROOT_DIR], [USER_CONF_FILEPATH, os.path.join(ROOT_DIR, "ProgramFiles")]])
                    self.showMsg(f"\nSuccesfully deleted user {USERNAME_TO_DELETE}")
                    if directInvoke: 
                        self.showMsg("\nThis window will automatically close in 10 seconds!")
                        self.ROOT.after(10000, self.ROOT.destroy)
            else:
                self.showMsg(f"\nUnknown Switch: {parameter} ")
            self.clearStdIn()
    def administrator(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get()) 
        with open(os.path.join(self.CWD, f"ProgramFiles/accConfiguration{self.getParams(1, ' ').lstrip('-')}.conf"), "r") as checkUser:
            usrname, pswd = checkUser.readlines()
            usrname = base64.urlsafe_b64decode(usrname.rstrip("\n")).decode("utf-8")
            pswd = base64.urlsafe_b64decode(pswd.rstrip("\n")).decode("utf-8")
            if self.getParams(2, " ").lstrip('-').rstrip("\n") == usrname and self.getParams(3, " ").lstrip('-').rstrip("\n") == pswd:
                self.ADMINISTRATOR = True
                self.showMsg("\nSuccesfully turned on administrator mode!")
                self.ROOT.title("Administrator - Command Interpreter")
            else:
                self.showMsg("\nEither the username or the password is incorrect. So authentication failed!")
        self.clearStdIn()
    def downArrowBind(self, e=None):
        if self.UP_ARROW_COUNT - 1 < 0: return
        self.UP_ARROW_COUNT -= 1
        self.clearStdIn()
        self.stdin.insert(tkinter.END, self.INPUTTED_COMMANDS_LIST[-self.UP_ARROW_COUNT])
    def upArrowBind(self, e=None):
        self.UP_ARROW_COUNT += 1
        self.clearStdIn()
        self.stdin.insert(tkinter.END, self.INPUTTED_COMMANDS_LIST[-self.UP_ARROW_COUNT])
    def showMsg(self, msg: str):
        try:
            self.stdout.configure(state="normal")
            self.LINE_COUNT += 1.0
            self.stdout.insert(f"{self.LINE_COUNT+1}", msg)
            self.stdout.see(f"{self.LINE_COUNT+1}")
            if "\n" in msg: self.LINE_COUNT += 1.0
            self.stdout.configure(state="disabled")
        except Exception as EXP: print(EXP)
    def launchCmd(self, directInvoke=False,  e=None):
        if " " not in self.stdin.get(): self.stdin.insert(tkinter.END, "  ")
        command = f"self.{self.getParams(0, ' ')}()"
        if directInvoke == True: print("hi"); command = f"self.{self.stdin.get().split(' ')[0]}(self.getParams(1, ' ').lstrip('-'))"

        if self.getParams(0, " ") in self.COMMAND_LIST and self.ACCEPT_COMMANDS: self.showMsg(f"\n>{self.stdin.get()}"); exec(command)
    def clearStdIn(self):
        self.stdin.delete(0, tkinter.END)
    def clear(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.clearStdIn()
        self.stdout.configure(state="normal")
        try: self.stdout.delete(1.0, tkinter.END)
        except Exception as exp: self.showMsg(f"\nERROR OCCURED while clearing terminal: {exp}")
        finally: self.INPUTTED_COMMANDS_LIST.append("clear"); self.stdout.configure(state="disabled")
    def shutdown(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.clearStdIn()
        self.showMsg("\nShutting down...")
        self.ROOT.after(5000, lambda: os._exit(0))
    def restart(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.ROOT.destroy()
        if self.getParams(1, "-") == "useparams": useparams = True; params = self.getParams(2, "-")
        self.clearStdIn()
        if useparams: os.system(f"""python3 "Windows 11.py" -{params}""")
        else: os.system(""" python3 "Windows 11.py" """)
        exit()
    def sfcRepair(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        try: import requests
        except Exception: pass
        if self.ADMINISTRATOR:
            def resetConfigurations():
                try:
                    userToreset =  self.getParams(2, "-")
                    if userToreset.lower() != "defaultuser0":
                        try: 
                            with shelve.open(f"ProgramFiles/{userToreset}/USER_CONFIG") as deleteIt: deleteIt.clear()
                        except Exception as exp: self.showMsg(f"ERROR OCCURED While resetting...!Error: {exp}")
                    shelveFilesToDelete = ["ProgramFiles/history", "ProgramFiles/IPChat/_serverConfig", "ProgramFiles/IPChat/serversList"]
                    for shelveToDelete in shelveFilesToDelete:
                        try:
                            with shelve.open(shelveToDelete) as deleteIt: deleteIt.clear()
                        except Exception: pass
                except Exception as exp:
                    self.showMsg(f"\nERROR OCCURED While resetting...!Error: {exp}")
            if self.getParams(1, " ") == "-online":
                self.showMsg("Repairing system...")
                import zipfile
                from io import BytesIO
                try:
                    Windows11MainDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/Windows 11.py", timeout=10)
                    ProgramFilesMainDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/ProgramFiles.zip", timeout=40)
                    with open("Windows 11.py", "w") as writeTo:
                        try:
                            writeTo.write(Windows11MainDownload.content.decode(encoding="UTF-8"))
                        except UnicodeEncodeError as UER:
                            self.showMsg(f"\nUnicodeDecodeError occured while repairing 'Windows 11.py'\n--MSG:{UER}")
                    if os.access("ProgramFiles", os.F_OK) and os.path.isdir("ProgramFiles"):
                        import pathlib3x
                        Location = pathlib3x.Path("ProgramFiles")
                        Location.rmtree(ignore_errors=True)
                    PrograFile = zipfile.ZipFile(BytesIO(ProgramFilesMainDownload.content))
                    PrograFile.extractall("ProgramFiles")
                    self.showMsg("\nRepair success!")
                except Exception as PROBLEM:
                    self.showMsg(f"\nRepairing Failed!\nREASON: {PROBLEM}")
            elif self.getParams(1, " ") == "-offline":
                self.showMsg("\nResetting your system...")
                resetConfigurations()
                self.showMsg("\nReset Success!")
            else:
                self.showMsg("\nParameter not found.\nHELP: '-online' param for Online repair and '-offline' for a reset ")
            self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        else:
            self.showMsg("\nPlease enable administrator mode before accessing sfcRepair")
        self.clearStdIn()
    def exit(self): self.ROOT.destroy();  
    def cd(self):
        import platform
        if self.getParams(1) not in  ["..", "/", " ", "  ", ""]:
            os.chdir(self.getParams(1))
            self.showMsg(f"\nCurrent Working Directory: {os.getcwd()}")
        elif self.getParams(1) == "/":
            os.chdir("/")
            self.showMsg(f"\nCurrent Working Directory: {os.getcwd()}")
        elif self.getParams(1) == "..":
            if platform.system() == "Windows": character = "\\"
            else: character = "/"
            fullDirList = os.getcwd().split(character)
            modifiedPath = "".join(f"{item}/" for item in fullDirList[:-1])
            os.chdir(modifiedPath)
            self.showMsg(f"\nCurrent Working Directory: {os.getcwd()}")
        elif self.getParams(1) == "/":
            os.chdir("/")
            self.showMsg(f"\nCurrent Working Directory: {os.getcwd()}")
        else:
            self.showMsg("\nInvalid parameter... ")
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.clearStdIn()
    def dir(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        for file in os.listdir(os.getcwd()):
            if os.path.isdir(os.path.join(os.getcwd(), file)):
                self.showMsg(f"\n{file} [DIRECTORY]")
            else:
                self.showMsg("\n"+file)
        self.clearStdIn()
    def mkd(self):
        os.mkdir(self.stdin.get().split(" ")[1])
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.clearStdIn()
        self.showMsg("\nFolder created succesfully!")
    def rmd(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        try:
            CurFS: ParWFS = None
            if self.FILE_SYSTEM: CurFS: ParWFS = self.FILE_SYSTEM
            else: CurFS = ParWFS("commandprompt")
            CurFS.deleteFiles([[self.getParams(1), os.getcwd()]])
        except Exception: self.showMsg("\nCannot load a file system, so the folder was not deleted!")
        else: self.showMsg("\nFolder removed succesfully!")
        finally: self.clearStdIn()
    def startFile(self):
        import subprocess
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        try:
            self.showMsg("\nSuccesfully started file!")
            subprocess.Popen(["python3", " ".join(string for string in self.stdin.get().split(" ")[1:])])
        except Exception as EXP: self.showMsg(f"\nCannot start the specified file, due to a technical error. \nError at {str(self.startFile)}\nError: {EXP} ")
    def mk(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        with open(self.getParams(2, '-'), "w") as CREATE_FILE: CREATE_FILE.writelines(self.getParams(1, ' ').replace("\\n", "\n"))
        self.clearStdIn()
        self.showMsg("\nCreated the file successfully!")
    def rm(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        if self.ADMINISTRATOR:
            os.remove(self.getParams(1, ' '))
            self.showMsg("\nRemoved the file successfully!")
        else: self.showMsg("\nPlease enable administrator mode before removing a file")
        self.clearStdIn()
    def getParams(self, paramToGet: int, includeParamSeparator: str = " ") -> str:
        return self.stdin.get().split(' ')[paramToGet].lstrip(includeParamSeparator)
    def fsLoadConfig(self):
        if not self.FILE_SYSTEM:
            self.showMsg("\nCannot load the given config: File system hasn't been initialised into the command prompt!")
            return None
        key = self.getParams(1, "-")
        path = "".join(word for word in self.stdin.get().split(" ")[2:]).lstrip("-")
        try: self.FILE_SYSTEM.loadConfig(path, key)
        except Exception as EXCP: self.showMsg(f"\nCan't load config!\nError: {EXCP}")
        else: self.showMsg("\nConfig loaded succesfully!")
        self.clearStdIn()

    def sendToRootTerminal(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        def run():
            def killer(*args):
                pipe.kill()
                self.showMsg("\nCommand killed with Ctrl-C!")
            pipe = subprocess.Popen(self.stdin.get().replace("sendToRootTerminal -", "").split(" "), stdout=subprocess.PIPE, bufsize=1, text=True, stderr=subprocess.PIPE)
            Unbinder= self.ROOT.bind("<Control-c>", killer)
            while pipe.poll() is None:
                msg = pipe.stdout.readline().strip() # read a line from the process output
                if msg:
                    print(msg, file=RedirectOutput(self))
            self.ROOT.unbind("<Control-c>", Unbinder)
            self.showMsg("\nCommand Ended!")
        if self.ADMINISTRATOR: 
            OLD_STD = sys.stdout
            sys.stdout = RedirectOutput(self)
            print("\n")
            threading.Thread(target=run).start()
            sys.stdout = OLD_STD
            #self.clearStdIn()
        else: 
            self.showMsg("\nYou don't have permissions to run this command! Enable Administrator Mode and try again.")
    def disableDWM(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.clearStdIn()
        try:
            try: from ProgramFiles import dwm
            except: import dwm
            if (self.getParams(1, '-') == "all"): dwm.dissociateAllDWMApps()
            else: dwm.dissociateFrameFromDWM(self.PID)
        except Exception as EXP: 
            self.showMsg(f"\nThe command did not execute succesfully!\n{EXP}")
        else:
            self.showMsg(f"\nThe command completed succesfully!")
    def enableDWM(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.clearStdIn()            
        try:
            try: from ProgramFiles import dwm
            except: import dwm
            if (self.getParams(1, '-') == "all"): dwm.reRegisterAllDWMApps()
            else: dwm.createTopFrame(self.ROOT, THEME_FOREGROUND, THEME_WINDOW_BG, "commandprompt", self.ROOT.title(), self.PID)
        except Exception as EXP: 
            self.showMsg(f"\nThe command did not execute succesfully!\n{EXP}")
        else:
            self.showMsg(f"\nThe command completed succesfully!")
    def taskkill(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        print("hi?")
        param = " ".join( char for char in self.stdin.get().split(" ")[1:])
        print(param)
        try:
            charList = param.split(".")
            print(charList)
            if charList[-1] == "py":
                if SHELL_MODULES_LOADED:
                    try: callHost.endTaskByName(callHost.appImportNameCheck(" ".join(char for char in charList[0:-1])), self.showMsg)
                    except Exception as EXP: self.showMsg(f"\nError Occured: {EXP}")
                    else: self.showMsg("\nKilled all!")
                else: self.showMsg("\nCould not end task by name, because shell modules are not loaded!")
            else: raise Exception("PID-Based stuff")
        except Exception:
            if SHELL_MODULES_LOADED:
                try: callHost.endTaskByPID(int(charList[0]))
                except Exception as EXP: self.showMsg(f"\nError Occured: {EXP}")
                else: self.showMsg(f"\nKilled process associated with {charList[0]}!")
            else: self.showMsg("\nCould not end task by PID, because shell modules are not loaded!")
        self.clearStdIn()
    def tasklist(self):
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        if SHELL_MODULES_LOADED:
            try:
                self.showMsg("\nPID \t PROCESS NAME")
                RUNNING_APPS = dict(callHost.returnRunningAppsList()[1])
                for i, item in enumerate(list(RUNNING_APPS.values())): self.showMsg(f"\n{list(RUNNING_APPS.keys())[i]} \t {item}")
            except Exception as EXP: self.showMsg(f"\nCouldn't list all tasks due to an error\nError: {EXP}")
        else: self.showMsg("\nCould not list all tasks because the shell modules are not loaded!")
        self.clearStdIn()

        
THEME_WINDOW_BG, THEME_FOREGROUND = shelve.open("ProgramFiles/SYS_CONFIG")["THEME"]
def main(FILE_SYSTEM, *args): 
    ABLE_TO_USE_DWM = False
    EXP = None
    INSTANCES[args[-1]] = tkinter.Tk()
    INSTANCES[args[-1]].configure(background=THEME_WINDOW_BG)
    try:
        from ProgramFiles import dwm
        dwm.createTopFrame(INSTANCES[args[-1]], THEME_FOREGROUND, THEME_WINDOW_BG, "commandprompt", "Command Prompt", args[-1])
        ABLE_TO_USE_DWM = True
    except Exception as erm: EXP = erm
    INSTANCES[args[-1]].title("Command Interpreter")
    text = tkinter.Text(INSTANCES[args[-1]], background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=100)
    text.grid(row=1, column=0)
    yourCommand = Entry(INSTANCES[args[-1]], background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    yourCommand.configure(insertbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG, selectbackground=THEME_FOREGROUND, width=110)
    yourCommand.grid(row=2, column=0)
    cmdInstance = cmdCommands(text, yourCommand, root=INSTANCES[args[-1]], FS=FILE_SYSTEM, username=args[0], PID=args[-1])
    yourCommand.focus()
    yourCommand.bind("<Return>", cmdInstance.launchCmd)
    if not ABLE_TO_USE_DWM:
        cmdInstance.showMsg(f"\nERROR Importing window manager libraries from ProgramFiles.dwm! Using OS-Default Window manager!\nProblem: {EXP}")
    else: 
        yourCommand.focus_force()
        yourCommand.update()
        yourCommand.update_idletasks()
        yourCommand.bind("<Button-1>", lambda e=None: yourCommand.focus_force())
    if args[0] == "AUTORECOVERYENV":
        cmdInstance.ADMINISTRATOR = True
        cmdInstance.showMsg("\nDetected launch from recovery environment\nSuccesfully turned on administrator mode!")
        cmdInstance.ROOT.title("Administrator - Command Interpreter")
    if args[2]: cmdInstance.stdin.insert(0, args[2]); cmdInstance.launchCmd(True)
    INSTANCES[args[-1]].mainloop()
    return args[-1]


def focusIn(PID): INSTANCES[PID].state(newstate='normal'); return True
def focusOut(PID): INSTANCES[PID].state(newstate='withdrawn'); return True
def endTask(PID):
    INSTANCES[PID].destroy()
    return True
def returnInformation(PID):
    return {
        "title": INSTANCES[PID].title(),
        "state": INSTANCES[PID].state()
        # Would add more stuff here in the future, such as memory usage and shi. 
    }
if __name__ == "__main__":
    main(None, None, "defaultuser0",  None, dict({"THEME": ["Black", "White"]}), 99999)
