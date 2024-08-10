import customtkinter as ctk
import cv2
import io
import numpy as np
import os

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from model.particlefluxgraphimages import ParticleFluxGraphImages
from model.solaractivityimages import SolarActivityImages
from view.appframe import AppFrame


## CONSTANTS --------------------------------------------------------------------------------------------------------- ##
# Screen formats
HORIZONTAL = "h"
VERTICAL = "v"

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

        # For debug 
        print(userRequest)
        
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

        # Resolution for particle flux graphs (video's by default)
        particle_graph_width, particle_graph_height = video_width, video_height


        # Dividing the width/height by 2 when both videos are selected
        if userRequest["btnSolarActivityVideo"] and userRequest["btnParticleFluxGraph"]:
            
            # --------------- For vertical video --------------- #
            if userRequest["Format"] == "Instagram (vertical)":

                # Dividing image height by 2
                solar_activity_height = solar_activity_height/2
                particle_graph_height = particle_graph_height/2
            
            # -------------- For horizontal video -------------- #
            elif userRequest["Format"] == "YouTube (horizontal)":

                # Dividing image width by 2
                solar_activity_width = solar_activity_width/2
                particle_graph_width = particle_graph_width/2

            # -------------------------------------------------- #
        
        # Reducing the height of the resolutions when a comment is written,
        # in order to let space on the screen for the comment
        if len(userRequest["Comment"]) != 0:
            
            # Case for vertical video with the two types of videos
            if userRequest["Format"] == "Instagram (vertical)" and userRequest["btnSolarActivityVideo"] and userRequest["btnParticleFluxGraph"]:

                solar_activity_height -= COMMENT_BLOCK_HEIGHT/2
                particle_graph_height -= COMMENT_BLOCK_HEIGHT/2
            
            # Other cases
            else:
                solar_activity_height -= COMMENT_BLOCK_HEIGHT
                particle_graph_height -= COMMENT_BLOCK_HEIGHT
        
        # Converting the resolutions into ints
        video_width, video_height = int(video_width), int(video_height)
        solar_activity_width, solar_activity_height = int(solar_activity_width), int(solar_activity_height)
        particle_graph_width, particle_graph_height = int(particle_graph_width), int(particle_graph_height)

        # For debug : Displaying the resolutions
        print("Video resolution :", video_width, "x", video_height)
        print("Solar activity resolution :", solar_activity_width, "x", solar_activity_height)
        print("Particle flux graph resolution :", particle_graph_width, "x", particle_graph_height)

        # ---------------------------------- #


        # ----- Creating images objects ----- #

        # Getting common userRequest data
        begin_datetime = userRequest["BeginDatetime"]
        end_datetime = userRequest["EndDatetime"]
        input_folder = userRequest["InputFolder"]

        # Creating lists of images
        solar_activity_images = []
        particle_graph_images = []

        # Solar activity
        if userRequest["btnSolarActivityVideo"]:
            
            # Creating solar activity object
            solar_activity_object = SolarActivityImages(beginDateTime=begin_datetime, endDateTime=end_datetime, imageWidth=solar_activity_width, imageHeight=solar_activity_height, inputFolder=input_folder)

            # Gathering images
            solar_activity_images = solar_activity_object.images
        
        # Particle flux graph
        if userRequest["btnParticleFluxGraph"]:

            # Considering that there are always less solar activity
            # images than particle flux graph images, if the solar
            # activity option is selected, we set the number of solar
            # activity images as the minimum number of video's frames
            number_of_images = None

            if len(solar_activity_images) > 0:
                number_of_images = len(solar_activity_images)

            # Creating particle flux graph object
            particle_graph_object = ParticleFluxGraphImages(beginDateTime=begin_datetime, endDateTime=end_datetime, dctEnergy=userRequest["EnergyData"], imageWidth=particle_graph_width, imageHeight=particle_graph_height, numberOfImages=number_of_images, inputFolder=input_folder)

            # Gathering images
            particle_graph_images = particle_graph_object.images
        # ----------------------------------- #

        # ----- Combining different images (with comment) ----- #

        # Defining the video format (horizontal/vertical)
        format = ""

        if userRequest["Format"] == "Instagram (vertical)":
            format = HORIZONTAL
        elif userRequest["Format"] == "YouTube (horizontal)":
            format = VERTICAL

        # Combining the different kind of images, with the comment if necessary
        final_images = self.combine_images(solar_activity_images, particle_graph_images, video_width, video_height, format, userRequest["Comment"])
        # ----------------------------------------------------- #

        # ----- Defining video name ----- #
        video_name = "SolarActivid"

        # Adding selected video types
        if userRequest["btnSolarActivityVideo"]:
            video_name += "_SA"
        
        if userRequest["btnParticleFluxGraph"]:
            video_name += "_PFG"
        
        # Adding Begin Datetime
        video_name += datetime.strftime(userRequest["BeginDatetime"], "_%Y%m%d_%H%M%S")
        
        # Adding End Datetime
        video_name += datetime.strftime(userRequest["EndDatetime"], "_%Y%m%d_%H%M%S")
        
        # Adding .mp4
        video_name += ".mp4"

        # ------------------------------- #

        # ----- Exporting the video ----- #
        self.generate_video(final_images, video_name=video_name, video_width=video_width, video_height=video_height, output_folder=userRequest["OutputFolder"])
        # ------------------------------- #


        
    # ----- Image combination algorithm ----- #
    def combine_images(self, solar_activity_images : list, particles_graph_images : list, video_width : float, video_height : float, format : str, comment = ""):

        # List that will store the final images
        final_images = []

        # --- Creating comment block if it exists --- #
        comment_block = None

        if len(comment) > 0:

            # Creating a new image
            comment_block = Image.new(mode="RGBA", size=(video_width, COMMENT_BLOCK_HEIGHT), color="white")

            # Creating the text 
            text_draw = ImageDraw.Draw(comment_block)

            # Setting text font
            text_font = ImageFont.truetype('arial.ttf', 24)

            # Drawing the text on the image
            text_draw.text((20, 20), comment, font=text_font, fill="black")

        # ------------------------------------------- #

        # --- Getting the number of images --- #
        number_of_images = 0

        # When the solar activity images are the only one set
        if not particles_graph_images:
            number_of_images = len(solar_activity_images)

        # When the particle flux graph images are the only one set
        elif not solar_activity_images:
            number_of_images = len(particles_graph_images)

        # When both are set
        else:
            
            # Raising a ValueError when the number of images of both types are unequal
            if len(solar_activity_images) != len(particles_graph_images):
                raise ValueError("Internal Problem | The number of solar activity images and the number of particle flux images are unequal. SA = " + str(len(solar_activity_images)) + " and PFG = " + str(len(particles_graph_images)))

            number_of_images = len(solar_activity_images)
        # ------------------------------------ #

        # --- Getting image dimensions --- #
        solar_activity_width, solar_activity_height = 0, 0
        particles_graph_width, particles_graph_height = 0, 0
        comment_width, comment_height = 0, 0

        # We take the first image of both image types as a reference
    
        # Case for solar activity image
        if len(solar_activity_images) > 0:
            image_reference = Image.open(solar_activity_images[0])
            solar_activity_width = image_reference.width
            solar_activity_height = image_reference.height
        
        # Case for particle flux graph image
        if len(particles_graph_images) > 0:
            image_reference = Image.open(particles_graph_images[0])
            particles_graph_width = image_reference.width
            particles_graph_height = image_reference.height

        # Case for the comment
        if comment_block is not None:
            comment_width = comment_block.width
            comment_height = comment_block.height
        # -------------------------------- #


        # --- Combining images --- #

        # Vertical format
        if format == VERTICAL:

            # Browsing every image
            for image_index in range(number_of_images):
                
                # Creating new image
                new_image = Image.new('RGB', (video_height, video_width))

                # Case for solar activity image
                if len(solar_activity_images) > 0:

                    # Opening the image
                    sa_image = Image.open(solar_activity_images[image_index])
                    
                    # Adding this image to the new image, from the beginning
                    new_image.paste(sa_image, (0, 0))
                
                # Case for comment, if it is defined
                if comment_block is not None:
                    
                    # Adding the comment to the new image
                    new_image.paste(comment_block, (0, solar_activity_height))
                
                # Case for particle flux graph image
                if len(particles_graph_images) > 0:

                    # Opening the image
                    pfg_image = Image.open(particles_graph_images[image_index])
                    
                    # Adding this image to the new image, after the solar activity image 
                    new_image.paste(pfg_image, (0, solar_activity_height+comment_height))


                # Creating a pure binary variable to store the new image
                new_image_byte = io.BytesIO()

                # Saving the new image in a pure binary format
                new_image.save(new_image_byte, format='png')

                # Adding the new image to the list
                final_images.append(new_image_byte)
        

        # Horizontal format
        elif format == HORIZONTAL:

            # Browsing every image
            for image_index in range(number_of_images):
                
                # Creating new image
                new_image = Image.new('RGB', (video_height, video_width))

                # Case for solar activity image
                if len(solar_activity_images) > 0:

                    # Opening the image
                    sa_image = Image.open(solar_activity_images[image_index])
                    
                    # Adding this image to the new image, from the beginning
                    new_image.paste(sa_image, (0, 0))
                
                # Case for particle flux graph image
                if len(particles_graph_images) > 0:

                    # Opening the image
                    pfg_image = Image.open(particles_graph_images[image_index])
                    
                    # Adding this image to the new image, after the solar activity image 
                    new_image.paste(pfg_image, (solar_activity_width, 0))
                
                # Case for comment, if it is defined
                if comment_block is not None:
                    
                    # Adding the comment to the new image
                    new_image.paste(comment_block, (0, video_height-comment_height))


                # Creating a pure binary variable to store the new image
                new_image_byte = io.BytesIO()

                # Saving the new image in a pure binary format
                new_image.save(new_image_byte, format='png')

                # Adding the new image to the list
                final_images.append(new_image_byte)        

        # Returning the final images list          
        return final_images
    # --------------------------------------- #



    # ----- Video generation algorithm ----- #
    def generate_video(self, frame_list, video_name, video_width, video_height, output_folder : str):

        # Saving previous working directory
        previous_working_directory = os.getcwd()
        
        # Setting working directory to output folder
        os.chdir(output_folder)

        # Configuring video writer
        output_video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 25, (video_width, video_height))

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

        # Returning to the previous working directory
        os.chdir(previous_working_directory)
    # -------------------------------------- #
    

