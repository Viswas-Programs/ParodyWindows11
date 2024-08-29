import tkinter
from ProgramFiles.errorHandler import messagebox as msgbox
TOOLTIPS_IN_USE = {}
def createToolTipAtGivenPos(event: tkinter.Event, id: str, root: tkinter.Tk, message: str, command, THEME_BG="Yellow", THEME_FG="Black"):
    global TOOLTIPS_IN_USE
    TOOLTIPS_IN_USE[id] = [None, None]
    def __actualCreateToolTip():
        global TOOLTIPS_IN_USE
        toolTipLabel = tkinter.Label(root, text=message, background=THEME_BG, foreground=THEME_FG)
        toolTipLabel.place(x=event.x_root, y=event.y_root)
        toolTipLabel.bind("<Button-1>", command)
        TOOLTIPS_IN_USE[id][0] = toolTipLabel
        return True
    TOOLTIPS_IN_USE[id][1] = root.after(1000, __actualCreateToolTip )
    return True
def deleteToolTip(id:str, root:tkinter.Tk):
    try:
        root.after_cancel(TOOLTIPS_IN_USE[id][1])
        toolTipToDelete = TOOLTIPS_IN_USE[id][0]
        toolTipToDelete.destroy()
        del TOOLTIPS_IN_USE[id]
    except Exception as EXP:
        pass
    return True