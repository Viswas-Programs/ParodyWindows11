import ParWFS
from ProgramFiles.callHost import getTheme, getRangeToGenPID, DIALOGUE_BOXES, addToRunningAppsList
import tkinter
class Notifications(object):

    
    def __init__(self):
        self.NotificationsList = []
        self.TimeofNotification = []
        self.actions = []
        self.notificationButton = None
    def createNotification(self, msg: str, time: str, action: str):
        self.NotificationsList.append(msg)
        self.TimeofNotification.append(time)
        self.actions.append(action)
        GLOBAL_VARS = ParWFS._instances["root"].GLOBAL_VARS
        GLOBAL_VARS.ROW_COUNT_NOTIFICATION_WINDOW += 1
        self.notificationButton.configure(text=f"Notifications ({len(self.NotificationsList)})")
    def showNotification(self, title: str, msg: str, time: str, action: str) -> None:
        from ProgramFiles.errorHandler import messagebox
        self.createNotification(msg=msg, time=time, action=action)
        GLOBAL_VARS = ParWFS._instances["root"].GLOBAL_VARS
        messagebox.showinfo(title, msg, GLOBAL_VARS.ROOT_WINDOW)
    def showNotificationsList(self, event=None):
        from ProgramFiles import dwm
        notificationsWindow = tkinter.Toplevel(background=getTheme()[0])
        PID = getRangeToGenPID(DIALOGUE_BOXES)
        addToRunningAppsList(PID, "Notification Window")
        dwm.createTopFrame(notificationsWindow, getTheme()[1], getTheme()[2], "info", "Notification Center", PID)
        self.notificationButton.configure(text="Notifications (0)")
        if len(self.NotificationsList) == 0:
            a = tkinter.Label(notificationsWindow, text="No notifications (yet)", background=getTheme()[0], foreground=getTheme()[1])
            a.grid(row=1, column=0)
        for index, notif in enumerate(self.NotificationsList):
            lbl = tkinter.Label(notificationsWindow, text=f"{notif}\t: {self.TimeofNotification[index]}", background=getTheme()[0], foreground=getTheme()[1])
            lbl.grid(row=index+1, column=0)
            lbl.bind('<Button-1>', self.actions[index])
        notificationsWindow.mainloop()
        self.NotificationsList, self.actions, self.TimeofNotification = [], [], []

notifications = Notifications()