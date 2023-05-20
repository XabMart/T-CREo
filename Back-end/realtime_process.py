# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json,udf
from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType, BooleanType, FloatType
from credibility import credibility
from kafka import KafkaProducer
import json
import tweepy
from pymongo import MongoClient
import time
import ssl
from confluent_kafka import Producer

# Configuración de acceso a la API de Twitter
app_key = 'a8JToLfAADc5ysGs1MMhLzCZZ'
app_secret = '3WKeaj916dzIGIleT5tPSoMyopw4TMfrY6tUdZjCIC4RzbUVxg'
oauth_token = '1522886161080926209-VJ3NljHTSUgOkalta0ctKO4lMbGK1C'
oauth_token_secret = '9uj4xVAHZqrwKPZVujzeyPhvf1fb5nv99Ja4oYcVcHFV0'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAPr0cQEAAAAA2cUBHe6coN8VnrJpNYxjY1lDJvM%3DmhH1Z1S1UxSKHhvk1XlrCAHvRMNqJIFNRTpHcJhsEy6W9mNjyW'

client = tweepy.Client(bearer_token,app_key,app_secret,oauth_token,oauth_token_secret)
auth = tweepy.OAuth1UserHandler(app_key,app_secret,oauth_token,oauth_token_secret)
api =  tweepy.API(auth)

# Configuración de acceso a MongoDB
dbName = 'Test'
dbCollectionA = 'CuentasTwitter'
dbCollectionT = 'Tweets'

mongo_uri = "mongodb+srv://xabier:ENXKLSNvrWqd3dYJ@cluster0.rmdseqj.mongodb.net/?retryWrites=true&w=majority"

mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client[dbName]
mongo_collection = mongo_db[dbCollectionA]

# Configuración de acceso a Kafka
def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf



# Configuración del Kafka Producer
kafka_producer = Producer(read_ccloud_config("client.properties"))


supported_languages = ['en', 'es', 'fr', 'pt', 'de', 'ru', 'ar']

def delete_all_rules():
    rules = stream.get_rules().data
    if rules is not None:
        ids= [rule.id for rule in rules]
        stream.delete_rules(ids)


def add_account_rules():
    # Conexión a MongoDB y obtención de las cuentas a seguir en Twitter
    #cuentas = mongo_collection.distinct('Twitter_handle')
    #rule = " OR ".join([f"from: {cuenta}" for cuenta in cuentas])
    #stream.add_rules(tweepy.StreamRule(rule))    
    stream.add_rules(tweepy.StreamRule('twitter'))    

# Clase que se encarga de leer los tweets de Twitter y enviarlos a Kafka
class MyStream(tweepy.StreamingClient):

    def on_connect(self):
        print("Connection succesful.")
    def on_data(self, data):
        struct = json.loads(data)
        #print(struct)
        user_id = struct['includes']['users'][0]['id']
        username = struct['includes']['users'][0]['username']
        tweet_id = struct['data']['id']
        text = struct['data']['text']
        created_at = struct['includes']['users'][0]['created_at']
        verified = struct['includes']['users'][0]['verified']
        followers_count = struct['includes']['users'][0]['public_metrics']['followers_count']
        following_count= struct['includes']['users'][0]['public_metrics']['following_count']
        retweet_count = struct['data']['public_metrics']['retweet_count']
        like_count = struct['data']['public_metrics']['like_count']
        lang = struct['data']['lang']
        tweetProc = {
            'user_id': user_id,
            'username' : username,
            'tweet_id':tweet_id,
            'text': text,
            'created_at': created_at,
            'verified': verified,
            'followers_count': followers_count,
            'following_count': following_count,
            'retweet_count': retweet_count,
            'like_count' : like_count,
            'lang': lang
        }
        print(tweetProc)
        if lang in supported_languages:
            kafka_producer.produce("twitter",value= json.dumps(tweetProc).encode('utf-8'))
        
    def on_connection_error(self):
        print("Connection error.")
        self.disconnect()



stream = MyStream(bearer_token=bearer_token)
delete_all_rules()
add_account_rules()
#print(stream.get_rules().data)


# Configuración del stream de Twitter
stream.filter(expansions = 'author_id', user_fields = ['id','username','created_at','verified','public_metrics'],tweet_fields = ['lang','public_metrics'])

