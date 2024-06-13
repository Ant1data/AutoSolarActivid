import os
import customtkinter as ctk

from PIL import Image
from view.videotypebutton import VideoTypeButton

# Path to app/img folder, in order to get image files 
IMG_FOLDER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "img") # We take the directory name of the parent directory where this file is located + img directory


class VideoTypeFrame(ctk.CTkFrame):
    
    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Grid layout configuration
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)

        # Video Type Label
        self.lblVideoType = ctk.CTkLabel(self, text="Video type")
        self.lblVideoType.grid(row=0, column=0, sticky="w", padx=8)

        # Particle Flux Graph Button
        self.icnGraph = ctk.CTkImage(Image.open(os.path.join(IMG_FOLDER_PATH, "graph.png"))) # Defining icon
        self.btnParticleFluxGraph = VideoTypeButton(self, text="Particle flux graph", image=self.icnGraph, compound="top")
        self.btnParticleFluxGraph.configure(command=lambda b=self.btnParticleFluxGraph: self.VideoTypeButtonClicked(b)) # Setting up command with itself as parameter 
        self.btnParticleFluxGraph.grid(row=1, column=0, sticky="e", padx=8)

        # Solar Activity Video Button
        self.icnSun = ctk.CTkImage(Image.open(os.path.join(IMG_FOLDER_PATH, "sun.png"))) # Defining icon
        self.btnSolarActivityVideo = VideoTypeButton(self, fg_color=("orange"), text="Solar activity video", image=self.icnSun, compound="top")
        self.btnSolarActivityVideo.configure(command=lambda b=self.btnSolarActivityVideo: self.VideoTypeButtonClicked(b)) # Setting up command with itself as parameter 
        self.btnSolarActivityVideo.grid(row=1, column=1, sticky="w", padx=8)

        # Dictionary to define which button is selected
        self.dctSelection = {self.btnParticleFluxGraph : True, self.btnSolarActivityVideo : False}
        self.updateVideoTypeButtons() 
    ## --------------------------------------------------------------------------------------------------------------------- ##


    ## METHODS ------------------------------------------------------------------------------------------------------------- ##

    ## This function, triggered by a VideoTypeButton, sets the boolean value
    ## for button selection on the dctSelection dictionary
    ## The two buttons can be selected, but at least one must be selected
    def VideoTypeButtonClicked(self, buttonClicked):

        # Checking if the button clicked is the only one on True.
        # If so, we skip the deselection
        if self.dctSelection[buttonClicked] == True:
            only_one_selected = True

            for oneButton in self.dctSelection.keys():
                if oneButton != buttonClicked and self.dctSelection[buttonClicked] == True:
                    only_one_selected = False
            
            if not only_one_selected:
                self.dctSelection[buttonClicked] = False
        else:
            self.dctSelection[buttonClicked] = True

        # For debug
        print("ButtonClicked :", buttonClicked)
        print(self.dctSelection)

        # We update every button's color
        self.updateVideoTypeButtons()
    

    ## This function updates every VideoTypeButton,
    ## according to dctSelection
    def updateVideoTypeButtons(self):

        # We browse every couple VideoTypeButton/Boolean element in the dictionary
        for key, value in self.dctSelection.items():

            # If the button is selected
            if value == True:
                key.select()                

            # If not
            else:
                key.deselect()