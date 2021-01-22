from tkinter import Button


class HoverButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event=None):
        self['relief'] = 'groove'

    def on_leave(self, event=None):
        self['relief'] = 'raised'
