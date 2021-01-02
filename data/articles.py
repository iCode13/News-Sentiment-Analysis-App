import os
from pynytimes import NYTAPI
import pandas as pd
import datetime

key = os.getenv("api-key")

nyt = NYTAPI(key)

# this pulls one month of articles at a time
data = nyt.archive_metadata(
    date = datetime.datetime(2019, 1, 1)
)

df = pd.DataFrame(data)

pd.options.display.max_columns = 999

df.to_csv("data/combined_fiction.csv", index=False)

# print(df.tail())
# print(df.shape[0])