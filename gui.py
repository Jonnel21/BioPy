from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from contextManager import ContextManager
import queue
from d10 import D10Strategy
from varient2 import VarientStrategy
from nbs import NbsStrategy
from contextManager import ContextManager
import tkinter.filedialog as fd

class Window:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Test GUI')
        self.csv_filename = ""
        self.radioOption = StringVar(value="0")
        self.q = queue.Queue()
        self.manager = ContextManager()

        self.container1 = Frame(parent)
        self.container1.pack(fill=BOTH, expand=2)

        self.saveContainer = Frame(parent)
        self.saveContainer.pack()

        self.optionContainter = Frame(parent)
        self.optionContainter.pack(anchor=E)

        self.listbox1 = Listbox(self.container1)
        self.listbox1.configure(width=100, height=20)
        self.listbox1.pack(fill=BOTH, expand=1)

        self.browseButton = Button(self.container1, text='Browse', background='green', 
                                  command=self.onBrowseClick)
        self.browseButton.pack(side=LEFT)

        self.clearAllButton = Button(self.container1, text='Clear All',
                                    command=self.clearListBox)
        self.clearAllButton.pack(side=RIGHT)

        self.buildCsvButton = Button(self.container1, text='Build_CSV_Test', command=self.onTestClick)
        self.buildCsvButton.pack()

        self.savePath = Listbox(self.saveContainer, width=50, height=1)
        self.savePath.insert(0, "Enter save location")
        self.savePath.pack(side=LEFT)

        self.saveButton = Button(self.saveContainer, text='Save As',
                                command=self.onButtonSaveClick)
        self.saveButton.pack(side=RIGHT)

        self.testButton = Button(self.container1, text='Automated_Test',
                                command=self.onTestClick)
        # self.testButton.pack()

        self.progressbar = ttk.Progressbar(self.container1, value=0, orient=HORIZONTAL, mode='indeterminate', length=100)

        self.option1 = Radiobutton(self.optionContainter, variable=self.radioOption, text='Varient', value='Varient', command=self.SelectVarientStrat)
        self.option1.pack(anchor=W)

        self.option2 = Radiobutton(self.optionContainter, variable=self.radioOption, text='D-10', value='D-10', command=self.selectD10Strat)
        self.option2.pack(anchor=W)

        self.option3 = Radiobutton(self.optionContainter, variable=self.radioOption, text='VNBS', value='VNBS', command=self.selectVNBS)
        self.option3.pack(anchor=W)

    def selectD10Strat(self):
        self.manager.set(D10Strategy())
        print(f'you have selected {self.radioOption.get()}!')
    
    def SelectVarientStrat(self):
        self.manager.set(VarientStrategy())
        print(f'you have selected {self.radioOption.get()}!')

    def selectVNBS(self):
        self.manager.set(NbsStrategy())
        print(f'you have selected {self.radioOption.get()}!')

    def onBrowseClick(self):
        filename = fd.askopenfiles(mode='r+b')
        if(len(filename) >= 1):
            for f in filename:
                print(f.name)
                self.listbox1.insert(END, f.name)

    def clearListBox(self):
        self.listbox1.delete(0, END)

    def onButtonSaveClick(self):
        csv = [("csv", "*.csv|*.CSV"), ("All files", "*")]
        self.csv_filename = fd.asksaveasfilename(title='Save As', defaultext='.csv', filetypes=csv)
        self.savePath.insert(0, self.csv_filename)

    def onTestClick(self):
        files = self.listbox1.get(0, END)
        if(len(files) == 0):
            messagebox.showerror('Error', 'Files not found.')
        elif(len(self.csv_filename) == 0):
            messagebox.showerror('Error', 'Save location is empty.')
        else:
            self.progressbar.pack()
            self.t1 = self.myThread(self.q, files, self.csv_filename, self.manager)
            self.progressbar.start(20)
            self.t1.start()
            self.testButton['state'] = DISABLED
            self.parent.after(1000, self.checkQ)

    def checkQ(self):
        try:
            str = self.q.get(0)
            if(str == "Error"):
                self.progressbar.stop()
                self.progressbar.pack_forget()
                self.testButton['state'] = NORMAL
                messagebox.showerror('Error', 'Please use valid pdf file.')
            else:

                self.progressbar.stop()
                if(messagebox.askquestion('Info', 'Complete!', parent=self.container1, 
                                            icon=messagebox.INFO, type=messagebox.OK)):
                    self.testButton['state'] = NORMAL
                    self.progressbar.pack_forget()
                    self.savePath.insert(0, "Enter save location")
                    self.csv_filename = ""


        except queue.Empty:
            self.parent.after(1000, self.checkQ)

    class myThread(Thread):
        def __init__(self, qu, elements, save, manager):
            Thread.__init__(self)
            self.qu = qu
            self.elements = elements
            self.save = save
            self.manager = manager

        def run(self):
                self.manager.get().convert_pdf(self.elements)
                self.manager.get().build_csv(self.save)            
                self.qu.put("Done")

        def getQueue(self):
            return self.qu

root = Tk()
app = Window(root)
root.mainloop()