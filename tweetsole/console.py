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
        '''
        Sets up instance variables for class console
        self.options is used to handle control flow for the main loop
        using defaultdict's get option
        :param api: the API object used to make calls through Tweepy
        '''
        self.api = api
        self.tweet_id = 0
        self.public_tweets = []
        self.temp_user = "@example"
        self.options = defaultdict(lambda: None,
                                   {'rt':self.retweet,
                                    '>>':self.retweet,
                                    'fav':self.favorite,
                                    '<3':self.favorite,
                                    'exit':lambda: print("Exiting..."),
                                    'compose':self.compose,
                                    'refresh':self.refresh,
                                    'help':self.help,
                                    'reply':self.reply,
                                    'reply':self.reply
                                    })


    def console(self):
        '''
        contains the main loop of the class
        Takes user input, passes it to other functions to handle it

        :return: 0 on successful exit
        '''
        # use an API call unless class is being run through main (self.api == 0)
        # use pickle to get locally stored tweets
        if(self.api != 0):
            try:
                self.public_tweets = self.api.home_timeline(tweet_mode='extended')
            except tweepy.TweepError:
                print("tweep error")
        else:
            self.public_tweets = pickler() 


        # print out tweets
        self.print_tweets(self.public_tweets)

        input = ''
        exit = False

        # while the input does not say exit
        while(not exit):
            input = self.get_console_input()
            
            exit = self.is_exit(input)
            # list of user commands
            args = input.split()

            # args are form of:
            # > cmd id
            # get cmd
            if(len(args) >= 1):
                cmd = args[0]

            # get tweet id
            if(len(args) > 1):
                try:
                    tweet_id = int(args[1])
                    self.tweet_id = tweet_id
                except:
                    self.tweet_id = 0
            else:
                self.tweet_id = 0

            # self.tweet_id corresponded to the number listed next to the tweet
            # now corresponds to twitter API id
            if(len(self.public_tweets) > self.tweet_id):
                self.temp_user = self.public_tweets[self.tweet_id].user._json['screen_name']
                self.tweet_id = self.public_tweets[self.tweet_id].id

            # pass input to control flow
            self.direct_input(cmd)

            # clear reused variables
            input = ''
            cmd = ''
            self.tweet_id = 0
            args.clear()


        return 0

    def is_exit(self, input):
        '''
        Checks if the input is the word exit
        :param input: the user's input
        :return: True if the input is exit, false if it is not exit
        '''
        if(input.lower() == "exit"):
            return True
        else:
            return False

    def get_console_input(self):
        '''
        Gets user input
        :return: returns the users input as a string
        '''
        print("> ", end ='')
        user_input = input()
        return user_input

    def direct_input(self, cmd):
        '''
        Maps the user's input to a function using
        defaultdicts get() function
        :param cmd: the command the user wants to execute
        :return: the function to be executed
        '''
        func = self.options[cmd] 
        if(func is not None):
            func()
        else:
            print("No such command exists")
    def retweet(self):
        '''
        Retweets a tweet
        :return: None
        '''
        try:
            self.api.retweet(self.tweet_id)
            print("Retweeted")
        except:
            print("Error retweeting, try again later")

    def favorite(self):
        '''
        Favorites a tweet
        :return: None
        '''
        try:
            self.api.create_favorite(self.tweet_id)
            print("Favorited")
        except:
            print("Error favoriting, try again later")

    def refresh(self):
        '''
        Refreshes tweetsole with new tweets
        :return: None
        '''
        try:
            self.public_tweets = self.api.home_timeline(tweet_mode='extended')
            self.print_tweets(self.public_tweets)
        except:
            print("Error refreshing, try again later")

    def compose(self):
        '''
        Create a new tweet
        :return: None
        '''
        self.post_tweet(False)

    def post_tweet(self, is_reply):
        '''
        Posts a tweet
        :param is_reply: if the tweet is a reply or not
        :return: None
        '''
        print("Enter a tweet to post: ", end = '')
        tweet_content = ''

        while(tweet_content == ''):
            tweet_content = input()
        
        try:
            if(is_reply):
                user = self.temp_user
                user = "@" + user

                self.api.update_status(user + " " + tweet_content, in_reply_to_status_id=self.tweet_id)
            else:
                self.api.update_status(tweet_content)
            
            print("Posted")
        except:
            print("Error posting tweet, try again later")

    def reply(self):
        '''
        Replies to a given tweet
        :return: None
        '''
        self.post_tweet(True)


    def help(self):
        '''
        Prints a menu of options
        :return: None
        '''
        print("From the tweetsole console, enter any of the following commands: ")
        print("rt <tweet ID>  OR >> <tweet ID>       retweets a tweet")
        print("fav <tweet ID> OR <3 <tweet ID>       favorites a tweet")
        print("reply <tweet ID>                      replies to a tweet")
        print("compose                               posts a new tweet")
        print("refresh                               loads 20 new tweets")
        print("help                                  show commands")
        print("exit                                  exits the app")
    def print_tweets(self, tweets):
        '''
        Prints out tweets with username, text, and tweet information
        :param tweets: the list of tweets to be printed
        :return: None
        '''

        tweet_dicts = []
        for tweet in tweets:
            tweet_dicts.append({
                'author':tweet.user._json['screen_name'],
                'retweets':tweet.retweet_count,
                'favorites':tweet.user._json['favourites_count'],
                'created_at':tweet.created_at,
                'favorited':tweet.favorited,
                'retweeted':tweet.retweeted,
                'tweet':tweet.full_text
            })


        for tweet in tweet_dicts:
            print(tweet_dicts.index(tweet), end='')
            print(". By @" + tweet['author'])
            print(tweet['tweet'])
            print("RTs: " + str(tweet['retweets']) + ", Favorites: " + str(tweet['favorites']))
            print(self.handle_date(tweet['created_at']))
            print(self.handle_graphics(tweet['favorited'], tweet['retweeted']))
            print("\n")


    def handle_graphics(self, favorited, retweeted):
        '''
        Creates symbols for retweets and favorites
        :param favorited: bool of whether the user favorited the tweet or not
        :param retweeted: bool of whether the user retweeted the tweet or not
        :return: a string to be printed under the tweet
        '''
        blank = '     '
        graphic = blank

        if(favorited):
            graphic = graphic + "<3"
        else:
            graphic = graphic + "| </3 |"

        graphic = graphic + blank

        if(retweeted):
            graphic = graphic + ">>"
        else:
            graphic = graphic + "| >/> |"

        return graphic

    def handle_date(self, datetime):
        '''
        Creates a formatted date string, puts date in local timezone
        :param datetime: the datetime object from the tweet
        :return: a string representing the date and time of the tweet's creation
        '''
        localtime = datetime_to_local(datetime)
        shift = datetime.hour - localtime.hour
        human_time = arrow.get(localtime).shift(hours=shift).humanize()

        date_string = 'Date: %a, %B %d, %Y // {}, %I:%M:%S %p'
        localtime = localtime.strftime(date_string.format(human_time))
        return localtime

def datetime_to_local(utc_datetime):
    '''
    Takes a datetime in UTC, converts the time to the system's
    local time
    :param utc_datetime: a datetime object with time in UTC
    :return: a datetime object with time converted to the system's timezone
    '''
    now = time.time()
    offset = datetime.datetime.fromtimestamp(now) - datetime.datetime.utcfromtimestamp(now)
    return utc_datetime + offset

def debug(name, var):
    '''
    Prints the name followed by a ": " and then the
    value of variable var
    :param name: the identifying variable name to be printed
    :param var: the variable containing the value to be printed
    :return: None
    '''
    print(str(name) + ": ", end='')
    print(var)

def pickler():
    '''
    Gets tweets from a .pkl file
    Used when the file is run by itself, helps with testing
    when too many API calls can cause a rate limit error
    :return: a list of tweets
    '''
    with open('tweet_data.pkl', 'rb') as input:
        self.public_tweets = pickle.load(input)

    return self.public_tweets

def main():
    '''
    Called when file is run by itself
    when self.api = 0, console() uses pickler to get tweets
    :return: None
    '''
    c = Console(0)
    c.console()


if __name__ == "__main__":
    main()
