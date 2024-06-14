import customtkinter as ctk
import tkinter as tk

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

        # Launching app
        self.main_window.mainloop()