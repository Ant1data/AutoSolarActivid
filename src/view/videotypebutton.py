import tkinter as tk
import customtkinter as ctk


# Constant color codes for deselected state
# common for every VideoTypeButton
DESELECTED_FG_COLORS = ("gray80", "gray5")
DESELECTED_HOVER_COLORS = ("gray70", "gray10")
DESELECTED_TEXT_COLORS = ("black", "white")

class VideoTypeButton(ctk.CTkButton):
    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs) # We call the CTkButton constructor

        # Hand cursor is only activated when the button is deselected
        # So, by default, it is enabled
        self.configure(cursor="hand2")

        # Hover effect is only activated when this button is deselected
        # So, by default, it is enabled
        self.configure(hover=True)

        # Default color values for selected state
        self.selected_fg_color = ("#3A7EBF", "#1F538D")
        self.selected_text_color = ("#DCE4EE", "#DCE4EE")

        # Changing color values if they are defined
        if 'fg_color' in kwargs:
            self.selected_fg_color = kwargs.get('fg_color')
        if 'text_color' in kwargs:
            self.selected_text_color = kwargs.get('text_color')

        self.selected = False # This variable defines if the button is selected or not

        self.update_colors() # We update the colors



    ## METHODS ------------------------------------------------------------------------------------------------------------- ##
    ## Function to update the button's colors,
    ## whether it is selected or not
    def update_colors(self):
        if self.selected :
            # We set up selected state colors, disable hover effect, and set cursor to arrow
            self.configure(hover=False, fg_color=self.selected_fg_color, text_color=self.selected_text_color, cursor="arrow")
        else:
            # We set up deselected state colors, enable hover effect, and set cursor to hand2
            self.configure(hover=True, fg_color=DESELECTED_FG_COLORS, hover_color=DESELECTED_HOVER_COLORS, text_color=DESELECTED_TEXT_COLORS, cursor="hand2")


    ## Function to switch to selected state
    ## and update the colors
    def select(self):
        self.selected = True
        self.update_colors

    ## Function to switch to deselected state
    ## and update the colors
    def deselect(self):
        self.selected = False
        self.update_colors
        
    