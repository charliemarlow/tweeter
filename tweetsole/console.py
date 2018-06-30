import tweepy
from collections import defaultdict
import string
import csv

class Console:              

    def __init__(self, api):
        self.api = api
        self.id = 0
        self.options = defaultdict(lambda: print("No such command exists"), {'rt':self.retweet, 'fav':self.favorite})


    def console(self):
        '''
        try:
            public_tweets = self.api.home_timeline()
            for tweet in public_tweets:
                print(tweet.text)
        except tweepy.TweepError:
            print("tweep error")

        '''
        public_tweets = [] 
        file = open("tweets.csv", 'r')
        with file:
            reader = csv.reader(file)
            for row in reader:
                public_tweets.append(row)

        for tweet in public_tweets:
            print(''.join(tweet))

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
            
            if(len(args) > 1 and type(args[1]) is int):
                self.id = args[1]
            else:
                self.id = 0

            self.id = public_tweets[int(self.id)].id

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

    def favorite(self):
        print("fav")
        

def debug(name, var):
    print(name, end='')
    print(var)
