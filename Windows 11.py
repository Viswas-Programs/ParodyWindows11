import tkinter
from tkinter import messagebox
import os

if os.access("theme_config.txt", os.F_OK):
    with open("theme_config.txt") as read_config:
        config = read_config.read().splitlines()
        THEME_WINDOW_BG, THEME_FOREGROUND = config
else:
    with open("theme_config.txt", "w") as FTR_write_config: #FirstTimeRun_Write_config, full form.
        THEME_WINDOW_BG = "Black"
        THEME_FOREGROUND = "White"
        FTR_write_config.write(f"{THEME_WINDOW_BG}\n{THEME_FOREGROUND}")



class Apps(object):
    def blackjackGame():
        """
        blackjack game activator
        :return: None
        """
        import ProgramFiles.Games.BlackJack.blackjack as blackjack
        blackjack.play()


    def guessinggame():
        """ guessing game CLI"""
        import ProgramFiles.Games.CLI_Comp_Guess as CLIGuessingGame
        CLIGuessingGame.play()


    def computergess():
        """ the computer guessing your number. don't have an indefinite answer :D"""
        import ProgramFiles.Games.CLI_Comp_Guess as CLICompGuess
        CLICompGuess.play()


    def memhgappGUI():
        import ProgramFiles.Utilities.MemoryHoggerGUI as MemHgGUI
        MemHgGUI.thePointOfNoReturn()

    def Notepad():
        import ProgramFiles.Utilities.Notepad.notepadGUI as notepad
        def main():
            """ main """
            root = tkinter.Tk()
            root.title("Notepad GUI v3.0 STABLE")
            text = tkinter.Text(root, height=20, width=100,
                                font=("Arial Rounded MT Bold",
                                    18), )
            text.grid(row=0, column=0, pady=10)
            saveTo = tkinter.Text(root, height=2, width=50,
                                font=("Arial Rounded MT Bold",
                                        12))
            saveTo.grid(row=1, column=0)
            notepad.NotepadRun(text_box=text, gui=root, saveTo=saveTo)
        if __name__ == "__main__":
            main()

    def fileshare():
        import ProgramFiles.Utilities.FileSharing.fileSharing as filesharing
        filesharing.main()

    def parodyBanking():
        def setup():
            import ProgramFiles.Utilities.ParodyBank.v5.bankaccountdatabase as setupAcc
            setupAcc.main()
        def launch():
            import ProgramFiles.Utilities.ParodyBank.v5.bankaccounts as launchApp
            launchApp.main()
        a = tkinter.Toplevel()
        a.configure(background=THEME_WINDOW_BG)
        msg = tkinter.Label(a, text="Do you want to setup the program, or to directly launch the app?")
        msg.grid(row=0, column=0)
        setup_btn = tkinter.Button(a, text="Setup Bank Account", command=setup,
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        setup_btn.grid(row=1, column=0)
        launch_main = tkinter.Button(a, text="Launch App", command=launch,
                                    background=THEME_WINDOW_BG,
                                    foreground=THEME_FOREGROUND)
        launch_main.grid(row=1, column=0)
        a.mainloop()
