import numpy as np
import matplotlib.pyplot as plt

def create_quantized_rainflow_matrix(counter):
    """
    Creates a quantized rainflow matrix based on the given counter.

    Parameters:
    counter (tuple): A tuple containing mean, range, and counts values.

    Returns:
    matrix (numpy array): A quantized rainflow matrix.
    mean_bins (numpy array): Bins for mean values.
    range_bins (numpy array): Bins for range values.
    """

    scale = 10
    mean_values, range_values, counts_values = counter[1], counter[0], counter[2]

    # Create an empty matrix of size scale x scale
    matrix = np.zeros((scale, scale))

    # Quantify the values of mean and range into scale bins
    mean_bins = np.linspace(np.min(mean_values), np.max(mean_values), scale)
    range_bins = np.linspace(np.min(range_values), np.max(range_values), scale)

    # Fill the matrix with the sums of count values
    for j in range(len(mean_values)):
        mean_index = np.clip(np.digitize(mean_values[j], mean_bins), 0, scale - 1) - 1
        range_index = np.clip(np.digitize(range_values[j], range_bins), 0, scale - 1) - 1
        matrix[mean_index, range_index] += counts_values[j]

    return matrix, mean_bins, range_bins


def show_matrix(counter_IGBT, counter_diode):
    """
    Displays the quantized rainflow matrices for IGBT and Diode.

    Parameters:
    counter_IGBT (tuple): A tuple containing mean, range, and counts values for IGBT.
    counter_diode (tuple): A tuple containing mean, range, and counts values for Diode.
    """

    matrix_1, mean_bins_1, range_bins_1 = create_quantized_rainflow_matrix(counter_IGBT)
    matrix_2, mean_bins_2, range_bins_2 = create_quantized_rainflow_matrix(counter_diode)

    # Create a new figure with two subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    ax = axes[0]
    im = ax.imshow(matrix_1, cmap='hot', interpolation='nearest')
    ax.set_title('IGBT')
    ax.set_xlabel('Delta T')
    ax.set_ylabel('Mean Tj')
    fig.colorbar(im, ax=ax, label='Count')
    ax.set_xticks(np.arange(len(range_bins_1)))
    ax.set_yticks(np.arange(len(mean_bins_1)))
    ax.set_xticklabels([str(int(val)) for val in range_bins_1])
    ax.set_yticklabels([str(int(val)) for val in mean_bins_1])

    # Plot the second matrix
    ax = axes[1]
    im = ax.imshow(matrix_2, cmap='hot', interpolation='nearest')
    ax.set_title('Diode')
    ax.set_xlabel('Delta T')
    ax.set_ylabel('Mean Tj')
    fig.colorbar(im, ax=ax, label='Count')
    ax.set_xticks(np.arange(len(range_bins_2)))
    ax.set_yticks(np.arange(len(mean_bins_2)))
    ax.set_xticklabels([str(int(val)) for val in range_bins_2])
    ax.set_yticklabels([str(int(val)) for val in mean_bins_2])

    plt.tight_layout()  # Adjust spacing between subplots
