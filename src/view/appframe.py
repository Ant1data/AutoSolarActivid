import os
import tkinter as tk
import customtkinter as ctk

from datetime import date
from PIL import Image
from view.timestampframe import TimestampFrame

# Path to app/img folder, in order to get image files 
IMG_FOLDER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "img") # We take the directory name of the parent directory where this file is located + img directory

class AppFrame(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ## VIEW ELEMENTS ----------------------------------------------------------------------------------------------------------- ##
        # ----- Title Bar ----- #
        self.frmTitleBar = ctk.CTkFrame(self)
        self.frmTitleBar.pack(anchor="center", fill="x")

        # Title Label
        self.lblTitle = ctk.CTkLabel(self.frmTitleBar, text="COSMIC ON AIR | Video Generator", font=ctk.CTkFont(size=20, weight="bold"))
        self.lblTitle.pack(pady=10)


        # ----- Video Type Frame ----- #
        self.frmVideoType = ctk.CTkFrame(self)

        # Configuring grid layout for this frame
        self.frmVideoType.columnconfigure((0,1), weight=1)
        self.frmVideoType.rowconfigure(0, weight=1)
        self.frmVideoType.rowconfigure(1, weight=3)
        self.frmVideoType.pack(anchor="center", fill="x", pady=10)

        # Video Type Label
        self.lblVideoType = ctk.CTkLabel(self.frmVideoType, text="Video type")
        self.lblVideoType.grid(row=0, column=0, sticky="w", padx=8)

        # Proton Flux Graph Button
        self.icnGraph = ctk.CTkImage(Image.open(os.path.join(IMG_FOLDER_PATH, "graph.png"))) # Defining icon
        self.btnProtonFluxGraph = ctk.CTkButton(self.frmVideoType, text="Proton flux graph", image=self.icnGraph, compound="top", cursor="hand2")
        self.btnProtonFluxGraph.grid(row=1, column=0, sticky="e", padx=8)

        # Solar Activity Video Button
        self.icnSun = ctk.CTkImage(Image.open(os.path.join(IMG_FOLDER_PATH, "sun.png"))) # Defining icon
        self.btnSolarActivityVideo = ctk.CTkButton(self.frmVideoType, text="Solar activity video", image=self.icnSun, compound="top", cursor="hand2")
        self.btnSolarActivityVideo.grid(row=1, column=1, sticky="w", padx=8)


        # ----- Timestamps Frame ----- #
        self.frmTimestamps = ctk.CTkFrame(self)

        # Configuring grid layout for Timestamps frame
        self.frmTimestamps.columnconfigure((0,2), weight=4)
        self.frmTimestamps.columnconfigure(1, weight=1)
        self.frmTimestamps.rowconfigure((0,1), weight=1)
        self.frmTimestamps.rowconfigure(2, weight=3)
        self.frmTimestamps.pack(anchor="center", fill="x", pady=10)

        # Timestamp label
        self.lblTimestamps = ctk.CTkLabel(self.frmTimestamps, text="Timestamps")
        self.lblTimestamps.grid(row=0, column=0, sticky="w", padx=8)

        # Begin label
        self.lblBegin = ctk.CTkLabel(self.frmTimestamps, text="Begin")
        self.lblBegin.grid(row=1, column=0)

        # End label
        self.lblEnd = ctk.CTkLabel(self.frmTimestamps, text="End")
        self.lblEnd.grid(row=1, column=2)


        # --- Begin TimestampFrame --- #
        self.tsfBegin = TimestampFrame(self.frmTimestamps)
        self.tsfBegin.grid(row=2, column=0) 

        # --- End TimestampFrame --- #
        self.tsfEnd = TimestampFrame(self.frmTimestamps)
        self.tsfEnd.grid(row=2, column=2)


        # ----- Energy Frame ----- #
        self.frmEnergy = ctk.CTkFrame(self)
        self.frmEnergy.pack(anchor="center", fill="x", pady=10)

        # Energy label
        self.lblEnergy = ctk.CTkLabel(self.frmEnergy, text="Energy")
        self.lblEnergy.pack(padx=8, anchor="w")

        # Proton Flux CheckBox
        self.chbProtonFlux = ctk.CTkCheckBox(self.frmEnergy, text="Proton Flux", border_width=1, checkbox_height=18, checkbox_width=18, command=self.switch_states_proton_subcheckboxes)
        self.chbProtonFlux.pack(anchor="w", padx=8)

        # Sub-Checkboxes for energy selection
        self.chb100MeV = ctk.CTkCheckBox(self.frmEnergy, text="< 100 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED)
        self.chb100MeV.pack(anchor="w", padx=16)
        self.chb200MeV = ctk.CTkCheckBox(self.frmEnergy, text="< 200 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED)
        self.chb200MeV.pack(anchor="w", padx=16)
        self.chb500MeV = ctk.CTkCheckBox(self.frmEnergy, text="< 500 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED)
        self.chb500MeV.pack(anchor="w", padx=16)

        # Neutron Flux CheckBox
        self.chbNeutronFlux = ctk.CTkCheckBox(self.frmEnergy, text="Neutron Flux", border_width=1, checkbox_height=18, checkbox_width=18)
        self.chbNeutronFlux.pack(anchor="w", padx=8)


    ## This function, triggered by self.chbProtonFlux, changes sub-checkboxes' states
    ## If self.chbProtonFlux is on, they become enabled,
    ## Otherwise, they become disabled
    def switch_states_proton_subcheckboxes(self):
        # Enabled
        if self.chbProtonFlux.get() == 1:
            self.chb100MeV.configure(state="enabled")
            self.chb200MeV.configure(state="enabled")
            self.chb500MeV.configure(state="enabled")
        # Disabled
        else:
            self.chb100MeV.configure(state="disabled")
            self.chb200MeV.configure(state="disabled")
            self.chb500MeV.configure(state="disabled")
        print(self.chbProtonFlux.get())