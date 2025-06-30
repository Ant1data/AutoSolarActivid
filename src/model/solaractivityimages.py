import cv2
import io
import numpy as np
import operator
import os

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from common.exceptions import NoDataFoundError
from controller.apphandler import UPDATE_PERCENTAGE

## CONSTANTS --------------------------------------------------------------------------------------------------------- ##

ADMITTED_RESOLUTIONS = ['512', '1024']
ADMITTED_IMAGE_TYPES = [
    'c2',
    'c3',
    'eit171',
    'eit195',
    'eit284',
    'eit304',
    'hmiigr',
    'hmimag'
]

## ------------------------------------------------------------------------------------------------------------------- ##

class SolarActivityImages():

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    ## It that will directly pick the images
    def __init__(self, beginDateTime : datetime, endDateTime : datetime, imageWidth : float, imageHeight : float, inputFolder : str, loadingFrameQueue = None):
        
        # Defining attributes from parameters
        self.beginDateTime = beginDateTime
        self.endDateTime = endDateTime
        self.imageWidth = imageWidth
        self.imageHeight = imageHeight
        self.inputFolder = inputFolder
        self.loadingFrameQueue = loadingFrameQueue


        # Defining the list of images
        self.images = []

        # Saving previous working directory
        previous_working_directory = os.getcwd()
        
        # Setting working directory to input folder
        os.chdir(self.inputFolder)

        # Defining the list to store the images file names
        self.images_filenames = []

        # Defining dictionaries to count the number of images of each resolution and types

        # Resolutions
        resolution_numbers = {}

        for key in ADMITTED_RESOLUTIONS:
            resolution_numbers[key] = 0
        
        # Types
        types_numbers = {}

        for key in ADMITTED_IMAGE_TYPES:
            types_numbers[key] = 0

        ## ----- Filtering file names of the directory ----- ##
        # This filter allows to pick only the images that are in the time bounds,
        # with admitted image types and resolutions. It relies on the file name.

        # We browse all the files in the directory
        for image_filename in os.listdir('.'):
            
            # Checking if the file is an image (JPG, JPEG or PNG)
            if image_filename.endswith(".jpg") or image_filename.endswith(".jpeg") or image_filename.endswith("png"):
                
                # Checking if the timestamp on the filename is between beginDateTime and endDateTime
                # According to the file name pattern, the date is specified in the 13 first characters
                filename_timestamp = datetime.strptime(image_filename[:13], '%Y%m%d_%H%M')
                if filename_timestamp >= self.beginDateTime and filename_timestamp <= self.endDateTime:
                    
                    # Incrementing value of a key on both resolution_numbers and types_numbers dictionaries,
                    # if this key has been found on the file name

                    # For resolutions
                    for one_key in resolution_numbers.keys():
                        try:
                            image_filename.index(one_key, 14) # Raises a ValueError whenever the one_key substring hasn't been found
                            resolution_numbers[one_key] += 1

                        # When the one_key is not found
                        except ValueError:
                            continue

                    # For types
                    for one_key in types_numbers.keys():
                        try:
                            image_filename.index(one_key, 14) # Raises a ValueError whenever the one_key substring hasn't been found
                            types_numbers[one_key] += 1

                        # When the one_key is not found, we ignore and continue
                        except ValueError:
                            continue
                    
                    # Adding the file name to the filenames list
                    self.images_filenames.append(image_filename)

        # Case when no images has been found,
        # We raise a NoDataFoundError exception
        if len(self.images_filenames) == 0:
            raise NoDataFoundError("No corresponding solar activity images has been found")
                    
        # Getting major resolution and type to select the images with the major resolution and type
        major_resolution = max(resolution_numbers.items(), key=operator.itemgetter(1))[0]
        major_type = max(types_numbers.items(), key=operator.itemgetter(1))[0]
        
        # We remove every filenames without major resolution or type
        for one_filename in self.images_filenames[:]:
            
            try:
                # Seeking for major resolution and major type on each filename
                one_filename.index(major_resolution, 14)
                one_filename.index(major_type, 14)

            # When one of those is not found,
            # We remove the filename from the images
            except ValueError:
                self.images_filenames.remove(one_filename)
        
        # Sorting the filenames
        self.images_filenames.sort()
        
        # Setting steps for LoadingFrame percentage
        current_step = 0
        total_steps = len(self.images_filenames)
        

        # Adding every image in Byte format
        for one_image in self.images_filenames:

            # Opening the image
            current_image = Image.open(one_image, mode='r')

            # Adding credits to the images
            draw = ImageDraw.Draw(current_image)
            arial_font = ImageFont.truetype('arial.ttf', 32)
            draw.text((20, 20), "© Solar and Heliospheric Observatory", font=arial_font)

            # Changing image size
            current_image_resized = current_image.resize((imageWidth, imageHeight))
            
            
            # Creating a pure binary variable to store the image
            current_image_byte = io.BytesIO()

            # Saving the image in a pure binary format
            current_image_resized.save(current_image_byte, format='png')

            # Adding the image to the list
            self.images.append(current_image_byte)

            # --- Increasing percentage on loading frame --- #
            current_step += 1
            self.loadingFrameQueue.put(UPDATE_PERCENTAGE, (current_step, total_steps))
            # ---------------------------------------------- #
        
        # Resetting working directory to the previous one
        os.chdir(previous_working_directory)
    ## --------------------------------------------------------------------------------------------------------------------- ##

## ---------- TEST ZONE ---------- ##

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

# begin_date_time = datetime(2024, 6, 17, 5, 0)
# end_date_time = datetime(2024, 6, 18, 17, 00)
# test_object_1 = SolarActivityImages(beginDateTime=begin_date_time, endDateTime=end_date_time, imageWidth=1280, imageHeight=720)

# generate_video(test_object_1.images, "solar_activid_test_solar_activity.mp4")