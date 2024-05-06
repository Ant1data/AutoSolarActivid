import tkinter as tk

import customtkinter as ctk

# Appearance settings
ctk.set_appearance_mode("System")  # Light/Dark mode
ctk.set_default_color_theme("blue")  # Default color

# Generating our frame
main_frame = ctk.CTk()
main_frame.geometry("640x480")  # Defining frame geometry
main_frame.title("Cosmic On Air")

# Running app
main_frame.mainloop()
