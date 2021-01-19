# set up and dependencies
import pandas as pd
import re
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
from flask import Flask, jsonify, render_template

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__)

PATH = os.path.join("..", "data", "files", "headlines_with_nid.csv")

def load_data():
    df = pd.read_csv(PATH)
    df = df[df["lead_paragraph"].notna()]
    return df

def plot_data():

    data = load_data()

    # Read news article data into dataframe and exclude rows with NaN in "lead_paragraph" column (200+ rows excluded)
    df = pd.read_csv(PATH)
    df = df[df["lead_paragraph"].notna()]

    # Choose which category to analyze for nGrams
    abstract = df["abstract"]
    headline = df["headline"]
    lead = df["lead_paragraph"]

    nltk.download("stopwords")
    stoplist = stopwords.words("english")

    # Get nGrams: (2, 2) for bigrams, (3, 3) for trigrams...
    vectorizer = CountVectorizer(stop_words=stoplist, ngram_range=(3, 3))
    X = vectorizer.fit_transform(headline)
    features = vectorizer.get_feature_names()
    print("X : \n", X.toarray())

    # Getting top ranking features
    sums = X.sum(axis=0)
    data = []
    for col, term in enumerate(features):
        data.append((term, sums[0, col]))
    ranking = pd.DataFrame(data, columns=["term", "rank"])
    words = ranking.sort_values("rank", ascending=False)
    print("Words : \n", words.head(20))

    # Select top 50 nGrams and add to new dataframe
    rank_df = words.head(n=50)

    return rank_df

##################################################################
    # Original plot before refactoring for JS Plotly: nGram bubble chart
def create_plot():

    fig = px.scatter(
        plot_data(),
        x="term",
        y="rank",
        hover_name="term",
        log_y=True,
        # text="term",
        size="rank",
        color="term",
        size_max=45,
        template="plotly_white",
        title="Trigram similarity and frequency",
        labels={"words": "Avg. Length<BR>(words)"},
        color_continuous_scale=px.colors.sequential.Sunsetdark,
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="Gray")))
    fig.update_xaxes(visible=True)
    fig.update_yaxes(visible=True)

    fig.show()

##################################################################
# Refactor to work with required JS Plotly format
def new_plot():

    data = plot_data()
    # term = data["term"]
    # rank = data["rank"]

    print("This is a test")
    # print(data["term"])

    # trace1 = {
    #     "x": [d["term"] for d in data],
    #     "y": [d["rank"] for d in data],
    #     "name": "Total Tests"
    # }

    trace1 = {
        "x": data["term"],
        "y": data["rank"],
        "mode": "markers",
        "marker": {
            "colorscale": "Jet", # or "Greens", "Greys", "Electric", "Earth"
            "size": "rank",
            # "size_max": 45,
        },

    }

    data_to_plot = [trace1,]

    plot_layout = {
        "title": "Trigram similarity and frequency",
        "height": 700,
        "width": 900,
    }

    data = json.dumps(data_to_plot, cls=plotly.utils.PlotlyJSONEncoder)
    layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return data, layout
##################################################################

# plot_data()
new_plot()
# create_plot()

# For reference, this is Ed's example for flask app, from p6w-6-python-only (app.py).
# Using this to test deployment and see plot results.

@app.route("/")
def home():
    data, layout = new_plot()
    return render_template("index.html", data=data, layout=layout)

@app.route("/express")
def express():
    fig = create_plot()
    return render_template("express.html", fig=fig)

if __name__ == "__main__":
    app.run(debug=True)