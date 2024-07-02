import abc
from abc import ABC, abstractmethod

# Abstract class for both ControllerData and ControllerSettings,
# having similar functions but different user request treatment
class ControllerGeneral(ABC):

    # Abstract class constructor
    @abstractmethod
    def __init__(self, frmApp):

        # Initializing userRequest dictionary
        self.userRequest = {}
        
        # Initializing App Frame 
        self.frmApp = frmApp
    

    # Getter of userRequest property
    @abstractmethod
    def getUserRequest(self):
        return self.userRequest
    
    # Function treating the user request
    # To be defined by subclasses
    @abstractmethod
    def treatUserRequest(self, userRequest : dict[str, any]):
        pass