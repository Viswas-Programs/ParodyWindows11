""" electricity bill!"""
import tkinter

def run():
    root = tkinter.Tk()
    program_welcome = tkinter.Label(root, text="Electricity bill")
    root.title("Electricity bill calculator v1.0")

    def calculate():
        """ calculate EB"""
        enter_name.configure(state='disabled')
        eb_num.configure(state='disabled')
        electric_unit.configure(state='disabled')
        enter.configure(state='disabled')
        units = int(electric_unit.get())
        if units <= 100:
            amount = 0
        elif units <= 200:
            amount = (units - 100) * 7
        elif units <= 300:
            amount = 100 * 7 + (units - 200) * 9.5
        else:
            amount = 100 * 0 + 100 * 7 + 100 * 9.5 + (units - 300) * 12
        result = tkinter.Label(root, text=f"Your electricity bill is -> {amount}")
        result.pack()

    program_welcome.pack()
    enter_name = tkinter.Entry(root, width=60)
    enter_name.pack()
    enter_name.insert(0, "What is your name")
    eb_num = tkinter.Entry(root, width=60)
    eb_num.pack()
    eb_num.insert(0, "What is your EB Number")
    electric_unit = tkinter.Entry(root, width=60)
    electric_unit.pack()
    electric_unit.insert(0, "What is the number of units that is consumed")
    enter = tkinter.Button(root, text="Continue", command=calculate)
    enter.pack()
    root.mainloop()


if __name__ == "__main__":
    run()