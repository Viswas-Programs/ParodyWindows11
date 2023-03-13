import errorHandler
import tkinter
root = tkinter.Tk()
errorHandler.messagebox.askyesorno("hi", "hi", root)
root = tkinter.Tk()
errorHandler.messagebox.askyesnocancel("hi", "hi", root)
root = tkinter.Tk()
errorHandler.messagebox.showinfo("hi", "hi", root)
root.mainloop()