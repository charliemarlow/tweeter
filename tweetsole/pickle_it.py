import pickle
import tweepy
from authorizer import Authorizer



auth = Authorizer()
auth = auth.authorize()
api = tweepy.API(auth)
public_tweets = api.home_timeline(tweet_mode='extended')


file = open("tweet_data.pkl", 'wb')
with file as output:
    pickle.dump(public_tweets, output)

print("all done")
