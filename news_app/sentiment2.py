import os
import pandas as pd
from nltk import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from tabulate import tabulate


def get_article_scores(FILE_NAME):
    # ------Read in news data--------
    df = pd.read_csv(FILE_NAME)

    # -------Sentiment Analysis-------
    # Create list of headlines as strings
    headlines = df["headline"].tolist()

    # Fix encoding issues for non-unicode characters
    for i in range(len(headlines)):
        headlines[i] = fix_text(headlines[i])

    # Create list of article lead paragraphs as strings
    articles = df["lead_paragraph"].tolist()

    # Fix encoding issues for non-unicode characters
    for i in range(len(articles)):
        if isinstance(articles[i], str):
            articles[i] = fix_text(articles[i])
         

    # Instantiate sentiment analyzer (VADER)
    analyzer = SentimentIntensityAnalyzer()

     # Analyze headlines
    headline_scores = []
    for headline in headlines:
        if isinstance(headline, str):
            headline_scores.append(analyzer.polarity_scores(headline)["compound"])
        else:
            headline_scores.append(0)

    # Tokenize articles into sentences and analyze
    # Article score is the average of its sentences' scores
    article_scores = []
    for article in articles:
        if isinstance(article, str):
            sentences = sent_tokenize(article)
            sentence_scores = []
            for sentence in sentences:
                sentence_scores.append(analyzer.polarity_scores(sentence)["compound"])
            article_scores.append(sum(sentence_scores)/len(sentence_scores))
        else:
            article_scores.append(0)

    # --------Extract keywords to columns----------
    # Create list of keywords as strings
    keywords = df["keywords"].tolist()

    # keyword names: 'organizations', 'persons', 'subject', 'glocations', 'creative_works'
    organizations = []
    persons = []
    subject = []
    glocations = []
    creative_works = []

    for i in range(len(keywords)):
        keywords_list = eval(fix_text(keywords[i]))
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


FILE_NAME_RAW = os.path.join("static", "data", "sentiment_test.csv")
FILE_NAME_SCORES = os.path.join("static", "data", "sentiment_scores_test.csv")

get_article_scores(FILE_NAME_RAW).to_csv(FILE_NAME_SCORES, index=False)

# find_articles(FILENAME_SCORES, "glocations", "Virginia")


