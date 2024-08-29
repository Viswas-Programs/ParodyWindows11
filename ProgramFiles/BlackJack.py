import ProgramFiles.Blackjack.blackjack as blackJack
def main(*args):
    blackJack.main()
    return args[-1]
def endTask():
    blackJack.endTask()
    return True
def returnInformation():
    return blackJack.returnInformation()
def focusIn():
    return blackJack.focusIn()
def focusOut():
    return blackJack.focusOut()