import json
import plotly
import os
import json
import calmap
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt, mpld3
import plotly.express as px
from sklearn.linear_model import LinearRegression
import pickle

# FILE_PATH = os.path.join("news_app", "static", "data", "headlines_scores_keywords.csv")

def article_vs_headline_plot(df_in):
    # Read in data
    # df = pd.read_csv(FILE_PATH)

    df = df_in[["headline_score", "article_score", "news_desk"]].loc[
        (df_in["headline_score"] != 0) & 
        (df_in["article_score"] != 0) & 
        (df_in["section_name"] != "Business Day") &
        (df_in["news_desk"] != "Media") &
        (df_in["news_desk"] != "National")
    ]
    # ['National' 'Business' 'Politics' 'Science' 'Climate']
    
    # Line colors
    lines_colors_dict = { 
        "Society": "dodgerblue",
        "Business": "gold",
        "Politics": "firebrick",
        "Science": "forestgreen",
        "Climate": "darkorange",
        "Arts&Leisure": "blueviolet",
    }

    # Marker fill colors with 50% opacity
    markers_colors_dict = { 
        "Society": "rgba(30, 144, 255, 0.3)", #"dodgerblue",
        "Business": "rgba(255, 215, 0, 0.3)", #"gold",
        "Politics": "rgba(178, 34, 34, 0.3)", #"firebrick",
        "Science": "rgba(34, 139, 34, 0.3)", #"forestgreen",
        "Climate": "rgba(255, 140, 0, 0.3)", #"darkorange"
        "Arts&Leisure": "rgba(138, 43, 226, 0.3)", #"blueviolet",
    }

    df["markers_colors"] = df["news_desk"].map(markers_colors_dict)


    plot_data = []

    for desk in df["news_desk"].unique():
        scatter_trace = {
            "x": df["headline_score"].loc[df["news_desk"] == desk],
            "y": df["article_score"].loc[df["news_desk"] == desk],
            "mode": "markers",
            "marker": {
                "color": df["markers_colors"].loc[df["news_desk"] == desk],
                "line": {
                    "color": "rgba(105, 105, 105, .5)", #dimgrey
                    "width": .5,
                }
            },
            "text": df["news_desk"].loc[df["news_desk"] == desk],
            "hovertemplate": '%{text} <br>Headline: %{x}<br>Article: %{y}<extra></extra>',
            "legendgroup": desk,
            "showlegend": False,
        }
        plot_data.append(scatter_trace)
        # # Create and save models
        # print(f"fitting {desk} model")
        # x = df["headline_score"].loc[df["news_desk"] == desk].to_frame().values
        # y = df["article_score"].loc[df["news_desk"] == desk].values
        # model = LinearRegression()
        # model.fit(x, y)
        # MODELS_FILEPATH = os.path.join("news_app", "static", "resources", "saved_models")
        # pickle_filename = f"pickle_model_{desk}.pkl"
        # with open(os.path.join(MODELS_FILEPATH, pickle_filename), "wb") as file:
        #     pickle.dump(model, file)

        # Open saved models
        MODELS_FILEPATH = os.path.join("news_app", "static", "resources", "saved_models")
        pickle_filename = f"pickle_model_{desk}.pkl"
        with open(os.path.join(MODELS_FILEPATH, pickle_filename), "rb") as file:
            model = pickle.load(file)
        
        x_trace = [-1, 1]
        y_trace = [model.predict([[-1]])[0], model.predict([[1]])[0]]

        line_trace = {
            "x": x_trace,
            "y": y_trace,
            "mode": "lines",
            "line": {
                "color": lines_colors_dict[desk],
                "width": 2,
            },
            "legendgroup": desk,
            "name": desk,
            "showlegend": True,
            'text': df["news_desk"].loc[df["news_desk"] == desk],
            "hovertemplate": '%{text}<extra></extra>',
        }
        plot_data.append(line_trace)

    plot_layout = {
        "title": "Article vs Headline Score",
        "xaxis": {
            "title": {
                "text": "Headline Scores",
            },
        },
        "yaxis": {
            "title": {
                "text": "Article Scores",
            },
        },
        "hovermode": "closest",
    }

    data = json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder)
    layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return data, layout

