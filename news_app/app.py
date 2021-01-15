from flask import Flask, jsonify, render_template, request, make_response
import requests

from news_app.plots import article_vs_headline_plot #, calendar_heatmap

# from news_app.sentiment import get_scores


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

    
  
@app.route("/visualizations")
def visualizations():
    article_headline_data, article_headline_layout = article_vs_headline_plot()
    # heatmap_data = calendar_heatmap()

    return render_template(
        "visualizations.html", 
        article_headline_data=article_headline_data, 
        article_headline_layout=article_headline_layout,
        # heatmap_data=heatmap_data,
  )


@app.route("/interactive")
def interactive():
    return render_template("interactive.html")
