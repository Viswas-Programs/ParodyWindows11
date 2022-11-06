""" Windows 11 setup, one of a GUI mess. I am fixing the mess now! 06/05/2022
UPDATE: FIXING IN FULL BLOW - 4/11/2022"""
import time
import tkinter
from tkinter import messagebox
import os
import requests
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

    def Install(self):
        """ installer for enterprise edition"""
        self.installWindow.title("Installing Windows 11...")
        ProgramFilesDownload = requests.get("https://github.com/Viswas-Programs/ParodyWindows11/raw/main/ProgramFiles.zip")
        ExtractFiles = zipfile.ZipFile(BytesIO(ProgramFilesDownload.content))
        ExtractFiles.extractall(os.getcwd())
        self.usersetup()


    def notagreedtoMStc(self):
        """ exit as the agreement is denied"""
        messagebox.showerror("Setup Error", "Error 0x00FRE334\n"
                                            "You can't install windows 11 on your "
                                            "computer . please run this again and "
                                            "accept the terms to install Windows 11")

install_now = Installer()