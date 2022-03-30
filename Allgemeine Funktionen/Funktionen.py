import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_overview(df, col):
    """
    Plots a overview of the dataframe.
    :param df: dataframe
    :param col: column to plot
    :return:
    """
    # creating a figure composed of two matplotlib.Axes objects (ax_box and ax_hist)
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True)

    # assigning a graph to each ax
    sns.boxplot(df[col], ax=ax_box)
    sns.histplot(data=df, x=col, ax=ax_hist)

    # Remove x axis name for the boxplot
    ax_box.set(xlabel='')
    plt.show()