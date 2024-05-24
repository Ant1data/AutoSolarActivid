import requests
import json

class ProtonFluxData:
    def __init__(self) -> None:
        pass

## ---------- TEST ZONE ---------- ##
http_request = requests.get("https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json")
print(http_request.json)