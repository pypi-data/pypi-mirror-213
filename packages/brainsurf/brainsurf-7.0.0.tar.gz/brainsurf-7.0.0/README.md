# Description
BrainSurf is a Python library for processing and analyzing EEG (electroencephalography) signals. It provides a collection of tools and methods for reading, preprocessing, analyzing, and visualizing EEG data. The library is built using the NumPy, SciPy, and Matplotlib packages and is designed to be easily extensible for custom analysis and visualization needs

# Installation
BrainSurf can be installed using pip, a Python package manager. To install the latest stable version of the library, run the following command :

`pip install brainsurf`

# Github
Alternatively, you can clone the repository from GitHub and install it from source:
`git clone https://github.com/preethihiremath/brainsurf`
`cd esp`
`pip install -r requirements.txt`
`python setup.py install`


# Usage
```python
import brainsurf.io.mff as load_input
import brainsurf.utils.data as util
import brainsurf.utils.performance as performance
import brainsurf.preprocessing.filtering as filter
import brainsurf.preprocessing.artifact_removal as artifact
import brainsurf.preprocessing.epoching as epoching

#load EEG data from file
suriya_baseline = load_input.convert_mff_to_eegdata("C:/Users/Preethi V Hiremath/Downloads/Meditators/Suriya/BS.mff")


values = np.asarray(suriya_baseline['sec'], dtype=object)
sampling_freq = util.estimate_sampling_frequency(values)


pre_preprocessed_data = preprocess_eeg_data(suriya_baseline,sampling_freq)

print(performance.calculate_memory_efficiency())
performance.monitor_resource_usage()