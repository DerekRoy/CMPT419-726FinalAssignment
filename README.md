# CMPT419-726FinalAssignment
A final assignment for CMPT 419/726 where we put together various tools from different locations in order to perfrom web scraping on Reddit communities in order to analyze user sentiment and emotion in regards to specific products or companies. There will also be an element of training our own sentiment analysis AI. 


Kaggle Rotten Tomatoes dataset: https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/data

scraper.py:
scraper.py takes in the name of the subreddit and collects each thread's title, body, and comments and writes them into an output .tsv file. It accepts the following paramters: 
  -s S        subreddit to scrape
  -d D        duration (in days)
  -o O        output .csv file
Example of usage: $ python scraper.py -s worldnews -d 15 -o out.tsv
this command would collect the subreddit "worldnews" threads (threads' title, body, and comments) from the past 15 days as a list of strings and write the results to the file "out.tsv"

Clean.py: 
clean.py takes in a file (tsv) and formats it correctly into 1 column. Processes the file removing urls, (unnamed,deleted,removed) posts, posts containing any mention of "thank you for following me", any non ascii characters like emojis and other language scripts (like arabic), any hashtags or user mentions, and unnecessary symbols or acronyms. 
Then overwrites the file wit the new data. 
