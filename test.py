from tkinter import *
import tkinter.filedialog as fd
from miner import *

class Window:
    def __init__(self, parent):
        self.parent = parent
        self.counter = 0

        self.container1 = Frame(parent)
        self.container1.pack()

        self.listbox1 = Listbox(self.container1)
        self.listbox1.pack()

        self.button1 = Button(self.container1, text='Browse', background='green')
        self.button1.bind('<Button-1>', self.onButton1Click)
        self.button1.pack()

        self.label1 = Label(self.container1, text='TestGui')
        self.label1.pack()

    def onButton1Click(self, event):
        filename = fd.askopenfiles(mode='r+b')
        csv_filename = fd.asksaveasfilename()
        print(csv_filename)
        build_csv(filename, csv_filename)
        if(len(filename) > 1):
            for f in filename:
                print(f.name)
        else:
            print(filename[0].name)


root = Tk()
app = Window(root)
root.mainloop()

