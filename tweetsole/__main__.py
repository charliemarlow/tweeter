import sys
import tweepy
from .authorizer import Authorizer
from .console import Console

def main():

    if(len(sys.argv) == 2):
        username = sys.argv[1]
        authorizer = Authorizer(user_arg=username)
    else:
        authorizer = Authorizer()

    auth = authorizer.authorize()

    api = tweepy.API(auth)
    console = Console(api)
    console.console()

    
if __name__ == '__main__':
    main()
