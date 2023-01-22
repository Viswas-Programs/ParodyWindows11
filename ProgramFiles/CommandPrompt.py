import tkinter
import os
os.system("pip install requests")
import requests
import shelve

class cmdCommands(object):
    global root
    def __init__(self, stdout: tkinter.Text, stdin: tkinter.Entry) -> None:
        self.UP_ARROW_COUNT = 0
        self.ACCEPT_COMMANDS = True
        self.stdout = stdout
        self.stdin = stdin
        self.LINE_COUNT = 0.0
        self.COMMAND_LIST = ["clear", "shutdown", "restart", "exit", "sfcRepair", "cd", "dir", "mkd", "rmd", "user"]
        self.INPUTTED_COMMANDS_LIST = []
        self.COMMAND_NOT_FOUND = "\nThe following command doesn't exist!"
        self.showMsg(f"Welcome to ParodyWindows11 Command Interpreter (OS Version 2.0)\nCurrent Working Directory: {os.getcwd()}\n>")
        try: root.bind("<Up>", self.upArrowBind); root.bind("<Down>", self.downArrowBind)
        except Exception as exp: print(f' {exp}')
    def user(self):
        pass
    def downArrowBind(self, e=None): self.clearStdIn(); self.stdin.insert(tkinter.END, self.INPUTTED_COMMANDS_LIST[-self.UP_ARROW_COUNT+1])
    def upArrowBind(self, e=None):
        self.UP_ARROW_COUNT += 1
        self.clearStdIn()
        self.stdin.insert(tkinter.END, self.INPUTTED_COMMANDS_LIST[-self.UP_ARROW_COUNT])
    def showMsg(self, msg: str):
        self.stdout.configure(state="normal")
        self.LINE_COUNT += 1.0
        self.stdout.insert(f"{self.LINE_COUNT+1}", msg)
        if "\n" in msg: self.LINE_COUNT += 1.0
        self.stdout.configure(state="disabled")
    def launchCmd(self, e=None):
        if " " not in self.stdin.get(): self.stdin.insert(tkinter.END, "  ")
        if self.stdin.get().split(" ")[0] in self.COMMAND_LIST and self.ACCEPT_COMMANDS: exec(f"self.{self.stdin.get().split(' ')[0]}()")
    def clearStdIn(self):
        self.stdin.destroy()
        self.stdin = tkinter.Entry(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=110)
        self.stdin.configure(insertbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG, selectbackground=THEME_FOREGROUND, )
        self.stdin.grid(row=1, column=0)
        self.stdin.bind("<Return>", self.launchCmd)
        self.stdin.focus()
    def clear(self):
        self.clearStdIn()
        self.stdout.configure(state="normal")
        try: self.stdout.delete(1.0, tkinter.END)
        except Exception as exp: self.showMsg(f"\nERROR OCCURED while clearing terminal: {exp}")
        finally: self.INPUTTED_COMMANDS_LIST.append("clear"); self.stdout.configure(state="disabled")
    def shutdown(self):
        self.clearStdIn()
        self.showMsg("\nShutting down...")
        root.after(5000, lambda: os._exit(0))
    def restart(self):
        self.clearStdIn()
        os.system("cd..")
        os.system("""python3 "Windows 11.py" """)
        exit()
    def sfcRepair(self):
        def resetConfigurations():
            try:
                txtFilesToDelete = ["theme_config.txt", "ProgramFiles/tkweb.txt", "ProgramFiles/pinnedApps.txt"]
                for fileToDelete in txtFilesToDelete:
                    try:
                        os.remove(fileToDelete)
                    except Exception: pass
                shelveFilesToDelete = ["ProgramFiles/history", "ProgramFiles/IPChat/_serverConfig", "ProgramFiles/IPChat/serversList"]
                for shelveToDelete in shelveFilesToDelete:
                    try:
                        with shelve.open(shelveToDelete) as deleteIt:
                            deleteIt.clear()
                    except Exception: pass
            except Exception as exp:
                self.showMsg(f"\nERROR OCCURED While resetting...!Error: {exp}")
        if self.stdin.get().split(" ")[1] == "-online":
            self.showMsg("Repairing system...")
            try:
                Windows11MainDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/Windows 11.py", timeout=40)
                resetConfigurations()
                self.showMsg("\nRepair success!")
                with open("Windows 11.py", "w") as writeTo:
                    try:
                        writeTo.write(Windows11MainDownload.content.decode(encoding="UTF-8"))
                    except UnicodeEncodeError as UER:
                        self.showMsg(f"\nUnicodeDecodeError occured while repairing 'Windows 11.py'\n--MSG:{UER}")
            except Exception as PROBLEM:
                self.showMsg(f"\nRepairing Failed!\nREASON: {PROBLEM}")
        elif self.stdin.get().split(" ")[1] == "-offline":
            self.showMsg("\nResetting your system...")
            resetConfigurations()
            self.showMsg("\nReset Success!")
        else:
            self.showMsg("\nParameter not found.\nHELP: '-online' param for Online repair and '-offline' for a reset ")
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.clearStdIn()
    def exit(): os._exit(0)
    def cd(self):
        import platform
        if self.stdin.get().split(" ")[1] not in  ["..", "/", " ", "  ", ""]:
            os.chdir(self.stdin.get().split(" ")[1])
            self.showMsg(f"\nCurrent Working Directory: {os.getcwd()}")
        elif self.stdin.get().split(" ")[1] == "/":
            os.chdir("/")
            self.showMsg(f"\nCurrent Working Directory: {os.getcwd()}")
        elif self.stdin.get().split(" ")[1] == "..":
            if platform.system() == "Windows": character = "\\"
            else: character = "/"
            fullDirList = os.getcwd().split(character)
            modifiedPath = "".join(f"{item}/" for item in fullDirList[:-1])
            os.chdir(modifiedPath)
            self.showMsg(f"\nCurrent Working Directory: {os.getcwd()}")
        elif self.stdin.get().split(" ")[1] == "/":
            os.chdir("/")
            self.showMsg(f"\nCurrent Working Directory: {os.getcwd()}")
        else:
            self.showMsg("\nInvalid parameter... ")
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.clearStdIn()
    def dir(self):
        for (filepath, dirname, filename) in os.walk(os.getcwd()):
            print(filepath, dirname)
            for file in dirname:
                self.showMsg(f"\n{dirname}/{file}")
        self.INPUTTED_COMMANDS_LIST.append(self.stdin.get())
        self.clearStdIn()
    def mkd(self):
        os.mkdir(self.stdin.get().split(" ")[1])
        self.clearStdIn()
        self.showMsg("\nFolder created succesfully!")
    def rmd(self):
        os.rmdir(self.stdin.get().split(" ")[1])
        self.clearStdIn()
        self.showMsg("\nFolder removed succesfully!")
