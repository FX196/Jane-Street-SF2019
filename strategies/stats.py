import datetime

import matplotlib.pyplot as plt
import numpy as np


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


def EMA(past_data, beta=0.7, t_length=10):
    t_length = min(len(past_data), t_length)
    v = beta ** np.arange(0, t_length)
    v = np.flip(v)
    return np.array(past_data[-t_length:]).dot(v)
