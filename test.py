from tkinter import *
from tkinter import ttk
import queue
import tkinter.filedialog as fd
from multiprocessing import Process
from threading import Thread
from miner import *

class Window:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Test GUI')
        self.csv_filename = ""
        self.stopThread = False

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

        self.button5 = Button(self.container1, text='Test')
        self.button5.bind('<Button-1>', self.onButton5Click)
        self.button5.pack()

        self.progressbar = ttk.Progressbar(self.container1, value=0, orient=HORIZONTAL, mode='indeterminate', length=100)
        self.progressbar.pack()

        self.queueButton = Button(self.container1, text='Get Queue')
        self.queueButton.bind('<Button-1>', self.onQueueButtonPress)
        self.queueButton.pack()

        # self.tt1 = Thread(target=build_csv, args=("Test_PDF//", 'Test_Runner.csv'))
        # self.p1 = Process(target=build_csv, args=("Test_PDF//", 'Test_Runner.csv'))
        self.q = queue.Queue()

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
        t1 = Thread(target=build_csv, args=(t, self.csv_filename))
        t2 = Thread(target=self.progressbar.start)
        t3 = Thread(target=self.progressbar.stop)

        self.progressbar.pack()
        # self.progressbar.start(interval=5)
        if(self.csv_filename):
            # build_csv(t, self.csv_filename)
            t1.start()
            t2.start()
        else:
            print("Error! Please enter a valid save location")
        
        print("BRUHHHH.")
        # self.progressbar.stop()
        # self.progressbar.pack_forget()

    def onButtonSaveClick(self, event):
        csv = [("csv", "*.csv|*.CSV"), ("All files", "*")]
        self.csv_filename = fd.asksaveasfilename(title='Save As', defaultext='.csv', filetypes=csv)
        self.listbox2.insert(0, self.csv_filename)

    def checkQ(self):
        try:
            str = self.q.get(0)
            self.progressbar.stop()
            print(str)
                
        except queue.Empty:
            self.parent.after(100, self.checkQ)
            print('Checking queue...')

    def onButton5Click(self, event):
        self.t1 = self.myThread(self.q, self.stopThread)
        self.progressbar.start(15)
        self.t1.start()
        self.parent.after(100, self.checkQ)
        # print(self.t1.getQueue.get(0))
        # self.parent.after(100, self.checkQ)
        # self.p1.start()
        # self.p1.join(timeout=0.6)
        # self.checkBuildThread()

    def onQueueButtonPress(self, event):
        self.listbox1.insert(END, self.t1.getQueue.get(0))

    class myThread(Thread):
        def __init__(self, qu, flag):
            Thread.__init__(self)
            self.qu = qu
            self.flag = flag

        def run(self):
            build_csv("Test_PDF//", 'Test_Runner.csv')
            self.qu.put("Done")

        def getQueue(self):
            return self.qu

    # def checkBuildThread(self):
    #     if(self.tt1.is_alive):
    #         self.parent.after(100, self.checkBuildThread)
    #         print('nanai')
    #     else:
    #         print("BuildThread is dead!")




root = Tk()
app = Window(root)
root.mainloop()