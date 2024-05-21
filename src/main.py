import customtkinter as ctk
import time

from view.appframe import AppFrame

# Appearance settings
ctk.set_appearance_mode("System")  # Light/Dark mode
ctk.set_default_color_theme("blue")  # Default color

# Creating main
main_window = ctk.CTk()
main_window.geometry("800x800")
main_window.minsize(500, 375)
main_window.title("SolarActivid")

# Adding app frame on main window
app_frame = AppFrame(main_window, width=1200, height=1400, fg_color="white")
app_frame.pack()

# Lauching app
main_window.mainloop()