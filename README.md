#### Team Members: Alicia Pelkey, Amy Banerji, David Vance, Rachel Reynolds

#### UT Data Analysis & Visualization Bootcamp | January 2021

# News Sentiment Analysis

Over the past several years, there was a visceral shift in news consumption for many people; from regular morning and evening news broadcasts to a 24-hour news cycle. People have feelings about the news, but our questions is: does the news itself project a particular feeling?

With data gathered from the New York Times Archives API, we analyzed over 50,000 news articles covering a full 3-year span, from 2015 - 2017. Natural Language Processing was used to examine sentiment across time, categories of news, and geographic locations. Users can explore the data through visualizations, search through articles by keyword, and test the sentiment of their own news headline!

## Table of Contents:
* [Data Set](#data-set)
* [Sentiment Analysis Using NLP](#sentiment-analysis)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Visualizations](#visualizations)
* [Interactive Features](#interactive)

## Data Set:
* [NY Times Archive API](https://developer.nytimes.com/docs/articlesearch-product/1/overview): 
Collected data from a 3-year period from 2015 to 2017.

## Sentiment Analysis Using Natural Language Processing (NLP):
A type of NLP called Sentiment Analysis was performed that attempts to determine some measure of the "feeling" of a text, often described as the text's positivity or negativity. A simple form of sentiment analysis was employed that uses a "lexicon," or a list of words that have been assigned meanings. 

A program then applies a lexicon-based sentiment analysis to a text, and breaks the text down into "tokens" which are usually root words. The pre-assigned sentiment values for tokens found in the lexicon are summed or averaged for the text the program is analyzing.

## Screenshots:
![Example screenshot](./img/screenshot.png)

## Technologies Used:
* NLTK
* pandas
* plotly
* HTML & CSS
* Jinja
* Python

## Data Analysis:
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

## Visualizations:
* Charts for different sentiments (most frequent terms for each sentiment, using NRC lexicon).
* Network diagram showing "bigrams" (two words commonly seen together) and "trigrams" (three words commonly seen together).
* Sentiment choropleth maps.
* Sentiment geographic heatmap.

## Interactive Features:
* Sentiment analysis of user inputted headline
* Article search by user inputted keyword(s)

