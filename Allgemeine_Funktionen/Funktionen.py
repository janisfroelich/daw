import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def count_na_absolt_relativ(df: pd.DataFrame):
    """Counts the number of missing values in a dataframe and returns a new DataFrame with the absolut and relativ value."""
    df_absolut_relativ = pd.DataFrame(columns=["absolut", "relativ"])
    df_absolut_relativ["absolut"] = df.isna().sum()
    df_absolut_relativ["relativ"] = df_absolut_relativ["absolut"] / len(df)
    return df_absolut_relativ

def overview(df, col):
    f, axs = plt.subplots(1,2, figsize=(9,6), gridspec_kw=dict(width_ratios=[15,10]))
    sns.boxplot(df[col], ax=axs[0])
    sns.distplot(df[col], ax=axs[1])
    return plt.show()

def corr_overview(df: pd.DataFrame, method_corr = 'pearson'):
    """Returns a correlation FacetGrid plot and a Dataframe with FacetGrid correlation coeffizient, select method_corr: person, spearman."""
    sns.pairplot(df, size=2.5)
    df_corr = df.corr(method = method_corr)
    return plt.show(), df_corr