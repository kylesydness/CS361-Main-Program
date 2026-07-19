import time
import tkinter as tk
from tkinter import ttk

speed = .02 # slow: 0.05, fast:  0.005

def tprint (text: str):
    for char in text:
        print(char, end = "")
        time.sleep(speed)
    print()