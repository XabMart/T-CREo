# -*- coding: utf-8 -*-
import pymongo
from twython import Twython


# Mejor ignorar estos tweets.
supported_languages = ['en', 'es', 'fr', 'pt', 'de','ru','ar']

def process_language(lang):
    if lang not in supported_languages:
        lang = 'en'
    return lang

keys = {
    "app_key": "a8JToLfAADc5ysGs1MMhLzCZZ",
    "app_secret": "3WKeaj916dzIGIleT5tPSoMyopw4TMfrY6tUdZjCIC4RzbUVxg",
    "oauth_token": "1522886161080926209-uK8aggJ9nrVvlnBpjUD1b7iM2hkGn2",
    "oauth_token_secret": "Z8YuiKhXoTyD8A1tFTBF6mDDvIbxC12JxbFJVpooyl4UZ"
}

def getKeys():
    return keys

def get_user_info(handle):
    twitter = Twython(**keys)
    user_info = twitter.show_user(screen_name=handle)
    tweet = twitter.get_user_timeline(screen_name=handle, count=1)	
    return user_info, tweet

def twitterStreamer():
    return Twython(**keys)

def mongo_connect():
    dbName = 'Test'
    dbCollectionA = 'CuentasTwitter'
    dbCollectionT = 'Tweets'

    dbStringConnection = "mongodb+srv://xabier:ENXKLSNvrWqd3dYJ@cluster0.rmdseqj.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(dbStringConnection)

    db = client[dbName]
    accounts = db[dbCollectionA]
    tweets = db[dbCollectionT]
    return db, accounts, tweets
