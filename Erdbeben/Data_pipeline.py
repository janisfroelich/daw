import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns


def data_pipeline_api(startdate : str, enddate: str, magnitude= -1):
    startdate, enddate = check_date_valid(startdate, enddate)
    magnitude = check_magnitude_valid(magnitude)
    df = gpd.read_file(f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={startdate}&endtime={enddate}&minmagnitude={magnitude}")
    df_reshaped = reshape_data(df)
    check_data(df_reshaped)
    box_plot(df_reshaped, "mag", "Boxplot of the magnitude")
    dist_plot(df_reshaped, "mag", "Magnitude", "Distribution of the magnitude")
    box_plot(df_reshaped, "depth", "Boxplot of the depth")
    dist_plot(df_reshaped, "depth", "Depth", "Distribution of the depth")
    plot_world(df_reshaped)

def check_magnitude_valid(magnitude: float):
    """
    Checks if the magnitude is between -1 and 10.
    """
    if magnitude < -1 or magnitude > 10:
        magnitude = input("Please enter a valid magnitude (between -1 and 10)")
    return magnitude

def check_date_valid(startdate: str, enddate: str):
    """
    Checks if the startdate is before the enddate.
    """
    if "-" not in startdate or "-" not in enddate:
        startdate = input("Please enter a valid startdate in the format yyyy-mm-dd")
        enddate = input("Please enter a valid enddate in the format yyyy-mm-dd")
    if "-" in startdate and "-" in enddate:
        if len(startdate.split("-")) != 3 or len(enddate.split("-")) != 3:
            startdate = input("Please enter a valid startdate in the format yyyy-mm-dd")
            enddate = input("Please enter a valid enddate in the format yyyy-mm-dd")
    return str(startdate), str(enddate)


def data_pipeline_url(url: str):
    df = gpd.read_file(url)
    df_reshaped = reshape_data(df)
    check_data(df_reshaped)
    box_plot(df_reshaped, "mag", "Boxplot of the magnitude")
    dist_plot(df_reshaped, "mag", "Magnitude", "Distribution of the magnitude")
    box_plot(df_reshaped, "depth", "Boxplot of the depth")
    dist_plot(df_reshaped, "depth", "Depth", "Distribution of the depth")
    plot_world(df_reshaped)


def read_geojson(url: str):
    df = gpd.read_file(url)
    return df

def reshape_data(df: gpd.GeoDataFrame):
    df = df.drop(columns=["url", "detail"])
    df = df.astype({"type": "category", "alert": "category", "magType": "category", "sources": "category", "tsunami": "category"})
    df["date"] = 0
    df["depth"] = 0
    for i in range(len(df)):
        df["date"][i] = datetime.datetime.fromtimestamp(df["time"][i] / 1000).strftime('%d/%m/%y %H:%M:%S')
        df["depth"][i] = df["geometry"][i].z
    return df

def dist_plot(df: gpd.GeoDataFrame, col: str, xlabel: str, title: str):
    """
    Plots the distribution of a column in a dataframe.
    """
    sns.distplot(df[col], hist=False)
    plt.xlabel(xlabel)
    plt.title(title)
    return plt.show()

def box_plot(df: gpd.GeoDataFrame, col: str, title: str):
    """
    Plots the boxplot of a column in a dataframe.
    """
    plt.boxplot(x=df[col])
    plt.title(title)
    return plt.show()

def check_data(df: gpd.GeoDataFrame):
    """
    Checks the data for missing values and outliers.
    """
    koordinaten_check = gpd.GeoSeries(df["geometry"])
    if koordinaten_check.is_valid.sum() < len(koordinaten_check):
        print("There are invalid geometries in the data.")
    invalid_mag = df[df["mag"] < -1]
    if len(invalid_mag) > 0:
        print("There are invalid magnitudes in the data.")
        print(invalid_mag)

def plot_world(df: gpd.GeoDataFrame):
    """
    Plots the world map.
    """
    #Prepare colors
    df["color"] = 0
    for i in range(len(df)):
        if df["mag"][i] > 5:
            df["color"][i] = "red"
        elif df["mag"][i] > 3:
            df["color"][i] = "orange"
        elif df["mag"][i] > 1:
            df["color"][i] = "yellow"
        else:
            df["color"][i] = "green"
    #Plot the world map
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    axis = world.plot(figsize=(50, 50), color='white', edgecolor='black')

    df.plot(ax=axis, color=df["color"], markersize=(df["mag"] * 100), alpha=0.6)
    plt.suptitle("green = mag < 1\n yellow = 3 > mag > 1 \n orange = 5 > mag > 3 \n red = mag > 5", x=1, y=0.5,
                 fontsize=50)
    return plt.show()

