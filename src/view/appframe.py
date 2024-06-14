import os
import tkinter as tk
import customtkinter as ctk

from datetime import date
from PIL import Image
from view.energyframe import EnergyFrame
from view.titlebar import TitleBar
from view.timestampframe import TimestampFrame
from view.videotypeframe import VideoTypeFrame

# Path to app/img folder, in order to get image files 
IMG_FOLDER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "img") # We take the directory name of the parent directory where this file is located + img directory

class AppFrame(ctk.CTkScrollableFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # ----- Title Bar ----- #
        self.frmTitleBar = TitleBar(self, corner_radius=0)
        self.frmTitleBar.pack(anchor="center", fill="x")


        # ----- Video Type Frame ----- #
        self.frmVideoType = VideoTypeFrame(self)
        self.frmVideoType.pack(anchor="center", fill="x", pady=10)


        # ----- Timestamps Frame ----- #
        self.frmTimestamps = TimestampFrame(self)
        self.frmTimestamps.pack(anchor="center", fill="x", pady=10)


        # ----- Energy Frame ----- #
        self.frmEnergy = EnergyFrame(self)
        self.frmEnergy.pack(anchor="center", fill="x", pady=10)

        # # Energy label
        # self.lblEnergy = ctk.CTkLabel(self.frmEnergy, text="Energy")
        # self.lblEnergy.pack(padx=8, anchor="w")

        # # Proton Flux CheckBox
        # self.chbProtonFlux = ctk.CTkCheckBox(self.frmEnergy, text="Proton Flux", border_width=1, checkbox_height=18, checkbox_width=18, command=self.switch_states_proton_subcheckboxes)
        # self.chbProtonFlux.pack(anchor="w", padx=8)

        # # Sub-Checkboxes for energy selection
        # self.chb100MeV = ctk.CTkCheckBox(self.frmEnergy, text="< 100 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED)
        # self.chb100MeV.pack(anchor="w", padx=16)
        # self.chb200MeV = ctk.CTkCheckBox(self.frmEnergy, text="< 200 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED)
        # self.chb200MeV.pack(anchor="w", padx=16)
        # self.chb500MeV = ctk.CTkCheckBox(self.frmEnergy, text="< 500 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED)
        # self.chb500MeV.pack(anchor="w", padx=16)

        # # Neutron Flux CheckBox
        # self.chbNeutronFlux = ctk.CTkCheckBox(self.frmEnergy, text="Neutron Flux", border_width=1, checkbox_height=18, checkbox_width=18)
        # self.chbNeutronFlux.pack(anchor="w", padx=8)


        # ----- Comment Frame ----- #
        self.frmComment = ctk.CTkFrame(self)
        self.frmComment.columnconfigure(0, weight=1)
        self.frmComment.rowconfigure(0, weight=1)
        self.frmComment.rowconfigure(1, weight=2)
        self.frmComment.pack(anchor="center", fill="x", pady=10)

        # Comment label
        self.lblComment = ctk.CTkLabel(self.frmComment, text="Comment")
        self.lblComment.grid(row=0, column=0, sticky="w", padx=8)

        # Comment textbox
        self.tbxComment = ctk.CTkTextbox(self.frmComment)
        self.tbxComment.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)


        # ----- Generate Button ----- #
        self.btnGenerate = ctk.CTkButton(self, text="Generate")
        self.btnGenerate.pack(anchor="center", pady=10)
    ## --------------------------------------------------------------------------------------------------------------------- ##


    ## METHODS ------------------------------------------------------------------------------------------------------------- ##

    # ## This function, triggered by self.chbProtonFlux, changes sub-checkboxes' states
    # ## If self.chbProtonFlux is on, they become enabled,
    # ## Otherwise, they become disabled
    # def switch_states_proton_subcheckboxes(self):
    #     # Enabled
    #     if self.chbProtonFlux.get() == 1:
    #         self.chb100MeV.configure(state=tk.NORMAL)
    #         self.chb200MeV.configure(state=tk.NORMAL)
    #         self.chb500MeV.configure(state=tk.NORMAL)
    #     # Disabled
    #     else:
    #         self.chb100MeV.configure(state=tk.DISABLED)
    #         self.chb200MeV.configure(state=tk.DISABLED)
    #         self.chb500MeV.configure(state=tk.DISABLED)

    
    # ## This function, triggered by a VideoTypeButton, sets the boolean value
    # ## for button selection on the dctSelection dictionary
    # def selectVideoTypeButton(self, idVideoTypeButton):

    #     # We check every key, which corresponds to a VideoTypeButton
    #     for key in self.dctSelection.keys():

    #         # If the current key equals to the calling VideoTypeButton
    #         if key == idVideoTypeButton:
    #             self.dctSelection[key] = True
    #         else:
    #             self.dctSelection[key] = False

    #     # We update every button's color
    #     self.updateVideoTypeButtons() 
        

    # ## This function updates every VideoTypeButton,
    # ## according to dctSelection
    # def updateVideoTypeButtons(self):

    #     # We browse every couple VideoTypeButton/Boolean element in the dictionary
    #     for key, value in self.dctSelection.items():

    #         # If the button is selected
    #         if value == True:
    #             key.select()                

    #         # If not
    #         else:
    #             key.deselect()

                
