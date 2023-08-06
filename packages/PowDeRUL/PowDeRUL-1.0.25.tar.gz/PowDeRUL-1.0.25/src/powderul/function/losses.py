import numpy as np

class Losses:
    def __init__(self, dic, file):
        """
        Initializes an instance of the Losses class.

        Parameters:
        dic (dict): Dictionary of constants and file parameters
        file (pandas DataFrame): A pandas DataFrame representation of the Excel file
        """
        # Extract relevant data and constants from the provided file and dictionary
        self.i_ref = file.iloc[(dic["excel_starting_row"]-1):(dic["excel_ending_row"]-1), (dic["excel_column_current"]-1)].values
        self.cosphi = file.iloc[(dic["excel_starting_row"]-1):(dic["excel_ending_row"]-1), (dic["excel_column_cosphi"]-1)].values
        self.m = file.iloc[(dic["excel_starting_row"]-1):(dic["excel_ending_row"]-1), (dic["excel_column_m"]-1)].values
      
        # Additional constants are also initialized here
        self.Vce0 = dic["Vce0"]
        self.Rce = dic["Rce"]
        self.f_sw = dic["f_sw"]
        self.E_sw = dic["E_sw"]
        self.Iref_sw = dic["Iref_sw"]
        self.Vdc = dic["Vdc"]
        self.Vref_sw = dic["Vref_sw"]
        self.kv_igbt = dic["kv_igbt"]
        self.Rd = dic["Rd"]
        self.E_d = dic["E_d"]
        self.Iref_d= dic["Iref_d"]
        self.ki_diode = dic["ki_diode"]
        self.Vref_d = dic["Vref_d"]
        self.Vd = dic["Vd"]
        self.kv_diode = dic["kv_diode"]
        self.number_IGBT = dic["number_IGBT"]
        self.number_IGBT_parallel = dic["number_IGBT_parallel"]

        # Initialize variables to hold losses
        self.P_T_cond = None
        self.P_T_sw = None
        self.pertes_igbt = None
        self.P_D_cond = None
        self.P_D_sw = None
        self.pertes_diode = None
        self.total_losses = None
        self.total_losses_cum = None
    
    def calculate_losses(self):
        """
        Calculates losses for both IGBT and Diode.

        IGBT losses are divided into conduction losses (P_T_cond) and switching losses (P_T_sw).
        Diode losses are divided into conduction losses (P_D_cond) and switching losses (P_D_sw).

        The total losses and their cumulative sum are also calculated and stored.
        """

        # Calculate IGBT losses
        self.P_T_cond = (1/(2*np.pi) + self.m*self.cosphi/8) * self.Vce0 * np.sqrt(2) * self.i_ref + (1/8 + self.m*self.cosphi/(3*np.pi)) * self.Rce * 2 * self.i_ref**2
        self.P_T_sw = self.f_sw * self.E_sw * np.sqrt(2) / np.pi * self.i_ref / self.Iref_sw * (self.Vdc / self.Vref_sw)**self.kv_igbt
        self.pertes_igbt = self.P_T_cond + self.P_T_sw

        # Calculate Diode losses
        self.P_D_cond = (1/(2*np.pi) + self.m*self.cosphi/8) * self.Vd * np.sqrt(2) * self.i_ref + (1/8 + self.m*self.cosphi/(3*np.pi)) * self.Rd * 2 * self.i_ref**2
        self.P_D_sw = self.f_sw * self.E_d * np.sqrt(2) / np.pi * (self.i_ref / self.Iref_d)**self.ki_diode * (self.Vdc / self.Vref_d)**self.kv_diode
        self.pertes_diode = self.P_D_cond + self.P_D_sw

        # Calculate total losses and their cumulative sum
        self.total_losses = np.asarray((self.pertes_igbt + self.pertes_diode) * self.number_IGBT, dtype=float)
        self.total_losses_cum = np.cumsum(self.total_losses)
