from flask import Flask, jsonify, render_template, request, make_response
import requests
import pandas as pd
import os
from datetime import datetime
import json

from news_app.plots import article_vs_headline_plot, calendar_heatmap
from news_app.sentiment import user_analysis, emotion_plotter

from nltk import data

NLTK_DATA_LOCATION = os.path.join("news_app", "static", "resources", "nltk_data")
data.path.append(NLTK_DATA_LOCATION)
NLTK_DATA_LOCATION = os.path.join(".", "news_app", "static", "resources", "nltk_data")
data.path.append(NLTK_DATA_LOCATION)


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


@app.route("/interactive")
def interactive():
    return render_template("interactive.html")


@app.route("/interactive/user-sentiment", methods=["POST", "GET"])
def user_sentiment():
    print("Running user_sentiment in app.py")
    user_text = request.get_json()
    print(user_text)
    print(type(user_text))

    gauge_data = user_analysis(user_text)
    emotion_plot_data, emotion_plot_layout = emotion_plotter(user_text) 

    response_dict = {
        "gauge_data": gauge_data,
        "emotion_plot_data": emotion_plot_data,
        "emotion_plot_layout": emotion_plot_layout
    }

    response = json.dumps(response_dict)
    return response
