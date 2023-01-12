""" Windows 11 setup, one of a GUI mess. I am fixing the mess now! 06/05/2022
UPDATE: FIXING IN FULL BLOW - 4/11/2022
UPDATE: Fixing successful! not a mess like before. 
UPDATE: 21/11/2022- Made the installer a little bit modulus, by not hardcoding every single file to be downloaded from github!
UPDATE: 09/01/2023- Reverted to zip file as the file structure is getting really complex, and modularizing would make it horribly hard!"""
import tkinter
from tkinter import messagebox
import os
import requests
import tkinter.messagebox as msgbox
import zipfile
from io import BytesIO

if os.access("theme_config.txt", os.F_OK):
    with open("theme_config.txt") as read_config:
        config = read_config.read().splitlines()
        THEME_WINDOW_BG, THEME_FOREGROUND = config
else:
    with open("theme_config.txt", "w") as FTR_write_config: #FirstTimeRun_Write_config, full form.
        THEME_WINDOW_BG = "Black"
        THEME_FOREGROUND = "White"
        FTR_write_config.write(f"{THEME_WINDOW_BG}\n{THEME_FOREGROUND}")


class Installer(object):
    def __init__(self):
        self.installWindow = tkinter.Tk()
        self.installWindow.title("Windows 11 Installer")
        self.installWindow.attributes("-fullscreen", True)
        self.installWindow.bind("<Escape>", quit)
        self.installWindow.configure(background=THEME_WINDOW_BG)
        welcometowindows11 = tkinter.Label(self.installWindow, text="Welcome to windows 11 setup\n"
                                            "do you want to agree to terms &"
                                            " conditions?",
                                            background=THEME_WINDOW_BG,
                                            foreground=THEME_FOREGROUND)
        agreetotc = tkinter.Button(self.installWindow, text="Yes, I agree to my terms and "
                            "conditions", command=self.Install,
                            background=THEME_WINDOW_BG,
                            foreground=THEME_FOREGROUND)
        noagreetotc = tkinter.Button(self.installWindow, text="No, I don't agree to my terms "
                                                "and conditions",
                                    command=self.notagreedtoMStc,
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        readtc = tkinter.Button(self.installWindow, text="Read the terms and conditions!", 
                                background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                                command=self.readTc)
        changeThemes = tkinter.Button(self.installWindow, text="Change themes!",
                                    command=self.changeTheme,
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        changeThemes.grid(row=1, column=1)
        welcometowindows11.grid(row=1, column=0)
        agreetotc.grid(row=2, column=0)
        noagreetotc.grid(row=2, column=1, padx=10)
        readtc.grid(row=2, column=5)
        self.installWindow.mainloop()

    def readTc(self):
        import tkinter.messagebox
        a = tkinter.Toplevel(background=THEME_WINDOW_BG)
        b = tkinter.Text(a, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
        b.grid(row=0 ,column=0)
        try:
            b.insert(tkinter.END, requests.get("https://github.com/Viswas-Programs/ParodyWindows11/raw/main/LICENSE", timeout=5).content.decode('utf-8'))
            b.configure(state="disabled")
        except Exception as PRB:
            tkinter.messagebox.showerror("ERROR!", f"Can't load terms and conditions!\n PROBLEM: {PRB}")
            b.insert(tkinter.END, "Can't load the terms and conditions! Sorry for the inconvenience! for now, use this window as a text editor! :)")
        a.mainloop()

    def changeTheme(self):
        if THEME_FOREGROUND == "White" and THEME_WINDOW_BG == "Black":
            THEME_FOREGROUND, THEME_WINDOW_BG = "Black", "White"
        else:
            THEME_WINDOW_BG, THEME_FOREGROUND = "White", "Black"

    def configUser(self):
        with open("ProgramFiles/accConfiguration.conf", "w") as config:
            config.write(f"{self.useraccount.get()}\n{self.password.get()}")
        try:
            os.remove("Windows 11 INSTALLER.py")
            os.mkdir("Users")
            folders = ["Documents", "Downloads", "Music", "Videos", "Pictures", "Desktop"]
            for folder in folders:
                os.mkdir(f"Users/{folder}")
            os.system("""python3 "Windows 11.py" """)
            exit()
        except Exception as PRB:
            msgbox.showerror("ERROR!", str(PRB))

    def usersetup(self):
        """ user setup """
        msgUserAcc =  tkinter.Label(self.installWindow, text="Enter your Username-> ",
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        msgUserAcc.grid(row=3, column=0)
        self.useraccount = tkinter.Entry(self.installWindow, width=60)
        self.useraccount.grid(row=3, column=1)
        msgUserPass =  tkinter.Label(self.installWindow, text="Enter your Username-> ",
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        msgUserPass.grid(row=4, column=0)
        self.password = tkinter.Entry(self.installWindow, width=60, show="*")
        self.password.grid(row=4, column=1)
        enterbutton = tkinter.Button(self.installWindow, text="Enter", command=self.configUser,
                                        background=THEME_WINDOW_BG,
                                        foreground=THEME_FOREGROUND)
        enterbutton.grid(row=4, column=2)

    def _midInstallFileWriter(self, downloadedFile, fileNamePath: str, encoding='utf-8') -> None:
        with open(f"ProgramFiles/{fileNamePath}/{fileNamePath}", "w") as writeTo:
            try:
                writeTo.write(downloadedFile.content.decode(encoding=encoding))
            except UnicodeEncodeError as UER:
                print(f"UnicodeDecodeError occured while writing {fileNamePath}\n--MSG:{UER}")
        
    def Install(self):
        """ installer for enterprise edition"""
        self.installWindow.title("Installing Windows 11...")
        try:
            ProgramFilesDownload = requests.get("https://github.com/Viswas-Programs/ParodyWindows11/raw/main/ProgramFiles.zip")
            # SyntaxCheckFileDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/syntax_checker.py")
            # FuncForBljckCheckFileDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/functions_for_blackjack.py")
            Windows11MainDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/Windows 11.py")
            # self._midInstallFileWriter(downloadedFile=SyntaxCheckFileDownload, fileNamePath="syntax_checker.py")
            # self._midInstallFileWriter(downloadedFile=FuncForBljckCheckFileDownload, fileNamePath="functions_for_blackjack.py")
            self._midInstallFileWriter(downloadedFile=Windows11MainDownload, fileNamePath="Windows 11.py")
            ExtractFiles = zipfile.ZipFile(BytesIO(ProgramFilesDownload.content))
            ExtractFiles.extractall(os.getcwd())
            # for repo, files in downloadFilesDict.items():
            #     for file in files:
            #         print(file, repo, sep=" : ")
            #         if file == "notepadGUI.py": writeFile = "Notepad.py"
            #         if file == "fileSharing.py": writeFile = "FileSharing.py"
            #         try:
            #             os.mkdir(f"ProgramFiles/{writeFile.removesuffix('.py')}")
            #         except FileExistsError as error:
            #             print(f"DEBUG<The install folder already exists.>\n"
            #             f"--MSG: {error} ")
            #         self._installFiles(repo, file, str(writeFile))
            os.system("pip3 install tkinterweb")
            os.system("pip3 install psutil")
            os.system("pip3 install requests")
            self.usersetup()
        except requests.exceptions.ConnectTimeout:
            msgbox.showerror("Erorr while connecting to server", "Error occured while trying to connect to"
                            "our servers. (DEBUG: the program encountered requests.exception.ConnectTimeout error!")


    def notagreedtoMStc(self):
        """ exit as the agreement is denied"""
        messagebox.showerror("Setup Error", "Error!\n"
                                            "You can't install windows 11 on your "
                                            "computer . please run this again and "
                                            "accept the terms to install Windows 11")

install_now = Installer()
print("The install woud've been finished, please close this if the window doesn't close automatically\n or if the OS is not starting up, please close this window and run Windows 11.py")