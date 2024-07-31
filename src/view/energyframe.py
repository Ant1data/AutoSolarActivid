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
        self.chbProtonFluxValue = tk.BooleanVar()
        self.chbProtonFlux = ctk.CTkCheckBox(self, text="Proton Flux", variable=self.chbProtonFluxValue, border_width=1, checkbox_height=18, checkbox_width=18, command=self.switch_states_proton_subcheckboxes)
        self.chbProtonFlux.pack(anchor="w", padx=8)

        # Sub-Checkboxes for energy selection
        self.chb1MeVValue = tk.BooleanVar()
        self.chb1MeV = ctk.CTkCheckBox(self, text=">=1 MeV", variable=self.chb1MeVValue, border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb1MeV.pack(anchor="w", padx=16)
        
        self.chb10MeVValue = tk.BooleanVar()
        self.chb10MeV = ctk.CTkCheckBox(self, text=">=10 MeV", variable=self.chb10MeVValue, border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb10MeV.pack(anchor="w", padx=16)

        self.chb100MeVValue = tk.BooleanVar()
        self.chb100MeV = ctk.CTkCheckBox(self, text=">=100 MeV", variable=self.chb100MeVValue, border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb100MeV.pack(anchor="w", padx=16)

        self.chb30MeVValue = tk.BooleanVar()
        self.chb30MeV = ctk.CTkCheckBox(self, text=">=30 MeV", variable=self.chb30MeVValue, border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb30MeV.pack(anchor="w", padx=16)

        self.chb5MeVValue = tk.BooleanVar()
        self.chb5MeV = ctk.CTkCheckBox(self, text=">=5 MeV", variable=self.chb5MeVValue, border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb5MeV.pack(anchor="w", padx=16)

        self.chb50MeVValue = tk.BooleanVar()
        self.chb50MeV = ctk.CTkCheckBox(self, text=">=50 MeV", variable=self.chb50MeVValue, border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb50MeV.pack(anchor="w", padx=16)

        self.chb500MeVValue = tk.BooleanVar()
        self.chb500MeV = ctk.CTkCheckBox(self, text=">=500 MeV", variable=self.chb500MeVValue, border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb500MeV.pack(anchor="w", padx=16)

        self.chb60MeVValue = tk.BooleanVar()
        self.chb60MeV = ctk.CTkCheckBox(self, text=">=60 MeV", variable=self.chb60MeVValue, border_width=1, checkbox_height=12, checkbox_width=12, corner_radius=0, state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
        self.chb60MeV.pack(anchor="w", padx=16)

        # Neutron Flux CheckBox
        self.chbNeutronFluxValue = tk.BooleanVar()
        self.chbNeutronFlux = ctk.CTkCheckBox(self, text="Neutron Flux", variable=self.chbNeutronFluxValue, border_width=1, checkbox_height=18, checkbox_width=18)
        self.chbNeutronFlux.pack(anchor="w", padx=8)
    ## --------------------------------------------------------------------------------------------------------------------- ##  

    ## METHODS ------------------------------------------------------------------------------------------------------------- ##

    ## This function, triggered by self.chbProtonFlux, changes sub-checkboxes' states
    ## If self.chbProtonFlux is on, they become enabled,
    ## Otherwise, they become disabled
    def switch_states_proton_subcheckboxes(self):
        # Enabled
        if self.chbProtonFlux.get() == 1:
            self.chb1MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb10MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb100MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb30MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb5MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb50MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb500MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)
            self.chb60MeV.configure(state=tk.NORMAL, fg_color=ENABLED_FG_COLORS, border_color=ENABLED_BORDER_COLORS)

        # Disabled
        else:
            self.chb1MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb10MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb100MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb30MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb5MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb50MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb500MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)
            self.chb60MeV.configure(state=tk.DISABLED, fg_color=DISABLED_COLORS, border_color=DISABLED_COLORS)


    ## This function, triggered by the Generate button, builds a dictionary
    ## specifying the value of each checkbox of the frame
    def get_user_choice(self) -> dict:

        # Building a final dictionary for energy data to send
        user_choice = dict()

        # Proton Flux and energies
        user_choice["ProtonFlux"] = self.chbProtonFluxValue.get()

        # If Proton Flux is selected, we get the energy booleans and store them in a dictionary
        if user_choice["ProtonFlux"] == True:
            user_choice["Energies"] = dict()
            user_choice["Energies"][self.chb1MeV.cget("text")] = self.chb1MeVValue.get()
            user_choice["Energies"][self.chb10MeV.cget("text")] = self.chb10MeVValue.get()
            user_choice["Energies"][self.chb100MeV.cget("text")] = self.chb100MeVValue.get()
            user_choice["Energies"][self.chb30MeV.cget("text")] = self.chb30MeVValue.get()
            user_choice["Energies"][self.chb5MeV.cget("text")] = self.chb5MeVValue.get()
            user_choice["Energies"][self.chb50MeV.cget("text")] = self.chb50MeVValue.get()
            user_choice["Energies"][self.chb500MeV.cget("text")] = self.chb500MeVValue.get()
            user_choice["Energies"][self.chb60MeV.cget("text")] = self.chb60MeVValue.get()

        # Neutron Flux
        user_choice["NeutronFlux"] = self.chbNeutronFluxValue.get()
        
        # Returning the dictionary
        return user_choice