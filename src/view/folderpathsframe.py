import customtkinter as ctk

from tkinter import filedialog

class FolderPathsFrame(ctk.CTkFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Grid configuration
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        # Folder paths label
        self.lblFolderPaths = ctk.CTkLabel(self, text="Folder paths")
        self.lblFolderPaths.grid(row=0, column=0, sticky="w", padx=8)

        # Input folder path
        self.lblInputPath = ctk.CTkLabel(self, text="Input folder path:")
        self.lblInputPath.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entInputPath = ctk.CTkEntry(self, width=250)
        self.entInputPath.grid(row=1, column=1, padx=10, pady=5)

        self.btnBrowseInput = ctk.CTkButton(self, text="Browse", command=self.browse_input_folder)
        self.btnBrowseInput.grid(row=1, column=2, padx=10, pady=5)

        # Output folder path
        self.lblOutputPath = ctk.CTkLabel(self, text="Output folder path:")
        self.lblOutputPath.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entOutputPath = ctk.CTkEntry(self, width=250)
        self.entOutputPath.grid(row=2, column=1, padx=10, pady=5)

        self.btnBrowseOutput = ctk.CTkButton(self, text="Browse", command=self.browse_output_folder)
        self.btnBrowseOutput.grid(row=2, column=2, padx=10, pady=5)

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