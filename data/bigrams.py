# set up and dependencies
import pandas as pd
import re
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

nltk.download("stopwords")

pd.set_option("display.max_rows", None)

path = "files/headlines.csv"

df = pd.read_csv(path)

# Bigrams
# Use TF-IDF method to generate bigrams and trigrams
txt1 = df["abstract"]
txt2 = df["headline"]

stoplist = stopwords.words("english")

# Get ABSTRACT bigrams
# vectorizer1 = CountVectorizer(stop_words=stoplist, ngram_range=(2, 2))
# X1 = vectorizer1.fit_transform(txt1)
# features = vectorizer1.get_feature_names()
# print("X1 : \n", X1.toarray())

# GET ABSTRACT bigrams - Applying TFIDF
# vectorizer2 = TfidfVectorizer(stop_words=stoplist, ngram_range=(2, 2))
# X2 = vectorizer2.fit_transform(txt1)
# scores = X2.toarray()
# print("Scores : \n", scores)

# Get HEADLINE bigrams
vectorizer3 = CountVectorizer(stop_words=stoplist, ngram_range=(2, 2))
X3 = vectorizer3.fit_transform(txt2)
features = vectorizer3.get_feature_names()
print("X1 : \n", X3.toarray())

# Get HEADLINE trigrams
# vectorizer3 = CountVectorizer(stop_words=stoplist, ngram_range=(3, 3))
# X3 = vectorizer3.fit_transform(txt1)
# features = vectorizer3.get_feature_names()
# print("X1 : \n", X1.toarray())

# Getting top ranking features
sums = X3.sum(axis=0)
data1 = []
for col, term in enumerate(features):
    data1.append((term, sums[0, col]))
ranking = pd.DataFrame(data1, columns=["term", "rank"])
words = ranking.sort_values("rank", ascending=False)
print("Words : \n", words.head(20))

rank_df = words.head(n=50)

# Plots
rank_df.plot(x="term", y="rank", style="o", rot=90)

# Bigram bubble chart
fig = px.scatter(
    rank_df,
    x="term",
    y="rank",
    hover_name="term",
    text="term",
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

# Scatter plot of n-grams
trigram = rank_df["term"]
rank = rank_df["rank"]

fig = go.Figure(
    data=go.Scattergl(
        x=trigram,
        y=rank,
        mode="markers",
        marker=dict(color=rank, colorscale="Viridis", line_width=1),
    )
)
fig.show()

# Bigram TF-IDF Logistic Regression
# bigram_tfidf_logistic_regression = make_pipeline(
#     CountVectorizer(
#         stop_words='english',
#         ngram_range=(1,2)
#     ),
#     TfidfTransformer(),
#     LogisticRegression()
# )

# bigram_tfidf_logistic_regression.fit(X_train, y_train)

# print(f'Accuracy: {bigram_tfidf_logistic_regression.score(X_test, y_test)} \n')
# print(classification_report(y_test, bigram_tfidf_logistic_regression.predict(X_test)))

