import tkinter as tk
import customtkinter as ctk

from tkcalendar import Calendar

class TimestampFrame(ctk.CTkFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ## TODO : create a personal Spinbox class

        # Grid configuration
        self.columnconfigure((0, 2, 4, 6, 8, 10), weight=3)
        self.columnconfigure((1, 3, 5, 7, 9), weight=1)
        self.rowconfigure((0, 3), weight=1)
        self.rowconfigure((1, 2), weight=2)

        # Timestamp label
        self.lblTimestamps = ctk.CTkLabel(self, text="Timestamps")
        self.lblTimestamps.grid(row=0, column=0, columnspan=2, sticky="w", padx=8)

        # ----- Begin Part ----- #
        # Begin label
        self.lblBegin = ctk.CTkLabel(self, text="Begin")
        self.lblBegin.grid(row=1, column=2)

        # Begin calendar
        self.cldrBegin = Calendar(self, showweeknumbers=False, locale='fr_FR')
        self.cldrBegin.grid(row=2, column=0, columnspan=5)

        # Begin time spinboxes
        self.spbBeginHour = tk.Spinbox(self, from_=0, to=23, width=10)
        self.spbBeginHour.grid(row=3, column=0)

        self.lblSemicolon1 = ctk.CTkLabel(self, text=":")
        self.lblSemicolon1.grid(row=3, column=1)

        self.spbBeginMinute = tk.Spinbox(self, from_=0, to=59, width=10)
        self.spbBeginMinute.grid(row=3, column=2)

        self.lblSemicolon2 = ctk.CTkLabel(self, text=":")
        self.lblSemicolon2.grid(row=3, column=3)

        self.spbBeginSecond = tk.Spinbox(self, from_=0, to=59, width=10)
        self.spbBeginSecond.grid(row=3, column=4)

        # ----- Separator Bar ----- #
        self.frmSeparator = ctk.CTkFrame(self, width=2, fg_color="gray20")
        self.frmSeparator.grid(row=1, column=5, rowspan=3, sticky="ns")

        # ----- End Part ----- #
        # End label
        self.lblEnd = ctk.CTkLabel(self, text="End")
        self.lblEnd.grid(row=1, column=8)

        # End calendar
        self.cldrEnd = Calendar(self, showweeknumbers=False, locale='fr_FR')
        self.cldrEnd.grid(row=2, column=6, columnspan=5)

        # End time spinboxes
        self.spbEndHour = tk.Spinbox(self, from_=0, to=23, width=10)
        self.spbEndHour.grid(row=3, column=6)

        self.lblSemicolon3 = ctk.CTkLabel(self, text=":")
        self.lblSemicolon3.grid(row=3, column=7)

        self.spbEndMinute = tk.Spinbox(self, from_=0, to=59, width=10)
        self.spbEndMinute.grid(row=3, column=8)

        self.lblSemicolon4 = ctk.CTkLabel(self, text=":")
        self.lblSemicolon4.grid(row=3, column=9)

        self.spbEndSecond = tk.Spinbox(self, from_=0, to=59, width=10)
        self.spbEndSecond.grid(row=3, column=10)