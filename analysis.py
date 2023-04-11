import pandas as pd
from flask import render_template
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from io import BytesIO
import base64


def generate_dashboard(trip_csv: str):
    """Handles data manipulation using pandas and creates all necesseary charts using matplotlib

    Args:
        trip_csv (str): path to csv file

    Returns:
        Any: render_template with relevant fields
    """
    df = pd.read_csv(trip_csv)  # read csv and store as dataframe
    df = wrangle_df(df)  # handle raw data

    # extract trip information from dataset (distance, time, mpg, avg speed, fuel consumed)
    trip_info = get_trip_info(df)

    # plot all given charts
    rpm_img = plot_rpm(df['time'], df['Engine RPM (rpm)'])
    ideal_speed_img = plot_ideal_speed(df['time'], df['Vehicle speed (mph)'])
    acc_img = plot_acceleration(df["time"], df["Vehicle acceleration (g)"])
    rpm_throttle = hexbin_rpm_throttle(
        df["Engine RPM (rpm)"], df["Throttle position (%)"])

    # return dashboard with generated charts as png
    return render_template(
        'dashboard.html',
        trip_info=trip_info,
        rpm_img=rpm_img,
        ideal_speed_img=ideal_speed_img,
        acc_img=acc_img,
        rpm_throttle=rpm_throttle
    )


def wrangle_df(df) -> pd.DataFrame:
    """Data wrangling: clean and transform the raw csv data

    Args:
        df (DataFrame): dataframe from inout csv

    Returns:
        pd.DataFrame: cleaned up dataframe
    """
    # convert time to pandas datetime
    df['time'] = pd.to_datetime(df['time'])

    # remove any unnamed columns
    for col in df.columns:
        if "Unnamed" in col:
            del df[col]

    # forward fill
    df.fillna(method='ffill', inplace=True)

    # backward fill
    df.fillna(method='bfill', inplace=True)

    return df


def get_trip_info(df: pd.DataFrame) -> dict:
    """Extracts the trip info - distance, time, mpg, avg speed, fuel consumed

    Args:
        df (pd.DataFrame): dataframe to be used

    Returns:
        dict: {distance, time, mpg, speed, fuel_consumed}
    """
    last_row_index = df.shape[0] - 1

    distance = round(df["Distance travelled (miles)"][last_row_index], 2)
    time = int((df["time"][last_row_index] - df["time"][0]).seconds / 60)
    mpg = int(df["Average fuel consumption (total) (MPG)"][last_row_index])
    speed = int(df["Average speed (mph)"][last_row_index])
    fuel_consumed = df["Fuel used (gallon)"][last_row_index]

    trip_info = {
        "distance": distance,
        "time": time,
        "mpg": mpg,
        "speed": speed,
        "fuel_consumed": fuel_consumed
    }

    return trip_info


def plot_rpm(x: pd.Series, y: pd.Series) -> str:
    """Plots Engine RPM vs Time to see the RPM progression over the trip duration

    Args:
        x (pd.Series): Engine RPM (rpm)
        y (pd.Series): time (pd.Timestamp)

    Returns:
        str: Image as PNG in buffer
    """

    # Define thresholds
    idling = 1000
    high_revs = 5000
    ideal_rpm = 2500

    # Create figure
    fig = Figure(figsize=(8, 5))
    ax = fig.subplots()

    # Set axis labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Engine RPM (rpm)')

    # Plot data
    ax.plot(x, y)
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter('%H:%M'))  # format timestamp

    # Create threshold lines
    ax.axhline(y=idling, color='k')
    ax.axhline(y=high_revs, color='k')
    ax.axhline(y=ideal_rpm, color='k')

    # Create spans with backround color
    ax.axhspan(y.min(), idling, facecolor='orange', alpha=0.2)
    ax.axhspan(idling, high_revs, facecolor='green', alpha=0.2)
    ax.axhspan(high_revs, y.max(), facecolor='red', alpha=0.2)

    # Return generated image
    return generate_image(fig)


def plot_ideal_speed(x: pd.Series, y: pd.Series) -> str:
    """Plots Vehicle Speed vs Time to see the speed progression over the trip duration

    Args:
        x (pd.Series): Vehicle Speed (mph)
        y (pd.Series): time (pd.Timestamp)

    Returns:
        str: Image as PNG in buffer
    """

    # Set threshold
    ideal_speed = 50

    # Create figure
    fig = Figure(figsize=(8, 5))
    ax = fig.subplots()

    # Set axis labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Vehicle speed (mph)')

    # Plot data
    ax.plot(x, y)
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter('%H:%M'))  # format timestamp

    # Create threshold line
    ax.axhline(y=ideal_speed, color='k')

    # Create spans with backround color
    ax.axhspan(0, ideal_speed, facecolor='green', alpha=0.2)
    ax.axhspan(ideal_speed, y.max(), facecolor='red', alpha=0.2)

    # Return generated image
    return generate_image(fig)


def plot_acceleration(x: pd.Series, y: pd.Series) -> str:
    """Plots Vehicle acceleration vs Time to see the acceleration progression over the trip duration

    Args:
        x (pd.Series): Vehicle acceleration (g)
        y (pd.Series): time (pd.Timestamp)

    Returns:
        str: Image as PNG in buffer
    """
    # Set threshold
    coasting = 0

    # Create figure
    fig = Figure(figsize=(8, 5))
    ax = fig.subplots()

    # Set axis labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Vehicle acceleration (g)')

    # Plot data
    ax.plot(x, y)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Create threshold line
    ax.axhline(y=coasting, color='k')

    # Create spans with backround color
    ax.axhspan(y.min(), coasting - 0.1, facecolor='orange', alpha=0.2)
    ax.axhspan(coasting - 0.1, coasting + 0.1, facecolor='green', alpha=0.2)
    ax.axhspan(coasting + 0.1, y.max(), facecolor='red', alpha=0.2)

    # Return generated image
    return generate_image(fig)


def hexbin_rpm_throttle(x: pd.Series, y: pd.Series) -> str:
    fig = Figure(figsize=(8, 7))
    ax = fig.subplots()

    ax.set_xlabel('Engine RPM (rpm)')
    ax.set_ylabel('Throttle Position (%)')

    ax.hexbin(x, y, gridsize=12)

    return generate_image(fig)


def generate_image(fig):
    """Creates PNG image from matplotlib fig and stores it in buffer

    Args:
        fig (Figure): matplotlib figure created in parent functions

    Returns:
        str: Image as PNG in buffer
    """
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"
