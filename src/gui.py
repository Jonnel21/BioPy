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
import traceback
import os
import queue
import sys
import pyxpdf
import tracemalloc
from datetime import datetime
import tkinter.filedialog as fd


class Window:

    def __init__(self, parent):
        self.parent = parent
        self.parent.title('BioPy')
        self.csv_filename = ""
        self.radioOption = StringVar(value="0")
        self.q = queue.Queue()
        self.manager = ContextManager()
        self.logs = os.path.join(os.getenv('programdata'), 'BioPy_Logs')
        try:
            os.mkdir(self.logs)
        except FileExistsError:
            pass

        self.container1 = tkinter.Frame(parent)
        self.container1.pack(fill=tkinter.BOTH, expand=2)

        self.menubar = tkinter.Menu(parent)
        self.menubar.add_command(label="About", command=self.onMenu)

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
                                yscrollcommand=self.scrollbar.set,
                                selectmode=tkinter.EXTENDED)
        self.listbox1.pack(fill=tkinter.BOTH, expand=1)

        self.browseButton = tkinter.Button(self.container1, text='Browse',
                                           background='green',
                                           command=self.onBrowseClick)
        self.browseButton.pack(side=tkinter.LEFT)

        self.clearAllButton = tkinter.Button(self.container1, text='Clear All',
                                             command=self.clearListBox)
        self.clearAllButton.pack(side=tkinter.RIGHT)

        self.clearButton = tkinter.Button(self.container1, text='Clear',
                                          command=self.clear)
        self.clearButton.pack(side=tkinter.RIGHT)

        self.buildCsvButton = tkinter.Button(self.container1, text='Start!',
                                             command=self.onBuildCsv)
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
                                           command=self.SelectVariantStrat)
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

        txt = os.path.join(sys._MEIPASS, "version.txt")
        with open(txt, "r") as f:
            version = f.readline()
        about = "A pdf converter of patient & control samples to csv format.\n\n"
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
                    self.listbox1.insert(tkinter.END, f.name)
        except Exception:
            path = os.path.join(self.logs, "error.txt")
            self.handleError("Error: Send logs to developers.")
            with open(path, "a+") as f:
                err = traceback.format_exception(*sys.exc_info())
                timedate = datetime.now()
                f.write(f"{timedate}: {str(err)}\n")

    def clearListBox(self):
        """Clears all entries in the listbox."""

        self.listbox1.delete(0, tkinter.END)

    def clear(self):
        """Clears selected entries in the listbox."""

        indicies = self.listbox1.curselection()
        for i, e in enumerate(reversed(indicies)):
            self.listbox1.delete(e)

    def disableAllButtons(self):
        """All buttons will return to a nonfunctional state."""

        self.browseButton['state'] = tkinter.DISABLED
        self.saveButton['state'] = tkinter.DISABLED
        self.clearButton['state'] = tkinter.DISABLED
        self.clearAllButton['state'] = tkinter.DISABLED
        self.buildCsvButton['state'] = tkinter.DISABLED
        self.testButton['state'] = tkinter.DISABLED

    def enableAllButtons(self):
        """All buttons will return to a functional state."""

        self.browseButton['state'] = tkinter.NORMAL
        self.saveButton['state'] = tkinter.NORMAL
        self.clearButton['state'] = tkinter.NORMAL
        self.clearAllButton['state'] = tkinter.NORMAL
        self.buildCsvButton['state'] = tkinter.NORMAL
        self.testButton['state'] = tkinter.NORMAL

    def onButtonSaveClick(self):
        """Opens a file dialog to enter a save name for a csv file."""

        csv = [("csv", "*.csv|*.CSV"), ("All files", "*")]
        self.csv_filename = fd.asksaveasfilename(title='Save As',
                                                 defaultext='.csv',
                                                 filetypes=csv)
        self.savePath.insert(0, self.csv_filename)

    def onBuildCsv(self):
        """Starts a thread for processing pdf files."""

        files = self.listbox1.get(0, tkinter.END)
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

        except queue.Empty:
            self.parent.after(1000, self.checkQ)

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
            with os.scandir(self.manager.get().temp_dir) as it:
                for entry in it:
                    with open(entry, 'r') as f:
                        txtlist = list(f.read().split())
                        if(self.manager.get().getType() in txtlist):
                            print(f"Success: file {entry} matches selected instrument family.")
                        else:
                            errors += f"Error: file {entry} is invalid!\n"
            if(errors):
                self.qu.put("Error")
                messagebox.showerror(title="Error", message=errors)
                return "Error"

        def run(self):
            """Runs the convert_pdf and build_csv methods in a thread"""
            try:
                self.manager.get().convert_pdf(self.elements)
            except pyxpdf.xpdf.PDFSyntaxError:
                messagebox.showerror(title="Error", message="Error parsing PDF file.")
            except Exception:
                path = os.path.join(self.logs, "error.txt")
                messagebox.showerror(title="Error", message="Error: Send logs to developers.")
                with open(path, "a+") as f:
                    err = traceback.format_exception(*sys.exc_info())
                    timedate = datetime.now()
                    f.write(f"{timedate}: {str(err)}\n")
                self.qu.put("Error")
            if(self.checkFiles() == 'Error'):
                pass
            else:
                self.manager.get().build_csv(self.save)
                self.qu.put("Done")

        def getQueue(self):
            """Queue for stopping thread

            :return: The shared queue between the window and thread
            :rtype: Queue
            """

            return self.qu


tracemalloc.start()

root = Tk()
app = Window(root)
root.mainloop()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)
