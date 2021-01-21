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
# from nltk.tokenize import word_tokenize
# nltk.download('punkt')

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
    abstracts = df["abstract"]
    headlines = df["headline"].astype(str)
    lead = df["lead_paragraph"]

    nltk.download("stopwords")
    stoplist = stopwords.words("english")

    ###############################
    # New method for getting n-grams with frequency counts...

    # f = open(PATH)  # Not sure how to actually get the data for this method since I'm pulling from a csv and originally put directly into a dataframe
    # raw = f.read()  # Gets the whole file, so need to figure out how to tokenize only headlines...
    # # print(raw)
    # print(headline)
    # tokens = headline.apply(nltk.word_tokenize)

    # #Create your bigrams
    # bgs = tokens.apply(nltk.bigrams)  # nltk.bigrams(tokens)
    # print(bgs.values)

    # #compute frequency distribution for all the bigrams in the text
    # fdist = bgs.apply(nltk.FreqDist)  # nltk.FreqDist(bgs)
    # print(fdist)
    # # for k,v in fdist.items():
    #     print(k,v)

    ###############################
    # Original method for getting n-grams and frequency count or rank

    # Get nGrams: (2, 2) for bigrams, (3, 3) for trigrams...
    vectorizer = CountVectorizer(stop_words=stoplist, ngram_range=(3, 3))
    X = vectorizer.fit_transform(headlines)
    features = vectorizer.get_feature_names()
    # df = pd.DataFrame(X, columns=features).sum(axis=1) # Ed's suggestion for getting trigrams and number of occurrences
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
# def create_plot():

#     fig = px.scatter(
#         plot_data(),
#         x="term",
#         y="rank",
#         hover_name="term",
#         log_y=True,
#         # text="term",
#         size="rank",
#         color="term",
#         size_max=45,
#         template="plotly_white",
#         title="Trigram similarity and frequency",
#         labels={"words": "Avg. Length<BR>(words)"},
#         color_continuous_scale=px.colors.sequential.Sunsetdark,
#     )
#     fig.update_traces(marker=dict(line=dict(width=1, color="Gray")))
#     fig.update_xaxes(visible=True)
#     fig.update_yaxes(visible=True)

#     fig.show()

##################################################################
# Refactor to work with required JS Plotly format
def new_plot():

    df_data = plot_data()
    term = df_data["term"]
    rank = df_data["rank"]
    # section = df_data["section_name"]

    trace1 = {
        "x": term,
        "y": rank,
        "mode": "markers",
        "text": term,
        "marker": {
            # "color": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], # or "Greens", "Greys", "Electric", "Earth"
            "color": rank,
            "size": rank,
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