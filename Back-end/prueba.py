# -*- coding: utf-8 -*-

import tweepy

app_key = 'a8JToLfAADc5ysGs1MMhLzCZZ'
app_secret = '3WKeaj916dzIGIleT5tPSoMyopw4TMfrY6tUdZjCIC4RzbUVxg'
oauth_token = '1522886161080926209-VJ3NljHTSUgOkalta0ctKO4lMbGK1C'
oauth_token_secret = '9uj4xVAHZqrwKPZVujzeyPhvf1fb5nv99Ja4oYcVcHFV0'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAPr0cQEAAAAA2cUBHe6coN8VnrJpNYxjY1lDJvM%3DmhH1Z1S1UxSKHhvk1XlrCAHvRMNqJIFNRTpHcJhsEy6W9mNjyW'


client = tweepy.Client(bearer_token,app_key,app_secret,oauth_token,oauth_token_secret)
auth = tweepy.OAuth1UserHandler(app_key,app_secret,oauth_token,oauth_token_secret)
api =  tweepy.API(auth)

search_terms = ["python"]

class MyStream(tweepy.StreamingClient):
	def on_connect(self):
		print("Connected")
	def on_tweet(self,tweet):
		if tweet.referenced_tweets == None:
			print(tweet.text)

stream = MyStream(bearer_token=bearer_token)
for term in search_terms:
	stream.add_rules(tweepy.StreamRule(term))

	stream.filter(tweet_fields=['referenced_tweets'])