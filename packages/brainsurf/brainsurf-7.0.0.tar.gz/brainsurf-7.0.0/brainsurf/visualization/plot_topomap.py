import numpy as np
import matplotlib.pyplot as plt

def plot_topomap(data, pos, vmin=None, vmax=None, cmap='viridis', show=True):
    fig, ax = plt.subplots()
    sc = ax.scatter(pos[:, 0], pos[:, 1], c=data, cmap=cmap, vmin=vmin, vmax=vmax)
    plt.colorbar(sc, ax=ax)
    ax.set_xlim([np.min(pos[:, 0]) - 0.1, np.max(pos[:, 0]) + 0.1])
    ax.set_ylim([np.min(pos[:, 1]) - 0.1, np.max(pos[:, 1]) + 0.1])
    ax.set_title('Topographic Map')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    if show:
        plt.show()
    
    return fig, ax
