import tkinter
TOOLTIPS_IN_USE = {}
THEME_BG="Yellow"
THEME_FG="Black"
def _createToolTipAtGivenPos(widget: tkinter.Widget, id: str, root: tkinter.Tk, message: str, command, event: tkinter.Event, ):
    global TOOLTIPS_IN_USE
    TOOLTIPS_IN_USE[id] = [None, None]
    widget.bind("<Enter>", )
    def __actualCreateToolTip():
        global TOOLTIPS_IN_USE
        toolTipLabel = tkinter.Label(root, text=message, background=THEME_BG, foreground=THEME_FG)
        toolTipLabel.place(x=event.x_root, y=event.y_root)
        toolTipLabel.bind("<Button-1>", command)
        TOOLTIPS_IN_USE[id][0] = toolTipLabel
        return True
    TOOLTIPS_IN_USE[id][1] = root.after(1000, __actualCreateToolTip )
    return True
def createToolTipAtGivenPos(widget: tkinter.Widget, id: str, root: tkinter.Tk, message: str, command=None):
    if (not command): command=widget.cget('command')
    widget.bind("<Enter>", lambda e: _createToolTipAtGivenPos(widget, id, root, message, command, e))
    widget.bind("<Leave>", lambda e: deleteToolTip(id, root))
def deleteToolTip(id:str, root:tkinter.Tk):
    try:
        root.after_cancel(TOOLTIPS_IN_USE[id][1])
        toolTipToDelete = TOOLTIPS_IN_USE[id][0]
        toolTipToDelete.destroy()
        del TOOLTIPS_IN_USE[id]
    except Exception as EXP:
        pass
    return True