import tkinter as tk

root = tk.Tk()
import time

word = 'hello, this is an example printout'

def print_desc(char=1):
    l.config(text=word[:char])
    if char < len(word):
        root.after(80, lambda: print_desc(char+1))
    if char >= len(word):
        root.after(80)
        b.pack()

b = tk.Button(root, text='go')
l = tk.Label(root, font=("Bodoni 72", 20))
print_desc()
#b.pack()
l.pack()

root.mainloop()