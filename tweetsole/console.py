import tweepy
from collections import defaultdict

class Console:              

    def __init__(self, api):
        self.api = api
        self.id = 0
        self.options = defaultdict(lambda: print("No such command exists"), {'rt':self.retweet, 'fav':self.favorite})


    def console(self):
        public_tweets = self.api.home_timeline()
        for tweet in public_tweets:
            print(tweet.text)

        input = ''
        while(input != "exit"):
            input = self.get_console_input()

            args = input.split()
            cmd = args[0]

            if(len(args) > 1):
                self.id = args[1]
            else:
                self.id = 0

            self.id = public_tweets[int(self.id)].id

            self.direct_input(cmd)

            input = ''
            cmd = ''
            args.clear()

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
        
