from flask import Flask, request, jsonify
import pymongo
from general_utils import get_user_info, mongo_connect
from flask_cors import CORS
import re

app = Flask(__name__)
db, accounts, tweets = mongo_connect()

CORS(app)

@app.route('/tweets_timeline', methods=['POST'])
def tweets_credibility():
    credibilities =[]
    url = request.get_json().get('url')
    accountName = re.search(r'twitter\.com/(\w+)?', url)
    accountName = accountName.group(1)
    query = {'Twitter_handle': accountName}
    result = accounts.find_one(query)
    print(accountName)
    timeline = tweets.find({'user.username': accountName}, sort=[('created_at', pymongo.DESCENDING)], limit=100)
      
    for tweet in timeline:
        credibilities.append(tweet['credibility'][0].get('text_credibility'))
    print(credibilities)
    return jsonify(credibilities)

if __name__ == '__main__':
    app.run()