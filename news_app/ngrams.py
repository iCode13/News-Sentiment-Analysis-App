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

# app = Flask(__name__)

PATH = os.path.join("data", "files", "headlines_with_nid.csv")

##################################################################
def load_data():
    df = pd.read_csv(PATH)
    df = df[df["lead_paragraph"].notna()]
    return df

##################################################################
def trigram_data():

    data = load_data()

    # Read news article data into dataframe and exclude rows with NaN in "lead_paragraph" column (200+ rows excluded)
    df = pd.read_csv(PATH)
    df = df[df["lead_paragraph"].notna()]

    # Choose which category to analyze for nGrams
    abstracts = df["abstract"]
    headlines = df["headline"].astype(str)
    lead = df["lead_paragraph"]

    nltk.download("stopwords")
    stoplist = stopwords.words("english")

    # Get nGrams: (2, 2) for bigrams, (3, 3) for trigrams...
    vectorizer = CountVectorizer(stop_words=stoplist, ngram_range=(3, 3))
    X = vectorizer.fit_transform(headlines)
    features = vectorizer.get_feature_names()
    # print("\n\nX : \n", X.toarray())

    # Applying TFIDF 
    vectorizer2 = TfidfVectorizer(stop_words=stoplist, ngram_range = (3,3)) 
    X2 = vectorizer2.fit_transform(headlines)
    features2 = vectorizer2.get_feature_names()
    scores = (X2.toarray()) 
    # print("\n\nX2 : \n", scores)

    # Getting top ranking features
    sums = X2.sum(axis=0)
    data1 = []
    for col, term in enumerate(features2):
        data1.append((term, sums[0, col]))
    ranking = pd.DataFrame(data1, columns=["term", "rank"])
    words = ranking.sort_values("rank", ascending=False)
    # print("\n\nWords : \n", words.head(20))

    # Select top 50 nGrams and add to new dataframe
    trigram_df = words.head(n=50)

    return trigram_df

##################################################################
# Refactor to work with required JS Plotly format
def trigram_plot():

    df_data = trigram_data()
    term = df_data["term"]
    frequency = df_data["rank"]
    # section = df_data["section_name"]

    trace1 = {
        "x": term,
        "y": frequency,
        "mode": "markers",
        "text": term,
        "marker": {
            # "color": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], # or "Greens", "Greys", "Electric", "Earth"
            "color": frequency,
            "size": frequency,
            "sizeref": 0.1,
            "sizemode": 'area',
            "opacity": 1,
        },
    }

    data_to_plot = [trace1,]

    plot_layout = {
        "title": "Trigram frequency",
        "autosize": "false",
        "height": 700,
        "width": 1200,
        "margin": {
          "l": 50,
          "r": 50,
          "b": 200,
          "t": 100,
          "pad": 4
        },
        "xaxis": {
            "title": 'Trigrams',
            "margin": "true",
            "tickangle": 45,
            "titlefont": {
                "family": 'Arial, bold',
                "size": 18,
                "color": 'black'
                },
            },
        "yaxis": {
            "title": 'Frequency Count',
            "automargin": "true",
            # "type": "log",
            "titlefont": {
                "family": 'Arial, sans-serif',
                "size": 18,
                "color": 'black'
                },
            }
    }

    tri_data = json.dumps(data_to_plot, cls=plotly.utils.PlotlyJSONEncoder)
    tri_layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return tri_data, tri_layout

##################################################################
def quadgram_data():

    data = load_data()

    # Read news article data into dataframe and exclude rows with NaN in "lead_paragraph" column (200+ rows excluded)
    df = pd.read_csv(PATH)
    df = df[df["lead_paragraph"].notna()]

    # Choose which category to analyze for nGrams
    abstracts = df["abstract"]
    headlines = df["headline"].astype(str)
    lead = df["lead_paragraph"]

    nltk.download("stopwords")
    stoplist = stopwords.words("english")

    # Get nGrams: (2, 2) for bigrams, (3, 3) for trigrams...
    vectorizer = CountVectorizer(stop_words=stoplist, ngram_range=(2, 3))
    X = vectorizer.fit_transform(headlines)
    features1 = vectorizer.get_feature_names()
    # print("\n\nX : \n", X.toarray())

    # Applying TFIDF 
    vectorizer2 = TfidfVectorizer(stop_words=stoplist, ngram_range = (2, 3)) 
    X2 = vectorizer2.fit_transform(headlines)
    features2 = vectorizer2.get_feature_names()
    scores = (X2.toarray()) 
    # print("\n\nX2 : \n", scores)

    # Getting top ranking features
    sums = X2.sum(axis=0)
    data1 = []
    for col, term in enumerate(features2):
        data1.append((term, sums[0, col]))
    ranking = pd.DataFrame(data1, columns=["term", "rank"])
    words = ranking.sort_values("rank", ascending=False)
    # print("\n\nWords : \n", words.head(20))

    # Select top 50 nGrams and add to new dataframe
    quadgram_df = words.head(n=50)

    return quadgram_df

##################################################################
# Refactor to work with required JS Plotly format
def quadgram_plot():

    df_data = quadgram_data()
    term = df_data["term"]
    frequency = df_data["rank"]
    # section = df_data["section_name"]

    trace1 = {
        "x": term,
        "y": frequency,
        "mode": "markers",
        "text": term,
        "marker": {
            # "color": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], # or "Greens", "Greys", "Electric", "Earth"
            "color": frequency,
            "size": frequency,
            "sizeref": 0.1,
            "sizemode": 'area',
            "opacity": 1,
        },
    }

    data_to_plot = [trace1,]

    plot_layout = {
        "title": "Bigrams and Trigrams, Oh My!",
        "autosize": "false",
        "height": 700,
        "width": 1200,
        "margin": {
          "l": 50,
          "r": 50,
          "b": 200,
          "t": 100,
          "pad": 4
        },
        "xaxis": {
            "title": 'Bigrams and Trigrams',
            "margin": "true",
            "tickangle": 45,
            "titlefont": {
                "family": 'Arial, bold',
                "size": 18,
                "color": 'black'
                },
            },
        "yaxis": {
            "title": 'Frequency Count',
            "automargin": "true",
            # "type": "log",
            "titlefont": {
                "family": 'Arial, sans-serif',
                "size": 18,
                "color": 'black'
                },
            }
    }

    quad_data = json.dumps(data_to_plot, cls=plotly.utils.PlotlyJSONEncoder)
    quad_layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return quad_data, quad_layout

##################################################################

trigram_plot()
quadgram_plot()

##################################################################
# For reference, this is Ed's example for flask app, from p6w-6-python-only (app.py).
# Using this to test deployment and see plot results.

# @app.route("/")
# def home():
#     tri_data, tri_layout = trigram_plot()
#     return render_template("index.html", data=tri_data, layout=tri_layout)

# @app.route("/quadgram")
# def quadgram():
#     quad_data, quad_layout = quadgram_plot()
#     return render_template("quadgram.html", data=quad_data, layout=quad_layout)

# if __name__ == "__main__":
#     app.run(debug=True)