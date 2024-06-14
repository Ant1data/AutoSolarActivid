import tkinter as tk
import customtkinter as ctk

class CommentFrame(ctk.CTkFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Grid configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        
        # Comment label
        self.lblComment = ctk.CTkLabel(self, text="Comment")
        self.lblComment.grid(row=0, column=0, sticky="w", padx=8)

        # Comment textbox
        self.tbxComment = ctk.CTkTextbox(self)
        self.tbxComment.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
    ## --------------------------------------------------------------------------------------------------------------------- ##