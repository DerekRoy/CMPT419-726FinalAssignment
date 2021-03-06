# CMPT419-726FinalAssignment
A final assignment for CMPT 419/726 where we put together various tools from different locations in order to perfrom web scraping on Reddit communities in order to analyze user sentiment and emotion in regards to specific products or companies. There will also be an element of training our own sentiment analysis AI. 


Kaggle Rotten Tomatoes dataset: https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/data

scraper.py:
scraper.py takes in the name of the subreddit and collects each thread's title, body, and comments and writes them into an output .tsv file. It accepts the following paramters: 

  -s S        subreddit to scrape
  -b B        before X days/hours ago (default = None)
  -a A        after X days/hours ago (default = None)
  -o O        output .tsv file (default = "output.tsv") 

parameters a, and b are used to specify the time period of the sumbmissions to collect. They must be used with units "s,m,h,d" (i.e. 30d for 30 days).

Example1: > python scraper.py -s worldnews -a 15d -o out.tsv

this command would collect the subreddit "worldnews" threads (threads' title, body, and comments) after 15 days ago as a list of strings and write the results to the file "out.tsv"

Example2: > python scraper.py -s simonfraser -a 30d -b 20d -o out.tsv

this command would collect the subreddit "simonfraser" threads (threads' title, body, and comments) after 30 days ago and before 20 days ago (between 20 and 30 days ago) as a list of strings and write the results to the file "out.tsv"

Clean.py: 
clean.py takes in a file (tsv) and formats it correctly into 1 column. Processes the file removing urls, (unnamed,deleted,removed) posts, posts containing any mention of "thank you for following me", any non ascii characters like emojis and other language scripts (like arabic), any hashtags or user mentions, and unnecessary symbols or acronyms. 
Then overwrites the file wit the new data. 

reddit_sentiment_model.py

Trains a sentiment model based on Twitter samples from NLTK's Corpus
- Requires NLTK and NLTK Corpus download
- Requires the pickle library
- Requires sklearn
- Requires a folder named "pickles" in the working directory

run with:
> python reddit_sentiment_model.py

or to download libraries and run in a virtual environment

> pipenv run python reddit_sentiment_model.py

The test accepts the same command line arguments as scraper.py. When user specifies a subreddit name using "-s" parameter, it will replace the hard-coded test data with data scraped from the subreddit based on the choice of command line arguments. 

reddit_sentiment_module.py

Uses a model generated by reddit_sentiment_model.py in classification of text as positive or negative

Functionality can be implemented in other files by importing this file and executing the process:

> reddit_sentiment_model.classify(*text*)

where *text* is a string

reddit_sentiment_test.py

Sample implementation of reddit_sentiment_module.py on r/Stadia

run with:
> python reddit_sentiment_test.py

or to download libraries and run in a virtual environment

> pipenv run python reddit_sentiment_test.py
