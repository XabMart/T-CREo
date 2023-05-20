# -*- coding: utf-8 -*-

import sys
import tweepy
from twitter_connection import twitterClient
import pymongo
from datetime import datetime,date
import time
import pandas as pd
import json
from apscheduler.schedulers.background import BackgroundScheduler
import threading
from datetime import datetime
import os
import time
import logging
import requests
from credibility import credibility,textCredibility,userCredibility,socialCredibility


#twitter = tweepy.Client(bearer_token, app_key, app_secret, oauth_token, oauth_token_secret)
twitter = twitterClient()

# Conexión a la base de datos de MongoDB
dbName = 'Test'
dbCollectionA = 'CuentasTwitter'
dbCollectionT = 'Tweets'

dbStringConnection = "mongodb+srv://xabier:ENXKLSNvrWqd3dYJ@cluster0.rmdseqj.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbStringConnection)

db = client[dbName]
accounts = db[dbCollectionA]
tweets = db[dbCollectionT]

user_fields =  ['created_at', 'description', 'id', 'location', 'name', 'protected', 'public_metrics', 'url', 'username', 'verified', 'verified_type']
tweet_fields = tweepy.tweet.PUBLIC_TWEET_FIELDS

class Tasks():

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler_running = False

    def run(self):

        accountsInDB = accounts.find()

        for user in accountsInDB:
            user_info = twitter.get_user(id=user['User_id'], user_fields = user_fields)
            print(user['Twitter_handle'])
            # Obtener el número de seguidores, seguidos y si la cuenta está verificada
            followers_count = user_info.data['public_metrics']['followers_count']
            following_count = user_info.data['public_metrics']['following_count']
            verified = user_info.data['verified']
            # Obtener la fecha de creación de la cuenta
            created_at = user_info.data['created_at']
            created_at_str = str(created_at)
            # Obtener el último tweet de la cuenta
            tweetsDownloaded = twitter.get_users_tweets(id = user['User_id'],expansions=['author_id'], max_results = 100, tweet_fields=tweet_fields,user_fields = user_fields)
            # Iterar sobre cada tweet
            for tweet in tweetsDownloaded.data:
                
                retweet_count = tweet['public_metrics']['retweet_count']
                like_count = tweet['public_metrics']['like_count']
                text = tweet['text']
                lang = tweet['lang']
                cuenta = user['Twitter_handle']
                tweetId = tweet['id']
                textCred = textCredibility(text,lang)
                userCred = userCredibility(verified,created_at_str)
                socialCred = socialCredibility(followers_count,following_count)
                totalCredibility = credibility(textCred,socialCred,userCred)

                outputLog = f'Account: {cuenta} \n Followers: {followers_count} \n Friends: {following_count} \n Verified: {verified} \n Created at: {created_at} \n CREDIBILITY: {totalCredibility}' 
                # Imprimir los resultados
                logging.info(outputLog)
                
                tweetProc = {
                    
                    'id':tweetId,
                    'text': text,
                    'retweet_count': retweet_count,
                    'like_count' : like_count,
                    'lang': lang,
                    'author_id':tweet['author_id'],
                    'created_at':tweet['created_at'],
                    'geo': tweet['geo'],
                    
                    'user':[{
                        'id': user['User_id'],
                        'username' : user['Twitter_handle'],
                        'name': user_info.data['name'],
                        'description': user_info.data['description'],
                        'created_at': created_at,
                        'verified': verified,
                        'verified_type':user_info.data['verified_type'],
                        'protected': user_info.data['protected'],
                        'followers_count': followers_count,
                        'following_count': following_count,
                        'location':user_info.data['location']

                    }],
                    'credibility':[{
                        'text_credibility':textCred,
                        'social_credibility':socialCred,
                        'user_credibility':userCred,
                        'global_credibility':totalCredibility
                    }]
                }

                # Verificar si el tweet ya está en la base de datos
                if tweets.find_one({'id': tweetId}):
                    print('Tweet '+str(tweetId)+' of account '+cuenta+ ' already exist in database.\n')
                else:
                    # Agregar el tweet a la base de datos
                    tweets.insert_one(tweetProc)
                    print('Tweet '+str(tweetId)+' of account ' + cuenta + ' added to database.\n')

        if not self.scheduler_running:
            self.scheduler.add_job(self.run, 'interval', minutes=1)
            self.scheduler.start()
            self.scheduler_running = True

        while (True):
            time.sleep(300)


logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("log.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

tasks = Tasks()
event = threading.Event()
thread = threading.Thread(target=tasks.run)
thread.start()
thread.join()
