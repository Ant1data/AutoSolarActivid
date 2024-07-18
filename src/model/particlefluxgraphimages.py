import csv
import datetime as dt
import json
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

        # Defining dictionaries for particle flux
        proton_flux_dictionary = None
        neutron_flux_dictionary = None
        
        # Getting Proton flux data dictionary if selected
        if dctEnergy["ProtonFlux"]:
            proton_flux_dictionary = self.proton_json_to_dict(self.beginDateTime, self.endDateTime, self.dctEnergy["Energies"])

        # Getting Neutron flux data dictionary if selected
        if dctEnergy["NeutronFlux"]:
            neutron_flux_dictionary = self.neutron_csv_to_dict(self.beginDateTime, self.endDateTime)

        self.dict_to_graph(proton_flux_dict=proton_flux_dictionary, neutron_flux_dict=neutron_flux_dictionary, image_width=1280, image_height=720)
    ## --------------------------------------------------------------------------------------------------------------------- ##
    


    ## FUNCTIONS ----------------------------------------------------------------------------------------------------------- ##

    # Function to convert GOES Proton Flux data file in JSON into a legible dictionary for the graph video algorithm
    # Dictionary format : {">=1 MeV" : {timestamp1 : flux, timestamp2 : flux, ...}, ">=10 MeV" : {timestamp1 : flux, timestamp2 : flux, ...}, ...}
    def proton_json_to_dict(self, begin_date_time : datetime, end_date_time : datetime, energy_dict : dict) -> dict:
        
        # Creating a dictionary that will store the proton flux data
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
        

            # Opening file
            json_file = open(f"{year}{month}{day}_integral-protons-1-day.json")

            # Loading data as a dictionary
            json_data = json.load(json_file)

            # Checking every measure in the json file
            for measure in json_data:

                # Getting current measure's energy
                # corresponding to the measure's flux
                current_energy = measure["energy"]

                # We add this measure if only the current energy was
                # selected on the user's request
                if energy_dict[current_energy] == True:
                    
                    # Adding current_energy key if it isn't set yet
                    if current_energy not in final_dict.keys():
                        final_dict[current_energy] = dict()

                    # Getting measure["time_tag"] property into a Python datetime format
                    current_measure_datetime = datetime.strptime(measure["time_tag"], '%Y-%m-%dT%H:%M:%SZ')

                    # We add this measure to the final dictionary if only the current_measure_datetime
                    # is between begin_date_time and end_date_time
                    if current_measure_datetime >= begin_date_time and current_measure_datetime <= end_date_time:

                        # Getting current measure's flux
                        current_flux = measure["flux"]

                        # Adding this measure to the final dictionary
                        final_dict[current_energy][current_measure_datetime] = current_flux
                    

            # Incrementing current_date_time by one day
            current_date_time += dt.timedelta(days=1)
        
        ## ------------------------------------------------ ##

        ### -------------------- /!\ TO CHANGE WHEN DEPLOYING THE APP /!\ -------------------- ###
        # Resetting working directory to the parent folder
        os.chdir('../')
        ### ---------------------------------------------------------------------------------- ###

        return final_dict



    # Function to convert NEST Neutron Flux data file in CSV into a legible dictionary for the graph video algorithm
    # Dictionary format : {"start_date_time" : [list of datetimes], "Measure" : [List of measures]}
    # Multiple stations version : {"start_date_time" : [list of datetimes], "KERG Measure" : [List of measures], "TERA Measure" : [List of measures]}
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

                    # We allow the current line to be added only if the start_date_time
                    # is between begin_date_time and end_date_time
                    if current_line["start_date_time"] >= begin_date_time and current_line["start_date_time"] <= end_date_time:

                        # For every key in the current line dictionary
                        for current_key in current_line.keys():

                            # Setting final_dict's tabs on its values
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

        ### -------------------- /!\ TO CHANGE WHEN DEPLOYING THE APP /!\ -------------------- ###
        # Resetting working directory to the parent folder
        os.chdir('../')
        ### ---------------------------------------------------------------------------------- ###

        return final_dict
    
    

    def dict_to_graph(self, proton_flux_dict = None, neutron_flux_dict = None, image_width = 640, image_height = 480) -> list:
        
        ### -------------------- /!\ TO CHANGE WHEN DEPLOYING THE APP /!\ -------------------- ###
        # Setting working directory to output
        os.chdir('output')
        ### ---------------------------------------------------------------------------------- ###
        
        # Determining how many graphs can be drawn
        number_of_graphs = 0

        # Verifying which dictionaries are set
        if proton_flux_dict is not None:
            number_of_graphs += 1
        if neutron_flux_dict is not None:
            number_of_graphs += 1
        
        # Determining how many images can be produced
        number_of_images = min(len(proton_flux_dict.keys()), len(neutron_flux_dict["start_date_time"]))

        
        ## --- Preparing data for graphs --- ##

        # Proton flux
        proton_start_datetimes = []

        if proton_flux_dict is not None:
            proton_start_datetimes = proton_flux_dict.keys()


        

        
    ## --------------------------------------------------------------------------------------------------------------------- ##




## ---------- TEST ZONE ---------- ##

# Defining parameters for the ParticleFluxGraphImages test instance
begin_date_time = datetime(2024, 6, 17, 5, 0)
end_date_time = datetime(2024, 6, 18, 17, 00)
dct_energy = {"ProtonFlux" : True, "Energies" : {">=10 MeV" : True, ">=50 MeV" : True, ">=100 MeV" : True,">=500 MeV" : True, ">=1 MeV" : False, ">=30 MeV" : False, ">=5 MeV" : False, ">=60 MeV" : False, },"NeutronFlux" : True}

# Building a test object
ParticleFluxGraphImages(beginDateTime=begin_date_time, endDateTime=end_date_time, dctEnergy=dct_energy, image_width=1280, image_height=720)