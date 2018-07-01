import tweepy
from collections import defaultdict
import string
import csv
import pickle
import datetime
import arrow
import time

class Console:              

    def __init__(self, api):
        self.api = api
        self.tweet_id = 0
        self.options = defaultdict(lambda: print("No such command exists"), 
                                   {'rt':self.retweet, 
                                    'fav':self.favorite,
                                    'exit':lambda: print("Exiting...")
                                    })


    def console(self):
        if(self.api != 0):
            try:
                public_tweets = self.api.home_timeline()
                for tweet in public_tweets:
                    print(tweet.text)
            except tweepy.TweepError:
                print("tweep error")
        else:
            public_tweets = pickler() 
        

        print(public_tweets[0].user)
        '''for tweet in public_tweets:
            print(tweet.text
        '''
        self.print_tweets(public_tweets)

        input = ''
        exit = False

        while(not exit):
            input = self.get_console_input()
            
            exit = self.is_exit(input)
            #debug("input", input)
            args = input.split()
            #debug("args list", args)
           
            cmd = args[0]
            # debug("cmd", cmd)
            
            if(len(args) > 1):
                tweet_id = int(args[1])
                self.tweet_id = tweet_id
            else:
                self.id = 0

            debug("Self id ", self.id)

            self.id = public_tweets[self.tweet_id].id
            debug("self id", self.tweet_id)

            self.direct_input(cmd)

            input = ''
            cmd = ''
            args.clear()

    def is_exit(self, input):
        if(input.lower() == "exit"):
            return True
        else:
            return False
    def get_console_input(self):
        print("> ", end ='')
        user_input = input()
        return user_input

    def direct_input(self, cmd):
        func = self.options[cmd] 
        if(func is not None):
            func()

    def retweet(self):
        print("rt")
        # self.api.retweet(self.tweet_id)

    def favorite(self):
        print("fav")
        '''
        if(tweet._json['favorited'] == True):
             print("already favorited")
        else:
             self.api.create_favorite(self.tweet_id)
        '''
    def print_tweets(self, tweets, option="cust"):
        authors = []
        retweets = []
        favorite_count = []
        favorited = []
        created_at = []

        for i, tweet in enumerate(tweets):            
            authors.append(tweet.user._json['screen_name'])
            retweets.append(tweet.retweet_count)
            favorite_count.append(tweet.user._json['favourites_count'])
            created_at.append(tweet.created_at)
            print(type(tweet.created_at))

        for i, tweet in enumerate(tweets):
            print(i, end='')
            print(". By @" + authors[i])
            print(tweet.full_text)
            print("RTs: " + str(retweets[i]) + ", Favorites: " + str(favorite_count[i]))
            print(self.handle_date(tweet.created_at))
            print("\n")

    def handle_date(self, datetime):
        localtime = datetime_to_local(datetime)
        #TODO: test in different timezone
        human_time = arrow.get(localtime).shift(hours=4).humanize()
        date_string = 'Date: %a, %B %d, %Y // {}, %I:%M:%S %p'
        localtime = localtime.strftime(date_string.format(human_time))
        return localtime

def datetime_to_local(utc_datetime):
    now = time.time()
    offset = datetime.datetime.fromtimestamp(now) - datetime.datetime.utcfromtimestamp(now)
    return utc_datetime + offset

def debug(name, var):
    print(str(name) + ": ", end='')
    print(var)

def pickler():
    with open('tweet_data.pkl', 'rb') as input:
        public_tweets = pickle.load(input)

    return public_tweets

def main():
    c = Console(0)
    c.console()


if __name__ == "__main__":
    main()
