# set up dependencies
import pandas as pd
pd.set_option('display.max_rows', None)

path = "files/headlines.csv"

df = pd.read_csv(path)

df.head()