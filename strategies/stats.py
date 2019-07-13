import numpy as np
import matplotlib.pyplot as plt
import datetime

def std(distribution):
    """
    Return the standard deviation of the current distribution
    """
    return np.std(distribution)

def mean(distribution):
    """
    return the mean of the distribution
    """
    return np.mean(distribution)

## in progress
def visualize(distribution, name):
    unique, counts = np.unique(distribution, return_counts=True)
    n_bins = 20
    plt.hist(distribution, bins=n_bins)
    now = datetime.datetime.now()
    plt.savefig("../figs/{}-{}.png".format(name, now.minute))
    return dict(zip(unique, counts))

