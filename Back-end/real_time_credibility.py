from twython import TwythonStreamer
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
import logging
from Flask import Flask, request

sc = SparkContext.getOrCreate()
sc.setLogLevel("INFO")
logger = sc._jvm.org.apache.log4j
logger.LogManager.getLogger("org"). setLevel(logger.Level.INFO)
logger.LogManager.getLogger("akka").setLevel(logger.Level.INFO)

#Creamos un servidor de Flask.
app = Flask(__name__)
@app.route('/', methods=['POST'])

# Inserta tus credenciales de Twitter
APP_KEY = 'a8JToLfAADc5ysGs1MMhLzCZZ'
APP_SECRET = '3WKeaj916dzIGIleT5tPSoMyopw4TMfrY6tUdZjCIC4RzbUVxg'
OAUTH_TOKEN = '1522886161080926209-uK8aggJ9nrVvlnBpjUD1b7iM2hkGn2'
OAUTH_TOKEN_SECRET = 'Z8YuiKhXoTyD8A1tFTBF6mDDvIbxC12JxbFJVpooyl4UZ'


class TwitterStreamer(TwythonStreamer):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, interval=10):
        super().__init__(app_key, app_secret, oauth_token, oauth_token_secret)
        self.interval = interval
        self.spark_context = SparkContext(appName="TwitterStreamApp")
        self.spark_context.setLogLevel("INFO")
        self.streaming_context = StreamingContext(self.spark_context, interval)

def process_tweet(tweet):
    followers = tweet['user']['followers_count']
    friends = tweet['user']['friends_count']
    ratio = float(friends) / followers if followers > 0 else 0
    return ratio

streamer = TwitterStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

tweets = streamer.statuses.filter(track='@premierleague')

tweets_dstream = tweets.transform(lambda rdd: rdd.map(lambda tweet: process_tweet(tweet)))

def update_function(new_values, running_total):
    if running_total is None:
        running_total = (0.0, 0)
    return (sum(new_values, running_total[0]), running_total[1] + len(new_values))

average_ratio = tweets_dstream.updateStateByKey(update_function).map(lambda x: x[1][0] / x[1][1] if x[1][1] > 0 else 0)

average_ratio.pprint()
tweets_dstream.count().pprint()
