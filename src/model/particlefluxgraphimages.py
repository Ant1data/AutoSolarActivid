import csv
import datetime as dt
import os

from datetime import datetime

class ParticleFluxGraphImages():

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    ## It that will directly build the graph images
    def __init__(self, beginDateTime : datetime, endDateTime : datetime, dctEnergy : dict[str, bool], image_width : float, image_height : float):
        
        # Defining attributes from parameters
        self.beginDateTime = beginDateTime
        self.endDateTime = endDateTime
        self.dctEnergy = dctEnergy

        # # Extracting the data from beginDateTime
        # start_year = self.beginDateTime.year
        # start_month = self.beginDateTime.month
        # start_day = self.beginDateTime.day
        # start_hour = self.beginDateTime.hour
        # start_min = self.beginDateTime.minute
        
        # # Extracting the data from endDateTime
        # end_year = self.endDateTime.year
        # end_month = self.endDateTime.month
        # end_day = self.endDateTime.day
        # end_hour = self.endDateTime.hour
        # end_min = self.endDateTime.minute
        
        
        ## ----- NEUTRON FLUX PART ----- ##
        if dctEnergy["NeutronFlux"]:
            self.neutron_csv_to_dict(self.beginDateTime, self.endDateTime)
    ## --------------------------------------------------------------------------------------------------------------------- ##
    


    ## FUNCTIONS ----------------------------------------------------------------------------------------------------------- ##
    # Function to convert CSV Neutron Flux data file into a legible dictionary for the graph video algorithm
    def neutron_csv_to_dict(self, begin_date_time : datetime, end_date_time : datetime) -> dict:
        
        # Creating a dictionary that will store the neutron flux data
        final_dict = dict()
        
        ### -------------------- /!\ TO CHANGE WHEN DEPLOYING THE APP /!\ -------------------- ###
        
        # Setting working directory to input
        os.chdir('input')
        
        ### ---------------------------------------------------------------------------------- ###


        ## ----- Checking every data file day per day ----- ##

        current_date_time = begin_date_time # Initializing current datetime
        while current_date_time <= end_date_time:
            
            # Importing year, month and day from current_date_time
            year = current_date_time.strftime('%Y')
            month = current_date_time.strftime('%m')
            day = current_date_time.strftime('%d')
        

            # Building the filename
            filename = f"neutron_flux_{year}_{month}_{day}.csv"


            ## --- Changing header line --- ##
            
            # Opening the file and importing data
            with open(filename, mode="r") as csv_file:
            
                # Importing file content in a list form
                file_content = csv_file.readlines()

                # Defining header string for the first line
                header="start_date_time"

                # Case when only one sensor is set on the file
                if ("RCORR_E" in file_content[0] or "; Neutron flux" in file_content[0]):
                    header = header + "; Neutron flux"
                
                # Other cases when there are many other sensors
                else:
                    # Adding KERG and TERA on the header if they exist
                    if ("KERG" in file_content[0]):
                        header = header + "; KERG Neutron flux"
                    if ("TERA" in file_content[0]):
                        header = header + "; TERA Neutron flux"
                
                # Adding line break
                header = header + "\n"
                
                # Setting the first line of the file to the content of header
                file_content[0] = header

            # Writing new content
            with open(filename, mode="w") as csv_file:
                csv_file.writelines(file_content)
            ## ---------------------------- ##


            ## --- Converting CSV file into dictionary --- ##

            # Opening and reading CSV file
            with open(filename, mode="r") as csv_file:    
                csv_content = csv.DictReader(csv_file, delimiter=";")

                # For every line of the CSV file 
                for current_line in csv_content:

                    # Converting datetimes into Python datetime format
                    reconverted_datetime = datetime.strptime(current_line["start_date_time"], '%Y-%m-%d %H:%M:%S')
                    current_line["start_date_time"] = reconverted_datetime

                    # For every key in the current line dictionary
                    for current_key in current_line.keys():

                        # Setting final_dict's keys
                        # if they are not already set
                        if not current_key in final_dict.keys():
                            final_dict[current_key] = []

                        # Converting neutron flux data in float (if current_key contains "Neutron Flux")
                        if "Neutron flux" in current_key:
                            final_dict[current_key].append(float(current_line[current_key]))
                        else:
                            final_dict[current_key].append(current_line[current_key])

            ## ------------------------------------------- ##

            # We increment the current_date_time by one day
            current_date_time += dt.timedelta(days=1)
        ## ------------------------------------------------ ##

        # For debug
        print(final_dict)
        return final_dict
    ## --------------------------------------------------------------------------------------------------------------------- ##




## ---------- TEST ZONE ---------- ##

# Defining parameters for the ParticleFluxGraphImages test instance
begin_date_time = datetime(2024, 6, 17, 0, 0)
end_date_time = datetime(2024, 6, 18, 23, 59)
dct_energy = {"NeutronFlux" : True}

# Building a test object
ParticleFluxGraphImages(beginDateTime=begin_date_time, endDateTime=end_date_time, dctEnergy=dct_energy, image_width=1280, image_height=720)