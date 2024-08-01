import os
import tkinter as tk
import customtkinter as ctk

from datetime import date, datetime
from PIL import Image

from view.commentframe import CommentFrame
from view.energyframe import EnergyFrame
from view.folderpathsframe import FolderPathsFrame
from view.formatqualityframe import FormatQualityFrame
from view.titlebar import TitleBar
from view.timestampframe import TimestampFrame
from view.videotypeframe import VideoTypeFrame

# Path to app/img folder, in order to get image files 
IMG_FOLDER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "img") # We take the directory name of the parent directory where this file is located + img directory

class AppFrame(ctk.CTkScrollableFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, apphandler, master, **kwargs):
        super().__init__(master, **kwargs)

        # Saving AppHandler handling this frame
        self.apphandler = apphandler

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

        ## Frame inside ParticleFluxOptionsFrame ------------------------ ##
        # Energy Frame
        self.frmEnergy = EnergyFrame(self.frmParticleFluxOptions)
        self.frmEnergy.pack(anchor="center", fill="x", padx=10, pady=10)
        ## ---------------------------------------------------------------- ##


        # --- Timestamp Frame --- #
        self.frmTimestamps = TimestampFrame(self)
        self.frmTimestamps.pack(anchor="center", fill="x", pady=10)
        

        # Creating a frame to put frmFormatQuality and frmFolderPaths side to side
        # --- FormatQualityFolder Frame --- #
        self.frmFormatQualityFolder = ctk.CTkFrame(self, fg_color=("#FFFFFF", "#000000"))
        self.frmFormatQualityFolder.pack(anchor="center", fill="x", pady=10)

        # --- FormatQuality Frame --- #
        self.frmFormatQuality = FormatQualityFrame(self.frmFormatQualityFolder)
        self.frmFormatQuality.pack(side="left", fill='y')

        # --- Folder Paths Frame
        self.frmFolderPaths = FolderPathsFrame(self.frmFormatQualityFolder)
        self.frmFolderPaths.pack(side="right", fill='y')


        # --- Comment Frame --- #
        self.frmComment = CommentFrame(self)
        self.frmComment.pack(anchor="center", fill="x", pady=10)


        # ----- Generate Button ----- #
        self.btnGenerate = ctk.CTkButton(self, text="Generate", command=self.btnGenerateClicked)
        self.btnGenerate.pack(anchor="center", pady=10)

    ## --------------------------------------------------------------------------------------------------------------------- ##


    ## METHODS ------------------------------------------------------------------------------------------------------------- ##
    
    ## This function, triggered by the Particle Flux Graph button,
    ## makes the ParticleFluxOptionsFrame appear if the button is
    ## selected, and make disappear otherwise
    def toggle_ParticleFluxOptionsFrame(self, button_is_selected):
        if button_is_selected:
            # We put back the frame on the interface, before the Comment Frame
            self.frmParticleFluxOptions.pack(before=self.frmTimestamps, anchor="center", fill="x")
        
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


        # ----- Timestamps data ----- #
        # --- Begin --- #
        # Begin date
        begin_date = self.frmTimestamps.cldrBegin.selection_get()

        # Begin time 
        hour = self.frmTimestamps.spbBeginHour.get()
        minute = self.frmTimestamps.spbBeginMinute.get()
        second = self.frmTimestamps.spbBeginSecond.get()
        time = f'{hour}:{minute}:{second}' # Gathering values into a string
        begin_time = datetime.strptime(time, "%H:%M:%S").time() # Converting time string into datetime format

        # Combining date and time
        user_request["BeginDatetime"] = datetime.combine(begin_date, begin_time)
        
        # --- End --- #
        # End date
        end_date = self.frmTimestamps.cldrEnd.selection_get()

        # End time 
        hour = self.frmTimestamps.spbEndHour.get()
        minute = self.frmTimestamps.spbEndMinute.get()
        second = self.frmTimestamps.spbEndSecond.get()
        time = f'{hour}:{minute}:{second}' # Gathering values into a string
        end_time = datetime.strptime(time, "%H:%M:%S").time() # Converting time string into datetime format

        # Combining date and time
        user_request["EndDatetime"] = datetime.combine(end_date, end_time)


        # ----- Format & Quality ----- #
        user_request["Format"] = self.frmFormatQuality.sgbFormatValue.get()
        user_request["Quality"] = self.frmFormatQuality.sgbQualityValue.get()


        # ----- Folder paths ----- #
        user_request["InputFolder"] = self.frmFolderPaths.entInputPathValue.get()
        user_request["OutputFolder"] = self.frmFolderPaths.entOutputPathValue.get()


        # ----- Energy data ----- #
        # Getting energy options if ParticleFluxGraph are selected
        if user_request["btnParticleFluxGraph"] == True:
            
            # Getting the user's choice in an inner dictionary
            user_request["EnergyData"] = self.frmEnergy.get_user_choice()
        
        # ----- Comment ----- #
        user_request["Comment"] = self.frmComment.tbxComment.get("0.0", "end")

        # Passing the user request to the data controller
        self.apphandler.treatUserRequest(userRequest=user_request)
    ## --------------------------------------------------------------------------------------------------------------------- ##

        
