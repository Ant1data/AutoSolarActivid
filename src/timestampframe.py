import os
import tkinter as tk
import customtkinter as ctk

from datetime import date
from tkcalendar import Calendar

class TimestampFrame(ctk.CTkFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root # Defining tkinter root container

        # Grid configuration
        self.columnconfigure((0,2,4), weight=3)
        self.columnconfigure((1,3), weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        
        # Adding elements
        self.calendar = Calendar() # TODO : put correct arguments inside
        self.grid(row=0, column=0) # rowstamp or smth like this remaining
