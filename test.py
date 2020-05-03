from tkinter import *
from tkinter import ttk
from threading import Thread
from miner import *
import queue
import tkinter.filedialog as fd

class Window:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Test GUI')
        self.csv_filename = ""
        self.q = queue.Queue()

        self.container1 = Frame(parent)
        self.container1.pack(fill=BOTH, expand=2)

        self.saveContainer = Frame(parent)
        self.saveContainer.pack()

        self.listbox1 = Listbox(self.container1)
        self.listbox1.configure(width=100, height=20)
        self.listbox1.pack(fill=BOTH, expand=1)

        self.browseButton = Button(self.container1, text='Browse', background='green')
        self.browseButton.bind('<Button-1>', self.onBrowseClick)
        self.browseButton.pack(side=LEFT)

        self.clearAllButton = Button(self.container1, text='Clear All')
        self.clearAllButton.bind('<Button-1>', self.clearListBox)
        self.clearAllButton.pack(side=RIGHT)

        self.buildCsvButton = Button(self.container1, text='Build_CSV_Test')
        self.buildCsvButton.pack()

        self.savePath = Listbox(self.saveContainer, width=50, height=1)
        self.savePath.insert(0, "Enter save location")
        self.savePath.pack(side=LEFT)

        self.saveButton = Button(self.saveContainer, text='Save')
        self.saveButton.bind('<Button-1>', self.onButtonSaveClick)
        self.saveButton.pack(side=RIGHT)

        self.testButton = Button(self.container1, text='Test')
        self.testButton.bind('<Button-1>', self.onTestClick)
        self.testButton.pack()

        self.progressbar = ttk.Progressbar(self.container1, value=0, orient=HORIZONTAL, mode='indeterminate', length=100)
        self.progressbar.pack()

    def onBrowseClick(self, event):
        filename = fd.askopenfiles(mode='r+b')
        if(len(filename) > 1):
            for f in filename:
                print(f.name)
                self.listbox1.insert(END, f.name)
        else:
            print(filename[0].name)

    def clearListBox(self, event):
        self.listbox1.delete(0, END)

    def onButtonSaveClick(self, event):
        csv = [("csv", "*.csv|*.CSV"), ("All files", "*")]
        self.csv_filename = fd.asksaveasfilename(title='Save As', defaultext='.csv', filetypes=csv)
        self.savePath.insert(0, self.csv_filename)

    def checkQ(self):
        try:
            str = self.q.get(0)
            self.progressbar.stop()
                
        except queue.Empty:
            print('Checking queue...')
            self.parent.after(1000, self.checkQ)

    def onTestClick(self, event):
        self.t1 = self.myThread(self.q)
        self.progressbar.start(15)
        self.t1.start()
        self.parent.after(1000, self.checkQ)

    class myThread(Thread):
        def __init__(self, qu):
            Thread.__init__(self)
            self.qu = qu

        def run(self):
            build_csv("Test_PDF//", 'Test_Runner.csv')
            self.qu.put("Done")

        def getQueue(self):
            return self.qu

root = Tk()
app = Window(root)
root.mainloop()