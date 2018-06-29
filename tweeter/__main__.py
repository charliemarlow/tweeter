import sys
import tweepy
from .tweeter import Tweeter
from .authorizer import Authorizer

def main():

    if(len(sys.argv) == 2):
        username = sys.argv[1]
        authorizer = Authorizer(user_arg=username)
    else:
        authorizer = Authorizer()

    auth = authorizer.authorize()

    api = tweepy.API(auth)
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    
if __name__ == '__main__':
    main()
