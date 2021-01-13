import json
import plotly
import os
import json
import calmap
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt, mpld3

FILE_PATH = os.path.join("news_app", "static", "data", "headlines_scores_keywords.csv")

def article_vs_headline_plot():

    trace1 = {
        "x": [10, 20, 30, 40, 50],
        "y": [115, 205, 393, 406, 542],
    }

    plot_data = [trace1,]
    plot_layout = {"title": "Articles vs Headlines"}

    data = json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder)
    layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return data, layout

def calendar_heatmap():
    # Read in data
    df = pd.read_csv(FILE_PATH)

    # Add datetime column that converts pub_date to timestamp
    df["datetime"] = df["pub_date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))

    # Create series where values are the average article score for that day
    # And the indexes are the unique instances of days in the data
    avg_day_scores = []
    for day in df["datetime"].unique():
        avg_day_scores.append(df["headline_score"].loc[df["datetime"] == day].mean())
    date_series = pd.Series(data=avg_day_scores, index=df["datetime"].unique())

    # Use calmap to create calendar plot -- returns matplotlib figure and axes array
    calmap_fig, axes = calmap.calendarplot(
        date_series,
        monthticks=3,
        daylabels="MTWTFSS",
        dayticks=[0, 2, 4, 6],
        cmap="YlGn",
        fillcolor="grey",
        linewidth=0,
        fig_kws=dict(figsize=(8, 4)),
    )

    figure = json.dumps(calmap_fig, cls=plotly.utils.PlotlyJSONEncoder)

    return figure