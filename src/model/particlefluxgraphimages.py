import csv
import datetime
import os
import requests

from datetime import datetime

class ParticleFluxGraphImages():

    # Constructor that will directly build the graph images,
    def __init__(self, beginDateTime : datetime, endDateTime : datetime, dctEnergy : dict[str, bool]):
        
        # Defining attributes from parameters
        self.beginDateTime = beginDateTime
        self.endDateTime = endDateTime
        self.dctEnergy = dctEnergy

        # Extracting the data from beginDateTime
        start_year = self.beginDateTime.year
        start_month = self.beginDateTime.month
        start_day = self.beginDateTime.day
        start_hour = self.beginDateTime.hour
        start_min = self.beginDateTime.minute
        
        # Extracting the data from endDateTime
        end_year = self.endDateTime.year
        end_month = self.endDateTime.month
        end_day = self.endDateTime.day
        end_hour = self.endDateTime.hour
        end_min = self.endDateTime.minute
        
        
        ## ----- NEUTRON FLUX PART ----- ##
        if dctEnergy["NeutronFlux"] == True:

            # Requesting and storing the csv data in a temporary file
            with open("src/tmp/neutron_flux.csv", "wb") as neutron_flux_file:
                
                # Defining the URL to call, with corresponding dates and times
                # url = f"http://nest.nmdb.eu/draw_graph.php?formchk=1&stations[]=KERG&stations[]=TERA&output=ascii&start_year={start_year}&start_month={start_month}&start_day={start_day}&start_hour={start_hour}&start_min={start_min}&end_year={end_year}&end_month={end_month}&end_day={end_day}&end_hour={end_hour}&end_min={end_min}&yunits=0"
                url = f"http://nest.nmdb.eu/draw_graph.php?formchk=1&stations[]=KERG&stations[]=KIEL&output=ascii&tabchoice=ori&dtype=corr_for_efficiency&date_choice=bydate&start_year=2009&start_month=09&start_day=01&start_hour=00&start_min=00&end_year=2009&end_month=09&end_day=05&end_hour=23&end_min=59&yunits=0"

                # For debug
                print("Downloading Neutron Flux data on NEST: ", url)

                # Requesting
                request_result = requests.get(url=url, proxies=proxies)

                # Writing file
                neutron_flux_file.write(request_result.content)
                
                # Tu en es là bg


## ---------- TEST ZONE ---------- ##

# Defining parameters for the ParticleFluxGraphImages test instance
begin_date_time = datetime(2024, 6, 6, 0, 0)
end_date_time = datetime(2024, 6, 6, 23, 59)
dct_energy = {"NeutronFlux" : True}

# Building a test object
ParticleFluxGraphImages(beginDateTime=begin_date_time, endDateTime=end_date_time, dctEnergy=dct_energy)