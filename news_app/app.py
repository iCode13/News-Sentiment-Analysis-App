from flask import Flask, jsonify, render_template, request, make_response
import requests
import pandas as pd
import os
from datetime import datetime

from news_app.plots import article_vs_headline_plot, calendar_heatmap

# from news_app.sentiment import get_scores

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

    
  
@app.route("/visualizations")
def visualizations():
    # Read in data
    FILE_PATH = os.path.join("news_app", "static", "data", "headlines_scores_keywords.csv")
    df = pd.read_csv(FILE_PATH)
    # df["datetime"] = df["pub_date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    
    article_headline_data, article_headline_layout = article_vs_headline_plot(df)
    calendar_heatmap_data, calendar_heatmap_layout = calendar_heatmap()

    return render_template(
        "visualizations.html", 
        article_headline_data=article_headline_data, 
        article_headline_layout=article_headline_layout,
        calendar_heatmap_data=calendar_heatmap_data,
        calendar_heatmap_layout=calendar_heatmap_layout,
  )


@app.route("/analyzer")
def analyzer():
    return render_template("analyzer.html")
