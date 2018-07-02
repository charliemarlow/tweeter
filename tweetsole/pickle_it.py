import pickle
import tweepy
from authorizer import Authorizer

'''
Stores 20 tweets in a .pkl file as a list
Used to store tweets while testing tweetsole 
so you don't create a rate-limit error from too 
many API calls
'''

# get authorization keys
auth = Authorizer()
auth = auth.authorize()
api = tweepy.API(auth)

# get tweets
public_tweets = api.home_timeline(tweet_mode='extended')

# store tweets in a .pkl file
file = open("tweet_data.pkl", 'wb')
with file as output:
    pickle.dump(public_tweets, output)

print("all done")
