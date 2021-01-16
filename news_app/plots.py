import json
import plotly
import os
import json
import calmap
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt, mpld3

FILE_PATH = os.path.join("news_app", "static", "data", "headlines_scores_keywords.csv")

def article_vs_headline_plot(df):
    # Read in data
    # df = pd.read_csv(FILE_PATH)

    scores_no_zeros = df[["headline_score", "article_score", "news_desk"]].loc[(df["headline_score"] != 0) & (df["article_score"] != 0) & (df["section_name"] == "U.S.")]
    # ['National' 'Business' 'Politics' 'Science' 'Climate']
    desk_colors_dict = {
        "National": "midnightblue",
        "Business": "gold",
        "Politics": "firebrick",
        "Science": "forestgreen",
        "Climate": "darkorange"
    }
    desk_colors = scores_no_zeros["news_desk"].map(desk_colors_dict)
    trace1 = {
        "x": scores_no_zeros["headline_score"],
        "y": scores_no_zeros["article_score"],
        "mode": "markers",
        "marker": {"color": desk_colors}
    }

    plot_data = [trace1,]
    plot_layout = {
        "title": "Articles vs Headlines"}

    data = json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder)
    layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return data, layout

def calendar_heatmap():
    # Read in data
    cal_heatmap_df = pd.read_csv(os.path.join("news_app", "static", "data", "calendar_heatmap.csv"))

    cal_heatmap_df["date"] = cal_heatmap_df["date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    # news_desks = []
    # dates = []
    # avg_day_scores = []
    # for desk in df["news_desk"].unique():
    #     for day in df["datetime"].unique():
    #         avg_day_scores.append(
    #             df["headline_score"]
    #             .loc[(df["datetime"] == day) & (df["news_desk"] == desk)]
    #             .mean()
    #         )
    #         dates.append(day)
    #         news_desks.append(desk)

    # cal_heatmap_df = pd.DataFrame(list(zip(dates, news_desks, avg_day_scores)),columns=["date", "news_desk", "avg_score"])

    # cal_heatmap_df.to_csv(os.path.join("news_app", "static", "data", "calendar_heatmap.csv"), index=False, encoding="utf-8-sig")

    trace2015 = {
        "z": cal_heatmap_df["avg_score"].loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2015)],
        "x": cal_heatmap_df["date"].loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2015)],
        "y": cal_heatmap_df["news_desk"].loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2015)],
        "type": "heatmap",
        "colorscale": "RdBu",
        "showscale": True,
    }

    trace2016 = {
        "z": cal_heatmap_df["avg_score"].loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2016)],
        "x": cal_heatmap_df["date"].loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2016)],
        "y": cal_heatmap_df["news_desk"].loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2016)],
        "xaxis": "x2",
        "yaxis": "y2",
        "type": "heatmap",
        "colorscale": "RdBu",
        "showscale": False,
    }

    trace2017 = {
        "z": cal_heatmap_df["avg_score"].loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2017)],
        "x": cal_heatmap_df["date"].loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2017)],
        "y": cal_heatmap_df["news_desk"].loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2017)],
        "xaxis": "x3",
        "yaxis": "y3",
        "type": "heatmap",
        "colorscale": "RdBu",
        "showscale": False,
    }

    plot_data = [trace2015, trace2016, trace2017]

    plot_layout = {
        "title": "Average Daily Sentiment by News Desk",
        "xaxis_nticks": 12,
        "grid": {
            "rows": 3, 
            "columns": 1, 
            "pattern": "independent",
            "roworder": "bottom to top",
        }
    }

    heatmap_data = json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder)
    heatmap_layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return heatmap_data, heatmap_layout


# def calendar_heatmap_old():
#     # Read in data
#     df = pd.read_csv(FILE_PATH)

#     # Add datetime column that converts pub_date to timestamp
#     df["datetime"] = df["pub_date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
#     df["datetime"] = df["datetime"].apply(lambda x: pd.to_datetime(x))
#     # Create series where values are the average article score for that day
#     # And the indexes are the unique instances of days in the data
#     avg_day_scores = []
#     for day in df["datetime"].unique():
#         avg_day_scores.append(df["headline_score"].loc[df["datetime"] == day].mean())
#     date_series = pd.Series(data=avg_day_scores, index=df["datetime"].unique())
    
#     # Use calmap to create calendar plot -- returns matplotlib figure and axes array
#     calmap_fig, axes = calmap.calendarplot(
#         date_series,
#         monthticks=3,
#         daylabels="MTWTFSS",
#         dayticks=[0, 2, 4, 6],
#         cmap="YlGn",
#         fillcolor="grey",
#         linewidth=0,
#         fig_kws=dict(figsize=(8, 4)),
#     )

#     # figure_mpld3 = mpld3.fig_to_dict(calmap_fig)
#     # figure_json = json.dumps(figure_mpld3, cls=plotly.utils.PlotlyJSONEncoder)

#     figure_json = json.dumps(mpld3.fig_to_dict(calmap_fig))
#     return figure_json

# article_vs_headline_plot()