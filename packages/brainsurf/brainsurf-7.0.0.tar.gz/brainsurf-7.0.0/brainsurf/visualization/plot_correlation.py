import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

def plot_cross_corr(data, channel_1, channel_2):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x='time', y='cross_corr', data=data, ax=ax)
    ax.set_title(f'Cross-correlation between {channel_1} and {channel_2}')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Cross-correlation')
    plt.show()

def visualize_interchannel_correlation(correlation_matrix, channel_labels):
    """
    Visualize the Inter-channel Correlation as a correlation matrix heatmap.

    Args:
    - correlation_matrix (numpy.ndarray): The correlation matrix with shape (n_channels, n_channels).
    - channel_labels (list): List of channel labels corresponding to the rows/columns of the correlation matrix.

    Returns:
    - None (displays the correlation matrix heatmap)
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, cmap='coolwarm', annot=False, fmt=".2f", xticklabels=channel_labels, yticklabels=channel_labels)
    plt.xlabel('Channels')
    plt.ylabel('Channels')
    plt.title('Inter-channel Correlation')
    plt.show()


def visualize_interchannel_scatter(correlation_matrix, channel_labels):
    """
    Visualize the Inter-channel Correlation as a scatter plot.

    Args:
    - correlation_matrix (numpy.ndarray): The correlation matrix with shape (n_channels, n_channels).
    - channel_labels (list): List of channel labels corresponding to the rows/columns of the correlation matrix.

    Returns:
    - None (displays the scatter plot)
    """
    n_channels = correlation_matrix.shape[0]
    
    # Create a figure with subplots
    fig, axes = plt.subplots(n_channels, n_channels, figsize=(12, 12))
    
    # Iterate over each pair of channels
    for i in range(n_channels):
        for j in range(n_channels):
            if i != j:
                # Plot scatter plot for the pair of channels
                axes[i, j].scatter(correlation_matrix[i, :], correlation_matrix[j, :], alpha=0.5)
                axes[i, j].set_xlabel(channel_labels[i])
                axes[i, j].set_ylabel(channel_labels[j])
    
    # Adjust spacing between subplots
    plt.tight_layout()
    
    # Show the scatter plot
    plt.show()



def visualize_correlation_circle(correlation_matrix, channel_labels):
    """
    Visualize the Correlation Matrix as a Circle Plot.

    Args:
    - correlation_matrix (numpy.ndarray): The correlation matrix with shape (n_channels, n_channels).
    - channel_labels (list): List of channel labels corresponding to the rows/columns of the correlation matrix.

    Returns:
    - None (displays the correlation matrix circle plot)
    """
    n_channels = correlation_matrix.shape[0]
    angles = np.linspace(0, 2 * np.pi, n_channels, endpoint=False).tolist()
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot the circles for each channel
    for angle, channel in zip(angles, channel_labels):
        x = np.cos(angle)
        y = np.sin(angle)
        ax.add_patch(Circle((x, y), radius=0.1, color='black'))
        ax.text(x, y, channel, ha='center', va='center')
    
    # Plot the lines between channels based on the correlation values
    lines = []
    colors = []
    widths = []
    for i in range(n_channels):
        for j in range(i + 1, n_channels):
            lines.append([(np.cos(angles[i]), np.sin(angles[i])), (np.cos(angles[j]), np.sin(angles[j]))])
            colors.append(correlation_matrix[i, j])
            widths.append(abs(correlation_matrix[i, j]) * 5)  # Adjust line width based on correlation strength
    
    lc = LineCollection(lines, colors=colors, linewidths=widths, cmap='coolwarm')
    ax.add_collection(lc)
    
    # Set aspect ratio and axis limits
    ax.set_aspect('equal')
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    
    # Add colorbar
    cbar = fig.colorbar(lc)
    cbar.set_label('Correlation')
    
    # Remove ticks and labels
    ax.axis('off')
    
    # Show the correlation matrix circle plot
    plt.show()
