import os
import pandas as pd
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.sentiment.util import demo_vader_instance
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import data
# import nltk
from ftfy import fix_text
from nrclex import NRCLex
from tabulate import tabulate

NLTK_DATA_LOCATION = os.path.join("static", "resources", "nltk_data")

data.path.append(NLTK_DATA_LOCATION)

def get_scores():	def get_scores():
    return 	    # Read in sample of headlines
    FILE_NAME = os.path.join("static", "data", "sentiment_test.csv")
    df = pd.read_csv(FILE_NAME)

    # Create list of headlines as strings
    documents = df["headline"].tolist()

    doc_tokens = []
    doc_tokens_filtered = []

    stop_words = set(stopwords.words("english"))

    # Fix encoding issues for non-unicode characters
    # Create word tokens
    for i in range(0, len(documents)):
        documents[i] = fix_text(documents[i])
        doc_tokens.append(regexp_tokenize(documents[i], "[\w']+"))

    # Remove stop words and assign part of speech
    for document in doc_tokens:
        filtered_tokens = []
        for word in document:
            if word.lower() not in stop_words:
                filtered_tokens.append(pos_tag(word_tokenize(word.lower())))
        doc_tokens_filtered.append(filtered_tokens)

    # Lemmatize words (identify base words from other forms of the word)
    lemmatizer = WordNetLemmatizer()
    doc_tokens_lemmatized = []
    for document in doc_tokens_filtered:
        lemmatized_doc = []
        for token in document:
            for word, tag in token:
                if tag.startswith('NN'):
                    pos = 'n'
                elif tag.startswith('VB'):
                    pos = 'v'
                else:
                    pos = 'a'
                lemmatized_doc.append(lemmatizer.lemmatize(word, pos))
        doc_tokens_lemmatized.append(lemmatized_doc)
        # print(lemmatized_doc)
    # print(doc_tokens_lemmatized)        

    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()

    document_scores = []
    for document in doc_tokens_lemmatized:
        word_scores = []
        for word in document:
            word_score = analyzer.polarity_scores(word)
            word_scores.append(word_score["compound"])
        document_scores.append(sum(word_scores)/len(word_scores))
    # print(document_scores)

    sentence_scores = []
    for sentence in documents:
        sentence_scores.append(analyzer.polarity_scores(sentence)["compound"])

    article_scores = []
    for article in df["lead_paragraph"].tolist():
        if isinstance(article, str):
            text = fix_text(article)
            article_scores.append(analyzer.polarity_scores(text)["compound"])
        else:
            article_scores.append(0)

    df_scores = pd.DataFrame(list(zip(documents, doc_tokens_lemmatized, document_scores, sentence_scores, article_scores)), columns=["headline", "tokens", "word score", "sentence score", "article score"])


    print(tabulate(df_scores, headers="keys"))

    return

get_scores()