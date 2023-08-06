from scipy import signal
from powderul.function.zth_materials import ZthMaterials

def calculate_temperature( losses, dic, file):
    """
    Function to calculate the temperature of IGBT and Diode.

    Parameters:
    losses (object): Object containing the loss data.
    dic (dict): Dictionary containing various constants and parameters.
    file (dataframe): Dataframe containing time and other necessary data.

    Returns:
    Temp_IGBT, Temp_diode (array): Calculated temperatures of IGBT and Diode respectively.
    """

    # Get the time values from the file dataframe
    time = file.iloc[7:1807, 0].values  # A8:A1808
    time = time.astype(float)
    ta = dic["Ta"]  # Ambient temperature
     
    # Instantiate a ZthMaterials object and calculate related properties
    zth_obj = ZthMaterials(dic)
    zth_obj.calculate_zth_cf()
    zth_obj.calculate_zth_foster()

    # Get Foster network numerators and denominators for diode and IGBT
    num_foster_diode = [
        zth_obj.num_foster_diode[order]
        for order in sorted(zth_obj.num_foster_diode.keys(), reverse=True)
    ]
    den_foster_diode = [
        zth_obj.den_foster_diode[order]
        for order in sorted(zth_obj.den_foster_diode.keys(), reverse=True)
    ]
    num_foster_IGBT = [
        zth_obj.num_foster_IGBT[order]
        for order in sorted(zth_obj.num_foster_IGBT.keys(), reverse=True)
    ]
    den_foster_IGBT = [
        zth_obj.den_foster_IGBT[order]
        for order in sorted(zth_obj.den_foster_IGBT.keys(), reverse=True)
    ]

    # Calculate case, IGBT, and diode temperatures using linear simulation
    temp_case = signal.lsim((zth_obj.num_cf, zth_obj.den_cf),losses.total_losses, time)[1] + ta
    temp_IGBT = signal.lsim((num_foster_IGBT[-1], den_foster_IGBT[-1]),losses.pertes_igbt, time)[1] + temp_case + 273.15
    temp_diode = signal.lsim((num_foster_diode[-1], den_foster_diode[-1]),losses.pertes_diode, time)[1] + temp_case + 273.15

    return temp_IGBT, temp_diode, temp_case
