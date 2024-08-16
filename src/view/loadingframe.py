import customtkinter as ctk

class LoadingFrame(ctk.CTkFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Percentage variable
        self.percentage = 0

        # Information label
        self.lblInfo = ctk.CTkLabel(self, text="Loading...")
        self.lblInfo.pack(pady=10, fill='x')

        # Loading ProgressBar
        self.pgbLoading = ctk.CTkProgressBar(self, orientation="horizontal")
        self.pgbLoading.pack(padx=10, fill='x', side="left")

        # Percentage label
        self.lblPercentage = ctk.CTkLabel(self, text="0%")
        self.lblPercentage.pack(side="right")

        # Changing Loading ProgressBar value
        self.pgbLoading.set(0)

    ## METHODS ------------------------------------------------------------------------------------------------------------- ##
    
    # This function, triggered by AppHandler, changes the percentage,
    # depending on the current step and the max step
    def updtae_step(self, current_step : int, max_steps : int):
        
        # Updating progress bar
        self.pgbLoading.set(current_step/max_steps)

        # Updating Percentage label
        self.lblPercentage._text = str(int((current_step/max_steps)*100)) + "%"
    

## ---------- TEST ZONE ---------- ##
# Appearance settings
ctk.set_appearance_mode("System")  # Light/Dark mode
ctk.set_default_color_theme("blue")  # Default color

# Creating main window
main_window = ctk.CTk()
main_window.geometry("800x600")
main_window.minsize(500, 375)
main_window.title("SolarActivid - LoadingFrame test")

test_loading_frame = LoadingFrame(master=main_window, fg_color="transparent")
test_loading_frame.pack()

main_window.mainloop()