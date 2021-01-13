import json
import plotly

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