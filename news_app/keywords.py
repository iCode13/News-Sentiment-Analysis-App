import os
import pandas as pd
from nltk import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ftfy import fix_text
from tabulate import tabulate

def keywords(FILE_NAME):
    # ------Read in news data--------
    df = pd.read_csv(FILE_NAME)

    # --------Extract keywords to columns----------
    # Create list of keywords as strings
    keywords = df["keywords"].tolist()

    # keyword names: 'organizations', 'persons', 'subject', 'glocations', 'creative_works'
    organizations = []
    persons = []
    subject = []
    glocations = []
    creative_works = []

    for i in range(0, 305):
        print(i if (not (i % 50)) else "", end="|") 
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
    
    return

FILE_NAME_RAW = os.path.join("static", "data", "headlines.csv")
keywords(FILE_NAME_RAW)