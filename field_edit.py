import tkinter as tk

class FieldEditDialog:
    def __init__(self, parent, key, value):
        top = self.top = tk.Toplevel(parent)
        self.key = key
        self.myLabel = tk.Label(top, text=key)
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top, textvariable=value)
        self.myEntryBox.pack()
        self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        self.f_value = self.myEntryBox.get()
        self.top.destroy()