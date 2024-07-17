import os
import tkinter as tk
import customtkinter as ctk

from datetime import date, datetime
from PIL import Image

from controller.controllerdata import ControllerData
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
        self.frmParticleFluxOptions = ctk.CTkFrame(self, corner_radius=10, fg_color=("#c4d2ff","#272A33"))

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
        self.btnGenerate = ctk.CTkButton(self, text="Generate", command=self.btnGenerateClicked)
        self.btnGenerate.pack(anchor="center", pady=10)

        
        # ----- Initializing dataController ----- #
        self.dataController = ControllerData(self) # Giving itself as frmApp

    ## --------------------------------------------------------------------------------------------------------------------- ##

    ## METHODS ------------------------------------------------------------------------------------------------------------- ##
    
    ## This function, triggered by the Particle Flux Graph button,
    ## makes the ParticleFluxOptionsFrame appear if the button is
    ## selected, and make disappear otherwise
    def toggle_ParticleFluxOptionsFrame(self, button_is_selected):
        if button_is_selected:
            # We put back the frame on the interface, before the Comment Frame
            self.frmParticleFluxOptions.pack(before=self.frmComment, anchor="center", fill="x")
        
        else:
            # We remove the Frame from the interface, without destroying it
            self.frmParticleFluxOptions.pack_forget()

    ## This function, triggered by a click on btnGenerate, 
    ## makes a dictionary of what the user selected in the frame
    ## and gives to dataController, in order to make a query
    def btnGenerateClicked(self):
        
        # Initializing user_request dictionary
        user_request = {}

        # Getting selected video type buttons
        user_request.update(self.frmVideoType.dctSelection)

        # Getting Particle Flux Graph options if this type is selected
        if user_request["btnParticleFluxGraph"] == True:

            # ----- Timestamps data ----- #

            # Begin date
            user_request["BeginDate"] = self.frmTimestamps.cldrBegin.selection_get()

            # Begin time 
            hour = self.frmTimestamps.spbBeginHour.get()
            minute = self.frmTimestamps.spbBeginMinute.get()
            second = self.frmTimestamps.spbBeginSecond.get()
            time = f'{hour}:{minute}:{second}' # Gathering values into a string
            user_request["BeginTime"] = datetime.strptime(time, "%H:%M:%S") # Converting time string into datetime format
            
            # End date
            user_request["EndDate"] = self.frmTimestamps.cldrEnd.selection_get()

            # End time 
            hour = self.frmTimestamps.spbEndHour.get()
            minute = self.frmTimestamps.spbEndMinute.get()
            second = self.frmTimestamps.spbEndSecond.get()
            time = f'{hour}:{minute}:{second}' # Gathering values into a string
            user_request["EndTime"] = datetime.strptime(time, "%H:%M:%S") # Converting time string into datetime format

            # ----- Energy data ----- #

            # Building an inner dictionary for energy data
            user_request["EnergyData"] = dict()

            # Proton Flux
            user_request["EnergyData"]["ProtonFlux"] = self.frmEnergy.chbProtonFluxValue.get()

            # If Proton Flux is selected, we get the energy booleans and store them in a dictionary
            if user_request["EnergyData"]["ProtonFlux"] == True:
                user_request["EnergyData"]["Energies"] = dict()
                user_request["EnergyData"]["Energies"]["10Mev"] = self.frmEnergy.chb10MeVValue.get()
                user_request["EnergyData"]["Energies"]["50Mev"] = self.frmEnergy.chb50MeVValue.get()
                user_request["EnergyData"]["Energies"]["100Mev"] = self.frmEnergy.chb100MeVValue.get()
                user_request["EnergyData"]["Energies"]["500Mev"] = self.frmEnergy.chb500MeVValue.get()

            # Neutron Flux
            user_request["EnergyData"]["NeutronFlux"] = self.frmEnergy.chbNeutronFluxValue.get()
        
        # Getting comment
        user_request["Comment"] = self.frmComment.tbxComment.get("0.0", "end")

        # Passing the user request to the data controller
        self.dataController.btnGenerateClicked(user_request=user_request)

        
