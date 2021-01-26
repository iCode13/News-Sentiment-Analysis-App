import json
import plotly
import os
import json
import calmap
import pandas as pd
from datetime import datetime

# Create heatmap csv
df = pd.read_csv(os.path.join("static", "data", "headlines_scores_keywords.csv"))

df["dates"] = df["pub_date"].apply(lambda x: datetime.strptime(x, "%m/%d/%Y"))

news_desks = []
dates = []
avg_day_scores = []
top_headlines = []

test_desk = ["Arts&Leisure"]
test_day = datetime.strptime("")

for desk in df["news_desk"].unique():
    print(f"Working on {desk} news")
    for day in df["dates"].unique():
        headlines_dict = {
            "headline": ["None", "None", "None"],
            "score": [0, 0, 0]
        }
        filtered_df = df.loc[(df["dates"] == day) & (df["news_desk"] == desk) & (df["headline_score"] !=0)]
        if filtered_df["headline_score"].to_list():
            avg_day_scores.append(filtered_df["headline_score"].mean())
            top_headlines_df = filtered_df.nlargest(3, "abs_headline_score")
            i = 0
            for index, article in top_headlines_df.iterrows():
                headlines_dict["headline"][i] = article["headline"]
                headlines_dict["score"][i] = article["headline_score"]
                i += 1
            top_headlines.append(headlines_dict)
        #     for i in range(0, 3):
        #         if len(top_headlines_df["headline"].to_list()) >= (i + 1):
        #             headlines_dict["headline"][i] = top_headlines_df["headline"].to_list()[i]
        #         if len(top_headlines_df["headline_score"].to_list()) >= (i + 1):
        #             headlines_dict["score"][i] = top_headlines_df["headline_score"].to_list()[i] 
        #     top_headlines.append(headlines_dict)
        else:
            avg_day_scores.append(0)
            top_headlines.append(headlines_dict)

        dates.append(day)
        news_desks.append(desk)


cal_heatmap_df = pd.DataFrame(
    list(zip(
        dates, 
        news_desks, 
        avg_day_scores,
        top_headlines,
    )),
    columns=[
        "date", 
        "news_desk", 
        "avg_score",
        "top_headlines"
    ])

print(cal_heatmap_df)

cal_heatmap_df.to_csv(os.path.join("static", "data", "calendar_heatmap_new2.csv"), index=False, encoding="utf-8-sig")
