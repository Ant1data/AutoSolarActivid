class ControllerData():
    def __init__(self, frmApp):
        
        # Initializing userRequest dictionary
        self.userRequest = {}
        
        # Initializing App Frame 
        self.frmApp = frmApp

    def btnGenerateClicked(self, user_request):
        self.userRequest = user_request
        
        # For debug
        print(self.userRequest)