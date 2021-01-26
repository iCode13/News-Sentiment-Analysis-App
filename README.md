<img src=Readme-Images/header.png width=1000></img>

#### UT Data Analysis & Visualization Bootcamp | January 2021
#### Team Members: Amy Banerji, Alicia Pelkey, Rachel Reynolds, David Vance

# News Sentiment Analysis App
Over the past several years, there has been a visceral shift in news consumption for many people; from regular morning and evening news broadcasts to a 24-hour news cycle. People have feelings about the news, but our questions is: does the news itself project a particular feeling?

With data gathered from the New York Times Archives API, we analyzed over 50,000 news articles covering a full 3-year span, from 2015 to 2017. Natural Language Processing was used to examine news sentiment across time, categories of news, and their geographic locations. Our app lets users explore the data through visualizations, search through articles by keyword, and test the sentiment of their own news headline!
##### [Link to App Deployed on Heroku](https://project3-news-app.herokuapp.com/)

## Table of Contents
* [Dataset](#dataset)
* [Sentiment Analysis Using Natural Language Processing](#sentiment-analysis-using-natural-language-processing)
* [Technologies Used](#technologies-used)
* [Data Analysis and Visualizations](#data-analysis-and-visualizations)
* [Interactive Features](#interactive-features)
* [Screenshots](#screenshots)
* [Citations](#citations)

## Dataset
* [New York Times Archives](https://developer.nytimes.com/docs/articlesearch-product/1/overview): 
Data from news articles over a 3-year period from 2015 to 2017.

## Sentiment Analysis Using Natural Language Processing
Natural Language Processing (NLP) is a form of machine learning that gleans information from humans' spoken or written words. For this app, a type of NLP called Sentiment Analysis was performed that attempts to determine some measure of the "feeling" of a text, often described as the text's positivity or negativity. A simple form of sentiment analysis was employed that uses a "lexicon", or a list of words that have been assigned meanings. A program then applies a lexicon-based sentiment analysis to a text, and breaks the text down into "tokens" which are usually root words. The pre-assigned sentiment values for tokens found in the lexicon are summed or averaged for the text the program is analyzing to come up with a sentiment score.

## Technologies Used
* New York Times and Google Geocoding API's
* Machine Learning and Sentiment Analysis tools:
    * Natural Language Toolkit (NLTK), scikit-learn, NRCLex, VADER
* pandas, geopy, calmap, pycountry, us
* Plotly, Matplotlib, D3
* HTML, CSS, Jinja
* Python, JavaScript
* Flask
* Heroku

## Data Analysis and Visualizations
* Article vs headline score scatter, contour, regression plot.
* Article score box plot.
* Average daily sentiment calendar heatmap.
* Average daily sentiment line chart.
* Frequency plots of "bigrams" (two words commonly seen together) and "trigrams" (three words commonly seen together).
* Choropleth map animations of article sentiment by day of the week, month and over time within the US and across the globe.
* Heatmap animation of headline sentiment score over time around the world.

## Interactive Features
* Sentiment Analyzer: Takes in a news headline as user input, and outputs overall sentiment as a "Senti-Meter" and a plot of the words' emotions.
* Article Search: Takes in keyword(s) in a chosen category as user input, and outputs a random sample of up to 5 articles and a "Senti-Meter".

## Screenshots
##### Home Page:
<img src=Readme-Images/index.png width=500></img>

##### Visualizations Page:
<img src=Readme-Images/viz1.png width=500></img>
<img src=Readme-Images/viz2.png width=500></img>

##### Geoviz Page:
<img src=Readme-Images/geo.png width=500></img>

##### Interactive Page:
<img src=Readme-Images/interactive1.png width=500></img>

## Limitations and Future Improvements:
* Improve app performance.
* Extend the timeframe of the data collected to see what changes in sentiment occurred during the pandemic compared to prior years.
* Test further methods and applications of n-grams for document classification and sentiment analysis.
* Add features that let the user filter by time period, location, news type, etc.
* Incorporate the search function to output vizzes that filter to user inputs.
* Use more JavaScript to create more dynamic visualizations.
* Lastly, but probably the biggest undertaking would be to build our own machine learning model for the sentiment analysis!

## Citations
* VADER Sentiment Analysis: 
   * C.J. Hutto and E.E. Gilbert. "VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text." Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI (June 2014).
* Natural Language Toolkit (NLTK) Project: 
   * Steven Bird, Edward Loper, and Ewan Klein. Natural Language Processing with Python. O’Reilly Media Inc. (2009).
* NRCLex API: 
   * Mark C. Bailey (2019).
* NRC Lexicon: 
   * National Research Council Canada (2016).

