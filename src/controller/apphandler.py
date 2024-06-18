import customtkinter as ctk
import tkinter as tk

from controller.controllerdata import ControllerData
from view.appframe import AppFrame
from view.settingsframe import SettingsFrame

class AppHandler():

    def __init__(self):
        # Appearance settings
        ctk.set_appearance_mode("System")  # Light/Dark mode
        ctk.set_default_color_theme("blue")  # Default color
        
        # Creating main window
        self.main_window = ctk.CTk()
        self.main_window.geometry("800x800")
        self.main_window.minsize(500, 375)
        self.main_window.title("SolarActivid")

        # Creating the main AppFrame
        self.frmApp = AppFrame(self.main_window, width=1200, height=1400, fg_color="white")
        self.frmApp.pack()

        # Launching app
        self.main_window.mainloop()