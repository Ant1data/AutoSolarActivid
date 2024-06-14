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

        # ----- Comment Frame ----- #
        self.frmComment = CommentFrame(self)
        self.frmComment.pack(anchor="center", fill="x", pady=10)

        # ----- Generate Button ----- #
        self.btnGenerate = ctk.CTkButton(self, text="Generate")
        self.btnGenerate.pack(anchor="center", pady=10)
    ## --------------------------------------------------------------------------------------------------------------------- ##

    ## METHODS ------------------------------------------------------------------------------------------------------------- ##