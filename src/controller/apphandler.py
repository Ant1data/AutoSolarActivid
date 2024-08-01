import customtkinter as ctk
import cv2
import numpy as np
import os

from PIL import Image
from view.appframe import AppFrame

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
    # Function to treat the user's request, after 
    def treatUserRequest(self, userRequest: dict[str, any]):
        
        # Setting image format and 
        pass

    

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
    

