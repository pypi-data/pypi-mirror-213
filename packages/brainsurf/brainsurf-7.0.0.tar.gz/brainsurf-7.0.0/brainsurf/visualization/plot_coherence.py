import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

def plot_coherence_lineplot(data, freq_range=None):
    if freq_range is not None:
        data = data[(data['frequency'] >= freq_range[0]) & (data['frequency'] <= freq_range[1])]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x='frequency', y='coherence', data=data, ax=ax)
    ax.set_title('Coherence Plot')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Coherence')
    plt.show()

def visualize_coherence_heatmap(coherence_matrix, channel_labels):
    plt.figure(figsize=(10, 8))
    sns.heatmap(coherence_matrix, cmap='coolwarm', annot=True, fmt=".2f", xticklabels=channel_labels, yticklabels=channel_labels)
    plt.xlabel('Channels')
    plt.ylabel('Channels')
    plt.title('Coherence Matrix')
    plt.show()

def visualize_coherence_circular(coherence_matrix, channel_labels):
    G = nx.Graph()
    for i, label in enumerate(channel_labels):
        G.add_node(label)

    # Add edges to the graph based on the coherence matrix
    num_channels = len(channel_labels)
    for i in range(num_channels):
        for j in range(i+1, num_channels):
            G.add_edge(channel_labels[i], channel_labels[j], weight=coherence_matrix[i, j])

    # Set the positions of nodes in a circular layout
    pos = nx.circular_layout(G)

    # Draw the nodes and edges
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5)

    # Add labels to the nodes
    nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

    # Set the title
    plt.title('Coherence Circular Graph')

    # Show the plot
    plt.axis('off')
    plt.show()