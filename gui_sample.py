# import gui package
from tkinter import *

count = 0 # global counter variable

root = Tk() # initalize window

# add a frame to window
container1 = Frame(root)
container1.pack()

# event handler function
def increment(event):
    global count
    count += 1
    x.set(value=count)

# add a button to frame
button1 = Button(container1, text='Press Me!', background='red')

button1.bind('<Button-1>', increment) # bind event handler function to left mouse click
button1.pack()

# add a label to frame
label1 = Label(container1)

# control variable to update variables automatically
x = IntVar(master=label1, value=0)

# allows update of x when x changes
label1["textvariable"] = x
label1.pack()

# infinite loop to run gui
root.mainloop()

