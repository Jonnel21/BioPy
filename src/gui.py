from tkinter import Listbox, Frame, Button
from tkinter import Tk, ttk, Menu
from tkinter import messagebox, StringVar
from tkinter import Scrollbar, Radiobutton
from tkinter import EXTENDED, HORIZONTAL
from tkinter import DISABLED, NORMAL
from tkinter import BOTH, LEFT, RIGHT, END
from tkinter import W, E, Y
from threading import Thread
from contextManager import ContextManager
from d10 import D10Strategy
from variant2 import VariantStrategy
from nbs import NbsStrategy
from traceback import format_exception
from os import getenv, path, mkdir, scandir
from queue import Queue, Empty
from pyxpdf.xpdf import PDFSyntaxError
from datetime import datetime
import tkinter.filedialog as fd
import sys


class Window:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('BioPy')
        self.csv_filename = ""
        self.radioOption = StringVar(value="0")
        self.q = Queue()
        self.manager = ContextManager()
        self.logs = path.join(getenv('programdata'), 'BioPy_Logs')
        try:
            mkdir(self.logs)
        except FileExistsError:
            pass

        self.container1 = Frame(parent)
        self.container1.pack(fill=BOTH, expand=2)

        self.menubar = Menu(parent)
        self.menubar.add_command(label="About", command=self.onMenu)

        self.saveContainer = Frame(parent)
        self.saveContainer.pack()

        self.optionContainter = Frame(parent)
        self.optionContainter.pack(anchor=E)

        self.listbox1 = Listbox(self.container1)

        self.scrollbar = Scrollbar(self.container1)
        self.scrollbar.configure(command=self.listbox1.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox1.configure(width=100,
                                height=20,
                                yscrollcommand=self.scrollbar.set,
                                selectmode=EXTENDED)
        self.listbox1.pack(fill=BOTH, expand=1)

        self.browseButton = Button(self.container1, text='Browse',
                                   background='green',
                                   command=self.onBrowseClick)
        self.browseButton.pack(side=LEFT)

        self.clearAllButton = Button(self.container1, text='Clear All',
                                     command=self.clearListBox)
        self.clearAllButton.pack(side=RIGHT)

        self.clearButton = Button(self.container1, text='Clear',
                                  command=self.clear)
        self.clearButton.pack(side=RIGHT)

        self.buildCsvButton = Button(self.container1, text='Start!',
                                     command=self.onBuildCsv)
        self.buildCsvButton.pack()

        self.savePath = Listbox(self.saveContainer, width=50, height=1)
        self.savePath.insert(0, "Enter save location...")
        self.savePath.pack(side=LEFT)

        self.saveButton = Button(self.saveContainer, text='Save As...',
                                 command=self.onButtonSaveClick)
        self.saveButton.pack(side=RIGHT)

        self.testButton = Button(self.container1,
                                 text='Automated_Test',
                                 command=self.onAutomatedTestClick)
        # self.testButton.pack()

        self.progressbar = ttk.Progressbar(self.container1, value=0,
                                           orient=HORIZONTAL,
                                           mode='indeterminate', length=100)

        self.option1 = Radiobutton(self.optionContainter,
                                   variable=self.radioOption,
                                   text='Variant', value='Variant',
                                   command=self.SelectVariantStrat)
        self.option1.pack(anchor=W)

        self.option2 = Radiobutton(self.optionContainter,
                                   variable=self.radioOption,
                                   text='D-10',
                                   value='D-10',
                                   command=self.selectD10Strat)
        self.option2.pack(anchor=W)

        self.option3 = Radiobutton(self.optionContainter,
                                   variable=self.radioOption,
                                   text='VNBS',
                                   value='VNBS',
                                   command=self.selectVNBS)
        self.option3.pack(anchor=W)
        self.parent.config(menu=self.menubar)

        positionRight = int(self.parent.winfo_screenwidth()/4)
        positionDown = int(self.parent.winfo_screenheight()/5)

        # Positions the window in the center of the page.
        self.parent.geometry("+{}+{}".format(positionRight, positionDown))

    def onMenu(self):
        """Handles when the 'About' menu item is clicked.

        :return: A messagebox showing a summary, version, and authors.
        :rtype: messagebox
        """

        txt = path.join(sys._MEIPASS, "version.txt")
        with open(txt, "r") as f:
            version = f.readline()
        about = "A pdf to csv tool for patient & control samples.\n\n"
        version += "\n"
        authors = "Jonnel Alcantara & Kevin Nganga"
        msg = f"{about}Version: {version}Authors: {authors}"
        return messagebox.showinfo(title="About", message=msg)

    def handleError(self, txt):
        """wrapper method to customize text of error

        :param txt: string describing the error.
        :type txt: str
        :return: error message box.
        :rtype: messagebox
        """

        return messagebox.showerror('Error', txt)

    def selectD10Strat(self):
        """Sets and use methods specific to D10 reports."""

        self.manager.set(D10Strategy())
        print(f'you have selected {self.radioOption.get()}!')

    def SelectVariantStrat(self):
        """Sets and use methods specific to varaint reports."""

        self.manager.set(VariantStrategy())
        print(f'you have selected {self.radioOption.get()}!')

    def selectVNBS(self):
        """Sets and use methods specific to VNBS reports."""

        self.manager.set(NbsStrategy())
        print(f'you have selected {self.radioOption.get()}!')

    def onBrowseClick(self):
        """Selects pdf files via the file dialog
           to be inserted in the listbox.
        """

        try:
            filename = fd.askopenfiles(mode='r+b')
            if len(filename) >= 1:
                for f in filename:
                    print(f.name)
                    self.listbox1.insert(END, f.name)
        except Exception:
            error = path.join(getenv('programdata'), "BioPy_Logs", "error.txt")
            self.handleError(f"Error see logs at {error}")
            with open(error, "a+") as f:
                err = format_exception(*sys.exc_info())
                timedate = datetime.now()
                f.write(f"{timedate}: {str(err)}\n")

    def clearListBox(self):
        """Clears all entries in the listbox."""

        self.listbox1.delete(0, END)

    def clear(self):
        """Clears selected entries in the listbox."""

        indicies = self.listbox1.curselection()
        for i, e in enumerate(reversed(indicies)):
            self.listbox1.delete(e)

    def disableAllButtons(self):
        """All buttons will return to a nonfunctional state."""

        self.browseButton['state'] = DISABLED
        self.saveButton['state'] = DISABLED
        self.clearButton['state'] = DISABLED
        self.clearAllButton['state'] = DISABLED
        self.buildCsvButton['state'] = DISABLED
        self.testButton['state'] = DISABLED

    def enableAllButtons(self):
        """All buttons will return to a functional state."""

        self.browseButton['state'] = NORMAL
        self.saveButton['state'] = NORMAL
        self.clearButton['state'] = NORMAL
        self.clearAllButton['state'] = NORMAL
        self.buildCsvButton['state'] = NORMAL
        self.testButton['state'] = NORMAL

    def onButtonSaveClick(self):
        """Opens a file dialog to enter a save name for a csv file."""

        csv = [("csv", "*.csv|*.CSV"), ("All files", "*")]
        self.csv_filename = fd.asksaveasfilename(title='Save As',
                                                 defaultext='.csv',
                                                 filetypes=csv)
        self.savePath.insert(0, self.csv_filename)

    def onBuildCsv(self):
        """Starts a thread for processing pdf files."""

        files = self.listbox1.get(0, END)
        if len(files) == 0:
            self.handleError('Files not found!')
        elif len(self.csv_filename) == 0:
            self.handleError('Save location is empty!')
        elif self.radioOption.get() == "0":
            self.handleError('Please select an instrument family!')
        else:
            self.progressbar.pack()
            self.t1 = self.myThread(self.q, files,
                                    self.csv_filename, self.manager)
            self.progressbar.start(20)
            self.t1.start()
            self.disableAllButtons()
            self.parent.after(100, self.checkQ)

    def onAutomatedTestClick(self):
        vnbs = 'vnbs'
        d10 = 'd10'
        variant = 'variant'
        directory = f'C:/Users/Jonnel/Documents/pdf/{vnbs}/'
        with os.scandir(directory) as it:
            for entry in it:
                temp = os.path.join(directory, entry.name)
                self.listbox1.insert(END, temp)
        files = self.listbox1.get(0, END)
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
            self.testButton['state'] = DISABLED
            self.parent.after(500, self.checkQ)

    def checkQ(self):
        """Checks the queue every second for a stop code to notify the user
           that the operation has completed.

           Checks the queue every second for an error code to notify the user
           that an error as occured.
        """

        try:
            str = self.q.get(0)
            if str == "Error":
                self.progressbar.stop()
                self.progressbar.pack_forget()
                self.enableAllButtons()

            elif str == "Done":
                self.progressbar.stop()
                if(messagebox.askquestion('Info', 'Complete!',
                                          parent=self.container1,
                                          icon=messagebox.INFO,
                                          type=messagebox.OK)):
                    self.enableAllButtons()
                    self.progressbar.pack_forget()
                    self.savePath.insert(0, "Enter save location")
                    self.csv_filename = ""
            else:
                pass

        except Empty:
            self.parent.after(100, self.checkQ)

    class myThread(Thread):
        def __init__(self, qu, elements, save, manager):
            Thread.__init__(self)
            self.qu = qu
            self.elements = elements
            self.save = save
            self.manager = manager

        def checkFiles(self):
            """Verifies that the files in the listbox
            is the same as what's selected by the
            user.

            :return: A string literal.
            :rtype: str
            """

            errors = ""
            with scandir(self.manager.get().temp_dir) as it:
                for entry in it:
                    with open(entry, 'r') as f:
                        txtlist = list(f.read().split())
                        if(self.manager.get().get_type() in txtlist):
                            print(f"Success: file {entry} matches selected instrument family.")
                        else:
                            errors += f"Error: file {entry.path} is invalid!\n"
            if(errors):
                self.qu.put("Error")
                messagebox.showerror(title="Error", message=errors)
                return "Error"
            else:
                return "Pass"

        def run(self):
            """Runs the convert_pdf and build_csv methods in a thread"""
            try:
                self.manager.get().convert_pdf(self.elements)
            except PDFSyntaxError:
                messagebox.showerror(title="Error", message="Error parsing PDF file.")
            except Exception:
                error = path.join(getenv('programdata'), "BioPy_Logs", "error.txt")
                messagebox.showerror(title="Error", message=f"Error see logs at {error}")
                with open(error, "a+") as f:
                    err = format_exception(*sys.exc_info())
                    timedate = datetime.now()
                    f.write(f"{timedate}: {str(err)}\n")
                self.qu.put("Error")
            if(self.checkFiles() == "Error"):
                return "Error"
            else:
                self.manager.get().build_csv(self.save)
                self.qu.put("Done")

        def getQueue(self):
            """Queue for stopping thread

            :return: The shared queue between the window and thread
            :rtype: Queue
            """

            return self.qu


root = Tk()
app = Window(root)
root.mainloop()
