import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def heatmap(data, cmap='coolwarm'):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(data, cmap=cmap, annot=True, fmt='.2f', ax=ax)
    plt.show()

