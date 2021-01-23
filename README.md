<img src=Readme-Images/header.png width=800></img>
#### Team Members: Alicia Pelkey, Amy Banerji, David Vance, Rachel Reynolds

#### UT Data Analysis & Visualization Bootcamp | January 2021

#### [Deployed Heroku Link](https://project3-news-app.herokuapp.com/)

# News Sentiment Analysis

Over the past several years, there was a visceral shift in news consumption for many people; from regular morning and evening news broadcasts to a 24-hour news cycle. People have feelings about the news, but our questions is: does the news itself project a particular feeling?

With data gathered from the New York Times Archives API, we analyzed over 50,000 news articles covering a full 3-year span, from 2015 - 2017. Natural Language Processing was used to examine sentiment across time, categories of news, and geographic locations. Our app lets users explore the data through visualizations, search through articles by keyword, and test the sentiment of their own news headline!

## Table of Contents:
* [Data Set](#data-set)
* [Sentiment Analysis Using NLP](#sentiment-analysis)
* [Technologies Used](#technologies-used)
* [Data Analysis and Visualizations](#data-analysis-visualizations)
* [Interactive Features](#interactive)
* [Screenshots](#screenshots)
* [Citations](#citations)

## Data Set:
* [New York Times Archives](https://developer.nytimes.com/docs/articlesearch-product/1/overview): 
Collected data from a 3-year period from 2015 to 2017.

## Sentiment Analysis Using Natural Language Processing (NLP):
A type of NLP called Sentiment Analysis was performed that attempts to determine some measure of the "feeling" of a text, often described as the text's positivity or negativity. A simple form of sentiment analysis was employed that uses a "lexicon," or a list of words that have been assigned meanings. 

A program then applies a lexicon-based sentiment analysis to a text, and breaks the text down into "tokens" which are usually root words. The pre-assigned sentiment values for tokens found in the lexicon are summed or averaged for the text the program is analyzing.

## Technologies Used:
* NLTK
* Scikit-learn
* Pandas
* Plotly
* D3
* JSON
* NY Times and Google Geocoding APIs
* geopy, calmap, pycountry, us libraries
* HTML & CSS
* Jinja template
* Javascript
* Python 3.7
* Flask
* Heroku

## Data Analysis and Visualizations:
* Article vs headline score scatter, contour, regression plot.
* Article score box plots.
* Average daily sentiment calendar heatmap.
* Average daily sentiment line chart.
* Frequency plots of "bigrams" (two words commonly seen together) and "trigrams" (three words commonly seen together).
* Choropleth maps of article sentiment by day of the week, month and over time (monthly) in the US and across the globe.
* Headline sentiment score over time around the world.

## Interactive Features:
* Sentiment analysis of user inputted headline -- gives results as overall sentiment ("Senti-meter") and emotions of words plot.
* Article search by user inputted keyword(s) in a chosen category -- gives results as a random sample of 5 articles and a Senti-meter.

## Screenshots:
![Example screenshot](./img/screenshot.png)

## Citations:
* VADER Sentiment Analysis: 
C.J. Hutto and E.E. Gilbert. "VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text." Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI (June 2014).
* Natural Language Toolkit (NLTK) Project:
    *Steven Bird, Edward Loper, and Ewan Klein. Natural Language Processing with Python. O’Reilly Media Inc. (2009).
* NRCLex API
    * Mark C. Bailey (2019).
* NRC Lexicon
    * National Research Council Canada (2016).

