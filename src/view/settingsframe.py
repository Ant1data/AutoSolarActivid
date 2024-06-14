import customtkinter as ctk
from tkinter import filedialog

class SettingsPanel(ctk.CTkFrame):

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

        # Input File Path
        self.lblInputPath = ctk.CTkLabel(self.frmVideo, text="Input File Path:")
        self.lblInputPath.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entInputPath = ctk.CTkEntry(self.frmVideo, width=250)
        self.entInputPath.grid(row=1, column=1, padx=10, pady=5)
        self.btnBrowseInput = ctk.CTkButton(self.frmVideo, text="Browse", command=self.browse_input_file)
        self.btnBrowseInput.grid(row=1, column=2, padx=10, pady=5)

        # Output File Path
        self.lblOutputPath = ctk.CTkLabel(self.frmVideo, text="Output File Path:")
        self.lblOutputPath.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entOutputPath = ctk.CTkEntry(self.frmVideo, width=250)
        self.entOutputPath.grid(row=2, column=1, padx=10, pady=5)
        self.btnBrowseOutput = ctk.CTkButton(self.frmVideo, text="Browse", command=self.browse_output_file)
        self.btnBrowseOutput.grid(row=2, column=2, padx=10, pady=5)

        # Video Format
        self.lblVideoFormat = ctk.CTkLabel(self.frmVideo, text="Video Format:")
        self.lblVideoFormat.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.cmbVideoFormat = ctk.CTkComboBox(self.frmVideo, values=["YouTube Video", "Instagram Reel"])
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

        # Proxy Configuration
        self.frmProxyConfiguration = ctk.CTkFrame(self.frmInternet)
        self.frmProxyConfiguration.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="we")
        self.lblProxyTitle = ctk.CTkLabel(self.frmProxyConfiguration, text="Proxy Configuration", font=("Arial", 14))
        self.lblProxyTitle.grid(row=0, column=0, columnspan=2, pady=5)
        self.lblProxyAddress = ctk.CTkLabel(self.frmProxyConfiguration, text="Proxy Address:")
        self.lblProxyAddress.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entProxyAddress = ctk.CTkEntry(self.frmProxyConfiguration, width=250)
        self.entProxyAddress.grid(row=1, column=1, padx=10, pady=5)
        self.lblProxyPort = ctk.CTkLabel(self.frmProxyConfiguration, text="Proxy Port:")
        self.lblProxyPort.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entProxyPort = ctk.CTkEntry(self.frmProxyConfiguration, width=100)
        self.entProxyPort.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        # ----------------------------------- #

    ## --------------------------------------------------------------------------------------------------------------------- ##


    def browse_input_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entInputPath.delete(0, ctk.END)
            self.entInputPath.insert(0, file_path)

    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if file_path:
            self.entOutputPath.delete(0, ctk.END)
            self.entOutputPath.insert(0, file_path)

# Example usage
if __name__ == "__main__":
    app = ctk.CTk()
    settings_panel = SettingsPanel(app)
    settings_panel.pack(padx=20, pady=20)
    app.mainloop()
