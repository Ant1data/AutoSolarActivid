import tkinter as tk
import customtkinter as ctk

# Constant color codes for enabled/disabled states
ENABLED_BORDER_COLORS = ("#3E454A", "#949A9F") # Comes from customtkinter default blue theme
ENABLED_FG_COLORS = ("#3B8ED0", "#1F6AA5") # Comes from customtkinter default blue theme
DISABLED_COLORS = ("gray80", "gray5")

class EnergyFrame(ctk.CTkFrame):

    ## CONSTRUCTOR --------------------------------------------------------------------------------------------------------- ##
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Energy label
        self.lblEnergy = ctk.CTkLabel(self, text="Energy")
        self.lblEnergy.pack(padx=8, anchor="w")

        # Proton Flux CheckBox
        self.chbProtonFlux = ctk.CTkCheckBox(self, text="Proton Flux", border_width=1, checkbox_height=18, checkbox_width=18, command=self.switch_states_proton_subcheckboxes)
        self.chbProtonFlux.pack(anchor="w", padx=8)

        # Sub-Checkboxes for energy selection
        self.chb10MeV = ctk.CTkCheckBox(self, text=">= 10 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb10MeV.pack(anchor="w", padx=16)

        self.chb50MeV = ctk.CTkCheckBox(self, text=">= 50 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb50MeV.pack(anchor="w", padx=16)

        self.chb100MeV = ctk.CTkCheckBox(self, text=">= 100 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb100MeV.pack(anchor="w", padx=16)

        self.chb500MeV = ctk.CTkCheckBox(self, text=">= 500 MeV", border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb500MeV.pack(anchor="w", padx=16)

        # Neutron Flux CheckBox
        self.chbNeutronFlux = ctk.CTkCheckBox(self, text="Neutron Flux", border_width=1, checkbox_height=18, checkbox_width=18)
        self.chbNeutronFlux.pack(anchor="w", padx=8)
    ## --------------------------------------------------------------------------------------------------------------------- ##  

    ## METHODS ------------------------------------------------------------------------------------------------------------- ##

    ## This function, triggered by self.chbProtonFlux, changes sub-checkboxes' states
    ## If self.chbProtonFlux is on, they become enabled,
    ## Otherwise, they become disabled
    def switch_states_proton_subcheckboxes(self):
        # Enabled
        if self.chbProtonFlux.get() == 1:
            self.chb10MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb50MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb100MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb500MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
        # Disabled
        else:
            self.chb10MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb50MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb100MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb500MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)