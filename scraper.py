import sys
import argparse
import json
import requests
import csv

def get_submissions(subreddit, size, before, after):
    submission_url = 'https://api.pushshift.io/reddit/search/submission/?subreddit={}&size={}&is_video=False'
    if after:
        submission_url += "&after={}".format(after)
    if before:
        submission_url += "&before={}".format(before)
    response = requests.get(url=submission_url.format(subreddit, size, before))
    try:
        response = response.json()
    except:
        return None
    response_data = response["data"]
    submissions = []
    for data in response_data:
        submissions.append(data['title'])
        try:
            if isinstance(data['selftext'], str):
                submissions.append(data['selftext'])
        except:
            pass
    return submissions

def get_comments(subreddit, size, before, after):
    comment_url = 'https://api.pushshift.io/reddit/search/comment/?subreddit={}&size={}'
    if after:
        comment_url += "&after={}".format(after)
    if before:
        comment_url += "&before={}".format(before)
    response = requests.get(url=comment_url.format(subreddit, size))
    try:
        response = response.json()
    except:
        return None
    response_data = response["data"]
    comments = []
    for data in response_data:
        comments.append(data["body"])
    return comments

if __name__ == '__main__':
    # include a parser for command line arguments
    parser = argparse.ArgumentParser(description='a script for the subreddits scraper')
    parser.add_argument("-s", help="subreddit to scrape", type=str)
    parser.add_argument("-b", help="before X days/hours/minutes/seconds ago", type=str, default=None)
    parser.add_argument("-a", help="after X days/hours/minutes/seconds ago", type=str, default=None)
    parser.add_argument("-o", help="output .tsv file", type=str, default="output.tsv")
    args = parser.parse_args()

    if not args.s:
        sys.exit("Must indicate which subreddit to scrape")

    subreddit = args.s
    size = 1000
    before = args.b
    after = args.a
    output = args.o

    # scrape comments and submissions
    comments = get_comments(subreddit, size, before, after)
    submissions = get_submissions(subreddit, size, before, after)
    results = comments + submissions
    
    # write result to .tsv file
    with open(output, 'w', newline='') as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        tsv_output.writerow(results)
    
    print("Scraping the subreddit {} is done! Results are saved in {}".format(subreddit, output))
    sys.exit(0)


    