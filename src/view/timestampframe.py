import tkinter as tk
import customtkinter as ctk

from tkcalendar import Calendar

class TimestampFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Grid configuration
        self.columnconfigure((0,2,4), weight=3)
        self.columnconfigure((1,3), weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        ## VIEW ELEMENTS ----------------------------------------------------------------------------------------------------------- ##
        # --- Date picker --- #
        self.cldrDatepicker = Calendar(self, showweeknumbers=False, locale='fr_FR') # TODO : put correct arguments inside
        self.cldrDatepicker.grid(row=0, column=0, columnspan=5)
    
        # --- Time Spinboxes --- #
        self.spbHour = tk.Spinbox(self, from_=0, to=23, width=10)
        self.spbHour.grid(row=1, column=0)

        self.lblSemicolon1 = ctk.CTkLabel(self, text=":")
        self.lblSemicolon1.grid(row=1, column=1)

        self.spbMinute = tk.Spinbox(self, from_=0, to=59, width=10)
        self.spbMinute.grid(row=1, column=2)

        self.lblSemicolon2 = ctk.CTkLabel(self, text=":")
        self.lblSemicolon2.grid(row=1, column=3)

        self.spbSecond = tk.Spinbox(self, from_=0, to=59, width=10)
        self.spbSecond.grid(row=1, column=4)

        ## TODO : create a personal Spinbox class

        
    




