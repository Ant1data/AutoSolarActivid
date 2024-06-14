import os
import tkinter as tk
import customtkinter as ctk

from datetime import date
from PIL import Image
from view.commentframe import CommentFrame
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

        # --- Title Bar --- #
        self.frmTitleBar = TitleBar(self, corner_radius=0)
        self.frmTitleBar.pack(anchor="center", fill="x")


        # --- Video Type Frame --- #
        self.frmVideoType = VideoTypeFrame(self)
        self.frmVideoType.pack(anchor="center", fill="x", pady=10)

        # ----- ParticleFluxOptionsFrame ----- #
        self.frmParticleFluxOptions = ctk.CTkFrame(self)

        # Particle Flux Options Label
        self.lblParticleFluxOptions = ctk.CTkLabel(self.frmParticleFluxOptions, text="Particle Flux Options", text_color="#3A7EBF", font=ctk.CTkFont(size=16, weight="bold"))
        self.lblParticleFluxOptions.pack(anchor="center", fill="x")

        ## Frames inside ParticleFluxOptionsFrame ------------------------ ##
        # Timestamps Frame
        self.frmTimestamps = TimestampFrame(self.frmParticleFluxOptions)
        self.frmTimestamps.pack(anchor="center", fill="x", padx=10, pady=10)


        # Energy Frame
        self.frmEnergy = EnergyFrame(self.frmParticleFluxOptions)
        self.frmEnergy.pack(anchor="center", fill="x", padx=10, pady=10)
        ## ---------------------------------------------------------------- ##

        # --- Comment Frame --- #
        self.frmComment = CommentFrame(self)
        self.frmComment.pack(anchor="center", fill="x", pady=10)


        # ----- Generate Button ----- #
        self.btnGenerate = ctk.CTkButton(self, text="Generate")
        self.btnGenerate.pack(anchor="center", pady=10)

        self.frmEnergy
    ## --------------------------------------------------------------------------------------------------------------------- ##

    ## METHODS ------------------------------------------------------------------------------------------------------------- ##
    
    ## This function, triggered by the Particle Flux Graph button,
    ## makes the ParticleFluxOptionsFrame appear if the button is
    ## selected, and make disappear otherwise
    def toggle_ParticleFluxOptionsFrame(self, button_is_selected: bool):
        if button_is_selected:
            # We put back the frame on the interface, before the Comment Frame
            self.frmParticleFluxOptions.pack(before=self.frmComment, anchor="center", fill="x")
        
        else:
            # We remove the Frame from the interface, without destroying it
            self.frmParticleFluxOptions.pack_forget()