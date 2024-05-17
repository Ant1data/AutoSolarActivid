import customtkinter as ctk

from appframe import AppFrame

# Appearance settings
ctk.set_appearance_mode("System")  # Light/Dark mode
ctk.set_default_color_theme("blue")  # Default color

# Creating app frame
main_app = AppFrame()
main_app.geometry("720x640")
main_app.title("Cosmic On Air")

# Lauching app
main_app.mainloop()