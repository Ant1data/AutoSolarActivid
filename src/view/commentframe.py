import tkinter as tk
import customtkinter as ctk

## CONSTANTS --------------------------------------------------------------------------------------------------------- ##
MAX_CHARACTERS = 128
## ------------------------------------------------------------------------------------------------------------------- ##

class CommentFrame(ctk.CTkFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Grid configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Comment label
        self.lblComment = ctk.CTkLabel(self, text=f"Comment ({MAX_CHARACTERS} characters maximum)")
        self.lblComment.grid(row=0, column=0, sticky="w", padx=8)

        # Comment textbox
        self.tbxComment = ctk.CTkTextbox(self, height=100)
        self.tbxComment.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        
        self.tbxComment.bind('<KeyPress>', self.char_count)
        self.tbxComment.bind('<KeyRelease>', self.char_count)

    ## --------------------------------------------------------------------------------------------------------------------- ##

    ## METHODS ------------------------------------------------------------------------------------------------------------- ##

    ## This function, triggered at every key press, erases the
    ## last character if it exceeds the MAX_CHARACTERS limit,
    ## in order to allow only a specific number of characters.
    ## Source : https://stackoverflow.com/questions/76260891/how-to-restrict-the-amount-of-characters-in-a-text-tkinter-box
    def char_count(self, event):

        # Getting the number of characters in the 
        number_of_characters = len(self.tbxComment.get('1.0', 'end-1c'))

        # If a key, other than backspace or delete, has been pressed, 
        # and the maximum of characters has been exceeded
        if number_of_characters >= MAX_CHARACTERS and event.keysym not in {'BackSpace', 'Delete'}:
            return 'break' # It will prevent from typing the character
        