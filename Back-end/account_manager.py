# -*- coding: iso-8859-1 -*-

from flask import Flask,request
from flask_cors import CORS
import re
import json
import pymongo
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import tweepy
from twitter_connection import twitterClient

# Conexión a la base de datos de MongoDB

dbName = 'Test'
dbCollectionA = 'CuentasTwitter'
dbCollectionT = 'Tweets'

dbStringConnection = "mongodb+srv://xabier:ENXKLSNvrWqd3dYJ@cluster0.rmdseqj.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(dbStringConnection)

db = client[dbName]
accounts = db[dbCollectionA]
tweets = db[dbCollectionT]

#Conexión a Twitter.

twitter = twitterClient()

def addAccountToDB(account):
    
    df = pd.DataFrame({
        'Twitter_handle': [account]
    })

    # Verificar si la cuenta ya existe en la base de datos
    if accounts.find_one({'Twitter_handle': account}):
        print('Account already exists in database.')
    else:
        user = twitter.get_user(username = account)
        user_id = user.data['id']
        df = pd.DataFrame({
        'Twitter_handle': [account],
        'User_id': [user_id]
         })
        accounts.insert_one(df.to_dict(orient='records')[0])
        print('Account @' + account + ' with ID: ' + str(user_id) + ' added to database.')

app = Flask(__name__)
CORS(app)

@app.route('/add-account', methods=['POST'])
def accountManager():
    account = request.form['url']
    print(account)
    addAccountToDB(account)
    return 'OK'

if __name__ == '__main__':
    app.run()