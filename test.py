from tkinter import *
import tkinter.filedialog as fd
from miner import *

class Window:
    def __init__(self, parent):
        self.parent = parent
        self.counter = 0
        self.parent.title('Test GUI')
        self.csv_filename = ""

        self.container1 = Frame(parent)
        self.container1.pack(fill=BOTH, expand=2)

        self.saveContainer = Frame(parent)
        self.saveContainer.pack()

        self.listbox1 = Listbox(self.container1)
        self.listbox1.configure(width=100, height=20)
        self.listbox1.pack(fill=BOTH, expand=1)

        self.button1 = Button(self.container1, text='Browse', background='green')
        self.button1.bind('<Button-1>', self.onButton1Click)
        self.button1.pack(side=LEFT)

        self.button2 = Button(self.container1, text='Clear All')
        self.button2.bind('<Button-1>', self.emptyListBox1)
        self.button2.pack(side=RIGHT)

        self.button3 = Button(self.container1, text='Build_CSV_Test')
        self.button3.bind('<Button-1>', self.onButton3Click)
        self.button3.pack()

        self.listbox2 = Listbox(self.saveContainer, width=50, height=1)
        self.listbox2.insert(0, "Enter save location")
        self.listbox2.pack(side=LEFT)

        self.button4 = Button(self.saveContainer, text='Save')
        self.button4.bind('<Button-1>', self.onButtonSaveClick)
        self.button4.pack(side=RIGHT)
        
    def onButton1Click(self, event):
        filename = fd.askopenfiles(mode='r+b')
        # print(self.csv_filename)
        if(len(filename) > 1):
            for f in filename:
                print(f.name)
                self.listbox1.insert(END, f.name)
        else:
            print(filename[0].name)
        # build_csv(filename, self.csv_filename)

    def emptyListBox1(self, event):
        self.listbox1.delete(0, END)

    def onButton3Click(self, event):
        t = self.listbox1.get(0, END)
        if(self.csv_filename):
            build_csv(t, self.csv_filename)
        else:
            print("Error! Please enter a valid save location")

    def onButtonSaveClick(self, event):
        csv = [("csv", "*.csv|*.CSV"), ("All files", "*")]
        self.csv_filename = fd.asksaveasfilename(title='Save As', defaultext='.csv', filetypes=csv)
        self.listbox2.insert(0, self.csv_filename)
                    


root = Tk()
app = Window(root)
root.mainloop()

