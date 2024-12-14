import ProgramFiles.Blackjack.blackjack as blackJack
NEEDS_FILESYSTEM_ACCESS = False
def main(*args):
    blackJack.main(args[-2], args[-1])
    return args[-1]
def endTask(PID):
    blackJack.endTask(PID)
    return True
def returnInformation(PID):
    return blackJack.returnInformation(PID)
def focusIn(PID):
    return blackJack.focusIn(PID)
def focusOut(PID):
    return blackJack.focusOut(PID)
