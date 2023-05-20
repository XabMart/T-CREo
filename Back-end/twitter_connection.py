import tweepy

app_key = 'a8JToLfAADc5ysGs1MMhLzCZZ'
app_secret = '3WKeaj916dzIGIleT5tPSoMyopw4TMfrY6tUdZjCIC4RzbUVxg'
oauth_token = '1522886161080926209-VJ3NljHTSUgOkalta0ctKO4lMbGK1C'
oauth_token_secret = '9uj4xVAHZqrwKPZVujzeyPhvf1fb5nv99Ja4oYcVcHFV0'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAPr0cQEAAAAA2cUBHe6coN8VnrJpNYxjY1lDJvM%3DmhH1Z1S1UxSKHhvk1XlrCAHvRMNqJIFNRTpHcJhsEy6W9mNjyW'

def twitterClient():
    twitter = tweepy.Client(
        consumer_key=app_key,
        consumer_secret=app_secret,
        access_token=oauth_token,
        access_token_secret=oauth_token_secret,
        bearer_token=bearer_token
    )
    return twitter
