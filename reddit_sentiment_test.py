import reddit_sentiment_module as red_sen
from scraper.py import get_comments, get_submissions
from clean.py import clean_data


if __name__ == '__main__':

    # include a parser for command line arguments
    parser = argparse.ArgumentParser(description='a script for the subreddits scraper')
    parser.add_argument("-s", help="subreddit to scrape", type=str)
    parser.add_argument("-b", help="before X days/hours/minutes/seconds ago", type=str, default=None)
    parser.add_argument("-a", help="after X days/hours/minutes/seconds ago", type=str, default=None)
    parser.add_argument("-o", help="output .tsv file", type=str, default="output.tsv")
    args = parser.parse_args()

    comments = [
        "Jeeez we need a community photo and clips sharing section",
        "I only wish AC Odyssey could hit 60fps at a lower resolution, but I guess that's a tall order for even something as powerful as Stadia. Still looks great!",
        "I might be wrong, but AC:O is 60fps @1080p isn't it?",
        "Unfortunately not, I've played other games that default to 1080/60 on a compatible setup and 4K/30 on a 2160p display, like Metro Exodus.",
        "But with AC Odyssey it's 30fps in both 1080p and 4K. I've tried this on Chromecast Ultra, Mac Mini, Chromebook and Pixel phones (2XL, 4XL) and it's always 30fps. I prefer the way it looks on my PS4 Pro with no artifacts, but for streaming this sure looks fantastic!",
        "I am playing it on my 4K TV, and it looks incredible. I am not sure if it is 4K, but the detail looks to be higher than 1080p. I swapped between my PS4Pro, Xbox One X, and Stadia, and Stadia looks much better, and the 60FPS makes the experience much better than the console version.",
        "Oh certainly, but they mentioned at lower resolution. I believe it's upscaled from 1440p when on the CCU.",
        "It does rock it's amazing, a true work of art..the tech is amazing. This platform is truly a gamechanger and the future looks amazing for Stadia. Amazing job the Stadia team has done and all the Publishers/Developers putting work on Stadia.",
        "I am sold also on cloud gaming, but more importantly on Stadia. This has made me a huge Google fan, next up time to get me a Google Pixel 4 XL Phone and Google Pixelbook Laptop.",
        "I am getting around 80 Mbs download average. I have no issues at all with Stadia gaming overall. I didnt realize how amazing this service was until I played a few games on my Xbox one X, or PS4 pro and almost fell over with the long load times, updates (that didnt happen in the background when I did have it in low power mode), crashed etc. I am sold on cloud gaming.",
        "I love hearing about all the issues everyone on other consoles are having. PC people having to download and reinstall drivers. I just purchased and jumped right into playing. Love Stadia!",
        "I would argue that the \"best way to game\" is quite subjective. The best way to game is the way that suits you. Different people, different expectations and requirements.",
        "Well, I mainly play on PC (and not a monster one just to be clear) and some of the things you mention are here as well (like secure payments, cross play), some other are not as bad as people make them (like updates, my launcher starts with PC so before I actually sit down to play if there was an update it's already done). Now, what Stadia doesn't offer me is access to the files so I can mess around with them. I also don't have mods, nor do I have access to emulation.",
        "Half of this goes for consoles as well. Secure payments, of course. Intrusive updates? My PS4 is in standby mode and in all honesty, I can't remember when was the last time I did see an update bar. I also have backwards compatibility for older games. Plus way bigger player base on both occasions which is critical for any online multiplayer game.",
        "Now, I'm not saying that Stadia is not a great gaming choice. I'm just pointing out that there are different people with different expectations and requirements therefore \"the best way to game\" is very subjective.",
        "Everything you said about PC wouldn't make me want to main it at all. It's a great second imo for older games that won't get a remake but any future title is best on Stadia. As times go on it won't even be close. This reminds me of blockbuster and Netflix. I remember people saying I don't mind returning the DVD, ease of use always wins out. At least to the masses. PC will be for connoisseur's.",
        "Doom requires too much precision to enjoy playing it on stadia, I had to return it unfortunately.",
        "I played it on PC as well, still not as good as it should be even running less than 4k. I have Gigabit internet.",
        "Plays fine for me. It's a twitch shooter at the end of the day. You gotta be a fairly competent gamer.",
        "Nice pics, shows Stadia is a powerful platform. But i assume those are using Stadia screen capture? If so they dont account for being streamed. I dont want to be negative, i love Stadia, but it just triggers something when i see people posting such images without disclaimer."
    ]

    if args.s:
        subreddit = args.s
        size = 1000
        before = args.b
        after = args.a
        output = args.o

        # scrape comments and submissions
        comments = get_comments(subreddit, size, before, after)
        submissions = get_submissions(subreddit, size, before, after)
        comments = comments + submissions

        # write result to .tsv file
        with open(output, 'w', newline='') as f_output:
            tsv_output = csv.writer(f_output, delimiter='\t')
            tsv_output.writerow(results)

        print("Scraping the subreddit {} is done! Results are saved in {}".format(subreddit, output))    

        clean_data(output)
        print("Data in {} has been filtered!".format(output))  

        # read the data from the .tsv file into a string
        with open('output', 'r') as file:
            comments = file.read().replace('\n', '')

        # split the string into list of comments and submissions
        comments = comments.split("\t")

    for comment in comments:
        print(comment)
    print(red_sen.classify(comment))

