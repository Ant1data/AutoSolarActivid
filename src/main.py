import os
import tkinter as tk
import customtkinter as ctk

from datetime import date
from PIL import Image
from tkcalendar import Calendar


## <a href="https://www.flaticon.com/fr/icones-gratuites/analytique" title="analytique icônes">Analytique icônes créées par Arafat Uddin - Flaticon</a> ##

# Path to app/img folder, in order to get image files 
img_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")

# Appearance settings
ctk.set_appearance_mode("System")  # Light/Dark mode
ctk.set_default_color_theme("blue")  # Default color

# Generating our main window
frmMain = ctk.CTk()
frmMain.geometry("640x480")  # Defining frame geometry
frmMain.title("Cosmic On Air")

 
## VIEW ELEMENTS ----------------------------------------------------------------------------------------------------------- ##
# ----- Title Bar ----- #
frmTitleBar = ctk.CTkFrame(frmMain)
frmTitleBar.pack(anchor="center", fill="x")

# Title Label
lblTitle = ctk.CTkLabel(frmTitleBar, text="COSMIC ON AIR | Video Generator", font=ctk.CTkFont(size=20, weight="bold"))
lblTitle.pack(pady=10)


# ----- Video Type Frame ----- #
frmVideoType = ctk.CTkFrame(frmMain)

# Configuring grid layout for this frame
frmVideoType.columnconfigure((0,1), weight=1)
frmVideoType.rowconfigure(0, weight=1)
frmVideoType.rowconfigure(1, weight=3)
frmVideoType.pack(anchor="center", fill="x", pady=10)

# Video Type Label
lblVideoType = ctk.CTkLabel(frmVideoType, text="Video type")
lblVideoType.grid(row=0, column=0, sticky="w", padx=8)

# Proton Flux Graph Button
icnGraph = ctk.CTkImage(Image.open(os.path.join(img_folder_path, "graph.png"))) # Defining icon
btnProtonFluxGraph = ctk.CTkButton(frmVideoType, text="Proton flux graph", image=icnGraph, compound="top", cursor="hand2")
btnProtonFluxGraph.grid(row=1, column=0, sticky="e", padx=8)

# Solar Activity Video Button
icnSun = ctk.CTkImage(Image.open(os.path.join(img_folder_path, "sun.png"))) # Defining icon
btnSolarActivityVideo = ctk.CTkButton(frmVideoType, text="Solar activity video", image=icnSun, compound="top", cursor="hand2")
btnSolarActivityVideo.grid(row=1, column=1, sticky="w", padx=8)


# ----- Timestamps Frame ----- #
frmTimestamps = ctk.CTkFrame(frmMain)

# Configuring grid layout for Timestamps frame
frmTimestamps.columnconfigure((0,2), weight=4)
frmTimestamps.columnconfigure(1, weight=1)
frmTimestamps.rowconfigure((0,1), weight=1)
frmTimestamps.rowconfigure(2, weight=3)
frmTimestamps.pack(anchor="center", fill="x", pady=10)

# Timestamp label
lblTimestamps = ctk.CTkLabel(frmTimestamps, text="Timestamps")
lblTimestamps.grid(row=0, column=0, sticky="w", padx=8)

# Begin label
lblBegin = ctk.CTkLabel(frmTimestamps, text="Begin")
lblBegin.grid(row=1, column=0)

# End label
lblEnd = ctk.CTkLabel(frmTimestamps, text="End")
lblEnd.grid(row=1, column=2)


# --- Begin Frame --- #


# Configuring grid layout for Begin frame
# frmBegin.columnconfigure((0,2,4), weight=2)
# frmBegin.columnconfigure((1,3), weight=1)
# frmBegin.rowconfigure((0,2), weight=1)
# frmBegin.rowconfigure(1, weight=2)
# frmBegin.grid(row=1, column=0, sticky="e", padx=8) # On the Timestamp grid

# # Begin label

# cldrBegin = Calendar(frmBegin, cursor="hand2")
# cldrBegin.grid(row=1, column=2)




# Running app
frmMain.mainloop()
