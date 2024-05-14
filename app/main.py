import os
import tkinter as tk
import customtkinter as ctk

from datetime import date
from PIL import Image
from tkcalendar import Calendar


## <a href="https://www.flaticon.com/fr/icones-gratuites/analytique" title="analytique icônes">Analytique icônes créées par Arafat Uddin - Flaticon</a> ##

# 
img_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")

# Appearance settings
ctk.set_appearance_mode("System")  # Light/Dark mode
ctk.set_default_color_theme("blue")  # Default color

# Generating our main window
frmMain = ctk.CTk()
frmMain.geometry("640x480")  # Defining frame geometry
frmMain.title("Cosmic On Air")

 
## ---------- VIEW ELEMENTS ---------- ##
# ----- Title Bar ----- #
frmTitleBar = ctk.CTkFrame(frmMain)
frmTitleBar.pack(anchor="center", fill="x")

lblTitle = ctk.CTkLabel(frmTitleBar, text="COSMIC ON AIR | Video Generator", font=ctk.CTkFont(size=20, weight="bold"))
lblTitle.pack(pady=10)


# ----- Video Type Frame ----- #
frmVideoType = ctk.CTkFrame(frmMain)
frmVideoType.pack(anchor="center", fill="x", pady=10)

lblVideoType = ctk.CTkLabel(frmVideoType, text="Video type")
lblVideoType.pack(padx=8, pady=8, anchor="w")

icnGraph = ctk.CTkImage(Image.open(os.path.join(img_folder_path, "graph.png")))

btnProtonFluxGraph = ctk.CTkButton(frmVideoType, text="Proton flux graph", image=icnGraph, compound="top")
btnProtonFluxGraph.pack(side="left", expand=True, fill=tk.X, padx=16, pady=8)

icnSun = ctk.CTkImage(Image.open(os.path.join(img_folder_path, "sun.png")))

btnSolarActivityVideo = ctk.CTkButton(frmVideoType, text="Solar activity video", image=icnSun, compound="top")
btnSolarActivityVideo.pack(side="left", expand=True, fill=tk.X, padx=16)


# ----- Timestamp Frame ----- #
frmTimestamp = ctk.CTkFrame(frmMain)
frmTimestamp.pack(anchor="center", fill="x", pady=10)


# Running app
frmMain.mainloop()