def calendar_heatmap():
    
    cal_heatmap_df = pd.read_csv(os.path.join("news_app", "static", "data", "calendar_heatmap_new.csv"))

    cal_heatmap_df["date"] = cal_heatmap_df["date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    cal_heatmap_df["top_headlines"] = cal_heatmap_df["top_headlines"].apply(lambda x: eval(x))

    df2015 = cal_heatmap_df.loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2015)]
    df2016 = cal_heatmap_df.loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2016)]
    df2017 = cal_heatmap_df.loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2017)]

    color_scale = [
        [0, "darkred"],
        [.1, "darkred"],
        [.1, "firebrick"],
        [.2, "firebrick"],
        [.2, "indianred"],
        [.3, "indianred"],
        [.3, "lightcoral"],
        [.4, "lightcoral"],
        [.4, "mistyrose"],
        [.475, "mistyrose"],
        [.475, "white"],
        [.525, "white"],
        [.525, "honeydew"],
        [.6, "honeydew"],
        [.6, "palegreen"],
        [.7, "palegreen"],
        [.7, "limegreen"],
        [.8, "limegreen"],
        [.8, "forestgreen"],
        [.9, "forestgreen"],
        [.9, "darkgreen"],
        [1, "darkgreen"],
    ]

    trace2015 = {
        "z": df2015["avg_score"],
        "x": df2015["date"],
        "y": df2015["news_desk"],
        "type": "heatmap",
        "colorscale": color_scale,
        "showscale": True,
        "text": df2015["top_headlines"],
        "hovertemplate": '<b>Most emotional %{y} headlines for %{x}</b>:' +
            '<br>%{text.score[0]} | %{text.headline[0]}' +
            '<br>%{text.score[1]} | %{text.headline[1]}' +
            '<br>%{text.score[2]} | %{text.headline[2]}' +
            "<br><b>Today's Average: %{z}</b><extra></extra>", 
        "showlegend": False,
        "name": "",
    }

    trace2016 = {
        "z": df2016["avg_score"],
        "x": df2016["date"],
        "y": df2016["news_desk"],
        "xaxis": "x2",
        "yaxis": "y2",
        "type": "heatmap",
        "colorscale": color_scale,
        "showscale": False,
        "text": df2016["top_headlines"],
        "hovertemplate": '<b>Most emotional %{y} headlines for %{x}</b>:' +
            '<br>%{text.score[0]} | %{text.headline[0]}' +
            '<br>%{text.score[1]} | %{text.headline[1]}' +
            '<br>%{text.score[2]} | %{text.headline[2]}' +
            "<br><b>Today's Average: %{z}</b><extra></extra>", 
        "showlegend": False,
        "name": "",
    }

    trace2017 = {
        "z": df2017["avg_score"],
        "x": df2017["date"],
        "y": df2017["news_desk"],
        "xaxis": "x3",
        "yaxis": "y3",
        "type": "heatmap",
        "colorscale": color_scale,
        "showscale": False,
        "text": df2017["top_headlines"],
        "hovertemplate": '<b>Most emotional %{y} headlines for %{x}:</b>' +
            '<br>%{text.score[0]} | %{text.headline[0]}' +
            '<br>%{text.score[1]} | %{text.headline[1]}' +
            '<br>%{text.score[2]} | %{text.headline[2]}' +
            "<br><b>Today's Average: %{z}</b><extra></extra>", 
        "showlegend": False,
        "name": "",
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

    # # Create heatmap csv
    # df = pd.read_csv(os.path.join("news_app", "static", "data", "headlines_scores_keywords.csv"))

    # df["dates"] = df["pub_date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    # news_desks = []
    # dates = []
    # avg_day_scores = []
    # top_headlines = []
    # for desk in df["news_desk"].unique():
    #     for day in df["dates"].unique():
    #         headlines_dict = {
    #             "headline": ["None", "None", "None"],
    #             "score": [0, 0, 0]
    #         }
    #         filtered_df = df.loc[(df["dates"] == day) & (df["news_desk"] == desk) & (df["headline_score"] !=0)]
    #         # print(filtered_df)
    #         if filtered_df["headline_score"].to_list():
    #             avg_day_scores.append(filtered_df["headline_score"].mean())
    #             top_headlines_df = filtered_df.nlargest(3, "abs_headline_score")
    #             for i in range(0, 3):
    #                 if len(top_headlines_df["headline"].to_list()) >= (i + 1):
    #                     headlines_dict["headline"][i] = top_headlines_df["headline"].to_list()[i]
    #                 if len(top_headlines_df["headline_score"].to_list()) >= (i + 1):
    #                     headlines_dict["score"][i] = top_headlines_df["headline_score"].to_list()[i] 
    #             top_headlines.append(headlines_dict)
    #         else:
    #             avg_day_scores.append(0)

    #         dates.append(day)
    #         news_desks.append(desk)


    # cal_heatmap_df_new = pd.DataFrame(
    #     list(zip(
    #         dates, 
    #         news_desks, 
    #         avg_day_scores,
    #         top_headlines,
    #     )),
    #     columns=[
    #         "date", 
    #         "news_desk", 
    #         "avg_score",
    #         "top_headlines"
    #     ])

    # cal_heatmap_df_new.to_csv(os.path.join("news_app", "static", "data", "calendar_heatmap_new2.csv"), index=False, encoding="utf-8-sig")
    # print(cal_heatmap_df_new.head(100))

def box_plots(df_in):
    # Read in data
    # df = pd.read_csv(FILE_PATH)

    df = df_in[["article_score", "news_desk"]].loc[
        (df_in["article_score"] != 0) & 
        (df_in["section_name"] != "Business Day") &
        (df_in["news_desk"] != "Media") &
        (df_in["news_desk"] != "National")
    ]
    # ['National' 'Business' 'Politics' 'Science' 'Climate']
    
    # Box colors
    box_colors_dict = { 
        "Society": "dodgerblue",
        "Business": "gold",
        "Politics": "firebrick",
        "Science": "forestgreen",
        "Climate": "darkorange",
        "Arts&Leisure": "blueviolet",
    }

    df["markers_colors"] = df["news_desk"].map(box_colors_dict)

    plot_data = []

    for desk in df["news_desk"].unique():
        scatter_trace = {
            "y": df["article_score"].loc[df["news_desk"] == desk],
            "type": "box",
            "name": desk,
            "marker": {
                "color": box_colors_dict[desk],
            },
            "boxpoints": "outliers",
            "showlegend": True,
        }
        plot_data.append(scatter_trace)

        plot_layout = {
            "title": "Article Score Statistics",
            "hovermode": "closest",
        }

    boxplot_data = json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder)
    boxplot_layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)
    
    return boxplot_data, boxplot_layout

