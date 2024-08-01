import customtkinter as ctk

class FormatQualityFrame(ctk.CTkFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Grid configuration
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        # Format & Quality label
        self.lblFormatQuality = ctk.CTkLabel(self, text="Format & Quality")
        self.lblFormatQuality.grid(row=0, column=0, sticky="w", padx=8)

        # Format label
        self.lblFormat = ctk.CTkLabel(self, text="Format")
        self.lblFormat.grid(row=1, column=0, sticky="e", padx=4)

        # Format Segmented Button
        self.sgbFormatValue = ctk.StringVar(value="Instagram (vertical)")
        self.sgbFormat = ctk.CTkSegmentedButton(self, values=["Instagram (vertical)", "YouTube (horizontal)"], variable=self.sgbFormatValue)
        self.sgbFormat.grid(row=1, column=1, columnspan=2)

        # Quality label
        self.lblQuality = ctk.CTkLabel(self, text="Quality")
        self.lblQuality.grid(row=2, column=0, sticky="e", padx=4)

        # Quality Segmented Button
        self.sgbQualityValue = ctk.StringVar(value="Medium (720p)")
        self.sgbQuality = ctk.CTkSegmentedButton(self, values=["Medium (720p)", "High (1080p)"], variable=self.sgbQualityValue)
        self.sgbQuality.grid(row=2, column=1, columnspan=2)

        
