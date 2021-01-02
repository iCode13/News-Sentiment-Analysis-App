# NY Times Sentiment Analysis Project

## Overview
### Using a dataset of news headlines, perform EDA on sentiment trends

## Data Source
* Option 1: [NY Times Archive API](https://developer.nytimes.com/docs/articlesearch-product/1/overview)
    * Constrain searches by years (e.g. 2015-2017), include election year?
    * Filter by news desk / article category
* Option 2: UC Irvine Machine Learning ["News Aggregator" dataset](http://archive.ics.uci.edu/ml/datasets/News+Aggregator) (420K+ headines, categorized)
* Option 3: ["Million Headlines" dataset](https://www.kaggle.com/therohk/million-headlines) (Australian Broadcasting Corporation news)

## Data Analysis
* Sentiment analysis using... bing lexicon, nrc lexicon, AFIIN lexicon
* Compare sentiment trends across... 
    * days of the week
    * months of the year
    * seasonal events 
        * holidays
        * political elections
        * entertainment seasons
* Compare sentiments between categories of news
    * political
    * business
    * entertainment
    * science

## Visualizations
* Word clouds (most common words for different categories of articles)
* Bar charts for different sentiments (most frequent terms for each sentiment, using NRC lexicon)
* Interactive with user-selected...
    * days of the week
    * article category
    * particular year
* Network diagram showing "bigrams" (two words commonly seen together) 
    * interactive?  
    * let user search for a bigram and see how many times it appears?
* Sentiment heatmap by geography
    * Use byline, Google Maps API, & mapbox for locations
    * Colorscale on AFIIN lexicon result (range -5 to +5)
* [Other Samples](https://www.kaggle.com/xvivancos/analyzing-the-lord-of-the-rings-data) (Lord of the Rings analysis project)

<img src=Readme-Images/wordcloud.png width=250></img>
<img src=Readme-Images/barcharts.png height=400></img>
<img src=Readme-Images/bigrams.png height=400></img>

## Project Elements // Roles & Responsibilities
* Data scraping / cleaning - *Alicia*
* Machine learning algorithm - *All together? Alicia, Amy, David, Rachel*
* Static visualization(s) - *1 each? Alicia, Amy, David, Rachel*
* Interactive visualization(s) - *?*
* Frontend landing page - *Amy*
* App structure & deployment - *David, Rachel*

---
#### Project Members: Alicia, Amy, David, Rachel