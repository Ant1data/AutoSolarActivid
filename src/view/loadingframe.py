import customtkinter as ctk

class LoadingFrame(ctk.CTkFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Percentage variable
        self.percentage = 0

        # Step label
        self.lblStep = ctk.CTkLabel(self, text="Loading...")
        self.lblStep.pack(pady=10, fill='x')

        # Loading ProgressBar
        self.pgbLoading = ctk.CTkProgressBar(self, orientation="horizontal")
        self.pgbLoading.pack(padx=10, fill='x', side="left")

        # Percentage label
        self.lblPercentage = ctk.CTkLabel(self, text="0%")
        self.lblPercentage.pack(side="right")

        # Changing Loading ProgressBar value
        self.pgbLoading.set(0)



    ## METHODS ------------------------------------------------------------------------------------------------------------- ##

    # This function changes the step information 
    def update_step(self, new_step_content : str, current_step = None, total_steps = None):

        # Creating the new label sentence
        new_label = ""

        # If the current step and max steps are defined,
        # we insert them on the step label
        if current_step is not None and total_steps is not None:
            new_label += "Step " + str(current_step) + " of " + str(total_steps) + ": "

        # Updating the new step content 
        new_label += new_step_content

        # Adding the new content on the lblStep
        self.lblStep = new_label


    
    
    # This function changes the percentage label and the progress bar,
    # depending on the current step and the max step
    def update_percentage(self, current_step : int, total_steps : int):
        
        # Updating progress bar
        self.pgbLoading.set(current_step/total_steps)

        # Updating Percentage label
        self.lblPercentage._text = str(int((current_step/total_steps)*100)) + "%"