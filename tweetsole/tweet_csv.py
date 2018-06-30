import csv
import tweepy
from authorizer import Authorizer

auth = Authorizer()
auth = auth.authorize()
api = tweepy.API(auth)
public_tweets = api.home_timeline()

file = open("tweets.csv", 'w+')
with file:
    writer = csv.writer(file)
    for tweet in public_tweets:
        writer.writerow(tweet.text)
        print("Writing {} to tweets.csv".format( (tweet.text[:10] + "..") if len(tweet.text) > 11 else tweet.text))

print("all done")
