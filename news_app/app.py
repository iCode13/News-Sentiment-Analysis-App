from flask import Flask, jsonify, render_template, request, make_response
import requests

from news_app.plots import article_vs_headline_plot 

# from news_app.sentiment import get_scores


app = Flask(__name__)

@app.route("/")
def index():
    data, layout = article_vs_headline_plot()
    return render_template("index.html", article_headline_data=data, article_headline_layout=layout)


@app.route("/visualizations")
def visualizations():
    return render_template("visualizations.html")


@app.route("/analyzer")
def analyzer():
    return render_template("analyzer.html")