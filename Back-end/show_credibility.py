# -*- coding: utf-8 -*-
import json
from twitter_connection import twitterClient
from text_credibility import textCredibility
from social_credibility import socialCredibility
from user_credibility import UserCredibility
import pymongo
from general_utils import get_user_info, mongo_connect
from flask import Flask,request,jsonify
from flask_cors import CORS
from flask_sockets import Sockets
from credibility import credibility
import re
# Conexión a la base de datos de MongoDB

db, accounts, tweets = mongo_connect()
lastAccount = ''
#totalCredibility = credibility(text,lang,friends_count,followers_count,verified,created_at)
    
# Definir la aplicación de Flask para recibir las peticiones de la extensión de Chrome
app = Flask(__name__)
CORS(app)

@app.route('/get-credibility', methods=['POST','GET'])

def get_credibility():
    url = request.get_json().get('url')
    if url is None:
        return jsonify({'credibility': 'Missing URL'})

    accountName = re.search(r'twitter\.com/(\w+)?', url)
    if accountName is None:
        return jsonify({'credibility': 'Invalid URL'})

    accountName = accountName.group(1)

    if accountName != lastAccount:
        query = {'Twitter_handle': accountName}
        result = accounts.find_one(query)
        print(accountName)
        if result is None:
            return jsonify({'credibility': 'Account not found'})
        
        lastTweet = tweets.find_one({'user.username': accountName}, sort=[('created_at', pymongo.DESCENDING)], limit=1)
    totalCredibility = lastTweet['credibility'][0].get('global_credibility')
    print(totalCredibility)
    return jsonify({'credibility': 'Credibility: '+ str(round(totalCredibility, 2))})

if __name__ == '__main__':
    app.run(port=8000)