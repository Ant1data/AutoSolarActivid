import requests
import json

class ProtonFluxData:
    def __init__(self) -> None:
        pass

## ---------- TEST ZONE ---------- ##

# Proxy configuration

irsn_proxy = {"https" : "http://roussel-mar:boqpag-mijxi2-Duhdyk@wpad.proton.intra.irsn.fr:3128"}
http_request = requests.get(url="https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json", proxies=irsn_proxy)
print(http_request.json())