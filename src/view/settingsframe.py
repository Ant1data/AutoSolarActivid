import customtkinter as ctk
import tkinter as tk

from tkinter import filedialog

class SettingsFrame(ctk.CTkFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Title label
        self.lblTitle = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.lblTitle.pack(anchor="center", pady=10)

        # ----- Video settings Frame ----- #
        self.frmVideo = ctk.CTkFrame(self)
        self.frmVideo.pack(anchor="center", padx=8, fill="x")

        # Video settings label
        self.lblVideoSettings = ctk.CTkLabel(self.frmVideo, text="Video Settings", font=ctk.CTkFont(size=14, weight="bold"))
        self.lblVideoSettings.grid(row=0, column=0, sticky="w", padx=8)

        # Input folder path
        self.lblInputPath = ctk.CTkLabel(self.frmVideo, text="Input folder path:")
        self.lblInputPath.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entInputPath = ctk.CTkEntry(self.frmVideo, width=250)
        self.entInputPath.grid(row=1, column=1, padx=10, pady=5)

        self.btnBrowseInput = ctk.CTkButton(self.frmVideo, text="Browse", command=self.browse_input_folder)
        self.btnBrowseInput.grid(row=1, column=2, padx=10, pady=5)

        # Output folder path
        self.lblOutputPath = ctk.CTkLabel(self.frmVideo, text="Output folder path:")
        self.lblOutputPath.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entOutputPath = ctk.CTkEntry(self.frmVideo, width=250)
        self.entOutputPath.grid(row=2, column=1, padx=10, pady=5)

        self.btnBrowseOutput = ctk.CTkButton(self.frmVideo, text="Browse", command=self.browse_output_folder)
        self.btnBrowseOutput.grid(row=2, column=2, padx=10, pady=5)

        # Video Format
        self.lblVideoFormat = ctk.CTkLabel(self.frmVideo, text="Video Format:")
        self.lblVideoFormat.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.cmbVideoFormat = ctk.CTkComboBox(self.frmVideo, values=["YouTube Video (Horizontal)", "Instagram Reel (Vertical)"])
        self.cmbVideoFormat.grid(row=3, column=1, padx=10, pady=5)

        # Quality
        self.lblQuality = ctk.CTkLabel(self.frmVideo, text="Quality:")
        self.lblQuality.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.cmbQuality = ctk.CTkComboBox(self.frmVideo, values=["Low (480p)", "Medium (720p)", "High (1080p)"])
        self.cmbQuality.grid(row=4, column=1, padx=10, pady=5)
        # -------------------------------- #

        # ----- Internet settings Frame ----- #
        self.frmInternet = ctk.CTkFrame(self)
        self.frmInternet.pack(anchor="center", padx=8, fill="x")

        # Internet settings label
        self.lblInternetSettings = ctk.CTkLabel(self.frmInternet, text="Internet Settings", font=ctk.CTkFont(size=14, weight="bold"))
        self.lblInternetSettings.grid(row=0, column=0, sticky="w", padx=8)

        # URL Source
        self.lblURLSource = ctk.CTkLabel(self.frmInternet, text="URL Source:")
        self.lblURLSource.grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.entURLSource = ctk.CTkEntry(self.frmInternet, width=250)
        self.entURLSource.grid(row=5, column=1, padx=10, pady=5)

        # --- Proxy Configuration Part --- #
        self.frmProxyConfiguration = ctk.CTkFrame(self.frmInternet)
        self.frmProxyConfiguration.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="we")

        # Use Proxy Switch
        self.swcUseProxyValue = tk.BooleanVar(value=False)
        self.swcUseProxy = ctk.CTkSwitch(self.frmProxyConfiguration, text="Use Proxy", command=self.toggle_swcUseProxy, variable=self.swcUseProxyValue, onvalue=True, offvalue=False)
        self.swcUseProxy.grid(row=0, column=0, padx=10, pady=5, sticky="e")


        # Proxy address
        self.lblProxyAddress = ctk.CTkLabel(self.frmProxyConfiguration, text="Proxy Address:")
        self.lblProxyAddress.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entProxyAddress = ctk.CTkEntry(self.frmProxyConfiguration, width=250)
        self.entProxyAddress.grid(row=1, column=1, padx=10, pady=5)

        # Proxy port
        self.lblProxyPort = ctk.CTkLabel(self.frmProxyConfiguration, text="Proxy Port:")
        self.lblProxyPort.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        self.entProxyPort = ctk.CTkEntry(self.frmProxyConfiguration, width=100)
        self.entProxyPort.grid(row=2, column=1, padx=10, pady=5, sticky="w")


        # --- Proxy Authentication Part --- #

        # Use Authentication Switch
        self.swcUseAuthValue = tk.BooleanVar(value=False)
        self.swcUseAuth = ctk.CTkSwitch(self.frmProxyConfiguration, text="Use Authentication", command=self.toggle_swcUseAuth, variable=self.swcUseAuthValue, onvalue=True, offvalue=False)
        self.swcUseAuth.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Username
        self.lblUsername = ctk.CTkLabel(self.frmProxyConfiguration, text="Username:")
        self.lblUsername.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.entUsername = ctk.CTkEntry(self.frmProxyConfiguration, width=250)
        self.entUsername.grid(row=4, column=1, padx=10, pady=5)

        # Password
        self.lblPassword = ctk.CTkLabel(self.frmProxyConfiguration, text="Password:")
        self.lblPassword.grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.entPassword = ctk.CTkEntry(self.frmProxyConfiguration, width=250, show="●")
        self.entPassword.grid(row=5, column=1, padx=10, pady=5)

        # ----------------------------------- #

        

    ## --------------------------------------------------------------------------------------------------------------------- ##

    ## METHODS ------------------------------------------------------------------------------------------------------------- ##

    ## This function, triggered by btnBrowseInput, opens a dialog window to choose the input folder
    ## where solar activity images are stored
    def browse_input_folder(self):
        folder_path = filedialog.askdirectory(title="Choose input folder...")
        if folder_path:
            self.entInputPath.delete(0, ctk.END)
            self.entInputPath.insert(0, folder_path)


    ## This function, triggered by btnBrowseOutput, opens a dialog window to choose the output folder
    ## where rendered videos will be stored
    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(title="Choose output folder...")
        if folder_path:
            self.entOutputPath.delete(0, ctk.END)
            self.entOutputPath.insert(0, folder_path)


    ## This function, triggered by swcUseProxy, enables or disables frmProxyConfiguration's inputs
    def toggle_swcUseProxy(self):

        # If switch is On
        if self.swcUseProxyValue.get() == True:

            # We enable those elements
            self.entProxyAddress.configure(state=ctk.NORMAL)
            self.entProxyPort.configure(state=ctk.NORMAL)
            self.swcUseAuth.configure(state=ctk.NORMAL)

            # We call the toggle_swcUseAuth function 
            # to enable authentication elements or keep them disabled
            self.toggle_swcUseAuth()
            
        # If switch is Off
        else:
            # We disable everything, no matter which part the element is in
            self.entProxyAddress.configure(state=ctk.DISABLED)
            self.entProxyPort.configure(state=ctk.DISABLED)
            self.swcUseAuth.configure(state=ctk.DISABLED)
            self.entUsername.configure(state=ctk.DISABLED)
            self.entPassword.configure(state=ctk.DISABLED)
    

    ## This function, triggered by swcUseAuth, enables or disables frmProxyConfiguration's inputs
    def toggle_swcUseAuth(self):

        # If switch is On
        if self.swcUseAuthValue.get() == True:
            self.entUsername.configure(state=ctk.NORMAL)
            self.entPassword.configure(state=ctk.NORMAL)

        # If switch is Off
        else:
            self.entUsername.configure(state=ctk.DISABLED)
            self.entPassword.configure(state=ctk.DISABLED)



# Example usage
if __name__ == "__main__":
    app = ctk.CTk()
    frmSettings = SettingsFrame(app)
    frmSettings.pack(padx=20, pady=20)
    app.title("Settings | SolarActivid")
    app.mainloop()
