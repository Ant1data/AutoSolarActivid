import customtkinter as ctk
import cv2
import io
import numpy as np
import os
import tkinter.messagebox as tkm

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from queue import Queue
from threading import Thread

from model.particlefluxgraphimages import ParticleFluxGraphImages
from model.solaractivityimages import SolarActivityImages
from view.appframe import AppFrame
from view.loadingframe import LoadingFrame


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

        # Creating frame variables
        self.frmApp = None
        self.frmLoading = None

        # Creating loading steps variables
        self.current_generation_step = 0
        self.total_generation_steps = 0

        # Starting a new user request
        self.newUserRequest()

        # Launching app
        self.main_window.mainloop()        
    ## --------------------------------------------------------------------------------------------------------------------- ##

    
    ## METHODS ------------------------------------------------------------------------------------------------------------- ##

    # Function to start a new user request
    def newUserRequest(self):

        # Removing the loading frame from the main_window if it exists
        if self.frmLoading is not None:
            self.frmLoading.pack_forget()

        # Creating and adding the app frame to the main_window
        self.frmApp = AppFrame(apphandler=self, master=self.main_window, width=1200, height=1400, fg_color=("white", "gray5"))
        self.frmApp.pack()
    
    
    # Function to display the loading frame
    # while treating the user's request
    def displayLoadingFrame(self):

        # Removing the app frame from the main_window
        self.frmApp.pack_forget()

        # Creating and adding the loading frame to the main_window
        self.frmLoading = LoadingFrame(master=self.main_window, fg_color="transparent")
        self.frmLoading.pack()
    

    # Function to treat the user's request,
    # triggered by the "Generate" button
    def treatUserRequest(self, userRequest: dict[str, any]):
        
        ## ---------- Defining the properties of the video to be generated ---------- ##
        try:

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

            # Resolution for solar activity (video's resolution by default)
            solar_activity_width, solar_activity_height = video_width, video_height

            # Resolution for particle flux graphs (video's resolution by default)
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
            
            # Initializing dictionary for video images dimensions
            videoDimensions = {}
            
            # Filling the data
            videoDimensions["video_width"], videoDimensions["video_height"] = int(video_width), int(video_height)
            videoDimensions["solar_activity_width"], videoDimensions["solar_activity_height"] = int(solar_activity_width), int(solar_activity_height)
            videoDimensions["particle_graph_width"], videoDimensions["particle_graph_height"] = int(particle_graph_width), int(particle_graph_height)

            # For debug : Displaying the resolutions
            print("Video resolution :", video_width, "x", video_height)
            print("Solar activity resolution :", solar_activity_width, "x", solar_activity_height)
            print("Particle flux graph resolution :", particle_graph_width, "x", particle_graph_height)

            # ---------------------------------- #


            # ----- Launching the generation process ----- #

            # Defining the total number of steps to generate the video
            self.total_generation_steps = 0

            # Adding a step : Solar activity video generation
            if userRequest["btnSolarActivityVideo"]:
                self.total_generation_steps += 1
            
            # Adding a step : Particle flux graph images
            if userRequest["btnParticleFluxGraph"]:
                self.total_generation_steps += 1
            
            # Checking if some content will be generated
            if self.total_generation_steps > 0:

                # Adding 2 steps (1 for combinging the images, 1 for exporting the video)
                self.total_generation_steps += 2
            
                # Setting the current step to 0
                self.current_generation_step = 0
            
                # Displaying the LoadingFrame on the window
                # self.displayLoadingFrame()

                # Creating queue to allow both videoGeneration and loadingFrame
                # threads to communicate between each other
                communicationQueue = Queue()

                # Loading threads 
                loadingFrameThread = Thread(target=self.handleLoadingFrame, args=(communicationQueue))
                videoGenerationThread = Thread(target=self.processVideoCreation, args=(communicationQueue, userRequest, videoDimensions))

                # Launching threads
                loadingFrameThread.start()
                videoGenerationThread.start()

                # Threads are working...

                # Waiting the queue's job to be done
                communicationQueue.join()

                # Shutting down the threads
                loadingFrameThread.join()
                videoGenerationThread.join()

                

            # -------------------------------------------- #
            

            # # ----- Creating images objects ----- #

            # # Getting common userRequest data
            # begin_datetime = userRequest["BeginDatetime"]
            # end_datetime = userRequest["EndDatetime"]
            # input_folder = userRequest["InputFolder"]

            # # Creating lists of images
            # solar_activity_images = []
            # particle_graph_images = []

            # # Solar activity
            # if userRequest["btnSolarActivityVideo"]:

            #     # FOR LOADING FRAME
            #     ###################
            #     # Incrementing current generation step
            #     self.current_generation_step += 1

            #     # Displaying the information on the Loading Frame
            #     self.frmLoading.update_info("Fetching solar activity images", self.current_generation_step, self.total_generation_steps)
            #     ###################

            #     # Creating solar activity object
            #     solar_activity_object = SolarActivityImages(self, beginDateTime=begin_datetime, endDateTime=end_datetime, imageWidth=solar_activity_width, imageHeight=solar_activity_height, inputFolder=input_folder)

            #     # Gathering images
            #     solar_activity_images = solar_activity_object.images
            
            # # Particle flux graph
            # if userRequest["btnParticleFluxGraph"]:

            #     # FOR LOADING FRAME
            #     ###################
            #     # Incrementing current generation step
            #     self.current_generation_step += 1

            #     # Displaying the information on the Loading Frame
            #     self.frmLoading.update_info("Generating particle flux graph images", self.current_generation_step, self.total_generation_steps)
            #     ###################

            #     # Considering that there are always less solar activity
            #     # images than particle flux graph images, if the solar
            #     # activity option is selected, we set the number of solar
            #     # activity images as the minimum number of video's frames
            #     number_of_images = None

            #     if len(solar_activity_images) > 0:
            #         number_of_images = len(solar_activity_images)

            #     # Creating particle flux graph object
            #     particle_graph_object = ParticleFluxGraphImages(self, beginDateTime=begin_datetime, endDateTime=end_datetime, dctEnergy=userRequest["EnergyData"], imageWidth=particle_graph_width, imageHeight=particle_graph_height, numberOfImages=number_of_images, inputFolder=input_folder)

            #     # Gathering images
            #     particle_graph_images = particle_graph_object.images
            # # ----------------------------------- #

            # # ----- Combining different images (with comment) ----- #

            # # FOR LOADING FRAME
            # ###################
            # # Incrementing current generation step
            # self.current_generation_step += 1

            # # Displaying the information on the Loading Frame
            # self.frmLoading.update_info("Combining images", self.current_generation_step, self.total_generation_steps)
            # ###################

            # # Defining the video format (horizontal/vertical)
            # format = ""

            # if userRequest["Format"] == "Instagram (vertical)":
            #     format = VERTICAL
            # elif userRequest["Format"] == "YouTube (horizontal)":
            #     format = HORIZONTAL

            # # Combining the different kind of images, with the comment if necessary
            # final_images = self.combineImages(solar_activity_images, particle_graph_images, video_width, video_height, format, userRequest["Comment"])
            # # ----------------------------------------------------- #

            # # ----- Defining video name ----- #
            # video_name = "SolarActivid"

            # # Adding selected video types
            # if userRequest["btnSolarActivityVideo"]:
            #     video_name += "_SA"
            
            # if userRequest["btnParticleFluxGraph"]:
            #     video_name += "_PFG"
            
            # # Adding Begin Datetime
            # video_name += datetime.strftime(userRequest["BeginDatetime"], "_%Y%m%d_%H%M%S")
            
            # # Adding End Datetime
            # video_name += datetime.strftime(userRequest["EndDatetime"], "_%Y%m%d_%H%M%S")
            
            # # Adding .mp4
            # video_name += ".mp4"

            # # ------------------------------- #

            # # ----- Exporting the video ----- #

            # # FOR LOADING FRAME
            # ###################
            # # Incrementing current generation step
            # self.current_generation_step += 1

            # # Displaying the information on the Loading Frame
            # self.frmLoading.update_info("Exporting video", self.current_generation_step, self.total_generation_steps)
            # ###################

            # self.generateVideo(final_images, video_name=video_name, video_width=video_width, video_height=video_height, output_folder=userRequest["OutputFolder"])
            # # ------------------------------- #
        
        # ---------------------------------- #

        # ----- Exceptions handling ----- #
        except Exception as e:

            # Creating a message box
            tkm.showerror(title="Error", message=str(e), )



    # ----- Function called as a thread to handle the loading frame ----- #
    def handleLoadingFrame(self, queue):
        pass

    # ----- Function called as a thread to generate video ----- #
    def processVideoCreation(self, queue, userRequest, videoDimensions):

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

            # FOR LOADING FRAME
            ###################
            # Incrementing current generation step
            self.current_generation_step += 1

            # Displaying the information on the Loading Frame
            self.frmLoading.update_info("Fetching solar activity images", self.current_generation_step, self.total_generation_steps)
            ###################

            # Creating solar activity object
            solar_activity_object = SolarActivityImages(self, beginDateTime=begin_datetime, endDateTime=end_datetime, imageWidth=videoDimensions["solar_activity_width"], imageHeight=videoDimensions["solar_activity_height"], inputFolder=input_folder)

            # Gathering images
            solar_activity_images = solar_activity_object.images
        
        # Particle flux graph
        if userRequest["btnParticleFluxGraph"]:

            # FOR LOADING FRAME
            ###################
            # Incrementing current generation step
            self.current_generation_step += 1

            # Displaying the information on the Loading Frame
            self.frmLoading.update_info("Generating particle flux graph images", self.current_generation_step, self.total_generation_steps)
            ###################

            # Considering that there are always less solar activity
            # images than particle flux graph images, if the solar
            # activity option is selected, we set the number of solar
            # activity images as the minimum number of video's frames
            number_of_images = None

            if len(solar_activity_images) > 0:
                number_of_images = len(solar_activity_images)

            # Creating particle flux graph object
            particle_graph_object = ParticleFluxGraphImages(self, beginDateTime=begin_datetime, endDateTime=end_datetime, dctEnergy=userRequest["EnergyData"], imageWidth=videoDimensions["particle_graph_width"], imageHeight=videoDimensions["particle_graph_height"], numberOfImages=number_of_images, inputFolder=input_folder)

            # Gathering images
            particle_graph_images = particle_graph_object.images
        # ----------------------------------- #

        # ----- Combining different images (with comment) ----- #

        # FOR LOADING FRAME
        ###################
        # Incrementing current generation step
        self.current_generation_step += 1

        # Displaying the information on the Loading Frame
        self.frmLoading.update_info("Combining images", self.current_generation_step, self.total_generation_steps)
        ###################

        # Defining the video format (horizontal/vertical)
        format = ""

        if userRequest["Format"] == "Instagram (vertical)":
            format = VERTICAL
        elif userRequest["Format"] == "YouTube (horizontal)":
            format = HORIZONTAL

        # Combining the different kind of images, with the comment if necessary
        final_images = self.combineImages(solar_activity_images, particle_graph_images, videoDimensions["video_width"], videoDimensions["video_height"], format, userRequest["Comment"])
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

        # FOR LOADING FRAME
        ###################
        # Incrementing current generation step
        self.current_generation_step += 1

        # Displaying the information on the Loading Frame
        self.frmLoading.update_info("Exporting video", self.current_generation_step, self.total_generation_steps)
        ###################

        self.generateVideo(final_images, video_name=video_name, video_width=videoDimensions["video_width"], video_height=videoDimensions["video_height"], output_folder=userRequest["OutputFolder"])
        # ------------------------------- #

    
        
    # ----- Image combination algorithm ----- #
    def combineImages(self, solar_activity_images : list, particles_graph_images : list, video_width : int, video_height : int, format : str, comment = ""):

        # For debug 
        print("Combining images")

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

        # For debug : printing the number of images
        print("Number of images (from AppHandler) :", number_of_images)

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
        
        # For debug
        print("Format : ", format)

        # Vertical format
        if format == VERTICAL:

            # Browsing every image
            for image_index in range(number_of_images):
                
                # Creating new image (with a black background)
                new_image = Image.new(mode="RGBA", size=(video_width, video_height), color="black")

                # Case for solar activity image
                if len(solar_activity_images) > 0:

                    # Opening the image
                    sa_image = Image.open(solar_activity_images[image_index])

                    # For debug : printing sa_image dimensions
                    print(sa_image.width,"x", sa_image.height)
                    
                    # Adding this image to the new image, from the beginning
                    new_image.paste(sa_image, (0, 0))
                
                # Case for comment, if it is defined
                if comment_block is not None:
                    
                    # For debug : printing sa_image dimensions
                    print(comment_block.width,"x", comment_block.height)

                    # Adding the comment to the new image
                    new_image.paste(comment_block, (0, solar_activity_height))
                
                # Case for particle flux graph image
                if len(particles_graph_images) > 0:

                    # Opening the image
                    pfg_image = Image.open(particles_graph_images[image_index])

                    # For debug : printing sa_image dimensions
                    print(pfg_image.width,"x", pfg_image.height)
                    
                    # Adding this image to the new image, after the solar activity image 
                    new_image.paste(pfg_image, (0, solar_activity_height+comment_height))

                
                # Creating a pure binary variable to store the new image
                new_image_byte = io.BytesIO()

                # Saving the new image in a pure binary format
                new_image.save(new_image_byte, format='png')

                # Adding the new image to the list
                final_images.append(new_image_byte)

                # --- Increasing percentage on loading frame --- #
                self.frmLoading.update_percentage(image_index+1, number_of_images)
                # ---------------------------------------------- #
        

        # Horizontal format
        elif format == HORIZONTAL:

            # Browsing every image
            for image_index in range(number_of_images):
                
                # Creating new image
                new_image = Image.new(mode="RGBA", size=(video_width, video_height), color="black")

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

                # --- Increasing percentage on loading frame --- #
                self.frmLoading.update_percentage(image_index+1, number_of_images)
                # ---------------------------------------------- #     


        # Returning the final images list          
        return final_images
    # --------------------------------------- #



    # ----- Video generation algorithm ----- #
    def generateVideo(self, frame_list, video_name, video_width, video_height, output_folder : str):

        # Saving previous working directory
        previous_working_directory = os.getcwd()
        
        # Setting working directory to output folder
        os.chdir(output_folder)

        # Configuring video writer
        output_video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 25, (video_width, video_height))

        # Defining the number of images
        number_of_images = len(frame_list)

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

            # --- Increasing percentage on loading frame --- #
            self.frmLoading.update_percentage(counter, number_of_images)
            # ---------------------------------------------- #

        # Exporting video
        cv2.destroyAllWindows()
        output_video.release()
        print("Video findable on " + os.getcwd() + "/" + video_name)

        # Returning to the previous working directory
        os.chdir(previous_working_directory)
    # -------------------------------------- #