def lat_lon_heatmap():
    GEOCODE_DATA = os.path.join("news_app", "static", "data", "geocoded_headlines_scores_keywords.csv")
    df = pd.read_csv(GEOCODE_DATA).dropna(how="any")

        def location(x):
        location_details = (
            x.replace("'", "$")
            .replace('"', "'")
            .replace("$", '"')
            .replace("""'Provence-Alpes-Côte d"Azur'""", '"Provence-Alpes-Côte dAzur"')
            .replace(
                """'Commune Petite Rivière de l"Artibonite'""",
                '"Commune Petite Rivière de lArtibonite"',
            )
        )
        location_dict = json.loads(location_details)
        location_string = ""
        if location_dict["city"]:
            location_string += location_dict["city"] + ", "
        if location_dict["state"]:
            location_string += location_dict["state"] + ", "
        if location_dict["country"]:
            location_string += location_dict["country"]
        return location_string
    
    df["latitude"] = df["lat_lon"].apply(lambda x: eval(x)[0])
    df["longitude"] = df["lat_lon"].apply(lambda x: eval(x)[1])
    df["date"] = df["pub_date"].apply(lambda x: datetime.strptime(x, "%m/%d/%Y"))
    df["month"] = df["date"].apply(lambda x: x.to_period("M"))
    df["month_str"] = df["month"].apply(lambda x: str(x))
    df["location_details_dict"] = df["location_details"].apply(lambda x: location(x))
    print(df.head())

    fig2 = px.scatter_mapbox(
        df,
        lon="longitude",
        lat="latitude",
        custom_data=["headline", "location_details_dict", "article_score"],
        color="article_score",
        color_continuous_scale="rdylgn",
        opacity=0.6,
        mapbox_style="light",
        zoom=1,
        hover_name="headline",
        hover_data={
            "article_score": True,
            "longitude": False,
            "latitude": False,
            "month_str": False,
        },
        animation_frame="month_str",
        height=500,
        width=800,
        center={"lat": 35, "lon": -60},
    )

    fig2.update_traces(
        mode="markers",
        marker={"size": 18,},
        hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Article Score: %{customdata[2]:.4f}",
    )

    fig2.update_layout(
        margin={"t": 5, "b": 5, "l": 5, "r": 5},
        mapbox_accesstoken=mapbox_token,
        sliders=[{"currentvalue": {"prefix": "Month: "}}],
    )

    fig2.update_coloraxes(colorbar_title={"text": "Article Sentiment"},)

    fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

    fig_json2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return fig_json2