THEME_WINDOW_BG, THEME_FOREGROUND = open("theme_config.txt").read().split("\n")
def main(): 
    global root
    def sendCommand(e=None):
        cmdInstance.showMsg(f"\n>{yourCommand.get()}")
        if " " not in yourCommand.get():
            yourCommand.insert(tkinter.END, "  ")
        if yourCommand.get().split(" ")[0] in cmdInstance.COMMAND_LIST and cmdInstance.ACCEPT_COMMANDS:
            exec(f"cmdInstance.{yourCommand.get().split(' ')[0]}()")
        elif not cmdInstance.ACCEPT_COMMANDS: cmdInstance.clear()
        else: cmdInstance.showMsg(cmdInstance.COMMAND_NOT_FOUND); print("COMMAND_NOT_FOUND!")
    root = tkinter.Tk()
    root.configure(background=THEME_WINDOW_BG)
    root.title("Command Interpreter")
    text = tkinter.Text(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=100)
    text.grid(row=0, column=0)
    yourCommand = tkinter.Entry(root, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
    yourCommand.configure(insertbackground=THEME_FOREGROUND, selectforeground=THEME_WINDOW_BG, selectbackground=THEME_FOREGROUND, width=110)
    yourCommand.grid(row=1, column=0)
    cmdInstance = cmdCommands(text, yourCommand)
    yourCommand.focus()
    yourCommand.bind("<Return>", sendCommand)
    root.mainloop()

if __name__ == "__main__":
    main()