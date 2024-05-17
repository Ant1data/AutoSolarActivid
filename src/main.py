import os
import tkinter as tk
import customtkinter as ctk

from datetime import date
from PIL import Image
from timestampframe import TimestampFrame


## <a href="https://www.flaticon.com/fr/icones-gratuites/analytique" title="analytique icônes">Analytique icônes créées par Arafat Uddin - Flaticon</a> ##

# Path to app/img folder, in order to get image files 
img_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")

# Appearance settings
ctk.set_appearance_mode("System")  # Light/Dark mode
ctk.set_default_color_theme("blue")  # Default color

# Generating our main window
frmMain = ctk.CTk()
frmMain.geometry("720x640")  # Defining frame geometry
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


# --- Begin TimestampFrame --- #
tsfBegin = TimestampFrame(frmTimestamps)
tsfBegin.grid(row=2, column=0) 

# --- End TimestampFrame --- #
tsfEnd = TimestampFrame(frmTimestamps)
tsfEnd.grid(row=2, column=2)


# ----- Energy Frame ----- #
frmEnergy = ctk.CTkFrame(frmMain)
frmEnergy.pack(anchor="center", fill="x", pady=10)

# Energy label
lblEnergy = ctk.CTkLabel(frmEnergy, text="Energy")
lblEnergy.pack(padx=8, anchor="w")

# Proton Flux CheckBox
chbProtonFlux = ctk.CTkCheckBox(frmEnergy, text="Proton Flux", border_width=1, checkbox_height=18, checkbox_width=18)
chbProtonFlux.pack(anchor="w", padx=8)

# Sub-Checkboxes for energy selection
chb100MeV = ctk.CTkCheckBox(frmEnergy, text="< 100 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED)
chb100MeV.pack(anchor="w", padx=16)
chb200MeV = ctk.CTkCheckBox(frmEnergy, text="< 200 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED)
chb200MeV.pack(anchor="w", padx=16)
chb500MeV = ctk.CTkCheckBox(frmEnergy, text="< 500 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED)
chb500MeV.pack(anchor="w", padx=16)

# Neutron Flux CheckBox
chbNeutronFlux = ctk.CTkCheckBox(frmEnergy, text="Neutron Flux", border_width=1, checkbox_height=18, checkbox_width=18)
chbNeutronFlux.pack(anchor="w", padx=8)

# Running app
frmMain.mainloop()