""" Windows 11 setup, one of a GUI mess. I am fixing the mess now! 06/05/2022
UPDATE: FIXING IN FULL BLOW - 4/11/2022
UPDATE: Fixing successful! not a mess like before. 
UPDATE: 21/11/2022- Made the installer a little bit modulus, by not hardcoding every single file to be downloaded from github!"""
import time
import tkinter
from tkinter import messagebox
import os
import requests
import tkinter.messagebox as msgbox

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
        self.installWindow.geometry("1024x620")
        self.installWindow.configure(background=THEME_WINDOW_BG)
        welcometowindows11 = tkinter.Label(self.installWindow, text="Welcome to windows 11 setup\n"
                                            "do you want to agree to terms &"
                                            " conditions?",
                                            background=THEME_WINDOW_BG,
                                            foreground=THEME_FOREGROUND)
        agreetotc = tkinter.Button(self.installWindow, text="Yes, I agree to Microsoft terms and "
                            "conditions", command=self.Install,
                            background=THEME_WINDOW_BG,
                            foreground=THEME_FOREGROUND)
        noagreetotc = tkinter.Button(self.installWindow, text="No, I don't agree to Microsoft terms "
                                                "and conditions",
                                    command=self.notagreedtoMStc,
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        changeThemes = tkinter.Button(self.installWindow, text="Change themes!",
                                    command=self.changeTheme,
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        changeThemes.grid(row=1, column=1)
        welcometowindows11.grid(row=1, column=0)
        agreetotc.grid(row=2, column=0)
        noagreetotc.grid(row=2, column=1, padx=10)
        self.installWindow.mainloop()

    def changeTheme(self):
        if THEME_FOREGROUND == "White" and THEME_WINDOW_BG == "Black":
            THEME_FOREGROUND, THEME_WINDOW_BG = "Black", "White"
        else:
            THEME_WINDOW_BG, THEME_FOREGROUND = "Black", "White"

    def configUser(self):
        with open("ProgramFiles/accConfiguration.conf", "w") as config:
            config.write(f"{self.useraccount.get()}\n{self.password.get()}")
        os.system("""python3 "Windows 11.py" """)
        os.remove("Windows 11 INSTALLER.py")
        os.mkdir("Users")
        folders = ["Documents", "Downloads", "Music", "Videos", "Pictures", "Desktop"]
        for folder in folders:
            os.mkdir(f"Users/{folder}")
        self.installWindow.destroy()

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
        enterbutton.grid()

    def _installFiles(self, GitHubRepoName: str, fileName, writeFileName: str, branch="main"):
        if GitHubRepoName == "ParodyWindows11":
            try:
                exec(f"ParodyWindows11Dwn = requests.get('https://github.com/Viswas-Programs/ParodyWindows11/raw/{branch}/Windows 11.py')")
                exec(f"self._installWindows11(downloadedFile=ParodyWindows11Dwn)")
            except requests.exceptions.ConnectTimeout:
                msgbox.showerror("Erorr while connecting to server", "Error occured while trying to connect to"
                                "our servers. (DEBUG: the program encountered requests.exception.ConnectTimeout error!")
        else:
            if GitHubRepoName == "BlackJack-Python-Game":
                GitHubRepoName = "BlackJack"
            try:
                exec(f"{GitHubRepoName}Dwn = requests.get('https://github.com/Viswas-Programs/{GitHubRepoName}/raw/{branch}/{fileName}')")
                WriteFileName = writeFileName.removesuffix(".py")
                print(WriteFileName, writeFileName)
                exec(f"self._midInstallFileWriter(downloadedFile={GitHubRepoName}Dwn, fileNamePath='{WriteFileName}')")
            except requests.exceptions.ConnectTimeout:
                msgbox.showerror("Erorr while connecting to server", "Error occured while trying to connect to"
                                "our servers. (DEBUG: the program encountered requests.exception.ConnectTimeout error!")

    def _midInstallFileWriter(self, downloadedFile, fileNamePath: str, encoding='utf-8') -> None:
        with open(f"ProgramFiles/{fileNamePath}/{fileNamePath}", "w") as writeTo:
            try:
                writeTo.write(downloadedFile.content.decode(encoding=encoding))
            except UnicodeEncodeError as UER:
                print(f"UnicodeDecodeError occured while writing {fileNamePath}\n--MSG:{UER}")

    def _installWindows11(self, downloadedFile,):
        with open("Windows 11.py", "w") as writeTo:
            try:
                writeTo.write(downloadedFile.content.decode(encoding='utf-8'))
            except UnicodeEncodeError as UER:
                print(f"UnicodeDecodeError occured while installing Windows 11 main file.\n--DEBUG({UER})")
        
    def Install(self):
        """ installer for enterprise edition"""
        self.installWindow.title("Installing Windows 11...")
        try:
            # ProgramFilesDownload = requests.get("https://github.com/Viswas-Programs/ParodyWindows11/raw/main/ProgramFiles.zip")
            # SyntaxCheckFileDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/syntax_checker.py")
            FuncForBljckCheckFileDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/functions_for_blackjack.py")
            # Windows11MainDownload = requests.get("https://raw.githubusercontent.com/Viswas-Programs/ParodyWindows11/main/Windows 11.py")
            # self._midInstallFileWriter(downloadedFile=SyntaxCheckFileDownload, fileNamePath="syntax_checker.py")
            self._midInstallFileWriter(downloadedFile=FuncForBljckCheckFileDownload, fileNamePath="functions_for_blackjack.py")
            # self._midInstallFileWriter(downloadedFile=Windows11MainDownload, fileNamePath="Windows 11.py")
            # ExtractFiles = zipfile.ZipFile(BytesIO(ProgramFilesDownload.content))
            # ExtractFiles.extractall(os.getcwd())
            downloadFilesDict = {"Notepad": ["notepadGUI.py", "syntax_checker.py", "spellcheck.txt"],
                                "ParodyWindows11": ["Windows 11.py"],
                                "BlackJack-Python-Game": ["blackjack.py"],
                                "FileSharing": ["fileSharing.py"],
                                "fileinspector": ["fileinspector.py"]}
            os.mkdir("ProgramFiles")
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
            for repository, filesToDownload in downloadFilesDict.items():
                if repository == "ParodyWindows11":
                    filesToDownloadWindows11 = ["Windows 11.py", "VERSION.txt", "CHANGELOG.txt", "updateManager.py", "Icons/Files.png", "Icons/Notepad.png"]
                    for file in filesToDownloadWindows11:
                        self._installFiles("ParodyWindows11", file, file)
                else:
                    for file in filesToDownload:
                        writeFile = file
                        if file == "notepadGUI.py": writeFile = "Notepad.py"
                        if file == "fileSharing.py": writeFile = "FileSharing.py"
                    os.mkdir(f"ProgramFiles/{writeFile.removesuffix('.py')}")
                    for file in filesToDownload:
                        self._installFiles(repository, file, f'{writeFile}')

            self.usersetup()
        except requests.exceptions.ConnectTimeout:
            msgbox.showerror("Erorr while connecting to server", "Error occured while trying to connect to"
                            "our servers. (DEBUG: the program encountered requests.exception.ConnectTimeout error!")


    def notagreedtoMStc(self):
        """ exit as the agreement is denied"""
        messagebox.showerror("Setup Error", "Error 0x00FRE334\n"
                                            "You can't install windows 11 on your "
                                            "computer . please run this again and "
                                            "accept the terms to install Windows 11")

install_now = Installer()