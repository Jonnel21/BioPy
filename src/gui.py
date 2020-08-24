import tkinter
from tkinter import StringVar
from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from contextManager import ContextManager
from d10 import D10Strategy
from variant2 import VariantStrategy
from nbs import NbsStrategy
import os
import queue
import tkinter.filedialog as fd


class Window:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('BioPy')
        self.csv_filename = ""
        self.radioOption = StringVar(value="0")
        self.q = queue.Queue()
        self.manager = ContextManager()

        self.container1 = tkinter.Frame(parent)
        self.container1.pack(fill=tkinter.BOTH, expand=2)

        self.saveContainer = tkinter.Frame(parent)
        self.saveContainer.pack()

        self.optionContainter = tkinter.Frame(parent)
        self.optionContainter.pack(anchor=tkinter.E)

        self.listbox1 = tkinter.Listbox(self.container1)

        self.scrollbar = tkinter.Scrollbar(self.container1)
        self.scrollbar.configure(command=self.listbox1.yview)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.listbox1.configure(width=100,
                                height=20,
                                yscrollcommand=self.scrollbar.set)
        self.listbox1.pack(fill=tkinter.BOTH, expand=1)

        self.browseButton = tkinter.Button(self.container1, text='Browse',
                                           background='green',
                                           command=self.onBrowseClick)
        self.browseButton.pack(side=tkinter.LEFT)

        self.clearAllButton = tkinter.Button(self.container1, text='Clear All',
                                             command=self.clearListBox)
        self.clearAllButton.pack(side=tkinter.RIGHT)

        self.buildCsvButton = tkinter.Button(self.container1, text='Start!',
                                             command=self.onTestClick)
        self.buildCsvButton.pack()

        self.savePath = tkinter.Listbox(self.saveContainer, width=50, height=1)
        self.savePath.insert(0, "Enter save location...")
        self.savePath.pack(side=tkinter.LEFT)

        self.saveButton = tkinter.Button(self.saveContainer, text='Save As...',
                                         command=self.onButtonSaveClick)
        self.saveButton.pack(side=tkinter.RIGHT)

        self.testButton = tkinter.Button(self.container1,
                                         text='Automated_Test',
                                         command=self.onAutomatedTestClick)
        # self.testButton.pack()

        self.progressbar = ttk.Progressbar(self.container1, value=0,
                                           orient=tkinter.HORIZONTAL,
                                           mode='indeterminate', length=100)

        self.option1 = tkinter.Radiobutton(self.optionContainter,
                                           variable=self.radioOption,
                                           text='Variant', value='Variant',
                                           command=self.SelectVarientStrat)
        self.option1.pack(anchor=tkinter.W)

        self.option2 = tkinter.Radiobutton(self.optionContainter,
                                           variable=self.radioOption,
                                           text='D-10',
                                           value='D-10',
                                           command=self.selectD10Strat)
        self.option2.pack(anchor=tkinter.W)

        self.option3 = tkinter.Radiobutton(self.optionContainter,
                                           variable=self.radioOption,
                                           text='VNBS',
                                           value='VNBS',
                                           command=self.selectVNBS)
        self.option3.pack(anchor=tkinter.W)

    def selectD10Strat(self):
        self.manager.set(D10Strategy())
        print(f'you have selected {self.radioOption.get()}!')

    def SelectVarientStrat(self):
        self.manager.set(VariantStrategy())
        print(f'you have selected {self.radioOption.get()}!')

    def selectVNBS(self):
        self.manager.set(NbsStrategy())
        print(f'you have selected {self.radioOption.get()}!')

    def onBrowseClick(self):
        filename = fd.askopenfiles(mode='r+b')
        if len(filename) >= 1:
            for f in filename:
                print(f.name)
                self.listbox1.insert(tkinter.END, f.name)

    def clearListBox(self):
        self.listbox1.delete(0, tkinter.END)

    def onButtonSaveClick(self):
        csv = [("csv", "*.csv|*.CSV"), ("All files", "*")]
        self.csv_filename = fd.asksaveasfilename(title='Save As',
                                                 defaultext='.csv',
                                                 filetypes=csv)
        self.savePath.insert(0, self.csv_filename)

    def onTestClick(self):
        files = self.listbox1.get(0, tkinter.END)
        if len(files) == 0:
            messagebox.showerror('Error', 'Files not found.')
        elif len(self.csv_filename) == 0:
            messagebox.showerror('Error', 'Save location is empty.')
        elif self.radioOption.get() == "0":
            messagebox.showerror('Error', 'Please select an instrument family.')
        else:
            self.progressbar.pack()
            self.t1 = self.myThread(self.q, files,
                                    self.csv_filename, self.manager)
            self.progressbar.start(20)
            self.t1.start()
            self.testButton['state'] = tkinter.DISABLED
            self.parent.after(1000, self.checkQ)

    def onAutomatedTestClick(self):
        vnbs = 'vnbs'
        d10 = 'd10'
        variant = 'variant'
        directory = f'C:/Users/Jonnel/Documents/pdf/{vnbs}/'
        with os.scandir(directory) as it:
            for entry in it:
                temp = os.path.join(directory, entry.name)
                self.listbox1.insert(tkinter.END, temp)
        files = self.listbox1.get(0, tkinter.END)
        self.csv_filename = 'C:/Users/Jonnel/Desktop/TEST.csv'
        self.manager.set(NbsStrategy())
        # self.manager.set(D10Strategy())
        # self.manager.set(VariantStrategy())

        if len(files) == 0:
            messagebox.showerror('Error', 'Files not found.')
        elif len(self.csv_filename) == 0:
            messagebox.showerror('Error', 'Save location is empty.')
        else:
            self.progressbar.pack()
            self.t1 = self.myThread(self.q, files,
                                    self.csv_filename, self.manager)
            # self.progressbar.start(20)
            self.t1.start()
            self.testButton['state'] = tkinter.DISABLED
            self.parent.after(1000, self.checkQ)

    def checkQ(self):
        try:
            str = self.q.get(0)
            if str == "Error":
                self.progressbar.stop()
                self.progressbar.pack_forget()
                self.testButton['state'] = tkinter.NORMAL
                messagebox.showerror('Error', 'Please use valid pdf file.')
            else:

                self.progressbar.stop()
                if(messagebox.askquestion('Info', 'Complete!',
                                          parent=self.container1,
                                          icon=messagebox.INFO,
                                          type=messagebox.OK)):
                    self.testButton['state'] = tkinter.NORMAL
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
