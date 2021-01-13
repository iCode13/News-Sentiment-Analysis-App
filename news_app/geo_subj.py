import os
import pandas as pd
from ftfy import fix_text
from tabulate import tabulate
import json


def get_location_subject():
    # Read in news data
    FILE_NAME = os.path.join("static", "data", "sentiment_test.csv")
    df = pd.read_csv(FILE_NAME)

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

    df_keywords = pd.DataFrame(
        list(zip(
            df["headline"].tolist(), 
            organizations, 
            persons, 
            subject,
            glocations,
            creative_works,
        )),
        columns=[
            "headline", 
            "organizations", 
            "persons", 
            "subject", 
            "glocations",
            "creative_works",
        ]
    )

    # print(tabulate(df_keywords, headers="keys"))
    return df_keywords

def find_articles(df, keyword_type, find):
    find_df = df.loc[df[keyword_type].apply(lambda x: search_column(x, find))]
    print(tabulate(find_df, headers="keys"))
    return find_df

def search_column(items, search_string):
    found = False
    for item in items:
        if search_string.lower() in item.lower():
            found = True
    return found

df_keywords = get_location_subject()


find_articles(df_keywords, "subject", "Gun")

