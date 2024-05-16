import os
import tkinter as tk
import customtkinter as ctk

from datetime import date
from tkcalendar import Calendar

class TimestampFrame(ctk.CTkFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root # Defining tkinter root container
        self.calendar = Calendar()
        
    # TODO : Create remaining elements