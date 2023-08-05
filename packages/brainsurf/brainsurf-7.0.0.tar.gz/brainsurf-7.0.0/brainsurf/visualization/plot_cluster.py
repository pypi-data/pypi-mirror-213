import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def cluster_plot(data):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.clustermap(data, cmap='coolwarm', standard_scale=1, ax=ax)
    plt.show()