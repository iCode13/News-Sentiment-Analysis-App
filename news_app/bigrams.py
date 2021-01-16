# set up and dependencies
import pandas as pd
import re
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def load_data():
    PATH = os.path.join("..", "data", "files", "headlines_with_nid.csv")
    df = pd.read_csv(PATH)
    df = df[df["lead_paragraph"].notna()]
    return df

def plot_ngrams():

    data = load_data()

    # Read news article data into dataframe and exclude rows with NaN in "lead_paragraph" column (200+ rows excluded)
    df = pd.read_csv(PATH)
    df = df[df["lead_paragraph"].notna()]

    abstract = df["abstract"]
    headline = df["headline"]
    lead = df["lead_paragraph"]

    nltk.download("stopwords")
    stoplist = stopwords.words("english")

    # Get trigrams
    vectorizer = CountVectorizer(stop_words=stoplist, ngram_range=(3, 3))
    X = vectorizer.fit_transform(lead)
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

def create_plot():

    ##################################################################
    # Original plot before refactoring for JS Plotly: nGram bubble chart
    fig = px.scatter(
        rank_df,
        x="term",
        y="rank",
        hover_name="term",
        log_y=True,
        # text="term",
        size="rank",
        color="term",
        size_max=45,
        template="plotly_white",
        title="Bigram similarity and frequency",
        labels={"words": "Avg. Length<BR>(words)"},
        color_continuous_scale=px.colors.sequential.Sunsetdark,
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="Gray")))
    fig.update_xaxes(visible=True)
    fig.update_yaxes(visible=True)

    fig.show()

    ##################################################################
    # Refactor to work with required JS Plotly format
    data = load_data()

    trace1 = {
        "x": [d["term"] for d in data],
        "y": [d["rank"] for d in data],
        "name": "nGram"
    }

    trace1 = {
        "x": [d["term"] for d in data],
        "y": [d["rank"] for d in data],
        "mode": "markers",
        "marker": {
            color_continuous_scale=px.colors.sequential.Sunsetdark,
        }
    }

    plot_data = [trace1, trace2, trace3]

    plot_layout = {
        "title": "Bigram similarity and frequency"
    }

    data = json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder)
    layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return data, layout
    ##################################################################

# For reference, this is Ed's example for flask app:

# @app.route("/")
# def home():
#     data, layout = create_plot()
#     return render_template("index.html", data=data, layout=layout)

# @app.route("/express")
# def express():
#     fig = create_plot_express()
#     return render_template("express.html", fig=fig)

# if __name__ == "__main__":
#     app.run(debug=True)