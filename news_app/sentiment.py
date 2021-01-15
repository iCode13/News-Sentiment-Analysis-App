import os
import pandas as pd
from nltk import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from tabulate import tabulate
import json
from nrclex import NRCLex
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk import data
from nltk.corpus import wordnet as wn

# NLTK_DATA_LOCATION = os.path.join("static", "resources", "nltk_data")
# data.path.append(NLTK_DATA_LOCATION)
# print(nltk.data.path)
# print(nltk.corpus)



def get_article_scores(FILE_NAME):
    # ------Read in news data--------
    df = pd.read_csv(FILE_NAME)

    # -------Sentiment Analysis-------
    # Create list of headlines as strings
    headlines = df["headline"].tolist()

    # Fix encoding issues for non-unicode characters
    print("\n\nFixing headlines...")
    for i in range(len(headlines)):
        if (not (i % 5000)):
            print(f"Fixing headline {i}")
        headlines[i] = fix_text(headlines[i])

    # Create list of article lead paragraphs as strings
    articles = df["lead_paragraph"].tolist()

    # Fix encoding issues for non-unicode characters
    print("\n\nFixing articles...")
    for i in range(len(articles)):
        if (not (i % 5000)):
            print(f"Fixing article {i}")
        if isinstance(articles[i], str):
            articles[i] = fix_text(articles[i])
         

    # Instantiate sentiment analyzer (VADER)
    analyzer = SentimentIntensityAnalyzer()

    # Analyze headlines
    print("\n\nScoring headlines...")
    headline_scores = []
    for headline in headlines:
        if isinstance(headline, str):
            headline_scores.append(analyzer.polarity_scores(headline)["compound"])
        else:
            headline_scores.append(0)

    # Tokenize articles into sentences and analyze
    # Article score is the average of its sentences' scores
    print("\n\nScoring articles...")
    article_scores = []
    for article in articles:
        if isinstance(article, str):
            sentences = sent_tokenize(article)
            sentence_scores = []
            for sentence in sentences:
                sentence_scores.append(analyzer.polarity_scores(sentence)["compound"])
            if len(sentence_scores):
                article_scores.append(sum(sentence_scores)/len(sentence_scores))
            else:
                article_scores.append(0)
        else:
            article_scores.append(0)

    # --------Extract keywords to columns----------
    # Create list of keywords as strings
    print("\n\nExtracting keywords...")
    keywords = df["keywords"].tolist()

    # keyword names: 'organizations', 'persons', 'subject', 'glocations', 'creative_works'
    organizations = []
    persons = []
    subject = []
    glocations = []
    creative_works = []

    for i in range(len(keywords)):
        if (not (i % 5000)):
            print(f"Keywords for article {i}") 
        text = keywords[i].replace("â€™", "").replace("’", "")
        keywords_list = eval(fix_text(text))
        keyword_dict = {
            "organizations": [],
            "persons": [],
            "subject": [],
            "glocations": [],
            "creative_works": [],
        }
        for keyword in keywords_list:
            keyword_dict[keyword["name"]].append(keyword["value"])
        organizations.append(keyword_dict["organizations"])
        persons.append(keyword_dict["persons"])
        subject.append(keyword_dict["subject"])
        glocations.append(keyword_dict["glocations"])
        creative_works.append(keyword_dict["creative_works"])

    # -----Compile headline and article data into new dataframe--------
    print("\n\nCompiling dataframe headlines...")
    df_scores = pd.DataFrame(
        list(zip(
            headlines, 
            articles, 
            headline_scores, 
            article_scores,
            df["pub_date"].tolist(),
            df["section_name"].tolist(),
            df["news_desk"].tolist(),
            organizations, 
            persons, 
            subject,
            glocations,
            creative_works,
        )),
        columns=[
            "headline", 
            "article", 
            "headline_score", 
            "article_score", 
            "pub_date",
            "section_name",
            "news_desk",
            "organizations", 
            "persons", 
            "subject", 
            "glocations",
            "creative_works",
        ]
    )

    print(tabulate(df_scores.head(), headers="keys"))
    return df_scores


def find_articles(FILE_NAME, keyword_type, find):
    df = pd.read_csv(FILE_NAME)
    find_df = df.loc[df[keyword_type].apply(lambda x: search_column(x, find))]
    print(tabulate(find_df, headers="keys"))
    return find_df

