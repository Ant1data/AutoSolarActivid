import customtkinter as ctk
import cv2
import numpy as np
import os

from PIL import Image
from view.appframe import AppFrame

## CONSTANTS --------------------------------------------------------------------------------------------------------- ##

# Screen resolutions for videos
RESOLUTION_HORIZONTAL_MED = (1280, 720)
RESOLUTION_VERTICAL_MED = (720, 1280)
RESOLUTION_HORIZONTAL_HIGH = (1920, 1080)
RESOLUTION_VERTICAL_HIGH = (1080, 1920)

# Comment block height
COMMENT_BLOCK_HEIGHT = 60

## ------------------------------------------------------------------------------------------------------------------- ##


class AppHandler():

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self):

        # Appearance settings
        ctk.set_appearance_mode("System")  # Light/Dark mode
        ctk.set_default_color_theme("blue")  # Default color
        
        # Creating main window
        self.main_window = ctk.CTk()
        self.main_window.geometry("800x600")
        self.main_window.minsize(500, 375)
        self.main_window.title("SolarActivid")

        # Creating the main AppFrame
        self.frmApp = AppFrame(apphandler=self, master=self.main_window, width=1200, height=1400, fg_color=("white", "gray5"))
        self.frmApp.pack()

        # Launching app
        self.main_window.mainloop()
    ## --------------------------------------------------------------------------------------------------------------------- ##

    
    ## METHODS ------------------------------------------------------------------------------------------------------------- ##
    # Function to treat the user's request,
    # triggered by the "Generate" button
    def treatUserRequest(self, userRequest: dict[str, any]):
        
        # ----- Video format and quality ----- #
        video_width, video_height = 0, 0

        # Vertical image
        if userRequest["Format"] == "Instagram (vertical)":
            
            # Medium resolution
            if userRequest["Quality"] == "Medium (720p)":
                
                video_width, video_height = RESOLUTION_VERTICAL_MED
            
            # High resolution
            elif userRequest["Quality"] == "High (1080p)":
                
                video_width, video_height = RESOLUTION_VERTICAL_HIGH

        # Horizontal image
        elif userRequest["Format"] == "YouTube (horizontal)":
            
            # Medium resolution
            if userRequest["Quality"] == "Medium (720p)":
                
                video_width, video_height = RESOLUTION_HORIZONTAL_MED
            
            # High resolution
            elif userRequest["Quality"] == "High (1080p)":
                
                video_width, video_height = RESOLUTION_HORIZONTAL_HIGH

        # ------------------------------------ #


        # ----- Image types resolution ----- #

        # Resolution for solar activity (video's by default)
        solar_activity_width, solar_activity_height = video_width, video_height

        # Resolution for particle graphs (video's by default)
        particle_graph_width, particle_graph_height = video_width, video_height


        # Case for both images selected
        if userRequest["btnSolarActivityVideo"] and userRequest["btnParticleFluxGraph"]:
            
            # -------------- For vertical video -------------- #
            if userRequest["Format"] == "Instagram (vertical)":

                # Dividing image height by 2
                solar_activity_height = solar_activity_height/2
                particle_graph_height = particle_graph_height/2

                # When a comment is written, it will be
                # displayed on the middle, between the 
                # solar activity and particle graph images
                if userRequest["Comment"] != "\n":

                    solar_activity_height -= COMMENT_BLOCK_HEIGHT/2
                    particle_graph_height -= COMMENT_BLOCK_HEIGHT/2
            
            # -------------- For horizontal video -------------- #
            elif userRequest["Format"] == "YouTube (horizontal)":

                # Dividing image width by 2
                solar_activity_width = solar_activity_width/2
                particle_graph_width = particle_graph_width/2

                # When a comment is written, it will be
                # displayed on the middle, between the 
                # solar activity and particle graph images
                if userRequest["Comment"] != "\n":

                    solar_activity_height -= COMMENT_BLOCK_HEIGHT/2
                    particle_graph_height -= COMMENT_BLOCK_HEIGHT/2
                    
                    


        

    

# ----- Video generation algorithm ----- #
def generate_video(frame_list, video_name):

    # Changing working directory to the output folder
    os.chdir('output')

    # Configuring video writer
    output_video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 25, (1280, 720))

    counter = 1
    for one_frame in frame_list:

        # Saving plot as a PIL image
        current_plot_pil = Image.open(one_frame)
        
        # Converting PIL image to OpenCV format
        current_plot_cv = np.array(current_plot_pil)
        current_plot_cv = cv2.cvtColor(current_plot_cv, cv2.COLOR_RGB2BGR) # Configuring color

        # Adding frame on the video
        output_video.write(current_plot_cv)

        # For debug
        print(f'Image {counter} written')
        counter += 1

    # Exporting video
    cv2.destroyAllWindows()
    output_video.release()
    print("Video findable on " + os.getcwd() + "/" + video_name)
    os.chdir('../')
# -------------------------------------- #
    

