import os
from pynytimes import NYTAPI
import pandas as pd
import datetime
import time
from pprint import pprint

# import api key
key = os.getenv("api-key")

# set up wrapper for API calls
nyt = NYTAPI(key)

# create list of dates for each month from 2015 - 2017
start_date = "2015-01-01"
end_date = "2017-12-01"

date_list = pd.date_range(start_date, end_date, freq="MS")

# convert to python datetime for API calls
dates = list(date_list.to_pydatetime())

# iterate over list of dates, append to list, convert to a dataframe
article_list = []

for date in dates:

    print(f"Processing Date: {date}")

    results = nyt.archive_metadata(date = date)

    for i in results:

        article = {}

        article["abstract"] = i["abstract"]
        article["byline"] = i["byline"]["original"]
        article["document_type"] = i["document_type"]
        article["headline"] = i["headline"]["main"]
        article["keywords"] = i["keywords"]
        article["lead_paragraph"] = i["lead_paragraph"]
        article["news_desk"] = i["news_desk"]
        article["pub_date"] = i["pub_date"]
        article["section_name"] = i["section_name"]
        article["snippet"] = i["snippet"]
        article["source"] = i["source"]
        article["type_of_material"] = i["type_of_material"]
        article["word_count"] = i["word_count"]
        article_list.append(article)

    time.sleep(6)

df = pd.DataFrame(article_list)

df.to_csv("files/nyt_2015_2017.csv", index=False)

pd.options.display.max_columns = 999

print(df.head())
print(len(df["abstract"]))