def search_column(items, search_string):
    found = False
    for item in items:
        if search_string.lower() in item.lower():
            found = True
    return found


def user_analysis(text):
    # Instantiate sentiment analyzer (VADER)
    analyzer = SentimentIntensityAnalyzer()
    overall_sentiment = analyzer.polarity_scores(text)["compound"]

    gauge_data = [{
        "domain": {"x": [0, 1], "y": [0, 1]},
        "value": overall_sentiment,
        "title": {"text": "Overall Sentiment"},
        "type": "indicator",
        "mode": "gauge+number+delta",
        "gauge": {
            "axis": {
                "range": [-1, 1],
                "nticks": 10,
            },
            "bar": {"color": "midnightblue"},
            "steps": [
                {"range": [-1, -.6], "color": "firebrick"},
                {"range": [-.6, -.2], "color": "darkorange"},
                {"range": [-.2, .2], "color": "gold"},
                {"range": [.2, .6], "color": "yellowgreen"},
                {"range": [.6, 1.1], "color": "forestgreen"},
            ],
            "shape": "angular",
        },
    }]

    return gauge_data

def emotion_plotter(text):
    # text = "Astronaut science is best most perfect great thing"
    print(text)

    # ---EMOTION ANALYSIS---
    # Tokenize text
    text_tokens = []
    text_tokens.append(regexp_tokenize(text.lower(), "[\w']+")) 
    # print(text_tokens[0])

    # Remove stop words and assign part of speech
    filtered_tokens = []
    for token in text_tokens[0]:
        if token not in stopwords.words('english'):
            filtered_tokens.append(pos_tag(word_tokenize(token)))
    # print(filtered_tokens)

    # Lemmatize words (identify base words from other forms of the word)
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = []
    morphy_tag = {'NN':'n', 'JJ':'a', 'VB':'v', 'RB':'r'}
    for token in filtered_tokens:
        for word, tag in token:
            if tag in morphy_tag.keys():
                morphy_pos = morphy_tag[tag]
            else:
                pos = ''
            if morphy_pos in ["a", "n", "v"]:
                lemmatized_tokens.append(lemmatizer.lemmatize(word, pos=morphy_pos))
            else:
                lemmatized_tokens.append(lemmatizer.lemmatize(word))
    # print(lemmatized_tokens)
        
    # Join lemmatized words back into sentence
    lemmatized_text = " ".join(lemmatized_tokens)
    print(lemmatized_text)

    print
    # Get emotions
    text_object = NRCLex(lemmatized_text)
    # print(text_object.words)
    # print(text_object.affect_dict)
    # print(text_object.raw_emotion_scores)
    # print(text_object.affect_frequencies)

    # Create emotion data for plot
    emotion_data = {"words": [], "emotions": []}
    for word, emotions in text_object.affect_dict.items():
        for emotion in emotions:
            emotion_data["words"].append(word)
            emotion_data["emotions"].append(emotion.title())

    print(emotion_data)

    emotion_trace = {
        "x": emotion_data["words"],
        "y": emotion_data["emotions"],
        "mode": "markers",
        "marker": {"size": 40, "color": "midnightblue",}
    }

    emotion_plot_data = [emotion_trace]

    emotion_plot_layout = {
        "xaxis": {
            "type": "category",
            "title": "Your Words",
        },
        "yaxis": {
            "type": "category",
            "title": "Emotions",
            "categoryorder": "array",
            "categoryarray": [
                "Disgust", 
                "Anger", 
                "Fear", 
                "Sadness", 
                "Negative",
                "Anticipation",
                "Positive",
                "Surprise",
                "Trust",
                "Joy",
            ]
        }
    }

    return emotion_plot_data, emotion_plot_layout

# FILE_NAME_RAW = os.path.join("static", "data", "headlines.csv")
# FILE_NAME_SCORES = os.path.join("static", "data", "headlines_scores_keywords.csv")

# get_article_scores(FILE_NAME_RAW).to_csv(FILE_NAME_SCORES, index=False, encoding="utf-8-sig")

# find_articles(FILENAME_SCORES, "glocations", "Virginia")





