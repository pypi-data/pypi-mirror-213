import matplotlib.pyplot as plt
import numpy as np

def graph(file, dic, losses, temp_IGBT, temp_diode, temp_case):
    """
    This function generates and displays two graphs based on the given file, losses, and dictionary.
    The first graph shows Torque and Speed as a function of Time.
    The second graph shows Current and Total losses as a function of Time.

    Parameters:
    file (pandas DataFrame): A pandas DataFrame representation of the Excel file
    losses (Losses object): An instance of the Losses class containing calculated losses
    dic (dict): Dictionary of constants and file parameters
    """

    # Extract relevant data from the Excel file
    time = file.iloc[(dic["excel_starting_row"]-1):(dic["excel_ending_row"]-1), (dic["excel_column_time"]-1)].values
    speed = file.iloc[(dic["excel_starting_row"]-1):(dic["excel_ending_row"]-1), (dic["excel_column_speed"]-1)].values
    torque = file.iloc[(dic["excel_starting_row"]-1):(dic["excel_ending_row"]-1), (dic["excel_column_torque"]-1)].values
    i_ref = file.iloc[(dic["excel_starting_row"]-1):(dic["excel_ending_row"]-1), (dic["excel_column_current"]-1)].values
    total_losses = losses.total_losses

    # Plot Torque and Speed vs Time
    fig1, ax1 = plt.subplots(dpi=600)
    ax1.plot(time, torque, label='Torque')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Torque')
    ax1.set_title('Torque & Speed vs Time')
    ax1.legend()

    ax2 = ax1.twinx()
    ax2.plot(time, speed, color='red', label='Speed')
    ax2.set_ylabel('Speed')
    ax2.legend()

    # Plot Current and Total losses vs Time
    fig2, ax3 = plt.subplots(dpi=600)
    ax3.plot(time, i_ref, label='Current')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Current')
    ax3.set_title('Current vs Time')
    ax3.legend()

    fig2b, ax4 = plt.subplots(dpi=600)
    ax4.plot(time, total_losses, color='red', label='Total losses')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Total losses vs Time')
    ax4.legend()

    # Plot Temperatures vs Time
    fig3, ax5 = plt.subplots(dpi=600)
    ax5.plot(time, temp_IGBT, label='Temp_IGBT')
    ax5.plot(time, temp_diode, label='Temp_diode')
    ax5.set_xlabel('Time')
    ax5.set_ylabel('Temperature')
    ax5.set_title('Temperatures vs Time')
    ax5.legend()
  
    # # Créer les données de D et n/Nf
    # D = np.linspace(0, 1, 100)  # Valeurs de D de 0 à 1
    # n_Nf = D  # n/Nf est égal à D dans ce cas
    # 
    # # Tracer la courbe
    # fig4, ax6 = plt.subplots()
    # ax6.plot(n_Nf, D)
    # ax6.set_xlabel('n/Nf')
    # ax6.set_ylabel('D')
    # ax6.set_title('Courbe linéaire de D en fonction de n/Nf')

    # Display the plots
    plt.show()
