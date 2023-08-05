 
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, signal
from sklearn.metrics import pairwise_distances

class ComparativeVisualizationFactory:
    @staticmethod
    def visualize_mean(data1, data2, label1='Data 1', label2='Data 2'):
        mean1 = np.mean(data1)
        mean2 = np.mean(data2)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plot
        x_labels = [label1, label2]
        line_x = range(2)
        line_y = [mean1, mean2]
        ax.plot(line_x, line_y, color='blue', linewidth=2, linestyle='--', marker='o', label='Mean')

        # Set the labels and title
        ax.set_xticks(line_x)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Mean')
        ax.set_title('Comparison of Mean Values')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def visualize_standard_deviation(data1, data2, label1='Data 1', label2='Data 2'):
        std1 = np.std(data1)
        std2 = np.std(data2)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plot
        x_labels = [label1, label2]
        line_x = range(2)
        line_y = [std1, std2]
        ax.plot(line_x, line_y, color='red', linewidth=2, linestyle='--', marker='o', label='Standard Deviation')

        # Set the labels and title
        ax.set_xticks(line_x)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Standard Deviation')
        ax.set_title('Comparison of Standard Deviation Values')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def visualize_median(data1, data2, label1='Data 1', label2='Data 2'):
        median1 = np.median(data1)
        median2 = np.median(data2)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plot
        x_labels = [label1, label2]
        line_x = range(2)
        line_y = [median1, median2]
        ax.plot(line_x, line_y, color='green', linewidth=2, linestyle='--', marker='o', label='Median')

        # Set the labels and title
        ax.set_xticks(line_x)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Median')
        ax.set_title('Comparison of Median Values')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def visualize_interquartile_range(data1, data2, label1='Data 1', label2='Data 2'):
        iqr1 = np.percentile(data1, 75) - np.percentile(data1, 25)
        iqr2 = np.percentile(data2, 75) - np.percentile(data2, 25)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plot
        x_labels = [label1, label2]
        line_x = range(2)
        line_y = [iqr1, iqr2]
        ax.plot(line_x, line_y, color='orange', linewidth=2, linestyle='--', marker='o', label='Interquartile Range')

        # Set the labels and title
        ax.set_xticks(line_x)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Interquartile Range')
        ax.set_title('Comparison of Interquartile Range Values')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def visualize_skewness(data1, data2, label1='Data 1', label2='Data 2'):
        skewness1 = data1.skew()
        skewness2 = data2.skew()

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the bar plot
        x_labels = [label1, label2]
        bar_x = range(2)
        bar_heights = [skewness1, skewness2]
        ax.bar(bar_x, bar_heights, color='purple', alpha=0.7)

        # Set the labels and title
        ax.set_xticks(bar_x)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Skewness')
        ax.set_title('Comparison of Skewness Values')

        # Show the plot
        plt.show()

    def visualize_kurtosis(data1, data2, label1='Data 1', label2='Data 2'):
        # Calculate the kurtosis values
        kurtosis1 = stats.kurtosis(data1)
        kurtosis2 = stats.kurtosis(data2)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plots
        x_labels = [label1, label2]
        line_x = range(2)
        line_y = [kurtosis1, kurtosis2]
        ax.plot(line_x, line_y, color='magenta', linewidth=2, linestyle='--', marker='o', label='Kurtosis')

        # Set the labels and title
        ax.set_xticks(line_x)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Kurtosis')
        ax.set_title('Comparison of Kurtosis Values')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def visualize_range(data1, data2, label1='Data 1', label2='Data 2'):
        # Calculate the range values
        range1 = np.max(data1) - np.min(data1)
        range2 = np.max(data2) - np.min(data2)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plots
        x_labels = [label1, label2]
        line_x = range(2)
        line_y = [range1, range2]
        ax.plot(line_x, line_y, color='brown', linewidth=2, linestyle='--', marker='o', label='Range')

        # Set the labels and title
        ax.set_xticks(line_x)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Range')
        ax.set_title('Comparison of Range Values')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def visualize_variance(data1, data2, label1='Data 1', label2='Data 2'):
        # Calculate the variance values
        variance1 = np.var(data1)
        variance2 = np.var(data2)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plots
        x_labels = [label1, label2]
        line_x = range(2)
        line_y = [variance1, variance2]
        ax.plot(line_x, line_y, color='gray', linewidth=2, linestyle='--', marker='o', label='Variance')

        # Set the labels and title
        ax.set_xticks(line_x)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Variance')
        ax.set_title('Comparison of Variance Values')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def visualize_rms(data1, data2, label1='Data 1', label2='Data 2'):
        # Calculate the root mean square (RMS) values
        rms1 = np.sqrt(np.mean(np.square(data1)))
        rms2 = np.sqrt(np.mean(np.square(data2)))

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plots
        x_labels = [label1, label2]
        line_x = range(2)
        line_y = [rms1, rms2]
        ax.plot(line_x, line_y, color='cyan', linewidth=2, linestyle='--', marker='o', label='RMS')

        # Set the labels and title
        ax.set_xticks(line_x)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('RMS')
        ax.set_title('Comparison of RMS Values')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def visualize_spectral_power(data1, data2, fs, label1='Data 1', label2='Data 2'):
        # Calculate the spectral power values using the periodogram method
        freq1, power1 = signal.periodogram(data1, fs)
        freq2, power2 = signal.periodogram(data2, fs)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plots
        ax.plot(freq1, power1, color='blue', linewidth=2, linestyle='--', label=label1)
        ax.plot(freq2, power2, color='red', linewidth=2, linestyle='--', label=label2)

        # Set the labels and title
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Power Spectral Density')
        ax.set_title('Comparison of Power Spectral Density')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def visualize_coherence(data1, data2, fs, label1='Data 1', label2='Data 2'):
        # Calculate the coherence values using Welch's method
        freq, coherence = signal.coherence(data1, data2, fs)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create the line plot
        ax.plot(freq, coherence, color='blue', linewidth=2, linestyle='--', label='Coherence')

        # Set the labels and title
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Coherence')
        ax.set_title('Coherence between Signals')
        ax.legend()

        # Show the plot
        plt.show()

    @staticmethod
    def calculate_boxcount(data, scales):
        distance_matrix = pairwise_distances(data)
        mean_distances = np.mean(distance_matrix, axis=1)

        counts = []
        for scale in scales:
            count = np.sum(mean_distances <= scale)
            counts.append(count)

        return counts

    @staticmethod
    def visualize_multi_person_time_series(num_persons, *data, labels=None, xlabel="Time", ylabel="Value"):
        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Define a colormap with enough colors for the number of persons
        colormap = plt.cm.get_cmap('tab10', num_persons)

        # Plot each time series with a different color from the colormap
        for i in range(num_persons):
            person_data = data[i]
            color = colormap(i)
            label = f'Person {i+1}' if labels is None else labels[i]
            ax.plot(person_data, color=color, label=label)

        # Set the labels and title
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title('Comparison Graph')
        ax.legend()

        # Show the plot
        plt.show()



    @staticmethod
    def visualize_multi_feature_time_series(data1, data2, xlabel='Time', ylabel='Value', title="Comparison of Time Series"):
        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot the first set of data
        ax.plot(data1, color='blue', label='Data 1')

        # Plot the second set of data
        ax.plot(data2, color='red', label='Data 2')

        # Set the labels and title
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()

        # Show the plot
        plt.show()


    