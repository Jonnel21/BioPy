from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from miner import *
import queue
import tkinter.filedialog as fd
import pdfreader.exceptions

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
            self.t1 = self.myThread(self.q, files, self.csv_filename)
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
        def __init__(self, qu, elements, save):
            Thread.__init__(self)
            self.qu = qu
            self.elements = elements
            self.save = save

        def run(self):
            try:
                build_csv(self.elements, self.save)            
                self.qu.put("Done")

            except pdfreader.exceptions.ParserException:
                self.qu.put("Error")

        def getQueue(self):
            return self.qu

root = Tk()
app = Window(root)
root.mainloop()