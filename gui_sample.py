from tkinter import *

class Addition:
    def __init__(self, parent):
        self.parent = parent
        self.counter = 0

        self.container1 = Frame(parent)
        self.container1.pack()

        self.button1 = Button(self.container1, text='Press Me!', background='green')
        self.button1.bind('<Button-1>', self.increment)
        self.button1.pack()

        self.label1 = Label(self.container1)
        self.control = IntVar(self.label1, value=0)
        self.label1['textvariable'] = self.control
        self.label1.pack()

    def increment(self, event):
        self.counter += 1
        self.control.set(self.counter)

root = Tk()
add = Addition(root)
root.mainloop()

