import os
import tkinter as tk
import customtkinter as ctk

from datetime import datetime, time
from tkcalendar import Calendar

class TimestampFrame(ctk.CTkFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root # Defining tkinter root container

        # Grid configuration
        self.columnconfigure((0,2,4), weight=3)
        self.columnconfigure((1,3), weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        ## ----- Adding GUI elements ----- ##
        # --- Date picker --- #
        self.cldrDatepicker = Calendar(self, showweeknumbers=False, locale='fr_FR') # TODO : put correct arguments inside
        self.cldrDatepicker.grid(row=0, column=0, columnspan=5)
    
        # --- Time ComboBoxes --- #
        # Generating values for comboboxes
        hours_values = [f"{i:02d}" for i in range(24)]
        minutes_seconds_values = [f"{i:02d}" for i in range(60)] 

        # Getting current time for instance
        current_time = datetime.today()

        current_hour = current_time.strftime("%H")
        current_minute = current_time.strftime("%M")
        current_second = current_time.strftime("%S")

        # Generating comboboxes and semicolon labels
        self.cbxHour_var = ctk.StringVar(value=current_hour) # Setting cbxHour variable, in order to get its value later
        self.cbxHour = ctk.CTkComboBox(self, values=hours_values, variable=self.cbxHour_var)
        self.cbxHour.grid(row=1, column=0)

        self.lblSemicolon1 = ctk.CTkLabel(self, text=":")
        self.lblSemicolon1.grid(row=1, column=1)

        self.cbxMinute_var = ctk.StringVar(value=current_minute) # Setting cbxMinute variable, in order to get its value later
        self.cbxMinute = ctk.CTkComboBox(self, values=minutes_seconds_values, variable=self.cbxMinute_var)
        self.cbxMinute.grid(row=1, column=2)

        self.lblSemicolon2 = ctk.CTkLabel(self, text=":")
        self.lblSemicolon2.grid(row=1, column=3)

        self.cbxSecond_var = ctk.StringVar(value=current_second) # Setting cbxSecond variable, in order to get its value later
        self.cbxSecond = ctk.CTkComboBox(self, values=minutes_seconds_values, variable=self.cbxSecond_var)
        self.cbxSecond.grid(row=1, column=4)



